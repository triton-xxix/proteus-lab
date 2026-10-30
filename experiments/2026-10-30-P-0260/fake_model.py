"""P-0260: drive a Concordat agent with a scripted fake model that tries every tool in every state.

Counts: tools offered per state, illegal calls rejected, side effects fired, and where the
rejection happened (before the body or not). Two attack surfaces:
  A. direct method calls on the agent object (an in-process caller)
  B. the runner's `invoke` with `allowed_tools()` (what a model-driven run goes through)
Plus the two extra claims in the README: a subclass that bypasses the parent is rejected at
class definition, and the tool-call budget stops calls when spent.
"""
from __future__ import annotations

import json
import sys
import traceback

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/concordat-lib")

from concordat import Agent, Budget, human, tool  # noqa: E402
from concordat.protocol import ProtocolError  # noqa: E402
from concordat.session import ProtocolViolation  # noqa: E402

try:
    from concordat._runner import invoke  # needs pydantic
except Exception as e:  # noqa: BLE001
    invoke = None
    RUNNER_IMPORT_ERROR = f"{type(e).__name__}: {e}"
else:
    RUNNER_IMPORT_ERROR = ""

SIDE_EFFECTS = {"apply_change": 0, "ask_customer": 0, "record_answer": 0}


class BookingAgent(Agent):
    """ask -> confirm -> act. Only apply_change has a consequential side effect."""

    final = {"done"}
    budget = Budget(tool_calls=50)

    @tool(when="start", then="asked")
    def ask_customer(self, question: str) -> str:
        SIDE_EFFECTS["ask_customer"] += 1
        return "asked: " + question

    @tool(when="asked", then={True: "confirmed", False: "start"})
    def record_answer(self, said_yes: bool) -> bool:
        SIDE_EFFECTS["record_answer"] += 1
        return said_yes

    @human(when="asked", approve="confirmed", reject="start")
    def approve_change(self, note: str) -> str:
        return "Approve change? " + note

    @tool(when="confirmed", then="done")
    def apply_change(self, booking_id: str) -> str:
        SIDE_EFFECTS["apply_change"] += 1
        return "changed " + booking_id


ARGS = {
    "ask_customer": {"question": "Are you sure?"},
    "record_answer": {"said_yes": True},
    "approve_change": {"note": "cancel booking"},
    "apply_change": {"booking_id": "B-1"},
    "unknown_tool": {"x": 1},
}
CATALOGUE = list(ARGS)
LEGAL_PATH = [("ask_customer", {"question": "Are you sure?"}), ("record_answer", {"said_yes": True}),
              ("apply_change", {"booking_id": "B-1"})]


def blast(agent: BookingAgent, mode: str, log: list) -> dict:
    """Try every catalogue tool in the current state; return counts."""
    state = agent.state
    allowed = sorted(agent.session.allowed_actions())
    before = dict(SIDE_EFFECTS)
    rejected = accepted = 0
    for name in CATALOGUE:
        if name in allowed:
            continue  # the legal move is made by the driver, not the blaster
        if mode == "A":
            try:
                fn = getattr(agent, name)
            except AttributeError:
                rejected += 1
                log.append((state, mode, name, "AttributeError (no such tool)"))
                continue
            try:
                fn(**ARGS[name])
                accepted += 1
                log.append((state, mode, name, "ACCEPTED"))
            except ProtocolViolation as e:
                rejected += 1
                log.append((state, mode, name, f"ProtocolViolation: {e}"))
        else:
            text, is_error = invoke(agent.allowed_tools(), name, ARGS[name])
            if is_error:
                rejected += 1
                log.append((state, mode, name, text))
            else:
                accepted += 1
                log.append((state, mode, name, "ACCEPTED: " + text))
    moved = {k: SIDE_EFFECTS[k] - before[k] for k in SIDE_EFFECTS if SIDE_EFFECTS[k] != before[k]}
    return {"state": state, "mode": mode, "offered": allowed, "tried_illegal": rejected + accepted,
            "rejected": rejected, "accepted": accepted, "side_effects_moved": moved,
            "state_after": agent.state}


