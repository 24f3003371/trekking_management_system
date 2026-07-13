<template>
  <div class="dashboard-layout">
    <!-- Sidebar Component -->
    <Sidebar />

    <!-- Main Content Area -->
    <main class="dashboard-main fade-in">
      <header class="dashboard-header border-bottom border-secondary-subtle pb-3 mb-4">
        <div>
          <h1 class="h3 fw-bold mb-1 font-display text-white">Welcome, {{ trekkerName }}!</h1>
          <p class="text-xs mb-0">Ready for your next high alpine expedition?</p>
        </div>
        <div class="d-flex align-items-center gap-2">
          <i class="bi bi-person-fill text-green fs-5"></i>
          <span class="fw-semibold text-white-50 text-xs">Trekker Account</span>
        </div>
      </header>

      <!-- Available Treks Grid -->
      <section class="mb-5">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h3 class="h5 fw-bold mb-0 text-white font-display">Available Treks</h3>
          <router-link to="/BrowseTrekking" class="text-green text-decoration-none text-xs hover-underline">
            View All Treks <i class="bi bi-arrow-right ms-1"></i>
          </router-link>
        </div>

        <div class="row g-4">
          <div class="col-md-6 col-lg-4" v-for="trek in availableTreks" :key="trek.id">
            <div class="card trek-card h-100 border-0 glass-card text-white overflow-hidden d-flex flex-column justify-content-between">
              <!-- Visual Card Header -->
              <div class="trek-card-img-placeholder d-flex align-items-end p-3 position-relative">
                <div class="trek-image-overlay"></div>
                <div class="position-relative z-1 w-100 d-flex justify-content-between align-items-center">
                  <span class="badge" :class="difficultyBadgeClass(trek.difficulty)">{{ trek.difficulty }}</span>
                  <span class="badge bg-dark bg-opacity-70 text-white border border-secondary text-xs"><i class="bi bi-clock me-1"></i>{{ trek.duration }}</span>
                </div>
              </div>

              <!-- Card Body -->
              <div class="p-3">
                <h4 class="h6 fw-bold mb-1 font-display text-white">{{ trek.name }}</h4>
                <div class="text-white-50 text-xs mb-3"><i class="bi bi-geo-alt-fill text-green me-1"></i>{{ trek.location }}</div>
                <p class="text-muted text-xs mb-3 line-clamp">{{ trek.description }}</p>
                
                <div class="d-flex justify-content-between align-items-center pt-2 border-top border-secondary border-opacity-10 text-xs">
                  <span class="text-white-50">Slots Left: <strong class="text-white">{{ trek.availableSlots }}</strong></span>
                  <span class="fw-bold text-green font-display text-base">₹{{ trek.price.toLocaleString('en-IN') }}</span>
                </div>
              </div>

              <!-- Card Footer Button -->
              <div class="p-3 pt-0">
                <button 
                  v-if="trek.availableSlots > 0" 
                  @click="bookTrek(trek.id)" 
                  class="btn btn-green w-100 py-2 text-xs font-display fw-semibold">
                  Book Now
                </button>
                <button 
                  v-else 
                  disabled 
                  class="btn btn-outline-secondary w-100 py-2 text-xs font-display fw-semibold border-secondary border-opacity-20 text-white-50">
                  Not Available
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- My Bookings Section -->
      <section class="glass-panel p-4 mb-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h3 class="h5 fw-bold mb-0 text-white font-display">My Bookings</h3>
          <router-link to="/TrekkingHistory" class="text-green text-decoration-none text-xs hover-underline">
            View Trekking History <i class="bi bi-clock-history ms-1"></i>
          </router-link>
        </div>

        <div class="table-responsive">
          <table class="table custom-table mb-0">
            <thead>
              <tr>
                <th scope="col">Booking ID</th>
                <th scope="col">Trek Name</th>
                <th scope="col">Booking Date</th>
                <th scope="col">Trek Dates</th>
                <th scope="col">Status</th>
                <th scope="col" class="text-end">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="booking in myBookings" :key="booking.id">
                <td class="fw-semibold text-green font-display">{{ booking.id }}</td>
                <td class="fw-semibold text-white">{{ booking.trekName }}</td>
                <td>{{ booking.bookingDate }}</td>
                <td>{{ booking.trekDates }}</td>
                <td>
                  <span class="badge" :class="statusBadgeClass(booking.status)">
                    {{ booking.status }}
                  </span>
                </td>
                <td class="text-end">
                  <button 
                    v-if="booking.status === 'Booked'" 
                    @click="cancelBooking(booking.id)" 
                    class="btn btn-sm btn-outline-danger px-3 py-1 text-xs font-display">
                    Cancel Booking
                  </button>
                  <span v-else class="text-muted text-xs">-</span>
                </td>
              </tr>
              <tr v-if="myBookings.length === 0">
                <td colspan="6" class="text-center  py-4">
                  <i class="bi bi-journal-x fs-3 d-block mb-2 text-white-50"></i>
                  You haven't booked any treks yet.
                </td>
              </tr>
            </tbody>
          </table>
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

const trekkerName = computed(() => store.currentUser?.name || 'Trekker');

const availableTreks = computed(() => {
  return store.treks.filter(t => t.status === 'Open').slice(0, 3);
});

const myBookings = computed(() => {
  if (!store.currentUser) return [];
  // Show active bookings (Booked state) first
  return store.bookings.filter(b => b.userId === store.currentUser.id && b.status === 'Booked');
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

const bookTrek = (trekId) => {
  const result = store.bookTrek(trekId);
  if (result.success) {
    alert("Trek successfully booked! You can monitor details and start dates from the dashboard.");
  } else {
    alert(result.message);
  }
};

const cancelBooking = (bookingId) => {
  if (confirm("Are you sure you want to cancel this booking?")) {
    store.cancelBooking(bookingId);
  }
};
</script>

<style scoped>
.text-xs {
  font-size: 0.8rem;
}

.text-base {
  font-size: 1rem;
}

.badge {
  font-size: 0.75rem;
  padding: 0.35em 0.6em;
  border-radius: 6px;
  font-weight: 500;
}

.trek-card {
  transition: transform 0.3s, border-color 0.3s;
  background: rgba(19, 37, 54, 0.35);
  border: 1px solid var(--border) !important;
}

.trek-card:hover {
  transform: translateY(-5px);
  border-color: rgba(5, 168, 92, 0.25) !important;
}

.trek-card-img-placeholder {
  height: 140px;
  background: linear-gradient(135deg, #102131, #0c1a24);
  /* Fallback mountain background styling */
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}

.trek-image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to top, rgba(8, 17, 27, 0.9), rgba(0,0,0,0.1));
}

.line-clamp {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 38px;
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

.hover-underline:hover {
  text-decoration: underline !important;
}
</style>