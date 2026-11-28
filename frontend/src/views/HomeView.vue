<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useI18n } from "vue-i18n";

import { api } from "../api/client";

const { t } = useI18n();
const status = ref<"checking" | "ok" | "unavailable">("checking");

onMounted(async () => {
  try {
    const { data } = await api.GET("/api/health");
    status.value = data?.status === "ok" ? "ok" : "unavailable";
  } catch {
    status.value = "unavailable";
  }
});
</script>

<template>
  <h1>{{ t("home.title") }}</h1>
  <p>{{ t("home.intro") }}</p>
  <p role="status">{{ t(`home.api.${status}`) }}</p>
</template>