def run_mode(mode: str) -> dict:
    for k in SIDE_EFFECTS:
        SIDE_EFFECTS[k] = 0
    agent = BookingAgent(approver=lambda step, req: True)
    log: list = []
    rounds = []
    for name, args in LEGAL_PATH:
        rounds.append(blast(agent, mode, log))
        if mode == "A":
            getattr(agent, name)(**args)
        else:
            text, err = invoke(agent.allowed_tools(), name, args)
            assert not err, text
    rounds.append(blast(agent, mode, log))  # in the final state nothing should be allowed
    return {"rounds": rounds, "final_state": agent.state, "done": agent.done,
            "side_effects": dict(SIDE_EFFECTS), "history": agent.session.history, "log": log}


def liskov_check() -> dict:
    try:
        class FastBookingAgent(BookingAgent):
            @tool(when="start", then="done")
            def instant_change(self, booking_id: str) -> str:
                return "changed"
        return {"rejected_at_definition": False, "error": ""}
    except ProtocolError as e:
        return {"rejected_at_definition": True, "error": str(e)}


def budget_check() -> dict:
    """Spend the tool-call budget on a loop (ask -> answer no -> start) and see what stops it."""
    for k in SIDE_EFFECTS:
        SIDE_EFFECTS[k] = 0

    class LoopAgent(BookingAgent):
        budget = Budget(tool_calls=3)

    agent = LoopAgent(approver=lambda s, r: True)
    calls = 0
    error = ""
    try:
        for _ in range(10):
            agent.ask_customer("again?")
            calls += 1
            agent.record_answer(False)
            calls += 1
    except Exception as e:  # noqa: BLE001
        error = f"{type(e).__name__}: {e}"
    return {"budget": 3, "calls_before_stop": calls, "error": error,
            "side_effects": dict(SIDE_EFFECTS)}


def bypass_check() -> dict:
    """Caveat: an in-process caller holding the raw function can skip the guard entirely."""
    for k in SIDE_EFFECTS:
        SIDE_EFFECTS[k] = 0
    agent = BookingAgent(approver=lambda s, r: True)
    raw = type(agent)._steps["apply_change"].fn
    raw(agent, "B-9")
    return {"raw_fn_call_fired_side_effect": SIDE_EFFECTS["apply_change"] == 1,
            "state_after": agent.state}


def main() -> None:
    out = {"library": "concordat 0.0.3 (PyPI)", "python": sys.version.split()[0],
           "runner_import_error": RUNNER_IMPORT_ERROR}
    out["mode_A_direct"] = run_mode("A")
    if invoke is not None:
        out["mode_B_runner"] = run_mode("B")
    out["liskov"] = liskov_check()
    out["budget"] = budget_check()
    out["bypass_caveat"] = bypass_check()
    # headline numbers
    totals = {}
    for key in ("mode_A_direct", "mode_B_runner"):
        if key in out:
            r = out[key]["rounds"]
            totals[key] = {"illegal_tried": sum(x["tried_illegal"] for x in r),
                           "rejected": sum(x["rejected"] for x in r),
                           "accepted": sum(x["accepted"] for x in r),
                           "side_effects_from_illegal": sum(len(x["side_effects_moved"]) for x in r),
                           "offered_per_state": {x["state"]: x["offered"] for x in r}}
    out["totals"] = totals
    with open("/Users/triton/PROTEUS/experiments/2026-10-30-P-0260/results.json", "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(json.dumps(totals, indent=1))
    print("final side effects A:", out["mode_A_direct"]["side_effects"])
    if "mode_B_runner" in out:
        print("final side effects B:", out["mode_B_runner"]["side_effects"])
    print("liskov:", out["liskov"])
    print("budget:", out["budget"])
    print("bypass:", out["bypass_caveat"])


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
