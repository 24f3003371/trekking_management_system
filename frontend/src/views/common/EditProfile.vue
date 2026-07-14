<template>
  <div class="dashboard-layout">
    <Sidebar />

    <main class="dashboard-main fade-in">
      <header class="dashboard-header border-bottom border-secondary-subtle pb-3 mb-4">
        <div>
          <h1 class="h3 fw-bold mb-1 font-display text-white">Edit Profile</h1>
          <p class="text-xs mb-0 text-white-50">Update your personal details</p>
        </div>
        <div>
          <button @click="goBack" class="btn btn-outline-secondary d-flex align-items-center gap-2 text-xs py-2 px-3">
            <i class="bi bi-arrow-left"></i>
            <span>Back to Dashboard</span>
          </button>
        </div>
      </header>

      <section class="glass-panel p-4 mb-4" style="max-width: 700px;">
        <h3 class="h5 fw-bold mb-4 text-white font-display">Personal Information</h3>

        <!-- Success / Error messages -->
        <div v-if="successMsg" class="alert alert-success border-0 bg-success bg-opacity-10 text-success p-3 rounded-xl text-xs d-flex align-items-center gap-2 mb-3">
          <i class="bi bi-check-circle-fill fs-5"></i>
          <span>{{ successMsg }}</span>
        </div>
        <div v-if="errorMsg" class="alert alert-danger border-0 bg-danger bg-opacity-10 text-danger p-3 rounded-xl text-xs d-flex align-items-center gap-2 mb-3">
          <i class="bi bi-exclamation-triangle-fill fs-5"></i>
          <span>{{ errorMsg }}</span>
        </div>

        <div class="row g-3">
          <!-- Username -->
          <div class="col-md-6">
            <label class="form-label text-white-50 text-xs mb-1">Username</label>
            <input v-model="form.username" type="text" class="form-control bg-transparent border-secondary text-white text-xs" />
          </div>

          <!-- Email (read-only) -->
          <div class="col-md-6">
            <label class="form-label text-white-50 text-xs mb-1">Email <span class="badge bg-secondary text-xs ms-1">read-only</span></label>
            <input :value="form.email" type="email" class="form-control bg-dark bg-opacity-50 border-secondary text-white-50 text-xs" disabled />
          </div>

          <!-- First Name -->
          <div class="col-md-6">
            <label class="form-label text-white-50 text-xs mb-1">First Name</label>
            <input v-model="form.firstname" type="text" class="form-control bg-transparent border-secondary text-white text-xs" placeholder="Enter first name" />
          </div>

          <!-- Last Name -->
          <div class="col-md-6">
            <label class="form-label text-white-50 text-xs mb-1">Last Name</label>
            <input v-model="form.lastname" type="text" class="form-control bg-transparent border-secondary text-white text-xs" placeholder="Enter last name" />
          </div>

          <!-- Phone -->
          <div class="col-md-6">
            <label class="form-label text-white-50 text-xs mb-1">Phone</label>
            <input v-model="form.phone" type="tel" class="form-control bg-transparent border-secondary text-white text-xs" placeholder="+91 98765 43210" />
          </div>

          <!-- Gender -->
          <div class="col-md-6">
            <label class="form-label text-white-50 text-xs mb-1">Gender</label>
            <select v-model="form.gender" class="form-select bg-transparent border-secondary text-white text-xs">
              <option value="" class="bg-dark">Select Gender</option>
              <option value="male" class="bg-dark">Male</option>
              <option value="female" class="bg-dark">Female</option>
              <option value="other" class="bg-dark">Other</option>
              <option value="prefer_not_to_say" class="bg-dark">Prefer not to say</option>
            </select>
          </div>

          <!-- Address -->
          <div class="col-12">
            <label class="form-label text-white-50 text-xs mb-1">Address</label>
            <textarea v-model="form.address" rows="2" class="form-control bg-transparent border-secondary text-white text-xs" placeholder="Enter your address"></textarea>
          </div>
        </div>

        <div class="d-flex gap-2 mt-4 pt-3 border-top border-secondary-subtle">
          <button @click="saveProfile" :disabled="isSaving" class="btn btn-green px-4 py-2 text-xs font-display">
            <span v-if="isSaving"><i class="bi bi-arrow-repeat spin me-1"></i> Saving…</span>
            <span v-else><i class="bi bi-check-lg me-1"></i> Save Changes</span>
          </button>
          <button @click="resetForm" class="btn btn-outline-secondary px-4 py-2 text-xs">Reset</button>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Sidebar from '@/components/dashboard/Sidebar.vue';
import { useTrekStore } from '@/store';
import { useRouter } from 'vue-router';
import bookingService from '@/services/bookingService';

const store = useTrekStore();
const router = useRouter();

const isSaving = ref(false);
const successMsg = ref('');
const errorMsg = ref('');

const form = ref({
  username: '',
  email: '',
  firstname: '',
  lastname: '',
  phone: '',
  gender: '',
  address: '',
});

onMounted(() => {
  fetchUserData();
});

const fetchUserData = async () => {
  errorMsg.value = '';
  try {
    const { data } = await bookingService.getProfile();
    if (data.user) {
      // Update store so it is in sync
      const updatedUser = { ...store.currentUser, ...data.user };
      store.currentUser = updatedUser;
      localStorage.setItem('user', JSON.stringify(updatedUser));
      
      populateForm(data.user);
    }
  } catch (err) {
    // fallback to store value if backend query fails
    const user = store.currentUser;
    if (user) {
      populateForm(user);
    }
    errorMsg.value = err.response?.data?.message || 'Could not fetch current profile details. Loaded from cache.';
  }
};

const populateForm = (user) => {
  form.value = {
    username: user.username || '',
    email: user.email || '',
    firstname: user.firstname || '',
    lastname: user.lastname || '',
    phone: user.phone || '',
    gender: user.gender || '',
    address: user.address || '',
  };
};

const loadUserData = () => {
  fetchUserData();
};

const resetForm = () => {
  fetchUserData();
  successMsg.value = '';
  errorMsg.value = '';
};

const saveProfile = async () => {
  isSaving.value = true;
  successMsg.value = '';
  errorMsg.value = '';
  try {
    const payload = {
      username: form.value.username,
      firstname: form.value.firstname,
      lastname: form.value.lastname,
      phone: form.value.phone,
      gender: form.value.gender,
      address: form.value.address,
    };
    const { data } = await bookingService.editProfile(payload);
    // Update localStorage and store with the updated user
    if (data.user) {
      const updatedUser = { ...store.currentUser, ...data.user };
      store.currentUser = updatedUser;
      localStorage.setItem('user', JSON.stringify(updatedUser));
    }
    successMsg.value = 'Profile updated successfully!';
  } catch (err) {
    errorMsg.value = err.response?.data?.message || 'Could not update profile. Try again.';
  } finally {
    isSaving.value = false;
  }
};

const goBack = () => {
  const role = store.currentUser?.role;
  if (role === 'admin') router.push('/AdminDashboard');
  else if (role === 'staff') router.push('/StaffDashboard');
  else router.push('/TrekkerDashboard');
};
</script>

<style scoped>
.text-xs {
  font-size: 0.8rem;
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
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.spin {
  display: inline-block;
  animation: spin 1s linear infinite;
}
</style>
