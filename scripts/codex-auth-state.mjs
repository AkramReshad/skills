import { createHash, createCipheriv, createDecipheriv, randomBytes } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const seed = process.env.CODEX_AUTH_JSON;
if (!seed) throw new Error('CODEX_AUTH_JSON is missing');
const key = createHash('sha256').update(seed).digest();
const authDirectory = join(process.env.HOME, '.codex');
const authFile = join(authDirectory, 'auth.json');
const stateFile = join(process.env.RUNNER_TEMP, 'codex-auth.enc');
const mode = process.argv[2];

if (mode === 'key') {
  process.stdout.write(key.toString('hex'));
} else if (mode === 'restore') {
  let auth = Buffer.from(seed);
  if (existsSync(stateFile)) {
    const stored = readFileSync(stateFile);
    const decipher = createDecipheriv('aes-256-gcm', key, stored.subarray(0, 12));
    decipher.setAuthTag(stored.subarray(12, 28));
    auth = Buffer.concat([decipher.update(stored.subarray(28)), decipher.final()]);
  }
  const credentials = JSON.parse(auth.toString());
  if (!credentials.tokens?.refresh_token) throw new Error('A managed Codex login with a refresh token is required');
  mkdirSync(authDirectory, { recursive: true, mode: 0o700 });
  writeFileSync(authFile, auth, { mode: 0o600 });
} else if (mode === 'save') {
  const iv = randomBytes(12);
  const cipher = createCipheriv('aes-256-gcm', key, iv);
  const encrypted = Buffer.concat([cipher.update(readFileSync(authFile)), cipher.final()]);
  writeFileSync(stateFile, Buffer.concat([iv, cipher.getAuthTag(), encrypted]), { mode: 0o600 });
} else {
  throw new Error('Expected key, restore, or save');
}
