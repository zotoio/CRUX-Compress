/**
 * Vitest setup file - runs before all tests.
 * Loads environment variables, enforces global max duration.
 */

import * as dotenv from "dotenv";
import * as path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const envPath = path.resolve(__dirname, ".env");

dotenv.config({ path: envPath });

if (!process.env.CURSOR_API_KEY) {
  console.error(
    "\n❌ CURSOR_API_KEY is not set.\n\n" +
      "1. Copy .env.example to .env:\n" +
      "   cp evals/sdk/.env.example evals/sdk/.env\n\n" +
      "2. Add your API key to evals/sdk/.env\n\n"
  );
  process.exit(1);
}

if (process.env.RIPGREP_PATH) {
  console.log(`✓ Using ripgrep at: ${process.env.RIPGREP_PATH}`);
}

// ---------------------------------------------------------------------------
// Global max duration — terminates all tests after a wall-clock deadline
// ---------------------------------------------------------------------------

const DEFAULT_MAX_DURATION_MS = 3_600_000; // 60 minutes
const maxDurationMs = parseInt(
  process.env.SDK_EVAL_MAX_DURATION_MS || String(DEFAULT_MAX_DURATION_MS),
  10
);

const suiteStartTime = Date.now();

const globalTimer = setTimeout(() => {
  const elapsed = Math.round((Date.now() - suiteStartTime) / 1000);
  console.error(
    `\n❌ GLOBAL TIMEOUT: Test suite exceeded max duration of ${Math.round(maxDurationMs / 60_000)} minutes ` +
      `(elapsed: ${elapsed}s). Terminating all tests and agents.\n` +
      `Last known state: process exiting at ${new Date().toISOString()}\n` +
      `Set SDK_EVAL_MAX_DURATION_MS to increase the limit.\n`
  );
  process.exit(1);
}, maxDurationMs);

globalTimer.unref();

console.log(
  `✓ Global max duration: ${Math.round(maxDurationMs / 60_000)} minutes ` +
    `(SDK_EVAL_MAX_DURATION_MS=${maxDurationMs})`
);

if (process.env.SDK_EVAL_SKIP_EXPENSIVE !== "false") {
  console.log(
    "✓ Expensive tests (Meditate, Integration) will be SKIPPED " +
      "(set SDK_EVAL_SKIP_EXPENSIVE=false to run them)"
  );
}
