<template>
  <div class="dashboard-layout">
    <!-- Sidebar Component -->
    <Sidebar />

    <!-- Main Content Area -->
    <main class="dashboard-main fade-in">
      <header class="dashboard-header border-bottom border-secondary-subtle pb-3 mb-4">
        <div>
          <h1 class="h3 fw-bold mb-1 font-display text-white">My Dashboard</h1>
          <p class=" text-xs mb-0">Trekking Staff Portal • Hello, {{ staffName }}</p>
        </div>
        <div class="d-flex align-items-center gap-2">
          <i class="bi bi-shield-check text-green fs-5"></i>
          <span class="fw-semibold text-white-50 text-xs">Trek Leader: {{ staffName }}</span>
        </div>
      </header>

      <!-- Stats Grid -->
      <section class="stats-grid mb-4">
        <div class="stats-card">
          <div class="stats-info">
            <h4>Assigned Treks</h4>
            <div class="stats-value text-white">{{ assignedTreks.length }}</div>
          </div>
          <div class="stats-icon-wrapper">
            <i class="bi bi-backpack-fill text-green"></i>
          </div>
        </div>

        <div class="stats-card">
          <div class="stats-info">
            <h4>Total Participants</h4>
            <div class="stats-value text-white">{{ totalParticipantsCount }}</div>
          </div>
          <div class="stats-icon-wrapper">
            <i class="bi bi-people-fill text-green"></i>
          </div>
        </div>

        <div class="stats-card">
          <div class="stats-info">
            <h4>Ongoing Treks</h4>
            <div class="stats-value text-white">{{ ongoingTreks.length }}</div>
          </div>
          <div class="stats-icon-wrapper">
            <i class="bi bi-arrow-repeat text-green"></i>
          </div>
        </div>

        <div class="stats-card">
          <div class="stats-info">
            <h4>Completed Treks</h4>
            <div class="stats-value text-white">{{ pastTreks.length }}</div>
          </div>
          <div class="stats-icon-wrapper">
            <i class="bi bi-patch-check-fill text-green"></i>
          </div>
        </div>
      </section>

      <!-- Search Bar -->
      <section class="glass-panel p-3 mb-4">
        <div class="input-group">
          <span class="input-group-text bg-transparent border-secondary border-end-0 text-white-50">
            <i class="bi bi-search"></i>
          </span>
          <input
            type="text"
            v-model="searchQuery"
            class="form-control bg-transparent border-secondary border-start-0 text-white text-xs"
            placeholder="Search treks by name, location..."
          />
        </div>
      </section>

      <!-- Ongoing Treks Section -->
      <section class="glass-panel p-4 mb-4">
        <h3 class="h5 fw-bold mb-3 text-white font-display">
          <i class="bi bi-arrow-repeat text-green me-2"></i>Ongoing Treks
        </h3>
        
        <div class="table-responsive">
          <table class="table custom-table mb-0">
            <thead>
              <tr>
                <th scope="col">Trek Name</th>
                <th scope="col">Trek Dates</th>
                <th scope="col">Participants</th>
                <th scope="col">Status</th>
                <th scope="col" class="text-end">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trek in filteredOngoingTreks" :key="trek.id">
                <td>
                  <div class="fw-semibold text-white">{{ trek.name }}</div>
                  <div class="text-muted text-xs mt-0.5"><i class="bi bi-geo-alt-fill text-green me-1"></i>{{ trek.location }} • {{ trek.difficulty }}</div>
                </td>
                <td class="text-xs">
                  {{ formatDateRange(trek.startDate, trek.endDate) }}
                </td>
                <td>
                  <span class="fw-bold text-white">{{ getParticipantCount(trek.id) }}</span>
                  <span class="text-muted text-xs"> (Max {{ trek.slots }})</span>
                </td>
                <td>
                  <span class="badge bg-success bg-opacity-10 text-success border border-success-subtle">
                    {{ trek.status }}
                  </span>
                </td>
                <td class="text-end">
                  <button 
                    @click="manageTrek(trek.id)" 
                    class="btn btn-sm btn-green px-3 py-1 text-xs font-display">
                    Manage
                  </button>
                </td>
              </tr>
              <tr v-if="filteredOngoingTreks.length === 0">
                <td colspan="5" class="text-center text-muted py-4">No ongoing treks.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Past Treks Section -->
      <section class="glass-panel p-4 mb-4">
        <h3 class="h5 fw-bold mb-3 text-white font-display">
          <i class="bi bi-patch-check-fill text-green me-2"></i>Past Treks
        </h3>
        
        <div class="table-responsive">
          <table class="table custom-table mb-0">
            <thead>
              <tr>
                <th scope="col">Trek Name</th>
                <th scope="col">Trek Dates</th>
                <th scope="col">Participants</th>
                <th scope="col">Status</th>
                <th scope="col" class="text-end">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trek in filteredPastTreks" :key="trek.id">
                <td>
                  <div class="fw-semibold text-white">{{ trek.name }}</div>
                  <div class="text-muted text-xs mt-0.5"><i class="bi bi-geo-alt-fill text-green me-1"></i>{{ trek.location }} • {{ trek.difficulty }}</div>
                </td>
                <td class="text-xs">
                  {{ formatDateRange(trek.startDate, trek.endDate) }}
                </td>
                <td>
                  <span class="fw-bold text-white">{{ getParticipantCount(trek.id) }}</span>
                  <span class="text-muted text-xs"> participated</span>
                </td>
                <td>
                  <span class="badge bg-info bg-opacity-10 text-info border border-info-subtle">
                    Completed
                  </span>
                </td>
                <td class="text-end">
                  <button 
                    @click="viewTrek(trek.id)" 
                    class="btn btn-sm btn-outline-light px-3 py-1 text-xs font-display">
                    View
                  </button>
                </td>
              </tr>
              <tr v-if="filteredPastTreks.length === 0">
                <td colspan="5" class="text-center text-muted py-4">No completed treks yet.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Sidebar from '@/components/dashboard/Sidebar.vue';
