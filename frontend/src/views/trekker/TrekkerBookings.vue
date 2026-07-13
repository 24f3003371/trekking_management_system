<template>
  <div class="dashboard-layout">
    <Sidebar />

    <main class="dashboard-main fade-in">
      <header class="dashboard-header border-bottom border-secondary-subtle pb-3 mb-4">
        <div>
          <h1 class="h3 fw-bold mb-1 font-display text-white">My Bookings</h1>
          <p class="text-xs mb-0">All your active and upcoming trek bookings</p>
        </div>
        <div class="d-flex align-items-center gap-2">
          <i class="bi bi-journal-bookmark-fill text-green fs-5"></i>
          <span class="fw-semibold text-white-50 text-xs">Active Bookings: {{ activeBookings.length }}</span>
        </div>
      </header>

      <!-- Empty State -->
      <div v-if="activeBookings.length === 0" class="glass-panel p-5 text-center">
        <i class="bi bi-journal-x fs-1 d-block mb-3 text-white-50"></i>
        <h5 class="text-white fw-bold font-display mb-2">No Active Bookings</h5>
        <p class="text-white-50 text-xs mb-4">You haven't booked any treks yet. Explore our curated trails and book your next expedition!</p>
        <router-link to="/BrowseTrekking" class="btn btn-green px-5 py-2 text-xs font-display fw-bold rounded-xl">
          Browse Treks <i class="bi bi-arrow-right ms-1"></i>
        </router-link>
      </div>

      <!-- Bookings Grid -->
      <div v-else class="row g-4">
        <div class="col-md-6 col-lg-4" v-for="booking in activeBookings" :key="booking.id">
          <div class="glass-panel booking-card h-100 d-flex flex-column">
            <!-- Trek Image Banner -->
            <div
              class="booking-banner d-flex align-items-end p-3 position-relative"
              :style="getTrekById(booking.trek_id)?.image
                ? { backgroundImage: `url(${getTrekById(booking.trek_id).image})`, backgroundSize: 'cover', backgroundPosition: 'center' }
                : {}"
            >
              <div class="booking-banner-overlay"></div>
              <div class="position-relative z-1 d-flex align-items-center gap-2">
                <span class="badge bg-success bg-opacity-15 text-success border border-success-subtle text-xs">
                  <i class="bi bi-check-circle me-1"></i>Booked
                </span>
              </div>
            </div>

            <!-- Booking Details -->
            <div class="p-4 flex-grow-1 d-flex flex-column">
              <h4 class="h6 fw-bold text-white font-display mb-1">{{ booking.trekName || `Trek #${booking.trek_id}` }}</h4>
              <div class="text-white-50 text-xs mb-3"><i class="bi bi-hash me-1 text-green"></i>Booking ID: {{ booking.id }}</div>

              <div class="d-flex flex-column gap-2 text-xs bg-dark bg-opacity-20 rounded-xl p-3 border border-secondary border-opacity-10 mb-4">
                <div class="d-flex justify-content-between">
                  <span class="text-white-50">Trek Dates</span>
                  <span class="fw-semibold text-white">{{ booking.trekDates || '—' }}</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-white-50">Booked On</span>
                  <span class="fw-semibold text-white">{{ booking.bookingDate || '—' }}</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-white-50">Payment</span>
                  <span class="fw-semibold text-green">
                    <i class="bi bi-shield-check me-1"></i>Paid
                  </span>
                </div>
              </div>

              <div class="mt-auto">
                <button
                  @click="cancelBooking(booking.id)"
                  class="btn btn-outline-danger w-100 py-2 text-xs font-display fw-semibold">
                  <i class="bi bi-x-circle me-1"></i>Cancel Booking
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer Note -->
      <div v-if="activeBookings.length > 0" class="mt-4 d-flex gap-2 text-white-50" style="font-size: 0.78rem;">
        <i class="bi bi-info-circle-fill text-green flex-shrink-0 mt-1"></i>
        <div>Completed or cancelled treks are archived in <router-link to="/TrekkingHistory" class="text-green text-decoration-none">Trekking History</router-link>.</div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import Sidebar from '@/components/dashboard/Sidebar.vue';
import { useTrekStore } from '@/store';

const store = useTrekStore();

onMounted(async () => {
  if (store.bookings.length === 0) {
    await store.fetchBookingHistory();
  }
});

const activeBookings = computed(() => {
  if (!store.currentUser) return [];
  return store.bookings.filter(b =>
    (b.userId === store.currentUser.id || !b.userId) && b.status === 'Booked'
  );
});

const getTrekById = (trekId) => {
  return store.treks.find(t => t.id === trekId) || null;
};

const cancelBooking = async (bookingId) => {
  if (confirm('Are you sure you want to cancel this booking?')) {
    const result = await store.cancelBooking(bookingId);
    if (!result.success) {
      if (result.message?.toLowerCase().includes('401') || result.message?.toLowerCase().includes('unauthorized')) {
        alert('Your session has expired. Please log out and log in again.');
      } else {
        alert('Could not cancel: ' + result.message);
      }
    }
  }
};
</script>

<style scoped>
.text-xs { font-size: 0.8rem; }

.booking-card {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  transition: transform 0.3s, border-color 0.3s;
  background: rgba(19, 37, 54, 0.35);
}

.booking-card:hover {
  transform: translateY(-4px);
  border-color: rgba(5, 168, 92, 0.3);
}

.booking-banner {
  height: 130px;
  background: linear-gradient(135deg, #102131, #0c1a24);
  position: relative;
}

.booking-banner-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(8, 17, 27, 0.85), rgba(0,0,0,0.1));
}

.btn-green {
  background-color: var(--primary);
  border-color: var(--primary);
  color: #fff;
  border-radius: 10px;
  transition: all 0.25s;
}

.btn-green:hover {
  background-color: var(--primary-hover);
  border-color: var(--primary-hover);
  transform: translateY(-2px);
}
</style>
