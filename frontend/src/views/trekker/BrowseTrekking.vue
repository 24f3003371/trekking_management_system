<template>
  <div class="dashboard-layout">
    <!-- Sidebar Component -->
    <Sidebar />

    <!-- Main Content Area -->
    <main class="dashboard-main fade-in">
      <header class="dashboard-header border-bottom border-secondary-subtle pb-3 mb-4">
        <div>
          <h1 class="h3 fw-bold mb-1 font-display text-white">Browse Treks</h1>
          <p class="text text-xs mb-0">Explore and book from our curated collection of stunning Indian trails</p>
        </div>
        <div class="d-flex align-items-center gap-2">
          <i class="bi bi-compass text-green fs-5"></i>
          <span class="fw-semibold text-white-50 text-xs">Total Available: {{ filteredTreks.length }}</span>
        </div>
      </header>

      <!-- Search & Filters Panel -->
      <section class="glass-panel p-3 mb-4">
        <div class="row g-2 align-items-center">
          <div class="col-md-6 col-lg-8">
            <div class="input-group">
              <span class="input-group-text bg-transparent border-secondary border-end-0 text-white-50"><i class="bi bi-search"></i></span>
              <input 
                type="text" 
                v-model="searchQuery" 
                class="form-control bg-transparent border-secondary border-start-0 text-white text-xs" 
                placeholder="Search treks by name, location, keywords..."
              />
            </div>
          </div>
          <div class="col-md-3 col-lg-2">
            <select v-model="filterDifficulty" class="form-select bg-transparent border-secondary text-white text-xs">
              <option value="" class="bg-dark">All Difficulties</option>
              <option value="Easy" class="bg-dark">Easy</option>
              <option value="Moderate" class="bg-dark">Moderate</option>
              <option value="Hard" class="bg-dark">Hard</option>
            </select>
          </div>
          <div class="col-md-3 col-lg-2">
            <select v-model="filterLocation" class="form-select bg-transparent border-secondary text-white text-xs">
              <option value="" class="bg-dark">All Locations</option>
              <option v-for="loc in uniqueLocations" :key="loc" :value="loc" class="bg-dark">{{ loc }}</option>
            </select>
          </div>
        </div>
      </section>

      <!-- Treks Grid List -->
      <section class="mb-4">
        <div class="row g-4">
          <div class="col-md-6 col-lg-4" v-for="trek in paginatedTreks" :key="trek.id">
            <div class="card trek-card h-100 border-0 glass-card text-white overflow-hidden d-flex flex-column justify-content-between">
              <!-- Visual Header -->
              <div
                class="trek-card-img-placeholder d-flex align-items-end p-3 position-relative"
                :style="trek.image ? { backgroundImage: `url(${trek.image})`, backgroundSize: 'cover', backgroundPosition: 'center' } : {}"
              >
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

              <!-- Card Action Button -->
              <div class="p-3 pt-0">
                <button 
                  @click="viewDetails(trek)" 
                  class="btn btn-green w-100 py-2 text-xs font-display fw-semibold">
                  View Details
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty state -->
        <div class="text-center py-5 glass-panel" v-if="filteredTreks.length === 0">
          <i class="bi bi-compass-fill fs-1 text-muted d-block mb-3"></i>
          <h4 class="text-white h5">No Treks Match Your Filters</h4>
          <p class="text-muted text-xs">Try adjusting your keyword search, location, or difficulty selection.</p>
        </div>
      </section>

      <!-- Mock Pagination -->
      <section class="d-flex justify-content-center mt-5" v-if="totalPages > 1">
        <nav aria-label="Page navigation">
          <ul class="pagination pagination-sm gap-2">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <button class="page-link glass-page-btn" @click="currentPage--" aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
              </button>
            </li>
            <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: currentPage === page }">
              <button class="page-link glass-page-btn" @click="currentPage = page">{{ page }}</button>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <button class="page-link glass-page-btn" @click="currentPage++" aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
              </button>
            </li>
          </ul>
        </nav>
      </section>

      <!-- High Fidelity Trek Details Modal -->
      <div v-if="selectedTrek" class="glass-modal-backdrop d-flex align-items-center justify-content-center p-3">
        <div class="glass-modal-container glass-panel p-4 p-md-5 w-100 fade-in overflow-y-auto" style="max-height: 90vh;">
          <div class="d-flex justify-content-between align-items-start border-bottom border-secondary-subtle pb-3 mb-4">
            <div>
              <span class="badge mb-2" :class="difficultyBadgeClass(selectedTrek.difficulty)">{{ selectedTrek.difficulty }}</span>
              <h3 class="h4 fw-bold text-white font-display mb-0">{{ selectedTrek.name }}</h3>
              <div class="text-white-50 text-xs mt-1"><i class="bi bi-geo-alt-fill text-green me-1"></i>{{ selectedTrek.location }}</div>
            </div>
            <button @click="closeDetails" class="btn-close btn-close-white"></button>
          </div>

          <div class="row g-4">
            <!-- Left Info Panel -->
            <div class="col-md-7">
              <div v-if="selectedTrek.image" class="mb-3 rounded-xl overflow-hidden border border-secondary border-opacity-20" style="max-height: 220px;">
                <img :src="selectedTrek.image" class="img-fluid w-100" style="max-height: 220px; object-fit: cover;" alt="Trek Image" />
              </div>
              <p class="text-white-50 text-xs leading-relaxed mb-4">{{ selectedTrek.description }}</p>
              
              <h4 class="h6 fw-bold text-white mb-2 font-display">Trek Information</h4>
              <div class="d-flex flex-column gap-2 mb-4 bg-dark bg-opacity-20 p-3 rounded-xl border border-secondary border-opacity-10 text-xs">
                <div class="d-flex justify-content-between">
                  <span class="text-white-50">Duration:</span>
                  <span class="fw-semibold text-white">{{ selectedTrek.duration }}</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-white-50">Trek Start Date:</span>
                  <span class="fw-semibold text-white">{{ formatDate(selectedTrek.startDate) }}</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-white-50">Trek End Date:</span>
                  <span class="fw-semibold text-white">{{ formatDate(selectedTrek.endDate) }}</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-white-50">Available Slots:</span>
                  <span class="fw-semibold text-white">{{ selectedTrek.availableSlots }} left / {{ selectedTrek.slots }} total</span>
                </div>
              </div>
            </div>

            <!-- Right Elevation Checkpoint Panel -->
            <div class="col-md-5">
              <h4 class="h6 fw-bold text-white mb-3 font-display">Trail Map & Elevation Points</h4>
              
              <div class="checkpoint-timeline ps-3 position-relative border-start border-secondary border-opacity-30 ms-2">
                <div class="checkpoint-node mb-3 position-relative" v-for="(node, index) in selectedTrek.checkpoints" :key="node.name">
                  <div class="timeline-dot bg-green"></div>
                  <div class="text-xs fw-semibold text-white">{{ node.name }}</div>
                  <div class="text-muted text-xs">{{ node.elevation }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Price & Booking Footer -->
          <div class="d-flex flex-sm-row justify-content-between align-items-center gap-3 mt-4 pt-3 border-top border-secondary-subtle">
            <div>
              <div class="text-muted text-xs">Total Trekking Fee (all inclusive)</div>
              <div class="fw-bold text-green font-display fs-4">₹{{ selectedTrek.price.toLocaleString('en-IN') }}</div>
            </div>
            
            <button 
              v-if="selectedTrek.availableSlots > 0"
              @click="confirmBooking(selectedTrek.id)"
              class="btn btn-green px-5 py-2.5 text-xs font-display fw-bold rounded-xl">
              Book Trek Now
            </button>
            <button 
              v-else
              disabled
              class="btn btn-outline-secondary px-5 py-2.5 text-xs font-display fw-bold rounded-xl text-white-50 border-secondary border-opacity-30">
              Not Available / Fully Booked
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import Sidebar from '@/components/dashboard/Sidebar.vue';
import { useTrekStore } from '@/store';

const store = useTrekStore();
const route = useRoute();

const searchQuery = ref('');
const filterDifficulty = ref('');
const filterLocation = ref('');

const selectedTrek = ref(null);

onMounted(async () => {
  if (store.treks.length === 0) {
    await store.fetchTreks();
  }
  const trekIdParam = route.query.id;
  if (trekIdParam) {
    const trekId = Number(trekIdParam);
    const trek = store.treks.find(t => t.id === trekId);
    if (trek) {
      selectedTrek.value = trek;
    }
  }
});

// Pagination
const currentPage = ref(1);
const itemsPerPage = 6;

const uniqueLocations = computed(() => {
  const locs = store.treks.map(t => t.location);
  return [...new Set(locs)];
});

const filteredTreks = computed(() => {
  return store.treks.filter(t => {
    if (t.status !== 'Open') return false;
    const matchesSearch = t.name.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                          t.location.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesDifficulty = filterDifficulty.value === '' || t.difficulty === filterDifficulty.value;
    const matchesLocation = filterLocation.value === '' || t.location === filterLocation.value;
    return matchesSearch && matchesDifficulty && matchesLocation;
  });
});

const totalPages = computed(() => {
  return Math.ceil(filteredTreks.value.length / itemsPerPage);
});

const paginatedTreks = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return filteredTreks.value.slice(start, start + itemsPerPage);
});

