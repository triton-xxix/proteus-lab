#!/usr/bin/env python3
"""P-0202: does 402mcp's keyless POST /api/v1/decode parse a hand-built x402 challenge and name the
retry header correctly?

Builds an x402 v1 challenge (JSON body) and an x402 v2 challenge (PAYMENT-REQUIRED header, base64 JSON)
from the scheme reference at /api/v1/schemes/x402, posts each to the decode endpoint in the shape the
OpenAPI document describes (falling back through a few plausible shapes if the first is rejected), and
records what came back. Nothing is paid; no wallet exists here.
Run: /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-23-P-0202/decode_test.py
"""
import base64
import json
import os
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://402mcp.org"
UA = "proteus-probe/P-0202 (+https://triton-xxix.github.io/proteus-lab/)"


def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, json.loads(r.read().decode())


def post(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(BASE + path, data=data, method="POST",
                                 headers={"User-Agent": UA, "Content-Type": "application/json",
                                          "Accept": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode()
            status = r.status
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        status = e.code
    ms = round((time.time() - t0) * 1000)
    try:
        parsed = json.loads(body)
    except Exception:
        parsed = body[:2000]
    return status, parsed, ms


def b64(obj):
    return base64.b64encode(json.dumps(obj).encode()).decode()


V1_BODY = {
    "x402Version": 1,
    "error": "Payment required",
    "accepts": [{
        "scheme": "exact",
        "network": "base-sepolia",
        "maxAmountRequired": "10000",
        "resource": "https://example.test/report",
        "description": "Proteus probe, hand-built v1 challenge",
        "mimeType": "application/json",
        "payTo": "0x0000000000000000000000000000000000000001",
        "maxTimeoutSeconds": 60,
        "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
        "extra": {"name": "USDC", "version": "2"},
    }],
}

V2_REQ = {
    "x402Version": 2,
    "accepts": [{
        "scheme": "exact",
        "network": "eip155:8453",
        "amount": "10000",
        "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "payTo": "0x0000000000000000000000000000000000000001",
        "maxTimeoutSeconds": 60,
        "extra": {"name": "USDC", "version": "2"},
    }],
    "resource": {"url": "https://example.test/report", "description": "Proteus probe, hand-built v2 challenge"},
}


def main():
    out = {"openapi_decode": None, "attempts": []}
    try:
        _, spec = get("/openapi.json")
        dec = spec.get("paths", {}).get("/api/v1/decode", {})
        out["openapi_decode"] = dec
        schema_ref = None
        try:
            schema_ref = dec["post"]["requestBody"]["content"]["application/json"]["schema"]
        except Exception:
            pass
        out["openapi_decode_schema"] = schema_ref
        comps = spec.get("components", {}).get("schemas", {})
        if isinstance(schema_ref, dict) and "$ref" in schema_ref:
            out["openapi_decode_component"] = comps.get(schema_ref["$ref"].split("/")[-1])
    except Exception as exc:
        out["openapi_error"] = repr(exc)

    v1_hdrs = {"Content-Type": "application/json"}
    v2_hdrs = {"PAYMENT-REQUIRED": b64(V2_REQ)}
    cases = {
        "x402 v1 (JSON body)": (v1_hdrs, json.dumps(V1_BODY)),
        "x402 v2 (PAYMENT-REQUIRED header)": (v2_hdrs, ""),
    }
    shapes = [
        lambda h, b: {"status": 402, "headers": h, "body": b},
        lambda h, b: {"statusCode": 402, "headers": h, "body": b},
        lambda h, b: {"response": {"status": 402, "headers": h, "body": b}},
        lambda h, b: {"headers": h, "body": b},
    ]
    for name, (h, b) in cases.items():
        for i, shape in enumerate(shapes):
            payload = shape(h, b)
            status, parsed, ms = post("/api/v1/decode", payload)
            rec = {"case": name, "shape": i, "request": payload, "status": status, "ms": ms, "response": parsed}
            out["attempts"].append(rec)
            print(name, "shape", i, "->", status, ms, "ms")
            if status == 200:
                print(json.dumps(parsed, indent=1)[:3000])
                break
            else:
                print("  ", json.dumps(parsed)[:400])
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
