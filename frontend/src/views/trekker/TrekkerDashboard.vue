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
              <div
                class="trek-card-img-placeholder d-flex align-items-end p-3 position-relative"
                :style="trek.image ? { backgroundImage: `url(${trek.image})`, backgroundSize: 'cover', backgroundPosition: 'center' } : {}"
              >
                <div class="trek-image-overlay"></div>
                <div class="position-relative z-1 w-100 d-flex justify-content-between align-items-center">
                  <span class="badge" :class="difficultyBadgeClass(trek.difficulty)">{{ trek.difficulty }}</span>
                  <span class="badge bg-dark bg-opacity-70 text-white border border-secondary text-xs"><i class="bi bi-clock me-1"></i>{{ trek.duration }} days</span>
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
                  v-if="store.bookedTrekIds.has(trek.id)"
                  disabled
                  class="btn btn-booked w-100 py-2 text-xs font-display fw-semibold">
                  <i class="bi bi-check-circle-fill me-1"></i>Booked
                </button>
                <button 
                  v-else-if="trek.availableSlots > 0" 
                  @click="openBookingModal(trek)" 
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

    <!-- ============================================================ -->
    <!-- Multi-Step Booking & Payment Modal                           -->
    <!-- ============================================================ -->
    <div v-if="selectedTrek" class="glass-modal-backdrop d-flex align-items-center justify-content-center p-3" @click.self="closeModal">
      <div class="glass-modal-container glass-panel p-4 p-md-5 w-100 fade-in overflow-y-auto" style="max-height: 90vh;">

        <!-- Step 1: Trek Details -->
        <div v-if="currentStep === 'details'">
          <div class="d-flex justify-content-between align-items-start border-bottom border-secondary-subtle pb-3 mb-4">
            <div>
              <span class="badge mb-2" :class="difficultyBadgeClass(selectedTrek.difficulty)">{{ selectedTrek.difficulty }}</span>
              <h3 class="h4 fw-bold text-white font-display mb-0">{{ selectedTrek.name }}</h3>
              <div class="text-white-50 text-xs mt-1"><i class="bi bi-geo-alt-fill text-green me-1"></i>{{ selectedTrek.location }}</div>
            </div>
            <button @click="closeModal" class="btn-close btn-close-white"></button>
          </div>

          <div class="row g-4">
            <div class="col-md-7">
              <div v-if="selectedTrek.image" class="mb-3 rounded-xl overflow-hidden border border-secondary border-opacity-20" style="max-height: 200px;">
                <img :src="selectedTrek.image" class="img-fluid w-100" style="max-height: 200px; object-fit: cover;" alt="Trek Image" />
              </div>
              <p class="text-white-50 text-xs leading-relaxed mb-4">{{ selectedTrek.description }}</p>

              <h4 class="h6 fw-bold text-white mb-2 font-display">Trek Information</h4>
              <div class="d-flex flex-column gap-2 bg-dark bg-opacity-20 p-3 rounded-xl border border-secondary border-opacity-10 text-xs">
                <div class="d-flex justify-content-between">
                  <span class="text-white-50">Duration:</span>
                  <span class="fw-semibold text-white">{{ selectedTrek.duration }} days</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-white-50">Available Slots:</span>
                  <span class="fw-semibold text-white">{{ selectedTrek.availableSlots }} left</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-white-50">Location:</span>
                  <span class="fw-semibold text-white">{{ selectedTrek.location }}</span>
                </div>
              </div>
            </div>

            <div class="col-md-5">
              <h4 class="h6 fw-bold text-white mb-3 font-display">Trail Checkpoints</h4>
              <div v-if="selectedTrek.checkpoints && selectedTrek.checkpoints.length > 0" class="checkpoint-timeline ps-3 position-relative border-start border-secondary border-opacity-30 ms-2">
                <div class="checkpoint-node mb-3 position-relative" v-for="node in selectedTrek.checkpoints" :key="node.name">
                  <div class="timeline-dot bg-green"></div>
                  <div class="text-xs fw-semibold text-white">{{ node.name }}</div>
                  <div class="text-muted text-xs">{{ node.elevation }}</div>
                </div>
              </div>
              <div v-else class="text-white-50 text-xs">No checkpoint data available.</div>
            </div>
          </div>

          <div class="d-flex flex-sm-row justify-content-between align-items-center gap-3 mt-4 pt-3 border-top border-secondary-subtle">
            <div>
              <div class="text-muted text-xs">Total Trekking Fee (all inclusive)</div>
              <div class="fw-bold text-green font-display fs-4">₹{{ selectedTrek.price.toLocaleString('en-IN') }}</div>
            </div>
            <button @click="currentStep = 'payment'" class="btn btn-green px-5 py-2 text-xs font-display fw-bold rounded-xl">
              Book Trek Now
            </button>
          </div>
        </div>

        <!-- Step 2: Payment -->
        <div v-else-if="currentStep === 'payment'">
          <div class="d-flex justify-content-between align-items-start border-bottom border-secondary-subtle pb-3 mb-4">
            <div>
              <span class="badge bg-green bg-opacity-10 text-green border border-success-subtle mb-2 text-xs">SECURE CHECKOUT</span>
              <h3 class="h4 fw-bold text-white font-display mb-0">Confirm Booking & Pay</h3>
              <div class="text-white-50 text-xs mt-1">{{ selectedTrek.name }} • ₹{{ selectedTrek.price.toLocaleString('en-IN') }}</div>
            </div>
            <button @click="closeModal" class="btn-close btn-close-white" :disabled="isPaying"></button>
          </div>

          <!-- Success Screen -->
          <div v-if="paymentSuccess" class="text-center py-5">
            <div class="mb-4">
              <i class="bi bi-check-circle-fill text-green" style="font-size: 4rem;"></i>
            </div>
            <h4 class="h5 text-white fw-bold font-display mb-2">Booking Confirmed!</h4>
            <p class="text-white-50 text-xs px-4 mb-4">
              Your payment of ₹{{ selectedTrek.price.toLocaleString('en-IN') }} has been processed successfully. Check your bookings below.
            </p>
            <button @click="closeModal" class="btn btn-green px-5 py-2 text-xs font-display fw-bold rounded-xl">
              Close
            </button>
          </div>

          <!-- Payment Form -->
          <div v-else class="row g-4">
            <!-- Method Selector -->
            <div class="col-md-5 border-end border-secondary border-opacity-20">
              <h4 class="h6 fw-bold text-white mb-3 font-display">Payment Method</h4>
              <div class="d-flex flex-column gap-2">
                <button type="button"
                  class="btn text-start text-xs p-3 rounded-xl border d-flex align-items-center gap-3 w-100"
                  :class="paymentMethod === 'card' ? 'btn-green-outline' : 'btn-dark-outline'"
                  @click="paymentMethod = 'card'">
                  <i class="bi bi-credit-card fs-5 text-white"></i>
                  <div>
                    <div class="fw-bold text-white">Credit / Debit Card</div>
                    <div class="text-white-50 text-xxs">Visa, Mastercard, RuPay</div>
                  </div>
                </button>

                <button type="button"
                  class="btn text-start text-xs p-3 rounded-xl border d-flex align-items-center gap-3 w-100"
                  :class="paymentMethod === 'upi' ? 'btn-green-outline' : 'btn-dark-outline'"
                  @click="paymentMethod = 'upi'">
                  <i class="bi bi-phone-vibrate fs-5 text-white"></i>
                  <div>
                    <div class="fw-bold text-white">UPI Payment</div>
                    <div class="text-white-50 text-xxs">Google Pay, PhonePe, BHIM</div>
                  </div>
                </button>

                <button type="button"
                  class="btn text-start text-xs p-3 rounded-xl border d-flex align-items-center gap-3 w-100"
                  :class="paymentMethod === 'netbanking' ? 'btn-green-outline' : 'btn-dark-outline'"
                  @click="paymentMethod = 'netbanking'">
                  <i class="bi bi-bank fs-5 text-white"></i>
                  <div>
                    <div class="fw-bold text-white">Net Banking</div>
                    <div class="text-white-50 text-xxs">Instant Bank Transfer</div>
                  </div>
                </button>
              </div>
            </div>

            <!-- Billing Details -->
            <div class="col-md-7">
              <h4 class="h6 fw-bold text-white mb-3 font-display">Billing Details</h4>

              <!-- Card -->
              <div v-if="paymentMethod === 'card'" class="d-flex flex-column gap-3">
                <div>
                  <label class="form-label text-white-50 text-xs">Cardholder Name</label>
                  <input type="text" class="form-control glass-input text-xs" v-model="dummyCard.name" />
                </div>
                <div>
                  <label class="form-label text-white-50 text-xs">Card Number</label>
                  <input type="text" class="form-control glass-input text-xs" v-model="dummyCard.number" placeholder="XXXX XXXX XXXX XXXX" />
                </div>
                <div class="row g-2">
                  <div class="col-6">
                    <label class="form-label text-white-50 text-xs">Expiry Date</label>
                    <input type="text" class="form-control glass-input text-xs" v-model="dummyCard.expiry" placeholder="MM/YY" />
                  </div>
                  <div class="col-6">
                    <label class="form-label text-white-50 text-xs">CVV</label>
                    <input type="password" class="form-control glass-input text-xs" v-model="dummyCard.cvv" placeholder="123" />
                  </div>
                </div>
              </div>

              <!-- UPI -->
              <div v-else-if="paymentMethod === 'upi'" class="d-flex flex-column gap-3">
                <div>
                  <label class="form-label text-white-50 text-xs">UPI Address ID</label>
                  <input type="text" class="form-control glass-input text-xs" v-model="dummyUpi" placeholder="username@upi" />
                </div>
                <div class="text-white-50 text-xs bg-dark bg-opacity-20 p-3 rounded-xl border border-secondary border-opacity-10">
                  <i class="bi bi-shield-check text-green me-2"></i>A secure dummy UPI request will be simulated. Click Pay to proceed.
                </div>
              </div>

              <!-- Net Banking -->
              <div v-else-if="paymentMethod === 'netbanking'" class="d-flex flex-column gap-3">
                <div>
                  <label class="form-label text-white-50 text-xs">Select Preferred Bank</label>
                  <select class="form-select glass-input text-xs text-white">
                    <option class="bg-dark">State Bank of India</option>
                    <option class="bg-dark">HDFC Bank</option>
                    <option class="bg-dark">ICICI Bank</option>
                    <option class="bg-dark">Axis Bank</option>
                  </select>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="d-flex gap-3 mt-4 pt-3 border-top border-secondary border-opacity-20">
                <button type="button" class="btn btn-outline-secondary text-xs px-4" :disabled="isPaying" @click="currentStep = 'details'">
                  Back
                </button>
                <button
                  type="button"
                  class="btn btn-green text-xs px-5 flex-grow-1 fw-bold d-flex align-items-center justify-content-center gap-2"
                  :disabled="isPaying"
                  @click="processPayment">
                  <span v-if="isPaying" class="spinner-border spinner-border-sm" role="status"></span>
                  <span>{{ isPaying ? 'Processing Payment...' : `Pay ₹${selectedTrek.price.toLocaleString('en-IN')}` }}</span>
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import Sidebar from '@/components/dashboard/Sidebar.vue';
import { useTrekStore } from '@/store';

