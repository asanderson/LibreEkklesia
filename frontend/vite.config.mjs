import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

// The browser app (member portal and staff admin) is served under /app/.
// The public site owns /, and Django owns /api/ (Caddy routes them in P0-09).
export default defineConfig({
  base: "/app/",
  plugins: [vue()],
  server: {
    // Same origin in development too: the dev server forwards API calls to Django.
    proxy: { "/api": "http://127.0.0.1:8000" },
  },
  test: {
    include: ["src/**/*.test.ts"],
    environment: "node",
  },
});
