<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { RouterLink, RouterView } from "vue-router";

import { sourceUrl } from "./source-url";

const { t } = useI18n();
const sourceCode = sourceUrl(import.meta.env.VITE_SOURCE_URL);
const thirdPartyLicenses = `${import.meta.env.BASE_URL}licenses.md`;
</script>

<template>
  <a class="skip-link" href="#main">{{ t("shell.skip") }}</a>
  <header class="site-header">
    <p class="site-name">{{ t("shell.siteName") }}</p>
    <nav :aria-label="t('shell.mainNav')">
      <ul>
        <li>
          <RouterLink to="/">{{ t("nav.home") }}</RouterLink>
        </li>
      </ul>
    </nav>
  </header>
  <main id="main" tabindex="-1">
    <RouterView />
  </main>
  <footer class="site-footer">
    <p>{{ t("shell.footer") }}</p>
    <!-- role="list": Safari drops list semantics from unstyled lists outside nav. -->
    <ul class="footer-links" role="list">
      <li>
        <a :href="sourceCode">{{ t("shell.sourceCode") }}</a>
      </li>
      <li>
        <a href="https://www.gnu.org/licenses/agpl-3.0.html">{{ t("shell.license") }}</a>
      </li>
      <li>
        <a :href="thirdPartyLicenses">{{ t("shell.thirdPartyLicenses") }}</a>
      </li>
    </ul>
  </footer>
</template>
