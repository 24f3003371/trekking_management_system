<template>
  <div class="landing-page min-vh-100 text-white">
    <!-- Navbar Component -->
    <Navbar />

    <header class="hero-section container-fluid d-flex align-items-center position-relative overflow-hidden pt-5">
      <div class="container position-relative z-1 pt-5 pb-5">
        <div class="row align-items-center g-4">
          <!-- Hero Left Column: PLAN. BOOK. CONQUER. -->
          <div class="col-lg-3 text-center text-lg-start mb-4 mb-lg-0 hero-corner">
            <div class="badge bg-green bg-opacity-10 text-green border border-success-subtle px-3 py-2 mb-3 text-xs d-inline-flex align-items-center gap-1">
              <i class="bi bi-tree-fill"></i>
              <span>Your Adventure, Our Responsibility</span>
            </div>
            
            <h1 class="hero-title fw-extrabold mb-3 text-uppercase font-display">
              Plan.<br />Book.<br />
              <span class="text-green text-glow">Conquer.</span>
            </h1>
            
            <p class="hero-desc text-white-50 mb-4 fs-6 leading-relaxed">
              Discover, book and manage treks across the most stunning and challenging trails in India. Experience high alpine expeditions.
            </p>
            
            <div class="d-flex flex-column flex-sm-row justify-content-center justify-content-lg-start gap-3">
              <router-link to="/BrowseTrekking" class="btn btn-green btn-lg py-1 px-1 text-s font-display  d-flex align-items-center justify-content-center gap-2">
                <span>Explore Treks</span>
                <i class="bi bi-arrow-right"></i>
              </router-link>
              
              <button @click="watchDemo" class="btn btn-outline-light btn-lg py-1 px-1 text-s font-display  d-flex align-items-center justify-content-center gap-2 bg-dark bg-opacity-35 border-secondary border-opacity-30">
                <i class="bi bi-play-circle-fill text-green"></i>
                <span>Watch Demo</span>
              </button>
            </div>
          </div>
        
    

          <!-- Hero Center Column: Interactive Mountain Image -->
          <div v-if="activeTrek" class="col-lg-6 position-relative my-5 my-lg-0 d-flex justify-content-center">
            <div class="mountain-viewport position-relative">
              <img 
                :src="mountainImage" 
                alt="Interactive Trekking Route" 
                class=" mountain-img float"
              />
              
              <!-- Checkpoint Pins Overlays (Interactive pins & always visible labels) -->
              <div 
                v-for="(pin, index) in activeTrek.checkpoints" 
                :key="pin.name" 
                class="checkpoint-pin-wrapper" 
                :style="getPinStyle(index, activeTrek.id)">
                
                <div 
                  class="pin-container" 
                  :class="[getPinColorClass(index), { active: activeCheckpointIndex === index }]" 
                  @click="selectCheckpoint(index)">
                  <i class="bi bi-geo-alt-fill pin-icon"></i>
                  <span class="pin-dot-white"></span>
                  <!-- Pulsing ring if active -->
                  <span class="pin-pulse" v-if="activeCheckpointIndex === index"></span>
                </div>
                
                <!-- Label which is ALWAYS visible next to the pin -->
                <div class="checkpoint-label">
                  <div class="checkpoint-name">{{ pin.name }}</div>
                  <div class="checkpoint-elev" :style="{ color: getPinColorHex(index) }">{{ pin.elevation }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Hero Right Column: Selected Trek Details Panel -->
          <div v-if="activeTrek" class="col-lg-3 hero-corner">
            <div class="card glass-panel border-0 text-white p-4 float-card-glow">
              <!-- Recommended badge -->
              <div class="mb-2" v-if="activeTrek.id === 'T004'">
                <span class="badge bg-warning bg-opacity-10 text-warning border border-warning-subtle text-xs py-1 px-2 d-inline-flex align-items-center gap-1">
                  <i class="bi bi-star-fill text-warning"></i> RECOMMENDED
                </span>
              </div>
              <div class="d-flex justify-content-between align-items-start mb-3">
                <h3 class="h5 fw-bold mb-0 text-white font-display">{{ activeTrek.name }}</h3>
                <span class="badge bg-success bg-opacity-10 text-success border border-success-subtle text-xs py-1 px-2">OPEN</span>
              </div>
              
              <div v-if="activeTrek.image" class="mb-3 rounded-xl overflow-hidden border border-secondary border-opacity-20 animate-fade-in" style="max-height: 120px;">
                <img :src="activeTrek.image" class="img-fluid w-100" style="max-height: 120px; object-fit: cover;" alt="Trek Image" />
              </div>
              
              <div class="text-white-50 text-xs mb-4">
                <i class="bi bi-geo-alt-fill text-green me-1"></i>{{ activeTrek.location }} • {{ activeTrek.duration }} days
              </div>

              <!-- Trek stats grid -->
              <div class="row g-3 mb-4 text-xs border-top border-bottom border-secondary border-opacity-10 py-3">
                <div class="col-6">
                  <div class="text-white-50 mb-1">Difficulty</div>
                  <div class="fw-bold" :class="difficultyColorClass(activeTrek.difficulty)">{{ activeTrek.difficulty }}</div>
                </div>
                <div class="col-6">
                  <div class="text-white-50 mb-1">Best Season</div>
                  <div class="fw-bold text-white">{{ getBestSeason(activeTrek.name) }}</div>
                </div>
                <div class="col-6">
                  <div class="text-white-50 mb-1">Available Slots</div>
                  <div class="fw-semibold text-white">{{ activeTrek.availableSlots }} / {{ activeTrek.slots }}</div>
                </div>
                <div class="col-6">
                  <div class="text-white-50 mb-1">Trek Progress</div>
                  <div class="fw-semibold text-white">{{ activeTrek.progress }}%</div>
                </div>
              </div>

              <!-- Progress bar -->
              <div class="mb-4">
                <div class="progress" style="height: 6px; background-color: rgba(255,255,255,0.08);">
                  <div class="progress-bar bg-green" role="progressbar" :style="{ width: activeTrek.progress + '%' }" :aria-valuenow="activeTrek.progress" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
              </div>

              <!-- Users booked avatars -->
              <div class="d-flex align-items-center gap-2 mb-4">
                <div class="avatar-group d-flex align-items-center">
                  <div class="avatar-sm bg-primary text-white">A</div>
                  <div class="avatar-sm bg-warning text-dark">P</div>
                  <div class="avatar-sm bg-info text-white">R</div>
                  <div class="avatar-sm bg-secondary text-white">S</div>
                </div>
                <span class="text-white-50 text-xs">+12 Booked</span>
              </div>

              <!-- Action button -->
              <button @click="viewTrekDetails(activeTrek.id)" class="btn btn-green w-100 py-1 text-s font-display fw-bold rounded-xl d-flex align-items-center justify-content-center gap-2">
                <span>View Details</span>
                <i class="bi-arrow-right"></i>
              </button>
            </div>
          </div>
          <div v-if="!activeTrek" class="col-lg-9 text-center text-white-50 py-5">
            <i class="bi bi-hourglass-split fs-2 d-block mb-2"></i>
            Loading trek preview...
          </div>
        </div>
        
        <!-- Floating Stats Bar (Visible within Hero Viewport) -->
        <div class="row mt-5">
          <div class="col-12">
            <div class="glass-panel py-3 px-md-5">
              <div class="row text-center g-3">
                <div class="col-6 col-md-3">
                  <div class="d-flex align-items-center justify-content-center gap-3">
                    <i class="bi bi-compass fs-3 text-green"></i>
                    <div class="text-start">
                      <div class="fw-bold fs-5 font-display text-white">120+</div>
                      <div class="text-white-50 text-xs">Treks Available</div>
                    </div>
                  </div>
                </div>
                <div class="col-6 col-md-3">
                  <div class="d-flex align-items-center justify-content-center gap-3">
                    <i class="bi bi-people-fill fs-3 text-green"></i>
                    <div class="text-start">
                      <div class="fw-bold fs-5 font-display text-white">5,000+</div>
                      <div class="text-white-50 text-xs">Happy Trekkers</div>
                    </div>
                  </div>
                </div>
                <div class="col-6 col-md-3">
                  <div class="d-flex align-items-center justify-content-center gap-3">
                    <i class="bi bi-flag-fill fs-3 text-green"></i>
                    <div class="text-start">
                      <div class="fw-bold fs-5 font-display text-white">300+</div>
                      <div class="text-white-50 text-xs">Treks Completed</div>
                    </div>
                  </div>
                </div>
                <div class="col-6 col-md-3">
                  <div class="d-flex align-items-center justify-content-center gap-3">
                    <i class="bi bi-star-fill fs-3 text-green"></i>
                    <div class="text-start">
                      <div class="fw-bold fs-5 font-display text-white">4.8/5</div>
                      <div class="text-white-50 text-xs">User Rating</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Popular Treks Section -->
    <section id="popular-treks" class="py-5 container">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 class="h4 fw-bold font-display text-white mb-1">Popular Treks</h2>
          <p class="text-muted text-xs mb-0">Highly rated expeditions by alpine club members</p>
        </div>
        <div class="d-flex gap-2">
          <button @click="scrollPopular('left')" class="btn btn-outline-secondary btn-sm p-2 rounded-circle border-opacity-30">
            <i class="bi bi-chevron-left text-white"></i>
          </button>
          <button @click="scrollPopular('right')" class="btn btn-outline-secondary btn-sm p-2 rounded-circle border-opacity-30">
            <i class="bi bi-chevron-right text-white"></i>
          </button>
        </div>
      </div>

      <!-- Horizontal Cards Container -->
      <div class="popular-slider-wrapper" ref="popularSlider">
        <div 
          v-for="trek in popularTreks" 
          :key="trek.id" 
          class="popular-card-item"
          @click="viewTrekDetails(trek.id)">
          
          <div 
            class="card trek-card border-0 glass-card text-white overflow-hidden h-100 d-flex flex-column justify-content-between cursor-pointer"
            :class="{ selected: activeTrek?.id === trek.id }">
            
            <div 
              class="trek-card-img-placeholder d-flex align-items-end p-3 position-relative"
              :style="trek.image ? { backgroundImage: `url(${trek.image})`, backgroundSize: 'cover', backgroundPosition: 'center' } : {}"
            >
              <div class="trek-image-overlay"></div>
              <!-- Recommended tag overlay -->
              <span v-if="trek.id === 'T004'" class="badge bg-warning text-dark position-absolute top-2 start-2 text-xs fw-bold shadow-sm" style="z-index: 5;">
                RECOMMENDED
              </span>
              <div class="position-relative z-1 w-100 d-flex justify-content-between align-items-center">
                <span class="badge" :class="difficultyBadgeClass(trek.difficulty)">{{ trek.difficulty }}</span>
                <span class="badge bg-dark bg-opacity-70 text-white border border-secondary text-xs">{{ trek.duration }} days</span>
              </div>
            </div>

            <div class="p-3">
              <h4 class="h6 fw-bold mb-1 font-display text-white text-truncate">{{ trek.name }}</h4>
              <div class="text-white-50 text-xs mb-3"><i class="bi bi-geo-alt-fill text-green me-1"></i>{{ trek.location }}</div>
              
              <div class="d-flex justify-content-between align-items-center pt-2 border-top border-secondary border-opacity-10 text-xs">
                <span class="text-white-50">{{ trek.availableSlots }} slots left</span>
                <span class="fw-bold text-green font-display text-base">₹{{ trek.price.toLocaleString('en-IN') }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Navbar from '@/components/common/Navbar.vue';
import { useTrekStore } from '@/store';
import { useRouter } from 'vue-router';

// Import mountain image renamed previously
import mountainImage from '@/assets/images/mountains/mountain.png';

const store = useTrekStore();
const router = useRouter();

onMounted(async () => {
  if (!store.treks.length) {
    try {
      await store.fetchTreks();
      if (store.treks.length > 0) {
        selectedTrekId.value = store.treks[0].id;
      }
    } catch (err) {
      // fail silently
    }
  } else {
    selectedTrekId.value = store.treks[0].id;
  }
});

const selectedTrekId = ref(null);
const activeCheckpointIndex = ref(1); // Default Camp 1 reached

const activeTrek = computed(() => {
  if (store.treks.length === 0) return null;
  return store.treks.find(t => t.id === selectedTrekId.value) || store.treks[0];
});

const popularTreks = computed(() => {
  return store.treks.slice(0, 4); // return first 4 treks
});

const popularSlider = ref(null);

const selectTrek = (id) => {
  selectedTrekId.value = id;
  activeCheckpointIndex.value = 0; // reset checkpoint indicator
};

const selectCheckpoint = (index) => {
  activeCheckpointIndex.value = index;
  // Update progress simulation accordingly
  if (activeTrek.value) {
    const checkpointsLength = activeTrek.value.checkpoints.length;
    const progress = Math.round((index / (checkpointsLength - 1)) * 100);
    activeTrek.value.progress = progress;
  }
};

const getPinStyle = (index, trekId) => {
  // Absolute overlay coordinates based on the image size
  // Kedarkantha Trek winding positions
  const coordsKedarkantha = [
    { bottom: '12%', left: '38%' }, // Base Camp
    { bottom: '39%', left: '44%' }, // Camp 1
    { bottom: '55%', left: '47%' }, // Camp 2
    { bottom: '71%', left: '55%' }, // Camp 3
    { bottom: '88%', left: '55%' }  // Summit
  ];
  
  // Generic fallback paths for other treks
  const coordsOther = [
    { bottom: '15%', left: '25%' },
    { bottom: '35%', left: '40%' },
    { bottom: '55%', left: '58%' },
    { bottom: '75%', left: '68%' },
    { bottom: '90%', left: '72%' }
  ];
  
  const coords = trekId === 'T004' ? coordsKedarkantha : coordsOther;
  return coords[index] || coordsOther[0];
};

const getPinColorClass = (index) => {
  if (index === 0 || index === 1) return 'pin-green';
  if (index === 2) return 'pin-yellow';
  if (index === 3) return 'pin-orange';
  return 'pin-red';
};

const getPinColorHex = (index) => {
  if (index === 0 || index === 1) return '#10b981';
  if (index === 2) return '#f59e0b';
  if (index === 3) return '#f97316';
  return '#ef4444';
};

const getBestSeason = (name) => {
  if (name.includes('Kedarkantha')) return 'Dec - Apr';
  if (name.includes('Flowers')) return 'Jul - Aug';
  if (name.includes('Hampta')) return 'Jun - Sep';
  if (name.includes('Roopkund')) return 'May - Oct';
  return 'May - Sep';
};

const difficultyBadgeClass = (diff) => {
  if (diff === 'Easy') return 'bg-success bg-opacity-10 text-success border border-success-subtle';
  if (diff === 'Moderate') return 'bg-warning bg-opacity-10 text-warning border border-warning-subtle';
  return 'bg-danger bg-opacity-10 text-danger border border-danger-subtle';
};

const difficultyColorClass = (diff) => {
  if (diff === 'Easy') return 'text-success';
  if (diff === 'Moderate') return 'text-warning';
  return 'text-danger';
};

const viewTrekDetails = (trekId) => {
  // If not logged in, take to login
  if (!store.currentUser) {
    router.push('/Login');
  } else if (store.currentUser.role === 'trekker') {
    // Navigate to browse page and open modal for this trek
    router.push(`/BrowseTrekking?id=${trekId}`);
  } else {
    // Go to respective dashboard
    router.push(store.currentUser.role === 'admin' ? '/AdminDashboard' : '/StaffDashboard');
  }
};

const watchDemo = () => {
  alert("Watch Demo: High-fidelity interactive prototype details. Click any of the pulsing points on the mountain route vector to see current trek checkpoints and update elevation state. Click Popular Trek cards below to switch mountain paths!");
};

const scrollPopular = (direction) => {
  if (!popularSlider.value) return;
  const scrollAmount = 300;
  if (direction === 'left') {
    popularSlider.value.scrollLeft -= scrollAmount;
  } else {
    popularSlider.value.scrollLeft += scrollAmount;
  }
};
</script>

<style scoped>
.landing-page {
  background-color: var(--bg-primary);
  font-family: 'Outfit', sans-serif;
  background-image: radial-gradient(circle at 10% 20%, rgba(13, 27, 42, 0.4) 0%, rgba(8, 17, 27, 1) 90%);
}

.hero-section {
  min-height: 100vh;
  top:-35px;
  
}

.hero-title {
  font-size: 3.8rem;
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.8rem;
  }
}

.text-glow {
  text-shadow: 0 0 20px rgba(5, 168, 92, 0.4);
}

.hero-desc {
  line-height: 1.6;
}

.btn-green {
  background-color: var(--primary);
  border-color: var(--primary);
  color: #ffffff;
  border-radius: 10px;
  transition: all 0.25s;
}

.btn-green:hover {
  background-color: var(--primary-hover);
  border-color: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(5, 168, 92, 0.3);
}

.text-xs {
  font-size: 0.8rem;
}

.text-base {
  font-size: 1rem;
}

/* Mountain Image Viewport */
.mountain-viewport {
  width: 100%;
  max-width: 1000px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle, rgba(16, 50, 85, 0.22) 0%, rgba(8, 17, 27, 0) 70%);
}

