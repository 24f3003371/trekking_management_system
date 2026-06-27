<template>
  <div class="login-page d-flex align-items-center justify-content-center min-vh-100 p-3 p-md-4">
    <div class="login-container glass-panel d-flex flex-column flex-lg-row overflow-hidden w-100 fade-in">
      

      <div class="form-panel d-flex flex-column justify-content-center p-4 p-md-5">
        <div class="form-wrapper mx-auto w-100">
          <div class="text-center text-lg-start mb-4">
            <h3 class="fw-bold font-display text-white mb-2">Welcome Back!</h3>
             </div>

          <div v-if="errorMessage" class="alert alert-danger border-0 bg-danger bg-opacity-10 text-danger p-3 mb-4 rounded-xl d-flex align-items-center gap-2" role="alert">
            <i class="bi bi-exclamation-triangle-fill"></i>
            <div>{{ errorMessage }}</div>
          </div>

          <form @submit.prevent="handleLogin" class="d-flex flex-column gap-3">
            <div class="form-group">
              <label for="email" class="form-label text-white-50">Email address</label>
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
              <label for="password" class="form-label text-white-50">Password</label>
              <div class="input-group">
                <span class="input-group-text glass-input-addon"><i class="bi bi-lock"></i></span>
                <input 
                  type="password" 
                  id="password" 
                  v-model="password" 
                  class="form-control glass-input" 
                  placeholder="Enter your password" 
                  required
                />
              </div>
            </div>

            <div class="d-flex justify-content-between align-items-center my-2">
              <div class="form-check">
                <input type="checkbox" class="form-check-input custom-checkbox" id="remember" v-model="rememberMe" />
                <label class="form-check-label text-white-50 text-xs" for="remember">Remember me</label>
              </div>
              <a href="#" @click.prevent="showDemoInfo" class="text-green text-decoration-none text-xs hover-underline">Forgot Password?</a>
            </div>

            <button type="submit" class="btn btn-green w-100 py-2.5 fw-bold font-display mt-2 shadow-sm rounded-xl">
              Login
            </button>
          </form>

          <div class="text-center mt-4">
            <p class="text-white-50 text-xs mb-0">
              Don't have an account? 
              <router-link to="/TrekkerRegisteration" class="text-green text-decoration-none fw-semibold hover-underline d-block d-sm-inline mt-1 mt-sm-0">
                Register as User (Trekker)
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

const selectedRole = ref('admin');
const email = ref('admin@trekflow.com');
const password = ref('admin123');
const rememberMe = ref(false);
const errorMessage = ref('');

const selectRole = (role) => {
  selectedRole.value = role;
  errorMessage.value = '';
  if (role === 'admin') {
    email.value = 'admin@trekflow.com';
    password.value = 'admin123';
  } else if (role === 'staff') {
    email.value = 'staff@trekflow.com';
    password.value = 'staff123';
  } else {
    email.value = 'user@trekflow.com';
    password.value = 'user123';
  }
};

const handleLogin = () => {
  errorMessage.value = '';
  const result = store.login(email.value, password.value);
  if (result.success) {
    if (result.user.role === 'admin') {
      router.push('/AdminDashboard');
    } else if (result.user.role === 'staff') {
      router.push('/StaffDashboard');
    } else {
      router.push('/TrekkerDashboard');
    }
  } else {
    errorMessage.value = result.message;
  }
};

const showDemoInfo = () => {
  alert("In this demonstration, you can log in using pre-configured role accounts. Click the tabs on the left to pre-fill credentials for Admin, Staff, or User.");
};
</script>

<style scoped>
.login-page {
  background: radial-gradient(circle at top right, rgba(16, 33, 49, 0.8), rgba(8, 17, 27, 1)), 
              url('@/assets/images/mountains/mountain.png') no-repeat center center;
  background-size: cover;
  background-blend-mode: multiply;
  color: var(--text);
  font-family: 'Outfit', sans-serif;
}

.login-container {
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

.btn-role {
  border: 1px solid rgba(255, 255, 255, 0.05);
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  padding: 0.85rem 1.2rem;
  color: var(--text-secondary);
  transition: all 0.25s;
}

.btn-role:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.btn-role.active {
  background: rgba(5, 168, 92, 0.12);
  border-color: var(--primary);
  color: #ffffff;
}

.btn-role i {
  font-size: 1.5rem;
  color: var(--text-secondary);
}

.btn-role.active i {
  color: #10b981;
}

.role-title {
  font-size: 0.95rem;
  font-weight: 600;
}

.role-desc {
  font-size: 0.75rem;
  opacity: 0.8;
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

.custom-checkbox {
  background-color: rgba(13, 27, 42, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.custom-checkbox:checked {
  background-color: var(--primary);
  border-color: var(--primary);
}

.text-xs {
  font-size: 0.8rem;
}
</style>