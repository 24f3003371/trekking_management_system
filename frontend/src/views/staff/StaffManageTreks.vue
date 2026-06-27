<template>
  <div class="dashboard-layout">
    <!-- Sidebar Component -->
    <Sidebar />

    <!-- Main Content Area -->
    <main class="dashboard-main fade-in">
      <header class="dashboard-header border-bottom border-secondary-subtle pb-3 mb-4">
        <div>
          <h1 class="h3 fw-bold mb-1 font-display text-white">Manage Trek Group</h1>
          <p class="text-muted text-xs mb-0">Update trail progress checkpoints and monitor participant roster</p>
        </div>
        <div>
          <router-link to="/StaffDashboard" class="btn btn-outline-secondary d-flex align-items-center gap-2 text-xs py-2 px-3">
            <i class="bi bi-arrow-left"></i>
            <span>Back to Dashboard</span>
          </router-link>
        </div>
      </header>

      <!-- Selection Dropdown in case no active trek is set -->
      <section v-if="assignedTreks.length > 1" class="glass-panel p-3 mb-4 d-flex align-items-center gap-3">
        <label class="text-white-50 text-xs mb-0 flex-shrink-0">Select Assigned Trek:</label>
        <select v-model="selectedTrekId" class="form-select bg-transparent border-secondary text-white text-xs" style="max-width: 320px;">
          <option v-for="t in assignedTreks" :key="t.id" :value="t.id" class="bg-dark">{{ t.name }}</option>
        </select>
      </section>

      <div class="row g-4" v-if="activeTrek">
        <!-- Left Column: Trek Info & Controls -->
        <div class="col-lg-5">
          <section class="glass-panel p-4 h-100 d-flex flex-column justify-content-between">
            <div>
              <div class="d-flex justify-content-between align-items-start mb-3">
                <h3 class="h4 fw-bold text-white font-display mb-0">{{ activeTrek.name }}</h3>
                <span class="badge" :class="difficultyBadgeClass(activeTrek.difficulty)">{{ activeTrek.difficulty }}</span>
              </div>
              <p class="text-muted text-xs mb-4"><i class="bi bi-geo-alt-fill text-green me-1"></i>{{ activeTrek.location }}</p>

              <!-- Trek Specs -->
              <div class="d-flex flex-column gap-3 mb-4 bg-dark bg-opacity-20 p-3 rounded-xl border border-secondary border-opacity-10">
                <div class="d-flex justify-content-between text-xs">
                  <span class="text-white-50">Duration:</span>
                  <span class="fw-semibold text-white">{{ activeTrek.duration }}</span>
                </div>
                <div class="d-flex justify-content-between text-xs">
                  <span class="text-white-50">Dates:</span>
                  <span class="fw-semibold text-white">{{ formatDate(activeTrek.startDate) }} - {{ formatDate(activeTrek.endDate) }}</span>
                </div>
                <div class="d-flex justify-content-between text-xs">
                  <span class="text-white-50">Slots Available:</span>
                  <span class="fw-semibold text-white">{{ activeTrek.availableSlots }} / {{ activeTrek.slots }}</span>
                </div>
                <div class="d-flex justify-content-between text-xs">
                  <span class="text-white-50">Group Status:</span>
                  <span class="badge" :class="activeTrek.status === 'Open' ? 'bg-success bg-opacity-10 text-success border border-success-subtle' : 'bg-info bg-opacity-10 text-info border border-info-subtle'">
                    {{ activeTrek.status }}
                  </span>
                </div>
              </div>

              <!-- Progress Controller -->
              <div class="mb-4" v-if="activeTrek.status === 'Open'">
                <label class="form-label text-white-50 text-xs d-flex justify-content-between mb-2">
                  <span>Trek Progress Checkpoints:</span>
                  <span class="fw-bold text-green font-display">{{ progressValue }}%</span>
                </label>
                
                <input 
                  type="range" 
                  class="form-range custom-range" 
                  min="0" 
                  max="100" 
                  step="25" 
                  v-model="progressValue"
                />
                
                <!-- Checkpoint indicators -->
                <div class="d-flex justify-content-between text-xs text-muted px-1 mt-1 font-display" style="font-size: 0.65rem;">
                  <span>Base</span>
                  <span>Camp 1</span>
                  <span>Camp 2</span>
                  <span>Camp 3</span>
                  <span>Summit</span>
                </div>
              </div>

              <div class="mb-4" v-else>
                <div class="alert alert-success border-0 bg-success bg-opacity-10 text-success p-3 rounded-xl text-xs d-flex align-items-center gap-2">
                  <i class="bi bi-patch-check-fill fs-5"></i>
                  <div>This trek group has successfully completed the journey and summit run.</div>
                </div>
              </div>
            </div>

            <!-- Actions buttons -->
            <div class="d-flex flex-column gap-2 mt-4 pt-3 border-top border-secondary-subtle" v-if="activeTrek.status === 'Open'">
              <button @click="updateProgress" class="btn btn-green w-100 py-2 text-xs font-display">
                Update Trek Checkpoint
              </button>
              <button @click="markAsCompleted" class="btn btn-outline-success w-100 py-2 text-xs font-display">
                Mark as Completed / Summit Completed
              </button>
            </div>
          </section>
        </div>

        <!-- Right Column: Participant Roster -->
        <div class="col-lg-7">
          <section class="glass-panel p-4 h-100">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h3 class="h5 fw-bold text-white font-display mb-0">Participants ({{ participants.length }})</h3>
              <span class="badge bg-secondary text-xs">Group Bookings</span>
            </div>

            <div class="table-responsive">
              <table class="table custom-table mb-0">
                <thead>
                  <tr>
                    <th scope="col">Name</th>
                    <th scope="col">Email</th>
                    <th scope="col">Booking Date</th>
                    <th scope="col">Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="p in participants" :key="p.id">
                    <td class="fw-semibold text-white">{{ p.userName }}</td>
                    <td>{{ p.email }}</td>
                    <td>{{ p.bookingDate }}</td>
                    <td>
                      <span class="badge" :class="statusBadgeClass(p.status)">
                        {{ p.status }}
                      </span>
                    </td>
                  </tr>
                  <tr v-if="participants.length === 0">
                    <td colspan="4" class="text-center text-muted py-5">
                      <i class="bi bi-people fs-2 d-block mb-2 text-white-50"></i>
                      No participants registered for this trek yet.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>
        </div>
      </div>

      <div class="text-center py-5 glass-panel" v-else>
        <i class="bi bi-exclamation-octagon fs-1 text-muted d-block mb-3"></i>
        <h3 class="text-white h5">No Assigned Trek Found</h3>
        <p class="text-muted text-xs">Please return to the dashboard and select a trek to manage.</p>
        <router-link to="/StaffDashboard" class="btn btn-green mt-3 text-xs">Go to Dashboard</router-link>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import Sidebar from '@/components/dashboard/Sidebar.vue';
