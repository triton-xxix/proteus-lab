#!/usr/bin/env python3
"""Read a secret from the Proteus vault in 1Password through the service account, for scripts.

The service account token lives outside the repo at ~/.config/proteus/op-service-account.token
(owner read only), and is granted read-only access to the one vault called Proteus. The token is
loaded into the environment of the `op` child only; nothing here prints a secret.

In a script:
    from secrets_proteus import get   # or: sys.path.insert(0, "/Users/triton/PROTEUS/bin"); import secrets as ...
    key = get("Youtube API Data v3")            # field "credential" by default

On the command line, never the value:
    python3 /Users/triton/PROTEUS/bin/secrets.py list                 # item titles in the vault
    python3 /Users/triton/PROTEUS/bin/secrets.py check "Item title" [field]   # prints the length only
"""
import json
import os
import subprocess
import sys

TOKEN_FILE = os.path.expanduser("~/.config/proteus/op-service-account.token")
VAULT = "Proteus"
OP = os.environ.get("OP_BIN") or "/usr/local/bin/op"


class SecretError(RuntimeError):
    pass


def _env():
    try:
        with open(TOKEN_FILE) as fh:
            token = fh.read().strip()
    except OSError as exc:
        raise SecretError("no service account token at %s (%s)" % (TOKEN_FILE, exc.__class__.__name__))
    if not token.startswith("ops_"):
        raise SecretError("token file does not hold a service account token")
    env = {k: v for k, v in os.environ.items() if k not in ("OP_SESSION", "OP_SERVICE_ACCOUNT_TOKEN")}
    env["OP_SERVICE_ACCOUNT_TOKEN"] = token
    return env


def _op(args, timeout=30):
    try:
        res = subprocess.run([OP] + args, capture_output=True, text=True, env=_env(), timeout=timeout)
    except FileNotFoundError:
        raise SecretError("op binary not found at %s" % OP)
    except subprocess.TimeoutExpired:
        raise SecretError("op timed out after %ds" % timeout)
    if res.returncode != 0:
        raise SecretError("op failed: " + (res.stderr or res.stdout).strip()[:200])
    return res.stdout


def get(item, field="credential", vault=VAULT):
    """The secret's value, for use inside a script. Do not print it."""
    return _op(["read", "op://%s/%s/%s" % (vault, item, field)]).rstrip("\n")


def titles(vault=VAULT):
    """Item titles in the vault, no values."""
    out = _op(["item", "list", "--vault", vault, "--format", "json"])
    return sorted(i.get("title", "") for i in json.loads(out or "[]"))


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("list", "check"):
        print(__doc__)
        sys.exit(2)
    try:
        if sys.argv[1] == "list":
            for t in titles():
                print(t)
        else:
            item = sys.argv[2]
            field = sys.argv[3] if len(sys.argv) > 3 else "credential"
            v = get(item, field)
            print("%s / %s: %d characters" % (item, field, len(v)))
    except SecretError as exc:
        print("secrets: " + str(exc))
        sys.exit(1)


if __name__ == "__main__":
    main()
