<template>
  <div class="dashboard-layout">
    <Sidebar />

    <main class="dashboard-main fade-in">
      <header
        class="dashboard-header border-bottom border-secondary-subtle pb-3 mb-4"
      >
        <div>
          <h1 class="h3 fw-bold mb-1 font-display text-white">Create Trek</h1>
          <p class="text text-xs mb-0">
            Create a new trek and assign it to trekking staff
          </p>
        </div>
      </header>

      <section class="glass-panel p-4 p-md-5 max-w-form mx-auto">
        <div
          class="d-flex justify-content-between align-items-start gap-3 border-bottom border-secondary-subtle pb-3 mb-4"
        >
          <div>
            <h3 class="h5 fw-bold mb-1 text-white font-display">
              Create New Trek
            </h3>
            <p class="text text-xs mb-0">
              Fill in the trek details, route, and staff assignment.
            </p>
          </div>
        </div>

        <div
          v-if="errorMessage"
          class="alert alert-danger border-0 bg-danger bg-opacity-10 text-danger p-3 mb-4 rounded-xl d-flex align-items-center gap-2 text-xs"
          role="alert"
        >
          <i class="bi bi-exclamation-triangle-fill"></i>
          <div>{{ errorMessage }}</div>
        </div>

        <div
          v-if="successMessage"
          class="alert alert-success border-0 bg-success bg-opacity-10 text-success p-3 mb-4 rounded-xl d-flex align-items-center gap-2 text-xs"
          role="alert"
        >
          <i class="bi bi-check-circle-fill"></i>
          <div>{{ successMessage }}</div>
        </div>

        <form @submit.prevent="submitForm">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs">Trek Name</label>
              <input
                v-model="form.name"
                type="text"
                class="form-control glass-input text-xs"
                required
                placeholder="e.g. Everest Base Camp"
              />
            </div>

            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs">Location</label>
              <input
                v-model="form.location"
                type="text"
                class="form-control glass-input text-xs"
                required
                placeholder="e.g. Nepal / Uttarakhand"
              />
            </div>

            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs">Start Date</label>
              <input
                v-model="form.startDate"
                type="date"
                class="form-control glass-input text-xs"
                required
              />
            </div>

            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs">End Date</label>
              <input
                v-model="form.endDate"
                type="date"
                class="form-control glass-input text-xs"
                required
              />
            </div>
            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs">Difficulty</label>
              <select
                v-model="form.difficulty"
                class="form-select glass-input text-xs"
                required
              >
                <option value="Easy">Easy</option>
                <option value="Moderate">Moderate</option>
                <option value="Hard">Hard</option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs">Duration</label>
              <input
                :value="trekDuration || 'Auto from dates'"
                type="text"
                class="form-control glass-input text-xs"
                readonly
              />
              <small class="text-white-50 d-block mt-1 text-xs">
                Auto-calculated from start and end date.
              </small>
            </div>

            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs"
                >Available Slots</label
              >
              <input
                v-model="form.availableSlot"
                type="number"
                min="1"
                class="form-control glass-input text-xs"
                required
                placeholder="e.g. 15"
              />
            </div>

            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs"
                >Assign Trekking Staff</label
              >
              <select
                v-model="form.staffId"
                class="form-select glass-input text-xs"
                required
              >
                <option disabled value="">Select staff</option>
                <option
                  v-for="member in activeStaff"
                  :key="member.id"
                  :value="member.id"
                >
                  {{ member.username }} ({{ member.phone || "No phone" }})
                </option>
              </select>
            </div>

            <div class="col-12">
              <label class="form-label text-white-50 text-xs">Route</label>
              <textarea
                v-model="form.route"
                class="form-control glass-input text-xs"
                rows="3"
                required
                placeholder="Describe the trek route, major stops, and itinerary"
              ></textarea>
            </div>

            <div class="col-12">
              <label class="form-label text-white-50 text-xs"
                >Major Stops</label
              >
              <div class="d-flex gap-2 mb-2">
                <input
                  v-model="majorStopDraft"
                  type="text"
                  class="form-control glass-input text-xs"
                  placeholder="Add a stop like Namche Bazaar or Phakding"
                  @keydown.enter.prevent="addMajorStop"
                />
                <button
                  type="button"
                  class="btn btn-outline-secondary text-xs px-3"
                  @click="addMajorStop"
                >
                  Add Stop
                </button>
              </div>
              <div class="d-flex flex-wrap gap-2">
                <span
                  v-for="(stop, index) in form.majorStops"
                  :key="`${stop}-${index}`"
                  class="chip-item"
                >
                  {{ stop }}
                  <button type="button" @click="removeMajorStop(index)">
                    ×
                  </button>
                </span>
              </div>
            </div>

            <div class="col-12">
              <label class="form-label text-white-50 text-xs"
                >Package Inclusions</label
              >
              <div class="row g-2">
                <div
                  v-for="tag in trekTagOptions"
                  :key="tag"
                  class="col-md-4 col-lg-3"
                >
                  <button
                    type="button"
                    class="btn w-100 text-xs inclusion-chip"
                    :class="{ active: form.trekTags.includes(tag) }"
                    @click="toggleTag(tag)"
                  >
                    {{ tag }}
                  </button>
                </div>
              </div>
            </div>

            <div class="col-md-6">
              <label class="form-label text-white-50 text-xs">
                Price per Person
              </label>
              <input
                v-model="form.price"
                type="number"
                min="0"
                step="1"
                class="form-control glass-input text-xs"
                required
                placeholder="e.g. 18999"
              />
            </div>

            <div class="col-12">
              <label class="form-label text-white-50 text-xs">Trek Image (Optional)</label>
              <div class="d-flex align-items-center gap-2">
                <input
                  type="file"
                  accept="image/*"
                  class="form-control glass-input text-xs d-none"
                  ref="fileInput"
                  @change="handleImageUpload"
                />
                <button
                  type="button"
                  class="btn btn-outline-secondary text-xs px-3"
                  @click="fileInput.click()"
                >
                  Choose Image
                </button>
                <button
                  type="button"
                  v-if="form.image"
                  class="btn btn-outline-danger text-xs px-3"
                  @click="clearImage"
                >
                  Remove
                </button>
                <span class="text-white-50 text-xs ms-2" v-if="form.image">Image selected</span>
                <span class="text-white-50 text-xs ms-2" v-else>No image chosen (optional)</span>
              </div>
              <div v-if="form.image" class="mt-2 rounded-xl overflow-hidden border border-secondary border-opacity-30" style="max-width: 200px;">
                <img :src="form.image" class="img-fluid" style="max-height: 120px; object-fit: cover;" alt="Preview" />
              </div>
            </div>

            <div class="col-12">
              <label class="form-label text-white-50 text-xs"
                >Description</label
              >
              <textarea
                v-model="form.description"
                class="form-control glass-input text-xs"
                rows="3"
                required
                placeholder="Provide a brief description of the trek"
              ></textarea>
            </div>
          </div>

          <div
            class="d-flex justify-content-start gap-3 mt-4 pt-3 border-top border-secondary-subtle"
          >
            <button
              type="submit"
              class="btn btn-green text-xs px-4 py-2"
              :disabled="isSubmitting"
            >
              {{ isSubmitting ? "Creating..." : "Create Trek" }}
            </button>
            <button
              type="button"
              @click="cancel"
              class="btn btn-outline-secondary text-xs px-4 py-2"
            >
              Cancel
            </button>
          </div>
        </form>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import Sidebar from "@/components/dashboard/Sidebar.vue";
