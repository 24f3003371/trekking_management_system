<template>
  <div class="dashboard-layout">
    <Sidebar />

    <main class="dashboard-main fade-in">
      <header class="dashboard-header border-bottom border-secondary-subtle pb-3 mb-4">
        <div>
          <h1 class="h3 fw-bold mb-1 font-display text-white">Site Settings</h1>
          <p class="text-xs mb-0 text-white-50">Manage homepage content, contact info, and visibility</p>
        </div>
      </header>

      <!-- Success / Error messages -->
      <div v-if="successMsg" class="alert alert-success border-0 bg-success bg-opacity-10 text-success p-3 rounded-xl text-xs d-flex align-items-center gap-2 mb-3" style="max-width: 900px;">
        <i class="bi bi-check-circle-fill fs-5"></i>
        <span>{{ successMsg }}</span>
      </div>
      <div v-if="errorMsg" class="alert alert-danger border-0 bg-danger bg-opacity-10 text-danger p-3 rounded-xl text-xs d-flex align-items-center gap-2 mb-3" style="max-width: 900px;">
        <i class="bi bi-exclamation-triangle-fill fs-5"></i>
        <span>{{ errorMsg }}</span>
      </div>

      <div class="row g-4" style="max-width: 900px;">
        <!-- Homepage Stats Toggle -->
        <div class="col-12">
          <section class="glass-panel p-4">
            <h3 class="h5 fw-bold mb-3 text-white font-display">
              <i class="bi bi-bar-chart-fill text-green me-2"></i>Homepage Statistics
            </h3>
            <div class="d-flex align-items-center justify-content-between">
              <div>
                <p class="text-white-50 text-xs mb-0">Show the statistics bar (Treks Available, Happy Trekkers, etc.) on the homepage.</p>
              </div>
              <div class="form-check form-switch">
                <input class="form-check-input" type="checkbox" v-model="form.show_stats" id="showStatsToggle" style="width: 3em; height: 1.5em;" />
              </div>
            </div>
          </section>
        </div>

        <!-- About Us -->
        <div class="col-12">
          <section class="glass-panel p-4">
            <h3 class="h5 fw-bold mb-3 text-white font-display">
              <i class="bi bi-info-circle-fill text-green me-2"></i>About Us
            </h3>
            <textarea v-model="form.about_us" rows="4" class="form-control bg-transparent border-secondary text-white text-xs" placeholder="Describe your trekking platform..."></textarea>
          </section>
        </div>

        <!-- How It Works -->
        <div class="col-12">
          <section class="glass-panel p-4">
            <h3 class="h5 fw-bold mb-3 text-white font-display">
              <i class="bi bi-diagram-3-fill text-green me-2"></i>How It Works
            </h3>
            <div v-for="(step, index) in form.how_it_works" :key="index" class="mb-3 p-3 bg-dark bg-opacity-20 rounded-xl border border-secondary border-opacity-10">
              <div class="d-flex align-items-center gap-2 mb-2">
                <span class="badge bg-green text-white">Step {{ step.step }}</span>
                <input v-model="step.title" type="text" class="form-control form-control-sm bg-transparent border-secondary text-white text-xs" placeholder="Step title" />
              </div>
              <textarea v-model="step.desc" rows="2" class="form-control bg-transparent border-secondary text-white text-xs" placeholder="Step description..."></textarea>
            </div>
          </section>
        </div>

        <!-- Contact Info -->
        <div class="col-12">
          <section class="glass-panel p-4">
            <h3 class="h5 fw-bold mb-3 text-white font-display">
              <i class="bi bi-telephone-fill text-green me-2"></i>Contact Information
            </h3>
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label text-white-50 text-xs mb-1">Email</label>
                <input v-model="form.contact_email" type="email" class="form-control bg-transparent border-secondary text-white text-xs" />
              </div>
              <div class="col-md-6">
                <label class="form-label text-white-50 text-xs mb-1">Phone</label>
                <input v-model="form.contact_phone" type="tel" class="form-control bg-transparent border-secondary text-white text-xs" />
              </div>
              <div class="col-12">
                <label class="form-label text-white-50 text-xs mb-1">Address</label>
                <input v-model="form.contact_address" type="text" class="form-control bg-transparent border-secondary text-white text-xs" />
              </div>
            </div>
          </section>
        </div>

        <!-- Save Button -->
        <div class="col-12">
          <button @click="saveSettings" :disabled="isSaving" class="btn btn-green px-5 py-2 text-xs font-display w-100">
            <span v-if="isSaving"><i class="bi bi-arrow-repeat spin me-1"></i> Saving…</span>
            <span v-else><i class="bi bi-check-lg me-1"></i> Save All Settings</span>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Sidebar from '@/components/dashboard/Sidebar.vue';
import api from '@/services/api';

const isSaving = ref(false);
const successMsg = ref('');
const errorMsg = ref('');

const form = ref({
  show_stats: true,
  about_us: '',
  how_it_works: [
    { step: 1, title: '', desc: '' },
    { step: 2, title: '', desc: '' },
    { step: 3, title: '', desc: '' },
  ],
  contact_email: '',
  contact_phone: '',
  contact_address: '',
});

onMounted(async () => {
  try {
    const { data } = await api.get('/admin/site-settings');
    form.value = {
      show_stats: data.show_stats ?? true,
      about_us: data.about_us || '',
      how_it_works: data.how_it_works || form.value.how_it_works,
      contact_email: data.contact_email || '',
      contact_phone: data.contact_phone || '',
      contact_address: data.contact_address || '',
    };
  } catch (err) {
    // defaults are fine
  }
});

const saveSettings = async () => {
  isSaving.value = true;
  successMsg.value = '';
  errorMsg.value = '';
  try {
    await api.put('/admin/site-settings', form.value);
    successMsg.value = 'Settings saved successfully! Changes will reflect on the homepage.';
  } catch (err) {
    errorMsg.value = err.response?.data?.message || 'Could not save settings.';
  } finally {
    isSaving.value = false;
  }
};
</script>

<style scoped>
.text-xs {
  font-size: 0.8rem;
}

.bg-green {
  background-color: var(--primary) !important;
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

.form-check-input:checked {
  background-color: var(--primary);
  border-color: var(--primary);
}
</style>
