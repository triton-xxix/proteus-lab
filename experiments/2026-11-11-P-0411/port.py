"""P-0411: lot-map's shell classifier, ported line for line to Python and run on the README's own examples.

The source (hooks/map.ts at commit 6370bf43, lines 120 to 217) was read as text and never executed.
This is my port of classifyShell with memory commands left empty (the default setup is not read here).
"""
import json
import re
import sys

FILE_WORDS = set("cat head tail sed grep rg find ls wc cp mv mkdir touch diff cmp sort uniq cut tr awk tee stat file du tree ln basename dirname realpath jq".split())
NEUTRAL_WORDS = set("echo printf cd export true set pwd sleep which test [".split())
NET_WORDS = set("curl wget gh ssh scp sftp ftp rsync nc ncat telnet ping dig nslookup".split())
NET_SUBCOMMANDS = {
    "git": {"push", "pull", "fetch", "clone", "ls-remote"},
    "npm": {"install", "i", "ci", "add", "update", "publish", "view", "audit"},
    "pnpm": {"install", "i", "add", "update", "publish"},
    "yarn": {"install", "add", "upgrade", "publish"},
    "bun": {"install", "add", "update", "publish"},
    "pip": {"install", "download"},
    "pip3": {"install", "download"},
    "docker": {"pull", "push", "login"},
    "brew": {"install", "update", "upgrade", "fetch"},
    "cargo": {"install", "fetch", "publish", "update"},
}
PS_FILE_WORDS = set("get-content gc type set-content add-content out-file get-childitem gci dir get-item gi select-string sls copy-item cpi copy move-item mi move rename-item rni ren new-item ni md test-path resolve-path get-filehash".split())
PS_NEUTRAL_WORDS = set("write-host write-output set-location sl get-location gl start-sleep select-object select where-object where ? foreach-object foreach % sort-object measure-object measure format-table ft format-list fl out-string out-null".split())
PS_NET_WORDS = set("invoke-webrequest iwr invoke-restmethod irm test-connection test-netconnection resolve-dnsname start-bitstransfer".split())

WORD = re.compile(r"""(?:[^\s"']|"[^"]*"?|'[^']*'?)+""")
SHALLOW = re.compile(r"&&|\|\||;|\||\n")
DEEP = re.compile(r"&&|\|\||;|\||\n|\$\(|`|\(|\)")
ASSIGN = re.compile(r"^[A-Za-z_]\w*=")
EXE = re.compile(r"\.(?:exe|cmd|bat)$", re.I)


def segments(command, deep=False):
    out = []
    for part in (DEEP if deep else SHALLOW).split(command):
        words = WORD.findall(part)
        i = 0
        while i < len(words) and ASSIGN.match(words[i]):
            i += 1
        words = words[i:]
        if words:
            out.append(words)
    return out


def base(word=""):
    name = re.sub(r"[\"']", "", word).replace("\\", "/").split("/")[-1]
    return EXE.sub("", name).lower() if EXE.search(name) else name


def classify(command, powershell=False):
    name = (lambda w: base(w).lower()) if powershell else base

    def own(words):
        if not powershell:
            return words
        i = 0
        if words and re.match(r"^\$[\w:]+$", words[0]) and len(words) > 1 and words[1] == "=":
            i = 2
        if i < len(words) and words[i] in ("&", "."):
            i += 1
        return words[i:]

    lines = [w for w in map(own, segments(command)) if w]
    for words in map(own, segments(command, True)):
        head = name(words[0]) if words else ""
        sub = words[1] if len(words) > 1 else ""
        if head in NET_WORDS or (powershell and head in PS_NET_WORDS) or sub in NET_SUBCOMMANDS.get(head, ()):
            return "network"
    neutral = lambda h: h in NEUTRAL_WORDS or (powershell and h in PS_NEUTRAL_WORDS)
    isfile = lambda h: h in FILE_WORDS or (powershell and h in PS_FILE_WORDS)
    real = [w for w in lines if not neutral(name(w[0]))]
    if real and all(isfile(name(w[0])) for w in real):
        return "files"
    return "shell"