import { useTrekStore } from "@/store";

const store = useTrekStore();
const router = useRouter();

const form = ref({
  name: "",
  location: "",
  difficulty: "Easy",
  startDate: "",
  endDate: "",
  availableSlot: "",
  staffId: "",
  route: "",
  majorStops: [],
  trekTags: [],
  price: "",
  description: "",
  status: "Open",
  image: "",
});

const majorStopDraft = ref("");

const trekTagOptions = [
  "Full Coverage Food",
  "Living Area",
  "Guide Included",
  "First Aid",
  "Permit Support",
  "Transport Included",
  "Camping Gear",
  "All Meals",
];

const errorMessage = ref("");
const successMessage = ref("");
const isSubmitting = ref(false);

const activeStaff = computed(() =>
  store.staff.filter((member) => member.is_active),
);

const trekDuration = computed(() => {
  if (!form.value.startDate || !form.value.endDate) {
    return "";
  }

  const start = new Date(form.value.startDate);
  const end = new Date(form.value.endDate);
  if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime())) {
    return "";
  }

  const diffInDays = Math.ceil((end - start) / (1000 * 60 * 60 * 24)) + 1;
  return diffInDays > 0 ? diffInDays : "";
});

onMounted(async () => {
  if (store.staff.length === 0) {
    await store.fetchStaff();
  }
  if (activeStaff.value.length > 0 && !form.value.staffId) {
    form.value.staffId = activeStaff.value[0].id;
  }
});

