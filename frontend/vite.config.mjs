import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

import { sourceUrl } from "./src/source-url.ts";

// Stops the build on a bad VITE_SOURCE_URL, read the way Vite reads it for the bundle, instead
// of shipping a broken source link.
const checkSourceUrl = {
  name: "check-source-url",
  configResolved(config) {
    sourceUrl(config.env.VITE_SOURCE_URL);
  },
};

// The browser app (member portal and staff admin) is served under /app/.
// The public site owns /, and Django owns /api/ (Caddy routes them in P0-09).
export default defineConfig({
  base: "/app/",
  plugins: [vue(), checkSourceUrl],
  define: {
    // vue-i18n runs in composition mode only (src/i18n.ts): drop the legacy API, the global
    // components and the devtools hooks from the bundle.
    __VUE_I18N_LEGACY_API__: false,
    __VUE_I18N_FULL_INSTALL__: false,
    __INTLIFY_PROD_DEVTOOLS__: false,
  },
  build: {
    // The bundle drops license comments, so write the bundled packages' notices next to it.
    license: { fileName: "licenses.md" },
  },
  server: {
    // Same origin in development too: the dev server forwards API calls to Django.
    proxy: { "/api": "http://127.0.0.1:8000" },
  },
  test: {
    include: ["src/**/*.test.ts"],
    environment: "node",
  },
});
