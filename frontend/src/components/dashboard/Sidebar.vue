<template>
  <aside class="dashboard-sidebar">
    <div class="sidebar-header pb-4 border-bottom border-secondary-subtle">
      <router-link to="/" class="sidebar-brand">
        <i class="bi bi-triangle-half text-green rotate-brand"></i>
        <span>TrekFlow</span>
      </router-link>
      <div class="app-sub-title text-muted text-uppercase mt-1 text-xs">
        Trekking Management
      </div>
    </div>

    <!-- Sidebar Menu depending on Role -->
    <nav class="sidebar-nav">
      <!-- ADMIN MENU -->
      <template v-if="role === 'admin'">
        <router-link to="/AdminDashboard" class="nav-item-btn" active-class="active">
          <i class="bi bi-grid-1x2-fill"></i>
          <span>Dashboard</span>
        </router-link>
        <router-link to="/AdminManageTreks" class="nav-item-btn" active-class="active">
          <i class="bi bi-compass"></i>
          <span>Treks</span>
        </router-link>
        <router-link to="/ManageStaff" class="nav-item-btn" :class="{ active: isStaffRoute }" active-class="active">
          <i class="bi bi-people-fill"></i>
          <span>Trekking Staff</span>
        </router-link>
        <router-link to="/ManageUser" class="nav-item-btn" active-class="active">
          <i class="bi bi-person-fill"></i>
          <span>Users (Trekkers)</span>
        </router-link>
        <button class="nav-item-btn" @click="notImplemented('Bookings')">
          <i class="bi bi-journal-text"></i>
          <span>Bookings</span>
        </button>
        <button class="nav-item-btn" @click="notImplemented('Search')">
          <i class="bi bi-search"></i>
          <span>Search</span>
        </button>
        <button class="nav-item-btn" @click="notImplemented('Reports')">
          <i class="bi bi-file-earmark-bar-graph"></i>
          <span>Reports</span>
        </button>
        <button class="nav-item-btn" @click="notImplemented('Settings')">
          <i class="bi bi-gear-fill"></i>
          <span>Settings</span>
        </button>
      </template>

      <!-- STAFF MENU -->
      <template v-else-if="role === 'staff'">
        <router-link to="/StaffDashboard" class="nav-item-btn" active-class="active">
          <i class="bi bi-grid-1x2-fill"></i>
          <span>Dashboard</span>
        </router-link>
        <router-link to="/StaffManageTreks" class="nav-item-btn" active-class="active">
          <i class="bi bi-map-fill"></i>
          <span>My Treks</span>
        </router-link>
        <button class="nav-item-btn" @click="notImplemented('Participants')">
          <i class="bi bi-people-fill"></i>
          <span>Participants</span>
        </button>
        <button class="nav-item-btn" @click="notImplemented('Profile')">
          <i class="bi bi-person-badge-fill"></i>
          <span>Profile</span>
        </button>
      </template>

      <!-- TREKKER MENU -->
      <template v-else-if="role === 'trekker'">
        <router-link to="/TrekkerDashboard" class="nav-item-btn" active-class="active">
          <i class="bi bi-grid-1x2-fill"></i>
          <span>Dashboard</span>
        </router-link>
        <router-link to="/BrowseTrekking" class="nav-item-btn" active-class="active">
          <i class="bi bi-compass-fill"></i>
          <span>Browse Treks</span>
        </router-link>
        <router-link to="/TrekkerDashboard" class="nav-item-btn" :class="{ active: false }">
          <i class="bi bi-journal-check"></i>
          <span>My Bookings</span>
        </router-link>
        <router-link to="/TrekkingHistory" class="nav-item-btn" active-class="active">
          <i class="bi bi-clock-history"></i>
          <span>History</span>
        </router-link>
        <button class="nav-item-btn" @click="notImplemented('Profile')">
          <i class="bi bi-person-circle"></i>
          <span>Profile</span>
        </button>
      </template>
    </nav>

    <!-- Sidebar User Footer -->
    <div class="sidebar-footer">
      <div class="user-profile-summary mb-3 d-flex align-items-center gap-2" v-if="store.currentUser">
        <div class="avatar-circle">
          {{ store.currentUser.name.charAt(0) }}
        </div>
        <div class="user-meta overflow-hidden">
          <div class="user-name text-truncate fw-semibold">{{ store.currentUser.name }}</div>
          <div class="user-role text-muted text-xs text-capitalize text-truncate">{{ store.currentUser.role }}</div>
        </div>
      </div>
      <button @click="logout" class="nav-item-btn text-danger-hover logout-btn">
        <i class="bi bi-box-arrow-left"></i>
        <span>Logout</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue';
import { useTrekStore } from '@/store';
import { useRouter, useRoute } from 'vue-router';

const store = useTrekStore();
const router = useRouter();
const route = useRoute();

const role = computed(() => store.currentUser?.role || 'trekker');

const isStaffRoute = computed(() => {
  return route.name === 'CreateStaff' || route.name === 'ManageStaff';
});

const logout = () => {
  store.logout();
  router.push('/');
};

const notImplemented = (section) => {
  alert(`${section} section will be loaded dynamically in production. For this prototype, all central trekking features (landing page, search/filters, bookings, staff management, and history) are fully interactive.`);
};
</script>

<style scoped>
.app-sub-title {
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  font-weight: 700;
  color: #4b6176 !important;
}

.rotate-brand {
  transform: rotate(45deg);
  font-size: 1.5rem;
}

.text-xs {
  font-size: 0.75rem;
}

.avatar-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--primary);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-weight: 700;
  flex-shrink: 0;
  box-shadow: 0 0 10px rgba(5, 168, 92, 0.2);
}

.user-meta {
  line-height: 1.2;
}

.user-name {
  font-size: 0.9rem;
}

.user-role {
  font-size: 0.75rem;
}

.text-danger-hover:hover {
  color: #ef4444 !important;
  background: rgba(239, 68, 68, 0.08) !important;
}

.logout-btn {
  margin-top: 0.5rem;
}
</style>
