<template>
  <div class="register-page d-flex align-items-center justify-content-center min-vh-100 p-3 p-md-4">
    <div class="register-container glass-panel d-flex flex-column flex-lg-row overflow-hidden w-100 fade-in">
      <!-- Left Panel: Info and Background -->
      <div class="brand-panel d-flex flex-column justify-content-between p-4 p-md-5">
        <div>
          <div class="d-flex align-items-center gap-2 mb-3">
            <i class="bi bi-triangle-half text-green rotate-brand fs-3"></i>
            <span class="fw-bold tracking-wider fs-3 text-white font-display">TrekFlow</span>
          </div>
          <h2 class="h4 text-white-50 mb-4 fw-normal text-uppercase tracking-wide font-display" style="font-size: 0.85rem; letter-spacing: 0.1em;">
            Trekking Management Application
          </h2>
        </div>

        <div class="my-4 text-center text-lg-start">
          <h1 class="h3 fw-bold text-white mb-3 font-display">Begin Your Journey</h1>
          <p class="text-white-50 fs-6">
            Register as a Trekker to explore paths, track your elevation progress, and book journeys.
          </p>
        </div>

        <div class="note-footer d-flex gap-2 text-white-50" style="font-size: 0.78rem; line-height: 1.4;">
          <i class="bi bi-info-circle-fill text-green flex-shrink-0 mt-0.5"></i>
          <div>
            <strong>Note:</strong> Only Users (Trekkers) can register themselves.
            Trekking Staff are created by Admin.
          </div>
        </div>
      </div>

      <!-- Right Panel: Registration Form -->
      <div class="form-panel d-flex flex-column justify-content-center p-4 p-md-5">
        <div class="form-wrapper mx-auto w-100">
          <div class="text-center text-lg-start mb-4">
            <h3 class="fw-bold font-display text-white mb-2">Create User Account</h3>
            <p class="text-muted">Register as a Trekker</p>
          </div>

          <div v-if="errorMessage" class="alert alert-danger border-0 bg-danger bg-opacity-10 text-danger p-3 mb-4 rounded-xl d-flex align-items-center gap-2" role="alert">
            <i class="bi bi-exclamation-triangle-fill"></i>
            <div>{{ errorMessage }}</div>
          </div>
          
          <div v-if="successMessage" class="alert alert-success border-0 bg-success bg-opacity-10 text-success p-3 mb-4 rounded-xl d-flex align-items-center gap-2" role="alert">
            <i class="bi bi-check-circle-fill"></i>
            <div>{{ successMessage }}</div>
          </div>

          <form @submit.prevent="handleRegister" class="d-flex flex-column gap-2.5">
            <div class="form-group">
              <label for="name" class="form-label text-white-50 mb-1">Full Name</label>
              <div class="input-group">
                <span class="input-group-text glass-input-addon"><i class="bi bi-person"></i></span>
                <input 
                  type="text" 
                  id="name" 
                  v-model="name" 
                  class="form-control glass-input" 
                  placeholder="Enter full name" 
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="email" class="form-label text-white-50 mb-1">Email address</label>
              <div class="input-group">
                <span class="input-group-text glass-input-addon"><i class="bi bi-envelope"></i></span>
                <input 
                  type="email" 
                  id="email" 
                  v-model="email" 
                  class="form-control glass-input" 
                  placeholder="name@example.com" 
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="contact" class="form-label text-white-50 mb-1">Contact Number</label>
              <div class="input-group">
                <span class="input-group-text glass-input-addon"><i class="bi bi-telephone"></i></span>
                <input 
                  type="tel" 
                  id="contact" 
                  v-model="contact" 
                  class="form-control glass-input" 
                  placeholder="e.g. 9876543210" 
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="password" class="form-label text-white-50 mb-1">Password</label>
              <div class="input-group">
                <span class="input-group-text glass-input-addon"><i class="bi bi-lock"></i></span>
                <input 
                  type="password" 
                  id="password" 
                  v-model="password" 
                  class="form-control glass-input" 
                  placeholder="Create password" 
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="confirmPassword" class="form-label text-white-50 mb-1">Confirm Password</label>
              <div class="input-group">
                <span class="input-group-text glass-input-addon"><i class="bi bi-lock-fill"></i></span>
                <input 
                  type="password" 
                  id="confirmPassword" 
                  v-model="confirmPassword" 
                  class="form-control glass-input" 
                  placeholder="Confirm password" 
                  required
                />
              </div>
            </div>

            <button type="submit" class="btn btn-green w-100 py-2.5 fw-bold font-display mt-3 shadow-sm rounded-xl">
              Register
            </button>
          </form>

          <div class="text-center mt-4">
            <p class="text-white-50 text-xs mb-0">
              Already have an account? 
              <router-link to="/Login" class="text-green text-decoration-none fw-semibold hover-underline">
                Login here
              </router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useTrekStore } from '@/store';
import { useRouter } from 'vue-router';

const store = useTrekStore();
const router = useRouter();

const name = ref('');
const email = ref('');
const contact = ref('');
const password = ref('');
const confirmPassword = ref('');
const errorMessage = ref('');
const successMessage = ref('');

const handleRegister = () => {
  errorMessage.value = '';
  successMessage.value = '';

  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match.';
    return;
  }

  const result = store.register(name.value, email.value, password.value, contact.value);
  if (result.success) {
    successMessage.value = 'Registration successful! Redirecting to login...';
    setTimeout(() => {
      router.push('/Login');
    }, 1500);
  } else {
    errorMessage.value = result.message;
  }
};
</script>

<style scoped>
.register-page {
  background: radial-gradient(circle at top right, rgba(16, 33, 49, 0.8), rgba(8, 17, 27, 1)), 
              url('@/assets/images/mountains/mountain.png') no-repeat center center;
  background-size: cover;
  background-blend-mode: multiply;
  color: var(--text);
  font-family: 'Outfit', sans-serif;
}

.register-container {
  max-width: 980px;
  min-height: 580px;
  border-radius: var(--radius);
}

.brand-panel {
  background: linear-gradient(135deg, rgba(8, 25, 38, 0.85), rgba(12, 33, 50, 0.7));
  border-right: 1px solid var(--border);
  flex: 1.1;
}

.form-panel {
  background: rgba(13, 27, 42, 0.4);
  flex: 1.2;
}

.form-wrapper {
  max-width: 380px;
}

.rotate-brand {
  transform: rotate(45deg);
}

.glass-input-addon {
  background: rgba(13, 27, 42, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-right: none;
  color: var(--text-secondary);
  border-top-left-radius: 10px;
  border-bottom-left-radius: 10px;
}

.glass-input {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
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
  transform: translateY(-1px);
}

.hover-underline:hover {
  text-decoration: underline !important;
}

.text-xs {
  font-size: 0.8rem;
}
</style>