const fileInput = ref(null);

const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    form.value.image = e.target.result;
  };
  reader.readAsDataURL(file);
};

const clearImage = () => {
  form.value.image = "";
  if (fileInput.value) {
    fileInput.value.value = "";
  }
};

const addMajorStop = () => {
  const value = majorStopDraft.value.trim();
  if (!value) {
    return;
  }

  if (!form.value.majorStops.includes(value)) {
    form.value.majorStops.push(value);
  }
  majorStopDraft.value = "";
};

const removeMajorStop = (index) => {
  form.value.majorStops.splice(index, 1);
};

const toggleTag = (tag) => {
  if (form.value.trekTags.includes(tag)) {
    form.value.trekTags = form.value.trekTags.filter((item) => item !== tag);
    return;
  }
  form.value.trekTags = [...form.value.trekTags, tag];
};

const submitForm = async () => {
  errorMessage.value = "";
  successMessage.value = "";

  if (!form.value.staffId) {
    errorMessage.value = "Please select an active trekking staff member.";
    return;
  }

  if (!trekDuration.value) {
    errorMessage.value = "Please select a valid start and end date.";
    return;
  }

  isSubmitting.value = true;
  const result = await store.addTrek({
    name: form.value.name,
    location: form.value.location,
    difficulty: form.value.difficulty,
    duration: Number(trekDuration.value),
    start_date: form.value.startDate,
    end_date: form.value.endDate,
    available_slot: Number(form.value.availableSlot),
    staff_id: Number(form.value.staffId),
    route: form.value.route,
    major_stops: form.value.majorStops,
    trek_tags: form.value.trekTags,
    price: Number(form.value.price),
    description: form.value.description,
    status: "open",
    image: form.value.image || null,
  });
  isSubmitting.value = false;

  if (result?.success === false) {
    errorMessage.value = result.message;
    return;
  }

  successMessage.value =
    "Trek created successfully! Redirecting to manage treks...";
  setTimeout(() => {
    router.push("/AdminManageTreks");
  }, 1200);
};

const cancel = () => {
  router.push("/AdminManageTreks");
};
</script>

<style scoped>
.text-xs {
  font-size: 0.8rem;
}

.max-w-form {
  max-width: 820px;
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

.chip-item {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.45rem 0.7rem;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #fff;
  font-size: 0.75rem;
  background: rgba(255, 255, 255, 0.04);
}

.chip-item button {
  border: none;
  background: transparent;
  color: inherit;
  padding: 0;
  line-height: 1;
}

.inclusion-chip {
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.03);
  color: #d1d5db;
}

.inclusion-chip.active {
  background: rgba(16, 185, 129, 0.15);
  color: #ffffff;
  border-color: rgba(16, 185, 129, 0.45);
}
</style>
