import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    testTimeout: 240_000,
    hookTimeout: 120_000,
    pool: "forks",
    poolOptions: {
      forks: {
        maxForks: 2,
      },
    },
    setupFiles: ["./vitest.setup.ts"],
    reporters: ["verbose"],
    printConsoleTrace: false,
  },
});
