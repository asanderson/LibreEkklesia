<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { RouterLink, RouterView } from "vue-router";

const { t } = useI18n();
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
  </footer>
</template>
