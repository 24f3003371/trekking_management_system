<template>
  <div class="dashboard-layout">
    <!-- Sidebar Component -->
    <Sidebar />

    <!-- Main Content Area -->
    <main class="dashboard-main fade-in">
      <header class="dashboard-header border-bottom border-secondary-subtle pb-3 mb-4">
        <div>
          <h1 class="h3 fw-bold mb-1 font-display text-white">Trekking History</h1>
          <p class="text text-xs mb-0">Record of your completed summits and cancelled bookings</p>
        </div>
        <div class="d-flex align-items-center gap-2">
          <i class="bi bi-clock-history text-green fs-5"></i>
          <span class="fw-semibold text-white-50 text-xs">Total Expeditions: {{ historyBookings.length }}</span>
        </div>
      </header>

      <!-- History Table -->
      <section class="glass-panel p-4 mb-4">
        <h3 class="h5 fw-bold mb-3 text-white font-display">Trekking History Log</h3>

        <div class="table-responsive">
          <table class="table custom-table mb-0">
            <thead>
              <tr>
                <th scope="col">Trek Name</th>
                <th scope="col">Trek Dates</th>
                <th scope="col">Completed/Cancelled On</th>
                <th scope="col">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="booking in historyBookings" :key="booking.id">
                <td class="fw-semibold text-white">
                  <div class="d-flex align-items-center gap-2">
                    <i class="bi bi-flag-fill text-green" v-if="booking.status === 'Completed'"></i>
                    <i class="bi bi-x-circle text-danger" v-else></i>
                    <span>{{ booking.trekName }}</span>
                  </div>
                </td>
                <td>{{ booking.trekDates }}</td>
                <td>{{ booking.bookingDate }}</td> <!-- bookingDate acts as reference date in history -->
                <td>
                  <span class="badge" :class="statusBadgeClass(booking.status)">
                    {{ booking.status }}
                  </span>
                </td>
              </tr>
              <tr v-if="historyBookings.length === 0">
                <td colspan="4" class="text-center  py-5">
                  <i class="bi bi-clock-history fs-2 d-block mb-2 text-white-50"></i>
                  No history records found. Your completed and cancelled treks will appear here.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="note-footer d-flex gap-2 text-white-50 mt-4 pt-3 border-top border-secondary-subtle" style="font-size: 0.78rem; line-height: 1.4;">
          <i class="bi bi-info-circle-fill text-green flex-shrink-0 mt-0.5"></i>
          <div>History shows all your completed and cancelled treks. If you just booked a trek, it will show on your active Dashboard.</div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import Sidebar from '@/components/dashboard/Sidebar.vue';
import { useTrekStore } from '@/store';

const store = useTrekStore();

const historyBookings = computed(() => {
  if (!store.currentUser) return [];
  // Filter for Completed and Cancelled statuses
  return store.bookings.filter(b => b.userId === store.currentUser.id && (b.status === 'Completed' || b.status === 'Cancelled'));
});

const statusBadgeClass = (status) => {
  if (status === 'Completed') return 'bg-info bg-opacity-10 text-info border border-info-subtle';
  return 'bg-danger bg-opacity-10 text-danger border border-danger-subtle';
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
</style>