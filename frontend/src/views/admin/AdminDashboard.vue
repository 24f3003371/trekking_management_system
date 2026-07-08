<template>
  <div class="dashboard-layout">
    <!-- Sidebar Component -->
    <Sidebar />

    <!-- Main Content Area -->
    <main class="dashboard-main fade-in">
      <header class="dashboard-header border-bottom border-secondary-subtle pb-3 mb-4">
        <div>
          <h1 class="h3 fw-bold mb-1 font-display text-white">Dashboard</h1>
          <p class="text-muted text-xs mb-0">Trekking Management Application Overview</p>
        </div>
        <div class="d-flex align-items-center gap-2">
          <i class="bi bi-person-fill-lock text-green fs-5"></i>
          <span class="fw-semibold text-white-50 text-xs">Admin Panel</span>
        </div>
      </header>

      <!-- Stats Grid -->
      <section class="stats-grid mb-4">
        <div class="stats-card">
          <div class="stats-info">
            <h4>Total Treks</h4>
            <div class="stats-value text-white">{{ store.totalTreks }}</div>
          </div>
          <div class="stats-icon-wrapper">
            <i class="bi bi-compass"></i>
          </div>
        </div>

        <div class="stats-card">
          <div class="stats-info">
            <h4>Total Users</h4>
            <div class="stats-value text-white">{{ store.totalUsers }}</div>
          </div>
          <div class="stats-icon-wrapper">
            <i class="bi bi-people"></i>
          </div>
        </div>

        <div class="stats-card">
          <div class="stats-info">
            <h4>Total Trekking Staff</h4>
            <div class="stats-value text-white">{{ store.totalStaff }}</div>
          </div>
          <div class="stats-icon-wrapper">
            <i class="bi bi-person-badge"></i>
          </div>
        </div>

        <div class="stats-card">
          <div class="stats-info">
            <h4>Total Bookings</h4>
            <div class="stats-value text-white">{{ store.totalBookings }}</div>
          </div>
          <div class="stats-icon-wrapper">
            <i class="bi bi-journal-text"></i>
          </div>
        </div>
      </section>

      <!-- Recent Bookings Table -->
      <section class="glass-panel p-4 mb-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h3 class="h5 fw-bold mb-0 text-white font-display">Recent Bookings</h3>
          <button @click="resetMockState" class="btn btn-sm btn-outline-secondary text-xs">
            <i class="bi bi-arrow-clockwise me-1"></i> Reset State
          </button>
        </div>

        <div class="table-responsive">
          <table class=" table custom-table mb-0">
            <thead>
              <tr>
                <th scope="col">Booking ID</th>
                <th scope="col">User (Trekker)</th>
                <th scope="col">Trek Name</th>
                <th scope="col">Booking Date</th>
                <th scope="col">Status</th>
                <th scope="col" class="text-end">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="booking in store.recentBookings" :key="booking.id">
                <td class="fw-semibold text-green font-display">{{ booking.id }}</td>
                <td>
                  <div class="fw-semibold text-white">{{ booking.userName }}</div>
                  <div class="text-muted text-xs">{{ booking.email }}</div>
                </td>
                <td>{{ booking.trekName }}</td>
                <td>{{ booking.bookingDate }}</td>
                <td>
                  <span class="badge" :class="statusBadgeClass(booking.status)">
                    {{ booking.status }}
                  </span>
                </td>
                <td class="text-end">
                  <div class="d-flex justify-content-end gap-2">
                    <button 
                      v-if="booking.status === 'Booked'" 
                      @click="store.cancelBooking(booking.id)" 
                      class="btn btn-sm btn-outline-danger py-0.5 px-2 text-xs"
                      title="Cancel Booking">
                      Cancel
                    </button>
                    <button 
                      v-if="booking.status === 'Booked'"
                      @click="markCompleted(booking.id)"
                      class="btn btn-sm btn-outline-success py-0.5 px-2 text-xs"
                      title="Mark as Completed">
                      Complete
                    </button>
                    <span v-else class="text-muted text-xs">-</span>
                  </div>
                </td>
              </tr>
              <tr v-if="store.recentBookings.length === 0">
                <td colspan="6" class="text-center text-muted py-4">No recent bookings found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import Sidebar from '@/components/dashboard/Sidebar.vue';
import { useTrekStore } from '@/store';

const store = useTrekStore();

const statusBadgeClass = (status) => {
  if (status === 'Booked') return 'bg-success bg-opacity-10 text-success border border-success-subtle';
  if (status === 'Completed') return 'bg-info bg-opacity-10 text-info border border-info-subtle';
  return 'bg-danger bg-opacity-10 text-danger border border-danger-subtle';
};

const markCompleted = (bookingId) => {
  const booking = store.bookings.find(b => b.id === bookingId);
  if (booking) {
    booking.status = 'Completed';
    store.saveState();
  }
};

const resetMockState = () => {
  if (confirm("Reset application state back to default mock data?")) {
    localStorage.removeItem('trekflow_state');
    window.location.reload();
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
</style>