"""My own case, not the repo's tests: a claim marked corroborated whose two artifacts are copies of one
record (same independence_group). Does the audit flag it, and does it pass once a second group exists?"""
import json, shutil, subprocess, sys
S = "/Users/triton/PROTEUS/sandbox/p0219-kinship/ex-ussr-kinship-research-main/scripts/"
CASE = "/Users/triton/PROTEUS/sandbox/p0219-kinship/case-weak"
ART = "{id},,title,url,,,,,,,P-0001,,,,direct,image-of-original,{group},clear,,,C-0001,,"
CLAIM = "C-0001,born 1901,P-0001,birth,{arts},{groups},,corroborated,moderate,rationale,"
PERSON = "P-0001,,,,,,,,,,,,,,,"


def audit(arts, groups, art_rows):
    shutil.rmtree(CASE, ignore_errors=True)
    subprocess.run([sys.executable, S + "init_case.py", "--case-dir", CASE, "--research-question", "q"], check=True, capture_output=True)
    with open(CASE + "/person-register.csv", "a") as f:
        f.write(PERSON + "\n")
    with open(CASE + "/artifact-register.csv", "a") as f:
        f.write("".join(r + "\n" for r in art_rows))
    with open(CASE + "/claims-register.csv", "a") as f:
        f.write(CLAIM.format(arts=arts, groups=groups) + "\n")
    p = subprocess.run([sys.executable, S + "audit_evidence.py", "--case-dir", CASE, "--json"], capture_output=True, text=True)
    return json.loads(p.stdout)


same = audit("A-0001;A-0002", "G1", [ART.format(id="A-0001", group="G1"), ART.format(id="A-0002", group="G1")])
fake = audit("A-0001;A-0002", "G1;G2", [ART.format(id="A-0001", group="G1"), ART.format(id="A-0002", group="G1")])
real = audit("A-0001;A-0002", "G1;G2", [ART.format(id="A-0001", group="G1"), ART.format(id="A-0002", group="G2")])
res = {"copies_one_group": same, "declared_second_group_without_artifact": fake, "two_real_groups": real}
json.dump(res, open("/Users/triton/PROTEUS/experiments/2026-10-25-P-0219/weak-results.json", "w"), indent=1, ensure_ascii=False)
for k, v in res.items():
    print(k, "errors", len(v.get("errors", [])), "warnings", len(v.get("warnings", [])))
    for m in (v.get("errors", []) + v.get("warnings", []))[:3]:
        print("   ", str(m)[:160])
