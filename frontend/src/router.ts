import { nextTick } from "vue";
import { createRouter, createWebHistory } from "vue-router";

import { i18n } from "./i18n";
import HomeView from "./views/HomeView.vue";
import NotFoundView from "./views/NotFoundView.vue";

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", name: "home", component: HomeView, meta: { title: "titles.home" } },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: NotFoundView,
      meta: { title: "titles.notFound" },
    },
  ],
});

let firstNavigation = true;

router.afterEach((to) => {
  const { t } = i18n.global;
  const titleKey = typeof to.meta.title === "string" ? to.meta.title : "titles.home";
  document.title = `${t(titleKey)} · ${t("shell.siteName")}`;
  if (firstNavigation) {
    firstNavigation = false;
    return;
  }
  // After an in-app navigation, move focus to the new content so screen readers announce it.
  void nextTick(() => document.getElementById("main")?.focus());
});
