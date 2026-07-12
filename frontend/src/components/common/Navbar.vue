<template>
  <nav class="navbar navbar-expand-lg navbar-dark fixed-top glass-navbar py-3">
    <div class="container">
      <router-link to="/" class="navbar-brand d-flex align-items-center gap-2">
        <i class="bi bi-triangle-half text-green rotate-brand"></i>
        <span class="fw-bold tracking-wider brand-name">TrekFlow</span>
      </router-link>
      
      <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav mx-auto gap-1 gap-lg-3 my-2 my-lg-0">
          <li class="nav-item">
            <a href="#" class="nav-link active">Home</a>
          </li>
          <li class="nav-item">
            <router-link v-if="isTrekker" to="/BrowseTrekking" class="nav-link">Treks</router-link>
            <a v-else href="#popular-treks" class="nav-link">Treks</a>
          </li>
          <li class="nav-item">
            <a href="#map" class="nav-link">Map</a>
          </li>
          <li class="nav-item">
            <a href="#how-it-works" class="nav-link">How It Works</a>
          </li>
          <li class="nav-item">
            <a href="#about" class="nav-link">About Us</a>
          </li>
          <li class="nav-item">
            <a href="#contact" class="nav-link">Contact</a>
          </li>
        </ul>
        
        <div class="d-flex align-items-center gap-3">
          <button class="btn btn-link text-white-50 p-0 text-decoration-none hover-white">
            <i class="bi bi-search fs-5"></i>
          </button>
          
          <template v-if="!store.currentUser">
            <router-link to="/Login" class="btn btn-link text-white text-decoration-none login-btn px-3">Login</router-link>
            <router-link to="/TrekkerRegisteration" class="btn btn-green signup-btn px-4">Sign Up</router-link>
          </template>
          
          <template v-else>
            <router-link :to="dashboardRoute" class="btn btn-outline-green px-3">
              <i class="bi bi-speedometer2 me-1"></i> Dashboard
            </router-link>
            <button @click="logout" class="btn btn-link text-white-50 text-decoration-none p-0">
              <i class="bi bi-box-arrow-right fs-5"></i>
            </button>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue';
import { useTrekStore } from '@/store';
import { useRouter } from 'vue-router';

const store = useTrekStore();
const router = useRouter();

const isTrekker = computed(() => store.currentUser?.role === 'trekker');

const dashboardRoute = computed(() => {
  if (!store.currentUser) return '/Login';
  if (store.currentUser.role === 'admin') return '/AdminDashboard';
  if (store.currentUser.role === 'staff') return '/StaffDashboard';
  return '/TrekkerDashboard';
});

const logout = () => {
  store.logout();
  router.push('/');
};
</script>

<style scoped>
.glass-navbar {
  background: rgba(8, 17, 27, 0.7);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  z-index: 1050;
  transition: all 0.3s;
}

.brand-name {
  font-family: 'Outfit', sans-serif;
  letter-spacing: 1px;
  font-size: 1.45rem;
}

.rotate-brand {
  transform: rotate(45deg);
  font-size: 1.6rem;
}

.nav-link {
  color: rgba(255, 255, 255, 0.7) !important;
  font-weight: 500;
  padding: 0.5rem 0.75rem !important;
  transition: color 0.2s, border-color 0.2s;
  border-bottom: 2px solid transparent;
  font-size: 0.95rem;
}

.nav-link:hover, .nav-link.active {
  color: #ffffff !important;
}

.nav-link.active {
  border-color: var(--primary);
}

.hover-white:hover {
  color: #ffffff !important;
}

.btn-green {
  background-color: var(--primary);
  border-color: var(--primary);
  color: #ffffff;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.2s;
}

.btn-green:hover {
  background-color: var(--primary-hover);
  border-color: var(--primary-hover);
  transform: translateY(-1px);
}

.btn-outline-green {
  border: 1px solid var(--primary);
  color: #10b981;
  font-weight: 600;
  border-radius: 8px;
  background: rgba(5, 168, 92, 0.05);
  transition: all 0.2s;
}

.btn-outline-green:hover {
  background-color: var(--primary);
  color: #ffffff;
}

.login-btn {
  font-weight: 600;
  transition: opacity 0.2s;
}

.login-btn:hover {
  opacity: 0.85;
}
</style>