# (command, powershell, the station the README names, where the README says it)
README = [
    ("cat notes.txt", False, "files", "Files row"),
    ("grep -rn TODO src", False, "files", "Files row"),
    ("mv a.txt b.txt", False, "files", "Files row"),
    ("sed -i 's/a/b/' file.txt", False, "files", "Files row"),
    ("tee out.log", False, "files", "Files row"),
    ("find . -name '*.tmp' -delete", False, "files", "Files row"),
    ("curl -s https://example.com", False, "network", "Network row"),
    ("gh pr list", False, "network", "Network row"),
    ("ssh host uptime", False, "network", "Network row"),
    ("rsync -a src/ host:dst/", False, "network", "Network row"),
    ("git push origin main", False, "network", "Network row"),
    ("npm install", False, "network", "Network row"),
    ("docker pull alpine", False, "network", "Network row"),
    ("echo $(curl -s https://example.com)", False, "network", "also inside $(...)"),
    ("Get-Content notes.txt", True, "files", "PowerShell"),
    ("Select-String -Pattern TODO -Path src", True, "files", "PowerShell"),
    ("Invoke-WebRequest https://example.com", True, "network", "PowerShell"),
    ("/usr/bin/curl -s https://example.com", False, "network", "full path"),
    ("& \"C:\\Program Files\\Git\\cmd\\git.exe\" push", True, "network", "quoted path with a space"),
    ("CURL.EXE -s https://example.com", True, "network", "CURL.EXE is curl"),
    ("python -c \"import urllib.request\"", False, "shell", "goes by name, not by what it does"),
]

# Ordinary commands the README's prose covers but does not list. What I would expect a reader to assume.
MINE = [
    ("grep -E 'foo|bar' notes.txt", False, "files", "a pipe inside quotes"),
    ("grep \"a;b\" notes.txt", False, "files", "a semicolon inside quotes"),
    ("awk '{print $1}' data.csv | sort | uniq -c", False, "files", "a file-only pipeline"),
    ("rm old.txt", False, "files", "the row says delete"),
    ("rm -rf build", False, "files", "the row says delete"),
    ("cp -r a b && chmod +x b/run.sh", False, "files", "chmod works on a file and nothing else"),
    ("cat a.txt > b.txt", False, "files", "redirection"),
    ("echo \"run git push later\"", False, "shell", "network words inside a quoted string"),
    ("echo \"first; curl is a tool\"", False, "shell", "a semicolon and a network word inside quotes"),
    ("git -C repo push", False, "network", "an option before the subcommand"),
    ("npm --prefix web install", False, "network", "an option before the subcommand"),
    ("sudo curl -s https://example.com", False, "network", "a wrapper before the command"),
    ("env TOKEN=x curl -s https://example.com", False, "network", "a wrapper before the command"),
    ("find . -name '*.url' -exec curl {} +", False, "network", "a network command run by find"),
    ("xargs curl < urls.txt", False, "network", "a network command run by xargs"),
    ("git status", False, "shell", "a git subcommand that stays local"),
    ("wget https://example.com/file", False, "network", "the and-the-like list"),
    ("pip install requests", False, "network", "the and-the-like list"),
    ("python3 fetch.py", False, "shell", "goes by name"),
    ("ls -la", False, "files", "reads a folder"),
]


def run(cases):
    rows = []
    for command, ps, want, why in cases:
        got = classify(command, ps)
        rows.append({"command": command, "powershell": ps, "expected": want, "got": got, "ok": got == want, "why": why})
    return rows


if __name__ == "__main__":
    readme, mine = run(README), run(MINE)
    out = {
        "source": "alexeyw/lot-map hooks/map.ts at 6370bf4314149e43594bf162aa47db1616f9c092, read as text, ported, not executed",
        "readme": {"n": len(readme), "ok": sum(r["ok"] for r in readme), "first13_ok": sum(r["ok"] for r in readme[:13]), "rows": readme},
        "mine": {"n": len(mine), "ok": sum(r["ok"] for r in mine), "rows": mine},
    }
    with open(sys.argv[1], "w") as f:
        json.dump(out, f, indent=1)
    for label, rows in (("README", readme), ("MINE", mine)):
        print(label, sum(r["ok"] for r in rows), "of", len(rows))
        for r in rows:
            if not r["ok"]:
                print("  MISS", repr(r["command"]), "expected", r["expected"], "got", r["got"], "|", r["why"])
