import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    include: ['tests/unit/**/*.unit.test.ts'],
    setupFiles: ['./test/server/helpers/test-env.mjs'],
    environment: 'node',
    testTimeout: 10000
  }
})