// Decrypts userkey.enc (iv[12] || AES-GCM ciphertext) produced by the relay Worker.
// Key = SHA-256(USER_KEY_SECRET). Writes user.p12, user.pass, user.alias into <outdir>. Prints nothing secret. MIT.
import { readFileSync, writeFileSync, chmodSync } from "node:fs";
const [, , inFile, outDir] = process.argv;
const secret = process.env.USER_KEY_SECRET;
if (!secret) { console.error("USER_KEY_SECRET is not configured"); process.exit(2); }
const buf = readFileSync(inFile);
const raw = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(secret));
const key = await crypto.subtle.importKey("raw", raw, "AES-GCM", false, ["decrypt"]);
let obj;
try {
  const pt = await crypto.subtle.decrypt({ name: "AES-GCM", iv: buf.subarray(0, 12) }, key, buf.subarray(12));
  obj = JSON.parse(new TextDecoder().decode(pt));
} catch { console.error("could not decrypt user key"); process.exit(3); }
for (const [f, v] of [["user.p12", Buffer.from(obj.keystore, "base64")], ["user.pass", obj.password], ["user.alias", obj.alias]]) {
  writeFileSync(`${outDir}/${f}`, v); chmodSync(`${outDir}/${f}`, 0o600);
}
console.log("user key ready");
