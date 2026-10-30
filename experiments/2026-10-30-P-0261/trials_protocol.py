"""P-0261: the Trials slot as a Concordat protocol, driven by the scripted fake model from P-0260.

States follow tasks/trials.md: start -> locked (runlock acquire) -> checked (halt-check CLEAR) ->
looping (probe next / shot / verdict / stop) -> scored (probe shots) -> committed (commit.py) ->
released (runlock release, final). Nothing here calls the real scripts: every tool is a stub that
increments a counter, so the measure is the guard layer only.
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/concordat-lib")

from concordat import Agent, Budget, tool  # noqa: E402
from concordat._runner import invoke  # noqa: E402
from concordat.session import ProtocolViolation  # noqa: E402

FIRED: dict[str, int] = {}


def fire(name: str) -> None:
    FIRED[name] = FIRED.get(name, 0) + 1


class TrialsAgent(Agent):
    """The 12:30 Trials run as a protocol."""

    final = {"released"}
    budget = Budget(tool_calls=150)  # probe.py's own call cap

    @tool(when="start", then={True: "locked", False: "released"})
    def acquire_lock(self, minutes: int) -> bool:
        fire("acquire_lock")
        return True

    @tool(when="locked", then={True: "checked", False: "scored"})
    def halt_check(self) -> bool:
        fire("halt_check")
        return True

    @tool(when="checked", then="looping")
    def probe_start(self, minutes: int, probes: int) -> str:
        fire("probe_start")
        return "started"

    @tool(when="looping", then={"GO": "shot_due", "STOP": "scored"})
    def probe_next(self) -> str:
        fire("probe_next")
        return "GO"

    @tool(when="shot_due", then="probing")
    def probe_shot(self, probe: str, expect: str, p: float) -> str:
        fire("probe_shot")
        return "shot"

    @tool(when="probing", then="looping")
    def probe_verdict(self, probe: str, verdict: str, note: str) -> str:
        fire("probe_verdict")
        return "verdict"

    @tool(when="scored", then="committed")
    def commit(self, message: str) -> str:
        fire("commit")
        return "committed"

    @tool(when="committed", then="released")
    def release_lock(self) -> str:
        fire("release_lock")
        return "released"


ARGS = {
    "acquire_lock": {"minutes": 40},
    "halt_check": {},
    "probe_start": {"minutes": 32, "probes": 6},
    "probe_next": {},
    "probe_shot": {"probe": "P-0261", "expect": "works", "p": 0.7},
    "probe_verdict": {"probe": "P-0261", "verdict": "works", "note": "x"},
    "commit": {"message": "trials"},
    "release_lock": {},
}
# the shape of the run that actually happened today: one probe to verdict, then stop
LEGAL_PATH = ["acquire_lock", "halt_check", "probe_start", "probe_next", "probe_shot",
              "probe_verdict", "probe_next", "commit", "release_lock"]


def blast(agent: TrialsAgent, log: list) -> dict:
    state = agent.state
    allowed = sorted(agent.session.allowed_actions())
    before = dict(FIRED)
    withheld = accepted = 0
    for name, args in ARGS.items():
        if name in allowed:
            continue
        # B: what a model sees (tool not offered)
        text, err = invoke(agent.allowed_tools(), name, args)
        # A: a direct call, which must raise before the body
        try:
            getattr(agent, name)(**args)
            direct = "ACCEPTED"
        except ProtocolViolation as e:
            direct = f"ProtocolViolation: {e}"
        if err and direct.startswith("ProtocolViolation"):
            withheld += 1
        else:
            accepted += 1
        log.append((state, name, text, direct))
    moved = {k: FIRED[k] - before.get(k, 0) for k in FIRED if FIRED[k] != before.get(k, 0)}
    return {"state": state, "offered": allowed, "withheld": withheld, "accepted": accepted,
            "side_effects_moved": moved}


def main() -> None:
    agent = TrialsAgent(approver=lambda s, r: True)
    log: list = []
    rounds = []
    # drive the legal path; probe_next returns GO the first time, STOP the second
    answers = iter(["GO", "STOP"])
    for name in LEGAL_PATH:
        rounds.append(blast(agent, log))
        if name == "probe_next":
            nxt = next(answers)
            agent.session.check("probe_next")
            fire("probe_next")
            agent.session.step("probe_next", "shot_due" if nxt == "GO" else "scored")
        else:
            text, err = invoke(agent.allowed_tools(), name, ARGS[name])
            assert not err, text
    rounds.append(blast(agent, log))
    states_seen = sorted({r["state"] for r in rounds})
    distinct = {}
    for r in rounds:
        distinct.setdefault(r["state"], r)
    totals = {
        "states_in_protocol": sorted(TrialsAgent.protocol.states),
        "distinct_states_visited": len(distinct),
        "tools": len(ARGS),
        "state_tool_pairs": len(distinct) * len(ARGS),
        "withheld_pairs": sum(r["withheld"] for r in distinct.values()),
        "legal_pairs": sum(len(r["offered"]) for r in distinct.values()),
        "accepted_illegal": sum(r["accepted"] for r in distinct.values()),
        "side_effects_from_withheld": sum(len(r["side_effects_moved"]) for r in distinct.values()),
        "offered_per_state": {s: r["offered"] for s, r in distinct.items()},
        "fired": dict(FIRED),
        "final_state": agent.state,
        "done": agent.done,
    }
    out = {"totals": totals, "rounds": rounds, "history": agent.session.history,
           "diagram": TrialsAgent.diagram(), "log": log, "states_seen": states_seen}
    with open("/Users/triton/PROTEUS/experiments/2026-10-30-P-0261/results.json", "w") as f:
        json.dump(out, f, indent=1, default=str)
    print(json.dumps(totals, indent=1))
    print(TrialsAgent.diagram())


if __name__ == "__main__":
    main()