import { useTrekStore } from '@/store';
import { useRouter } from 'vue-router';

const store = useTrekStore();
const router = useRouter();

const selectedTrekId = ref(localStorage.getItem('staff_active_trek_id') || '');
const progressValue = ref(0);

const assignedTreks = computed(() => {
  if (!store.currentUser) return [];
  return store.treks.filter(t => t.assignedStaffId === store.currentUser.id);
});

const activeTrek = computed(() => {
  if (!selectedTrekId.value && assignedTreks.value.length > 0) {
    return assignedTreks.value[0];
  }
  return store.treks.find(t => t.id === selectedTrekId.value);
});

const participants = computed(() => {
  if (!activeTrek.value) return [];
  return store.bookings.filter(b => b.trekId === activeTrek.value.id && b.status !== 'Cancelled');
});

// Watch trek changes to update slide progress value
watch(activeTrek, (newVal) => {
  if (newVal) {
    progressValue.value = newVal.progress;
    selectedTrekId.value = newVal.id;
    localStorage.setItem('staff_active_trek_id', newVal.id);
  }
}, { immediate: true });

onMounted(() => {
  if (activeTrek.value) {
    progressValue.value = activeTrek.value.progress;
  }
});

const difficultyBadgeClass = (diff) => {
  if (diff === 'Easy') return 'bg-success bg-opacity-10 text-success border border-success-subtle';
  if (diff === 'Moderate') return 'bg-warning bg-opacity-10 text-warning border border-warning-subtle';
  return 'bg-danger bg-opacity-10 text-danger border border-danger-subtle';
};

const statusBadgeClass = (status) => {
  if (status === 'Booked') return 'bg-success bg-opacity-10 text-success border border-success-subtle';
  if (status === 'Completed') return 'bg-info bg-opacity-10 text-info border border-info-subtle';
  return 'bg-danger bg-opacity-10 text-danger border border-danger-subtle';
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' });
};

const updateProgress = () => {
  if (!activeTrek.value) return;
  store.updateTrekProgress(activeTrek.value.id, progressValue.value);
  alert(`Trek progress successfully updated to ${progressValue.value}%!`);
};

const markAsCompleted = () => {
  if (!activeTrek.value) return;
  if (confirm("Are you sure you want to mark this trek as completed? All registered bookings will be marked as Completed and participants will receive certificates.")) {
    store.completeTrek(activeTrek.value.id);
    progressValue.value = 100;
  }
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

.custom-range::-webkit-slider-runnable-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  height: 8px;
}

.custom-range::-webkit-slider-thumb {
  background: var(--primary);
  border: 2px solid #ffffff;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  margin-top: -5px;
  cursor: pointer;
}

.custom-range::-moz-range-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  height: 8px;
}

.custom-range::-moz-range-thumb {
  background: var(--primary);
  border: 2px solid #ffffff;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  cursor: pointer;
}

.btn-green {
  background-color: var(--primary);
  border-color: var(--primary);
  color: #ffffff;
}

.btn-green:hover {
  background-color: var(--primary-hover);
  border-color: var(--primary-hover);
}
</style>