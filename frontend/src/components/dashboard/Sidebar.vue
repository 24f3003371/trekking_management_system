<template>
  <aside class="dashboard-sidebar">
    <router-link to="/" class="sidebar-brand">
      <i class="bi bi-triangle-half text-green rotate-brand"></i>
      <span>TrekFlow</span>
    </router-link>

    <nav class="sidebar-nav">
      <template v-if="role === 'admin'">
        <router-link to="/AdminDashboard" class="nav-item-btn" :class="{ active: isActive('/AdminDashboard') }">
          <i class="bi bi-speedometer2"></i> Dashboard
        </router-link>
        <router-link to="/AdminManageTreks" class="nav-item-btn" :class="{ active: isActive('/AdminManageTreks') }">
          <i class="bi bi-map"></i> Manage Treks
        </router-link>
        <router-link to="/ManageStaff" class="nav-item-btn" :class="{ active: isActive('/ManageStaff') }">
          <i class="bi bi-people"></i> Manage Staff
        </router-link>
        <router-link to="/CreateStaff" class="nav-item-btn" :class="{ active: isActive('/CreateStaff') }">
          <i class="bi bi-person-plus"></i> Create Staff
        </router-link>
        <router-link to="/ManageUser" class="nav-item-btn" :class="{ active: isActive('/ManageUser') }">
          <i class="bi bi-person-lines-fill"></i> Manage Users
        </router-link>
      </template>

      <template v-else-if="role === 'staff'">
        <router-link to="/StaffDashboard" class="nav-item-btn" :class="{ active: isActive('/StaffDashboard') }">
          <i class="bi bi-speedometer2"></i> Dashboard
        </router-link>
        <router-link to="/StaffManageTreks" class="nav-item-btn" :class="{ active: isActive('/StaffManageTreks') }">
          <i class="bi bi-map"></i> Manage Treks
        </router-link>
      </template>

      <template v-else>
        <router-link to="/TrekkerDashboard" class="nav-item-btn" :class="{ active: isActive('/TrekkerDashboard') }">
          <i class="bi bi-speedometer2"></i> Dashboard
        </router-link>
        <router-link to="/BrowseTrekking" class="nav-item-btn" :class="{ active: isActive('/BrowseTrekking') }">
          <i class="bi bi-compass"></i> Browse Treks
        </router-link>
        <router-link to="/TrekkingHistory" class="nav-item-btn" :class="{ active: isActive('/TrekkingHistory') }">
          <i class="bi bi-clock-history"></i> Trekking History
        </router-link>
      </template>
    </nav>

    <div class="sidebar-footer">
      <button class="nav-item-btn" @click="logout">
        <i class="bi bi-box-arrow-right"></i> Logout
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useTrekStore } from '@/store';

const route = useRoute();
const router = useRouter();
const store = useTrekStore();

const role = computed(() => store.currentUser?.role);

const isActive = (path) => route.path === path;

const logout = () => {
  store.logout();
  router.push('/');
};
</script>