const store = useTrekStore();

const trekkerName = computed(() => store.currentUser?.name || 'Trekker');

const availableTreks = computed(() => {
  return store.treks.filter(t => t.status === 'Open').slice(0, 3);
});

const myBookings = computed(() => {
  if (!store.currentUser) return [];
  return store.bookings.filter(b => b.userId === store.currentUser.id && b.status === 'Booked');
});

// --- Modal State ---
const selectedTrek = ref(null);
const currentStep = ref('details');
const paymentMethod = ref('card');
const isPaying = ref(false);
const paymentSuccess = ref(false);

const dummyCard = ref({
  name: 'John Doe',
  number: '4111 2222 3333 4444',
  expiry: '12/28',
  cvv: '123',
});
const dummyUpi = ref('trekker@okaxis');

const openBookingModal = (trek) => {
  selectedTrek.value = trek;
  currentStep.value = 'details';
  paymentSuccess.value = false;
  isPaying.value = false;
  paymentMethod.value = 'card';
};

const closeModal = () => {
  if (isPaying.value) return;
  selectedTrek.value = null;
  paymentSuccess.value = false;
  isPaying.value = false;
  currentStep.value = 'details';
};

const processPayment = async () => {
  if (isPaying.value) return;
  isPaying.value = true;

  // Simulate 1.5s payment gateway delay
  await new Promise(resolve => setTimeout(resolve, 1500));

  const result = await store.bookTrek(selectedTrek.value.id);
  isPaying.value = false;

  if (result.success) {
    paymentSuccess.value = true;
  } else {
    alert(result.message || 'Booking failed. Please try again.');
  }
};

