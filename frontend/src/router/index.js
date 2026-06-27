//createRouter()-->creates router for App
// createWebHistory()-->makes url looks clean 

import { createRouter, createWebHistory  } from "vue-router";

import Login from '../views/Login.vue'

import AdminDashboard from "@/views/AdminDashboard.vue";
import StaffDashboard from "@/views/StaffDashboard.vue";
import ManageStaff from "@/views/ManageStaff.vue";
import ManageUser from "@/views/ManageUser.vue";
import TrekkerRegisteration from "@/views/TrekkerRegisteration.vue";    
import TrekkerDashboard from "@/views/TrekkerDashboard.vue";
import BrowseTrekking from "@/views/BrowseTrekking.vue";
import CreateStaff from "@/views/CreateStaff.vue";
import LandingPage from "@/views/LandingPage.vue";
import TrekkingHistory from "@/views/TrekkingHistory.vue";
import AdminManageTreks from "@/views/AdminManageTreks.vue";
import StaffManageTreks from "@/views/StaffManageTreks.vue";
const routes = [
  { path: "Login", name: "Login", component: Login },
  { path: "AdminDashboard", name: "AdminDashboard", component: AdminDashboard },
  { path: "StaffDashboard", name: "StaffDashboard", component: StaffDashboard },
  { path: "ManageUser", name: "ManageUser", component: ManageUser },
  { path: "ManageStaff", name: "ManageStaff", component: ManageStaff },
  {
    path: "TrekkerRegisteration",
    name: "TrekkerRegisteration",
    component: TrekkerRegisteration,
  },
  {
    path: "TrekkerDashboard",
    name: "TrekkerDashboard",
    component: TrekkerDashboard,
  },
  { path: "LandingPage", name: "LandingPage", component: LandingPage },
  {path: "TrekkingHistory",name: "TrekkingHistory",
    component: TrekkingHistory,
  },
  {
    path: "AdminManageTreks",
    name: "AdminManageTreks",
    component: AdminManageTreks,
  },
  { path: "CreateStaff", name: "CreateStaff", component: CreateStaff },
  {
    path: "StaffManageTreks",
    name: "StaffManageTreks",
    component: StaffManageTreks,
  },

  { path: "BrowseTrekking", name: "BrowseTrekking", component: BrowseTrekking },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
export default router;