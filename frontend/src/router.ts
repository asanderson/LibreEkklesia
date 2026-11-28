import { nextTick } from "vue";
import { START_LOCATION, createRouter, createWebHistory } from "vue-router";

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
  // Back and forward restore the old position; a new page starts at the top; changes that
  // stay on the same page (a query or an anchor) leave the scroll position alone.
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    // An anchor that is not on the page (yet) falls through to the rules below.
    if (to.hash && document.getElementById(to.hash.slice(1))) {
      return { el: to.hash };
    }
    return to.path === from.path ? false : { top: 0 };
  },
});

router.afterEach((to, from, failure) => {
  // Blocked, cancelled and repeated navigations change nothing.
  if (failure) {
    return;
  }
  const { t } = i18n.global;
  const siteName = t("shell.siteName");
  document.title = typeof to.meta.title === "string" ? `${t(to.meta.title)} · ${siteName}` : siteName;
  // Move focus to the new content after an in-app page change, so screen readers announce it.
  // The first load and same-page changes keep the browser's own focus.
  if (from === START_LOCATION || to.path === from.path) {
    return;
  }
  void nextTick(() => document.getElementById("main")?.focus());
});