// --- Helpers ---
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

const cancelBooking = (bookingId) => {
  if (confirm('Are you sure you want to cancel this booking?')) {
    store.cancelBooking(bookingId);
  }
};
</script>

<style scoped>
.text-xs {
  font-size: 0.8rem;
}

.text-xxs {
  font-size: 0.7rem;
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

.btn-booked {
  background: rgba(5, 168, 92, 0.12);
  border: 1px solid rgba(5, 168, 92, 0.35);
  color: var(--primary);
  cursor: default;
}

.hover-underline:hover {
  text-decoration: underline !important;
}

/* Modal */
.glass-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(8px);
  z-index: 1060;
}

.glass-modal-container {
  max-width: 760px;
  background: rgba(13, 27, 42, 0.97);
  box-shadow: 0 24px 50px rgba(0, 0, 0, 0.6);
  border-radius: var(--radius);
  scrollbar-width: thin;
  scrollbar-color: rgba(5, 168, 92, 0.4) transparent;
}

/* Timeline */
.timeline-dot {
  position: absolute;
  left: -21px;
  top: 4px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid #ffffff;
}

.checkpoint-node {
  padding-left: 0.5rem;
}

/* Payment method buttons */
.btn-green-outline {
  background: rgba(5, 168, 92, 0.08) !important;
  border: 1px solid var(--primary) !important;
  color: #ffffff !important;
  text-align: left;
}

.btn-dark-outline {
  background: rgba(13, 27, 42, 0.4) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  color: var(--text-secondary) !important;
  text-align: left;
}

.btn-dark-outline:hover {
  background: rgba(13, 27, 42, 0.6) !important;
  border-color: rgba(255, 255, 255, 0.25) !important;
  color: #ffffff !important;
}
</style>