const difficultyBadgeClass = (diff) => {
  if (diff === 'Easy') return 'bg-success bg-opacity-10 text-success border border-success-subtle';
  if (diff === 'Moderate') return 'bg-warning bg-opacity-10 text-warning border border-warning-subtle';
  return 'bg-danger bg-opacity-10 text-danger border border-danger-subtle';
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' });
};

const viewDetails = (trek) => {
  selectedTrek.value = trek;
};

const closeDetails = () => {
  selectedTrek.value = null;
};

const confirmBooking = (trekId) => {
  const result = store.bookTrek(trekId);
  if (result.success) {
    alert("Trek successfully booked! You can monitor details and start dates from the dashboard.");
    closeDetails();
  } else {
    alert(result.message);
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

.glass-page-btn {
  background: rgba(13, 27, 42, 0.4);
  border: 1px solid var(--border);
  color: var(--text-secondary);
  transition: all 0.2s;
  border-radius: 8px;
  padding: 0.4rem 0.75rem;
}

.glass-page-btn:hover {
  background: rgba(5, 168, 92, 0.1);
  color: #ffffff;
  border-color: var(--primary);
}

.pagination .active .glass-page-btn {
  background: var(--primary) !important;
  color: #ffffff !important;
  border-color: var(--primary) !important;
}

.glass-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  z-index: 1060;
}

.glass-modal-container {
  max-width: 720px;
  background: rgba(13, 27, 42, 0.95);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
  border-radius: var(--radius);
}

/* Timeline Elevation Points */
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
</style>