.mountain-img {
  width: 200%;
  height: 100%;
  object-fit: contain;
}

/* Interactive Checkpoint Pins & Labels wrapper */
.checkpoint-pin-wrapper {
  position: absolute;
  z-index: 10;
  display: flex;
  align-items: center;
}

.pin-container {
  position: relative;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s;
  z-index: 10;
}

.pin-container:hover, .pin-container.active {
  transform: scale(1.18);
}

.pin-icon {
  font-size: 1.85rem;
  line-height: 1;
  filter: drop-shadow(0 2px 5px rgba(0,0,0,0.6));
}
.hero-corner{
  position: relative;
    z-index: 10;
    top:-80px;
}


/* Specific colors */
.pin-green { color: #10b981 !important; }
.pin-yellow { color: #f59e0b !important; }
.pin-orange { color: #f97316 !important; }
.pin-red { color: #ef4444 !important; }

.pin-dot-white {
  position: absolute;
  top: 9px;
  width: 7px;
  height: 7px;
  background-color: #ffffff;
  border-radius: 50%;
  z-index: 3;
}

/* Pulsing effect */
.pin-pulse {
  position: absolute;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  border: 1.5px solid currentColor;
  animation: pulseAnim 2.5s infinite;
  z-index: 1;
  pointer-events: none;
}

/* Label next to pin */
.checkpoint-label {
  margin-left: 8px;
  background: rgba(13, 27, 42, 0.55);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 4px 10px;
  border-radius: 8px;
  pointer-events: none;
  box-shadow: var(--card-shadow);
  line-height: 1.3;
  text-align: left;
  min-width: 90px;
}

.checkpoint-name {
  font-size: 0.75rem;
  font-weight: 700;
  color: #ffffff;
  font-family: 'Outfit', sans-serif;
}

.checkpoint-elev {
  font-size: 0.68rem;
  font-weight: 600;
}

.float-card-glow {
  box-shadow: 0 10px 30px rgba(5, 168, 92, 0.08);
}

.avatar-group {
  margin-left: 0.25rem;
}

.avatar-sm {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: 2px solid #0c1a24;
  margin-left: -6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  font-weight: bold;
}

/* Popular slider horizontal */
.popular-slider-wrapper {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 0.5rem 0.25rem 1.5rem 0.25rem;
}

.popular-slider-wrapper::-webkit-scrollbar {
  height: 6px;
}

.popular-slider-wrapper::-webkit-scrollbar-track {
  background: rgba(255,255,255,0.02);
  border-radius: 4px;
}

.popular-slider-wrapper::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.1);
  border-radius: 4px;
}

.popular-slider-wrapper::-webkit-scrollbar-thumb:hover {
  background: rgba(5, 168, 92, 0.3);
}

.popular-card-item {
  min-width: 260px;
  flex: 0 0 auto;
}

.trek-card {
  transition: transform 0.3s, border-color 0.3s;
  background: rgba(19, 37, 54, 0.35);
  border: 1px solid var(--border) !important;
}

.trek-card:hover, .trek-card.selected {
  transform: translateY(-5px);
  border-color: rgba(5, 168, 92, 0.35) !important;
  box-shadow: 0 8px 25px rgba(5, 168, 92, 0.08);
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
  background: linear-gradient(to top, rgba(8, 17, 27, 0.95), rgba(0,0,0,0.1));
}
</style>
