"""P-0178: the Hugging Face agents course Thought-Action-Observation loop, in plain Python.

No model here (none on this Mac), so the "Thought" step is a scripted policy that emits the same
text the course shows: a Thought line and a JSON action blob. The parts under test are the ones a
model-backed loop also needs: pulling the JSON action out of free text, refusing bad blobs with an
observation the policy can react to, calling a real tool, and stopping on a final answer.

    python3 agent_loop.py            # writes result.json beside this file
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAX_STEPS = 6


def get_max_temp(latitude, longitude, day_index=1):
    url = ("https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s&models=icon_seamless"
           "&daily=temperature_2m_max&timezone=Europe%%2FBerlin&forecast_days=3" % (latitude, longitude))
    with urllib.request.urlopen(url, timeout=30) as r:
        d = json.load(r)["daily"]
    return {"date": d["time"][day_index], "icon_max_c": d["temperature_2m_max"][day_index]}


TOOLS = {"get_max_temp": (get_max_temp, {"latitude", "longitude"})}


def parse_action(text):
    """Find the first balanced {...} after 'Action:' (or anywhere), parse it, check its shape.
    Returns (action_dict, None) or (None, error string for the observation)."""
    start = text.find("{", text.find("Action:") if "Action:" in text else 0)
    if start < 0:
        return None, "no JSON object found"
    depth, end, in_str, esc = 0, None, False, False
    for i in range(start, len(text)):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end is None:
        return None, "unbalanced braces (truncated blob)"
    try:
        blob = json.loads(text[start:end])
    except json.JSONDecodeError as e:
        return None, "invalid JSON: %s" % e.msg
    if not isinstance(blob, dict) or "action" not in blob:
        return None, "missing 'action' key"
    name = blob["action"]
    if name == "final_answer":
        return blob, None
    if name not in TOOLS:
        return None, "unknown tool %r" % name
    args = blob.get("action_input")
    if not isinstance(args, dict):
        return None, "action_input must be an object"
    missing = TOOLS[name][1] - set(args)
    if missing:
        return None, "missing arguments %s" % sorted(missing)
    return blob, None


def scripted_policy(history):
    """Stands in for the LLM. Emits course-format text; on an error observation it retries once
    with a clean blob, as the course says a model would re-enter the cycle."""
    last = history[-1] if history else None
    if last and last["kind"] == "observation" and "error" not in last["data"]:
        t = last["data"]["icon_max_c"]
        return ("Thought: I have ICON's max. The city station runs about 1C warm of it.\n"
                'Action: {"action": "final_answer", "action_input": {"date": "%s", "icon_max_c": %s, '
                '"city_station_estimate_c": %s}}' % (last["data"]["date"], t, round(t + 1.0, 1)))
    return ("Thought: I need tomorrow's Munich max from the forecast tool.\n"
            'Action: {"action": "get_max_temp", "action_input": {"latitude": 48.137, "longitude": 11.575}}')


def run(policy, first_text=None):
    history, steps = [], 0
    while steps < MAX_STEPS:
        steps += 1
        text = first_text if (first_text is not None and steps == 1) else policy(history)
        history.append({"kind": "thought_action", "text": text})
        blob, err = parse_action(text)
        if err:
            history.append({"kind": "observation", "data": {"error": err}})
            continue
        if blob["action"] == "final_answer":
            return {"steps": steps, "answer": blob["action_input"], "history": history}
        fn = TOOLS[blob["action"]][0]
        try:
            obs = fn(**blob["action_input"])
        except Exception as e:  # the tool's failure is an observation too
            obs = {"error": "%s: %s" % (type(e).__name__, e)}
        history.append({"kind": "observation", "data": obs})
    return {"steps": steps, "answer": None, "history": history, "stopped": "max steps"}


MALFORMED = {
    "truncated": 'Thought: get it.\nAction: {"action": "get_max_temp", "action_input": {"latitude": 48.1',
    "trailing_comma": 'Action: {"action": "get_max_temp", "action_input": {"latitude": 48.137, "longitude": 11.575,}}',
    "unknown_tool": 'Action: {"action": "get_weather", "action_input": {"location": "Munich"}}',
    "missing_arg": 'Action: {"action": "get_max_temp", "action_input": {"latitude": 48.137}}',
    "no_json": "Thought: I will just guess it is about 12C.",
    "brace_in_string": 'Thought: note "{" here.\nAction: {"action": "get_max_temp", "action_input": '
                       '{"latitude": 48.137, "longitude": 11.575, "note": "a } inside"}}',
}


def main():
    out = {"clean": None, "malformed": {}}
    clean = run(scripted_policy)
    direct = get_max_temp(48.137, 11.575)
    out["clean"] = {"steps": clean["steps"], "answer": clean["answer"], "direct_tool_call": direct,
                    "matches_direct": bool(clean["answer"]) and clean["answer"]["icon_max_c"] == direct["icon_max_c"]}
    for name, text in MALFORMED.items():
        r = run(scripted_policy, first_text=text)
        first_obs = r["history"][1]["data"] if len(r["history"]) > 1 else None
        out["malformed"][name] = {"first_observation": first_obs, "recovered": r["answer"] is not None,
                                  "steps": r["steps"]}
    (HERE / "result.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
