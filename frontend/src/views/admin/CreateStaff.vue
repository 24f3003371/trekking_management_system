<template>
  <div class="dashboard-layout">
    <!-- Sidebar Component -->
    <Sidebar />

    <!-- Main Content Area -->
    <main class="dashboard-main fade-in">
      <header class="dashboard-header border-bottom border-secondary-subtle pb-3 mb-4">
        <div>
          <h1 class="h3 fw-bold mb-1 font-display text-white">Create Trekking Staff</h1>
          <p class="text-muted text-xs mb-0">Register a new guide or coordinator for trek groups</p>
        </div>
        <div>
          <router-link to="/ManageStaff" class="btn btn-outline-secondary d-flex align-items-center gap-2 text-xs py-2 px-3">
            <i class="bi bi-arrow-left"></i>
            <span>Back to Staff List</span>
          </router-link>
        </div>
      </header>

      <!-- Staff Creation Form Card -->
      <section class="glass-panel p-4 p-md-5 max-w-form mx-auto">
        <h3 class="h5 fw-bold mb-4 text-white font-display">Create New Trekking Staff</h3>

        <div v-if="errorMessage" class="alert alert-danger border-0 bg-danger bg-opacity-10 text-danger p-3 mb-4 rounded-xl d-flex align-items-center gap-2 text-xs" role="alert">
          <i class="bi bi-exclamation-triangle-fill text-xs"></i>
          <div>{{ errorMessage }}</div>
        </div>

        <div v-if="successMessage" class="alert alert-success border-0 bg-success bg-opacity-10 text-success p-3 mb-4 rounded-xl d-flex align-items-center gap-2 text-xs" role="alert">
          <i class="bi bi-check-circle-fill text-xs"></i>
          <div>{{ successMessage }}</div>
        </div>

        <form @submit.prevent="submitForm">
          <div class="row g-3.5">
            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs">Full Name</label>
              <input type="text" v-model="form.name" class="form-control glass-input text-xs" required placeholder="e.g. Vikram Singh" />
            </div>

            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs">Email Address</label>
              <input type="email" v-model="form.email" class="form-control glass-input text-xs" required placeholder="name@trekflow.com" />
            </div>

            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs">Contact Number</label>
              <input type="tel" v-model="form.contact" class="form-control glass-input text-xs" required placeholder="e.g. 9876543210" />
            </div>

            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs">Experience (in years)</label>
              <input type="number" v-model="form.experience" class="form-control glass-input text-xs" required placeholder="e.g. 5" min="0" />
            </div>

            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs">Password</label>
              <input type="password" v-model="form.password" class="form-control glass-input text-xs" required placeholder="Create staff password" />
            </div>

            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs">Confirm Password</label>
              <input type="password" v-model="form.confirmPassword" class="form-control glass-input text-xs" required placeholder="Confirm staff password" />
            </div>

            <div class="col-12">
              <label class="form-label text-white-50 text-xs">Specialization</label>
              <input type="text" v-model="form.specialization" class="form-control glass-input text-xs" required placeholder="e.g. High Altitude Climbing, Wilderness First Aid" />
            </div>

            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs">Status</label>
              <select v-model="form.status" class="form-select glass-input text-xs">
                <option value="Active">Active</option>
                <option value="Blocked">Blocked</option>
              </select>
            </div>
          </div>

          <div class="d-flex justify-content-end gap-3 mt-4 pt-3 border-top border-secondary-subtle">
            <button type="button" @click="cancel" class="btn btn-outline-secondary text-xs px-4 py-2">Cancel</button>
            <button type="submit" class="btn btn-green text-xs px-4 py-2">Create Staff</button>
          </div>
        </form>

        <div class="note-footer d-flex gap-2 text-white-50 mt-4 pt-3 border-top border-secondary-subtle" style="font-size: 0.78rem; line-height: 1.4;">
          <i class="bi bi-info-circle-fill text-green flex-shrink-0 mt-0.5"></i>
          <div>The staff member will receive an email with their login credentials to access the system.</div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Sidebar from '@/components/dashboard/Sidebar.vue';
import { useTrekStore } from '@/store';
import { useRouter } from 'vue-router';

const store = useTrekStore();
const router = useRouter();

const form = ref({
  name: '',
  email: '',
  contact: '',
  experience: '',
  password: '',
  confirmPassword: '',
  specialization: '',
  status: 'Active'
});

const errorMessage = ref('');
const successMessage = ref('');

const submitForm = () => {
  errorMessage.value = '';
  successMessage.value = '';

  if (form.value.password !== form.value.confirmPassword) {
    errorMessage.value = 'Passwords do not match.';
    return;
  }

  const result = store.createStaff(
    form.value.name,
    form.value.email,
    form.value.contact,
    form.value.password,
    form.value.experience,
    form.value.specialization
  );

  if (result.success) {
    // If blocked was chosen, update that in store (store.createStaff creates as Active)
    if (form.value.status === 'Blocked') {
      const created = store.staff.find(s => s.email === form.value.email);
      if (created) created.status = 'Blocked';
      store.saveState();
    }

    successMessage.value = 'Trekking staff created successfully!';
    setTimeout(() => {
      router.push('/ManageStaff');
    }, 1200);
  } else {
    errorMessage.value = result.message;
  }
};

const cancel = () => {
  router.push('/ManageStaff');
};
</script>

<style scoped>
.text-xs {
  font-size: 0.8rem;
}

.max-w-form {
  max-width: 680px;
}
</style>