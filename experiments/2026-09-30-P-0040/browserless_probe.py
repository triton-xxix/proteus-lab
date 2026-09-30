#!/usr/bin/env python3
"""P-0040: Browserless /function with the vault key. A page posts itself a message after 1.5s;
the hosted browser waits for it and screenshots. Never prints the key. Writes shot.png and result.json."""
import base64, json, sys, time, urllib.request, urllib.error
sys.path.insert(0, "/Users/triton/PROTEUS/bin")
import secrets as vault

OUT = "/Users/triton/PROTEUS/experiments/2026-09-30-P-0040/"
CODE = r"""
export default async function ({ page }) {
  const t0 = Date.now();
  await page.setViewport({ width: 800, height: 400 });
  await page.setContent(`<html><body style="font:40px sans-serif;padding:40px">
    <div id="h">waiting</div>
    <script>
      window.addEventListener('message', e => { document.getElementById('h').textContent = 'got: ' + e.data; window.__got = Date.now(); });
      setTimeout(() => window.postMessage('ping from P-0040', '*'), 1500);
    </script></body></html>`);
  let waited = 'ok';
  try { await page.waitForFunction('window.__got', { timeout: 10000 }); } catch (e) { waited = 'timeout: ' + e.message; }
  const text = await page.$eval('#h', e => e.textContent);
  const png = await page.screenshot({ type: 'png', encoding: 'base64' });
  return { data: { waited, text, ms: Date.now() - t0, png }, type: 'application/json' };
}
"""

try:
    key = vault.get("Browserless API")
except vault.SecretError as e:
    print("vault: %s" % e)
    sys.exit(1)

res = {}
for host in ("production-sfo.browserless.io", "production-lon.browserless.io"):
    url = "https://%s/function?token=%s" % (host, key)
    req = urllib.request.Request(url, data=json.dumps({"code": CODE}).encode(),
                                 headers={"Content-Type": "application/json", "User-Agent": "proteus-probe/0.2"})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = json.load(r)
            res = {"host": host, "http": r.status, "wall_s": round(time.time() - t, 2),
                   "units_headers": {k: v for k, v in r.headers.items() if "unit" in k.lower() or "limit" in k.lower() or "remaining" in k.lower()}}
            d = body.get("data", body) if isinstance(body, dict) else {}
            png = d.pop("png", None)
            res.update({"waited": d.get("waited"), "text": d.get("text"), "in_browser_ms": d.get("ms")})
            if png:
                open(OUT + "shot.png", "wb").write(base64.b64decode(png))
                res["png_bytes"] = len(base64.b64decode(png))
        break
    except urllib.error.HTTPError as e:
        res = {"host": host, "http": e.code, "wall_s": round(time.time() - t, 2),
               "error": e.read()[:300].decode("utf-8", "replace").replace(key, "KEY")}
        if e.code not in (404, 502, 503):
            break
    except Exception as e:
        res = {"host": host, "error": str(e)[:200].replace(key, "KEY"), "wall_s": round(time.time() - t, 2)}
        break

json.dump(res, open(OUT + "result.json", "w"), indent=1)
print(json.dumps(res, indent=1))