import { useTrekStore } from '@/store';
import { useRouter } from 'vue-router';

const store = useTrekStore();
const router = useRouter();

const searchQuery = ref('');

const staffName = computed(() => store.currentUser?.name || store.currentUser?.username || 'Trek Leader');

onMounted(async () => {
  try {
    await store.fetchAdminTreks();
    const staffId = store.currentUser?.id;
    if (staffId) {
      const trekIds = store.treks
        .filter(trek => Number(trek.assignedStaffId) === Number(staffId))
        .map(trek => trek.id);
      await Promise.all(trekIds.map(trekId => store.fetchParticipants(trekId).catch(() => {})));
    }
  } catch (err) {
    console.error("Failed to load staff treks on mount:", err);
  }
});

const assignedTreks = computed(() => {
  if (!store.currentUser) return [];
  return store.treks.filter(t => Number(t.assignedStaffId) === Number(store.currentUser.id));
});

// Count ALL non-cancelled participants (Booked + Completed)
const getParticipantCount = (trekId) => {
  return (store.participantsByTrek[trekId] || [])
    .filter(booking => booking.status !== 'Cancelled').length;
};

const totalParticipantsCount = computed(() => {
  let count = 0;
  assignedTreks.value.forEach(t => {
    count += getParticipantCount(t.id);
  });
  return count;
});

const ongoingTreks = computed(() => {
  return assignedTreks.value.filter(t => t.status !== 'Completed');
});

const pastTreks = computed(() => {
  return assignedTreks.value.filter(t => t.status === 'Completed');
});

const filteredOngoingTreks = computed(() => {
  if (!searchQuery.value) return ongoingTreks.value;
  const q = searchQuery.value.toLowerCase();
  return ongoingTreks.value.filter(t =>
    t.name.toLowerCase().includes(q) || t.location.toLowerCase().includes(q)
  );
});

const filteredPastTreks = computed(() => {
  if (!searchQuery.value) return pastTreks.value;
  const q = searchQuery.value.toLowerCase();
  return pastTreks.value.filter(t =>
    t.name.toLowerCase().includes(q) || t.location.toLowerCase().includes(q)
  );
});

const formatDateRange = (start, end) => {
  if (!start || !end) return '';
  const opt = { day: 'numeric', month: 'short' };
  const dStart = new Date(start).toLocaleDateString('en-US', opt);
  const dEnd = new Date(end).toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' });
  return `${dStart} - ${dEnd}`;
};

const manageTrek = (trekId) => {
  localStorage.setItem('staff_active_trek_id', trekId);
  router.push('/StaffManageTreks');
};

const viewTrek = (trekId) => {
  localStorage.setItem('staff_active_trek_id', trekId);
  router.push('/StaffManageTreks');
};
</script>

<style scoped>
.text-xs {
  font-size: 0.8rem;
}

.badge {
  font-size: 0.75rem;
  padding: 0.35em 0.6em;
  border-radius: 6px;
  font-weight: 500;
}

.bg-green {
  background-color: var(--primary) !important;
}

.btn-green {
  background-color: var(--primary);
  border-color: var(--primary);
  color: #ffffff;
  transition: all 0.2s;
}

.btn-green:hover {
  background-color: var(--primary-hover);
  border-color: var(--primary-hover);
}
</style>
