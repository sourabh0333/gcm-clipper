import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In development the API runs on the laptop at :8770 (python -m aigcm.api); Vite forwards to it.
const api = "http://localhost:8770";

export default defineConfig({
  plugins: [react()],
  server: { proxy: { "/api": api, "/auth": api, "/media": api } },
  build: { outDir: "dist", sourcemap: false },
  test: { environment: "jsdom", setupFiles: ["./src/test-setup.ts"] },
});
