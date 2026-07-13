import { createRouter, createWebHistory } from "vue-router";
import { useTrekStore } from "@/store";

import LandingPage from "@/views/LandingPage.vue";
import Login from "@/views/auth/Login.vue";
import TrekkerRegisteration from "@/views/auth/TrekkerRegisteration.vue";

import AdminDashboard from "@/views/admin/AdminDashboard.vue";
import CreateTrek from "@/views/admin/CreateTrek.vue";
import AdminManageTreks from "@/views/admin/AdminManageTreks.vue";
import CreateStaff from "@/views/admin/CreateStaff.vue";
import ManageStaff from "@/views/admin/ManageStaff.vue";
import ManageUser from "@/views/admin/ManageUser.vue";

import StaffDashboard from "@/views/staff/StaffDashboard.vue";
import StaffManageTreks from "@/views/staff/StaffManageTreks.vue";

import TrekkerDashboard from "@/views/trekker/TrekkerDashboard.vue";
import BrowseTrekking from "@/views/trekker/BrowseTrekking.vue";
import TrekkingHistory from "@/views/trekker/TrekkingHistory.vue";

const routes = [
  { path: "/", name: "LandingPage", component: LandingPage },
  { path: "/Login", name: "Login", component: Login },
  {
    path: "/TrekkerRegisteration",
    name: "TrekkerRegisteration",
    component: TrekkerRegisteration,
  },

  // Admin Routes
  {
    path: "/AdminDashboard",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/CreateTrek",
    name: "CreateTrek",
    component: CreateTrek,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/AdminManageTreks",
    name: "AdminManageTreks",
    component: AdminManageTreks,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/CreateStaff",
    name: "CreateStaff",
    component: CreateStaff,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/ManageStaff",
    name: "ManageStaff",
    component: ManageStaff,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/ManageUser",
    name: "ManageUser",
    component: ManageUser,
    meta: { requiresAuth: true, role: "admin" },
  },

  // Staff Routes
  {
    path: "/StaffDashboard",
    name: "StaffDashboard",
    component: StaffDashboard,
    meta: { requiresAuth: true, role: "staff" },
  },
  {
    path: "/StaffManageTreks",
    name: "StaffManageTreks",
    component: StaffManageTreks,
    meta: { requiresAuth: true, role: "staff" },
  },

  // Trekker Routes
  {
    path: "/TrekkerDashboard",
    name: "TrekkerDashboard",
    component: TrekkerDashboard,
    meta: { requiresAuth: true, role: "trekker" },
  },
  {
    path: "/BrowseTrekking",
    name: "BrowseTrekking",
    component: BrowseTrekking,
    meta: { requiresAuth: true, role: "trekker" },
  },
  {
    path: "/TrekkingHistory",
    name: "TrekkingHistory",
    component: TrekkingHistory,
    meta: { requiresAuth: true, role: "trekker" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

router.beforeEach((to, from, next) => {
  const store = useTrekStore();
  const user = store.currentUser;

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!user) {
      next({ name: "Login" });
    } else {
      const requiredRole = to.meta.role;
      if (requiredRole && user.role !== requiredRole) {
        // Redirect to their respective dashboards if they have the wrong role
        if (user.role === "admin") next({ name: "AdminDashboard" });
        else if (user.role === "staff") next({ name: "StaffDashboard" });
        else next({ name: "TrekkerDashboard" });
      } else {
        next();
      }
    }
  } else {
    // If logged in, don't let them visit login/register pages
    if (user && (to.name === "Login" || to.name === "TrekkerRegisteration")) {
      if (user.role === "admin") next({ name: "AdminDashboard" });
      else if (user.role === "staff") next({ name: "StaffDashboard" });
      else next({ name: "TrekkerDashboard" });
    } else {
      next();
    }
  }
});

export default router;
