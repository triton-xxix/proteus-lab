#!/usr/bin/env node
// Seal the dashboard payload: node bin/dash-seal.cjs <keyfile> <outfile>  (plaintext JSON on stdin)
// PBKDF2-HMAC-SHA256 (600,000 iterations, the key file's salt) -> AES-256-GCM with a fresh 12-byte IV.
// Output: {v, kdf, iter, salt, iv, ct (ciphertext||tag, base64), built_at, bytes}. Node's own crypto, no deps.
'use strict';
const fs = require('fs');
const crypto = require('crypto');

const [keyfile, outfile] = process.argv.slice(2);
if (!keyfile || !outfile) { console.error('usage: dash-seal.cjs <keyfile> <outfile>'); process.exit(2); }
const key = JSON.parse(fs.readFileSync(keyfile, 'utf8'));
const plaintext = fs.readFileSync(0);
const ITER = 600000;
const salt = Buffer.from(key.salt, 'base64');
const k = crypto.pbkdf2Sync(Buffer.from(key.passphrase, 'utf8'), salt, ITER, 32, 'sha256');
const iv = crypto.randomBytes(12);
const cipher = crypto.createCipheriv('aes-256-gcm', k, iv);
const ct = Buffer.concat([cipher.update(plaintext), cipher.final(), cipher.getAuthTag()]);
const out = { v: 1, kdf: 'PBKDF2-SHA256', iter: ITER, salt: key.salt, iv: iv.toString('base64'), ct: ct.toString('base64'), built_at: new Date().toISOString(), bytes: plaintext.length };
fs.writeFileSync(outfile, JSON.stringify(out));
console.log('sealed', plaintext.length, 'bytes ->', outfile);
