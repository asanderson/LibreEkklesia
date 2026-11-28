import { createI18n } from "vue-i18n";

import en from "./locales/en.json";

// English first; more locales are added as message files (built for translation).
export const i18n = createI18n({
  legacy: false,
  locale: "en",
  fallbackLocale: "en",
  messages: { en },
});
