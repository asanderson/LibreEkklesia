<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { RouterLink } from "vue-router";

const { t } = useI18n();
</script>

<template>
  <h1>{{ t("notFound.title") }}</h1>
  <p>{{ t("notFound.body") }}</p>
  <p>
    <RouterLink to="/">{{ t("notFound.home") }}</RouterLink>
  </p>
</template>
