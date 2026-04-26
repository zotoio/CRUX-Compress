/**
 * Configuration loader for SDK tests.
 * Loads environment variables from .env file using dotenv.
 */

import * as dotenv from "dotenv";
import * as path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const envPath = path.resolve(__dirname, "..", ".env");

dotenv.config({ path: envPath });

export interface Config {
  cursorApiKey: string;
}

let cachedConfig: Config | null = null;

export function loadConfig(): Config {
  if (cachedConfig) {
    return cachedConfig;
  }

  const cursorApiKey = process.env.CURSOR_API_KEY;

  if (!cursorApiKey) {
    throw new Error(
      "CURSOR_API_KEY is not set.\n\n" +
        "1. Copy .env.example to .env:\n" +
        "   cp evals/sdk/.env.example evals/sdk/.env\n\n" +
        "2. Add your API key to evals/sdk/.env:\n" +
        "   CURSOR_API_KEY=your-key-here\n\n" +
        "Get your key from https://cursor.com/dashboard/cloud-agents"
    );
  }

  cachedConfig = { cursorApiKey };
  return cachedConfig;
}

export function getApiKey(): string {
  return loadConfig().cursorApiKey;
}
