#!/usr/bin/env python3
"""Read a secret from the Proteus vault in 1Password through the service account, for scripts.

The service account token lives outside the repo at ~/.config/proteus/op-service-account.token
(owner read only). Read through 1Password's Python SDK (in the project venv), not the op binary.
This code reads only the PROTEUS vault. Found 30 Sep 2026: the token can also see Luke's main vault,
which the charter says it should not; the refusal below is code, the re-scope is Luke's. Nothing
here prints a secret.

In a script:
    from secrets_proteus import get   # or: sys.path.insert(0, "/Users/triton/PROTEUS/bin"); import secrets as ...
    key = get("Youtube API Data v3")            # field "credential" by default

On the command line, never the value:
    python3 /Users/triton/PROTEUS/bin/secrets.py list                 # item titles in the vault
    python3 /Users/triton/PROTEUS/bin/secrets.py check "Item title" [field]   # prints the length only
"""
import asyncio
import json
import os
import sys

TOKEN_FILE = os.path.expanduser("~/.config/proteus/op-service-account.token")
VAULT = "PROTEUS"   # the only vault this code will read, whatever else the token can see
VENV_SITE = "/Users/triton/PROTEUS/.venv/lib/python%d.%d/site-packages" % sys.version_info[:2]
TIMEOUT = 30

# 30 Sep 2026: the op binary hangs at startup reading 1Password's app group container, a macOS
# "data from other apps" consent that nobody answers at night. The SDK talks HTTPS with the same
# service account token and never touches the container, so it replaced op here.
if VENV_SITE not in sys.path and os.path.isdir(VENV_SITE):
    sys.path.append(VENV_SITE)


class SecretError(RuntimeError):
    pass


def _token():
    try:
        with open(TOKEN_FILE) as fh:
            token = fh.read().strip()
    except OSError as exc:
        raise SecretError("no service account token at %s (%s)" % (TOKEN_FILE, exc.__class__.__name__))
    if not token.startswith("ops_"):
        raise SecretError("token file does not hold a service account token")
    return token


def _run(coro_fn):
    try:
        from onepassword.client import Client
    except ImportError:
        raise SecretError("onepassword-sdk not installed in %s" % VENV_SITE)

    async def go():
        client = await Client.authenticate(auth=_token(), integration_name="proteus-secrets", integration_version="0.2")
        return await coro_fn(client)
    try:
        return asyncio.run(asyncio.wait_for(go(), TIMEOUT))
    except asyncio.TimeoutError:
        raise SecretError("1Password SDK timed out after %ds" % TIMEOUT)
    except SecretError:
        raise
    except Exception as exc:
        raise SecretError("1Password SDK failed: %s" % str(exc)[:200])


# Items outside the PROTEUS vault that Luke has named for use, one line each with his word and date.
# Nothing else in any other vault is read; there is no listing of other vaults.
ALLOWED_OUTSIDE = {
    ("Tritons World", "XAI API Credentials"): "Luke in session, 30 Sep 2026: 'u can use the xai key if we have one'",
}


def _check_vault(vault, item=None):
    if vault.upper() == VAULT:
        return
    if (vault, item) in ALLOWED_OUTSIDE:
        return
    raise SecretError("refused: this code reads only the %s vault, plus the items Luke named in ALLOWED_OUTSIDE" % VAULT)


def get(item, field="credential", vault=VAULT):
    """The secret's value, for use inside a script. Do not print it."""
    _check_vault(vault, item)
    v = VAULT if vault.upper() == VAULT else vault
    return _run(lambda c: c.secrets.resolve("op://%s/%s/%s" % (v, item, field))).rstrip("\n")


def titles(vault=VAULT):
    """Item titles in the vault, no values."""
    _check_vault(vault)

    async def ls(c):
        vid = [v.id for v in await c.vaults.list() if v.title.upper() == VAULT]
        if not vid:
            raise SecretError("vault %s not visible to this token" % VAULT)
        return sorted(i.title for i in await c.items.list(vid[0]))
    return _run(ls)


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
