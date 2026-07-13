<template>
  <div class="dashboard-layout">
    <!-- Sidebar Component -->
    <Sidebar />

    <!-- Main Content Area -->
    <main class="dashboard-main fade-in">
      <header
        class="dashboard-header border-bottom border-secondary-subtle pb-3 mb-4"
      >
        <div>
          <h1 class="h3 fw-bold mb-1 font-display text-white">Treks</h1>
          <p class="text-muted text-xs mb-0">Manage and create hiking routes</p>
        </div>
        <div>
          <router-link
            to="/CreateTrek"
            class="btn btn-green d-flex align-items-center gap-2 text-xs py-2 px-3"
          >
            <i class="bi bi-plus-lg"></i>
            <span>Create Trek</span>
          </router-link>
        </div>
      </header>

      <!-- Search & Filters -->
      <section class="glass-panel p-3 mb-4">
        <div class="row g-2 align-items-center">
          <div class="col-md-6 col-lg-8">
            <div class="input-group">
              <span
                class="input-group-text bg-transparent border-secondary border-end-0 text-white-50"
                ><i class="bi bi-search"></i
              ></span>
              <input
                type="text"
                v-model="searchQuery"
                class="form-control bg-transparent border-secondary border-start-0 text-white text-xs"
                placeholder="Search treks by name, location..."
              />
            </div>
          </div>
          <div class="col-md-3 col-lg-2">
            <select
              v-model="filterDifficulty"
              class="form-select bg-transparent border-secondary text-white text-xs"
            >
              <option value="" class="bg-dark">All Difficulties</option>
              <option value="Easy" class="bg-dark">Easy</option>
              <option value="Moderate" class="bg-dark">Moderate</option>
              <option value="Hard" class="bg-dark">Hard</option>
            </select>
          </div>
          <div class="col-md-3 col-lg-2">
            <select
              v-model="filterStatus"
              class="form-select bg-transparent border-secondary text-white text-xs"
            >
              <option value="" class="bg-dark">All Statuses</option>
              <option value="Open" class="bg-dark">Open</option>
              <option value="Completed" class="bg-dark">Completed</option>
            </select>
          </div>
        </div>
      </section>

      <!-- Treks List Table -->
      <section class="glass-panel p-4 mb-4">
        <div class="table-responsive">
          <table class="table custom-table mb-0">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Trek Name</th>
                <th scope="col">Location</th>
                <th scope="col">Route</th>
                <th scope="col">Difficulty</th>
                <th scope="col">Available Slots</th>
                <th scope="col">Status</th>
                <th scope="col" class="text-end">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(trek, index) in filteredTreks" :key="trek.id">
                <td class="text-white-50 text-xs">{{ index + 1 }}</td>
                <td>
                  <div class="fw-semibold text-white">{{ trek.name }}</div>
                  <div class="text-muted text-xs d-flex gap-2 mt-0.5">
                    <span
                      ><i class="bi bi-clock me-1"></i
                      >{{ trek.duration }} days</span
                    >
                    <span>•</span>
                    <span
                      ><i class="bi bi-geo me-1"></i
                      >{{ trek.route || "No route added" }}</span
                    >
                  </div>
                </td>
                <td>
                  <i class="bi bi-geo-alt-fill text-green me-1"></i
                  >{{ trek.location }}
                </td>
                <td class="text-white-50 text-xs">
                  {{ trek.route || "N/A" }}
                </td>
                <td>
                  <span
                    class="badge"
                    :class="difficultyBadgeClass(trek.difficulty)"
                  >
                    {{ trek.difficulty }}
                  </span>
                </td>
                <td>
                  <span class="fw-bold text-white">{{
                    trek.available_slot
                  }}</span>
                </td>
                <td>
                  <span class="badge" :class="statusBadgeClass(trek.status)">
                    {{ trek.status }}
                  </span>
                </td>
                <td class="text-end">
                  <div class="d-flex justify-content-end gap-1">
                    <button
                      @click="openEditModal(trek)"
                      class="btn btn-sm btn-outline-light border-0 text-white-50 hover-green-btn p-1.5"
                      title="Manage Route / Edit Trek"
                    >
                      <i class="bi bi-pencil-square"></i>
                    </button>
                    <button
                      @click="deleteTrek(trek.id)"
                      class="btn btn-sm btn-outline-light border-0 text-white-50 hover-danger-btn p-1.5"
                      title="Delete Trek"
                    >
                      <i class="bi bi-trash-fill"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredTreks.length === 0">
                <td colspan="8" class="text-center text-white py-4">
                  No treks found.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Glassmorphic Modal for Add / Edit Trek -->
      <div
        v-if="showModal"
        class="glass-modal-backdrop d-flex align-items-center justify-content-center p-3"
      >
        <div class="glass-modal-container glass-panel p-4 p-md-5 w-100 fade-in">
          <div
            class="d-flex justify-content-between align-items-center border-bottom border-secondary-subtle pb-3 mb-4"
          >
            <h3 class="h5 fw-bold mb-0 text-white font-display">
              {{ isEditing ? "Edit Trek Details" : "Create New Trek" }}
            </h3>
            <button
              @click="closeModal"
              class="btn-close btn-close-white"
            ></button>
          </div>

          <form @submit.prevent="submitForm">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label text-white-50 text-xs"
                  >Trek Name</label
                >
                <input
                  type="text"
                  v-model="form.name"
                  class="form-control glass-input text-xs"
                  required
                  placeholder="e.g. Everest Base Camp"
                />
              </div>
              <div class="col-md-6">
                <label class="form-label text-white-50 text-xs">Location</label>
                <input
                  type="text"
                  v-model="form.location"
                  class="form-control glass-input text-xs"
                  required
                  placeholder="e.g. Nepal / Uttarakhand"
                />
              </div>
              <div class="col-md-4">
                <label class="form-label text-white-50 text-xs"
                  >Difficulty</label
                >
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
              <div class="col-md-4">
                <label class="form-label text-white-50 text-xs">Duration</label>
                <input
                  :value="trekDuration || 'Auto from dates'"
                  type="text"
                  class="form-control glass-input text-xs"
                  readonly
                />
                <small class="text-white-50 d-block mt-1 text-xs"
                  >Auto-calculated from start and end date.</small
                >
              </div>
              <div class="col-md-6">
                <label class="form-label text-white-50 text-xs"
                  >Start Date</label
                >
                <input
                  type="date"
                  v-model="form.startDate"
                  class="form-control glass-input text-xs"
                  required
                />
              </div>
              <div class="col-md-6">
                <label class="form-label text-white-50 text-xs">End Date</label>
                <input
                  type="date"
                  v-model="form.endDate"
                  class="form-control glass-input text-xs"
                  required
                />
              </div>
              <div class="col-md-6">
                <label class="form-label text-white-50 text-xs"
                  >Available Slots</label
                >
                <input
                  type="number"
                  v-model="form.availableSlot"
                  class="form-control glass-input text-xs"
                  required
                  placeholder="e.g. 15"
                  min="1"
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
                  placeholder="Describe the route, checkpoints, and itinerary..."
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
                    placeholder="Add stops like Namche Bazaar or Gorakshep"
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
                  type="number"
                  v-model="form.price"
                  class="form-control glass-input text-xs"
                  required
                  placeholder="e.g. 18999"
                  min="0"
                  step="1"
                />
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
                  placeholder="Provide a brief description of the trekking trail..."
                ></textarea>
              </div>
              <div class="col-md-4" v-if="isEditing">
                <label class="form-label text-white-50 text-xs">Status</label>
                <select
                  v-model="form.status"
                  class="form-select glass-input text-xs"
                >
                  <option value="Open">Open</option>
                  <option value="Completed">Completed</option>
                </select>
              </div>
            </div>

            <div
              class="d-flex justify-content-end gap-3 mt-4 pt-3 border-top border-secondary-subtle"
            >
              <button
                type="button"
                @click="closeModal"
                class="btn btn-outline-secondary text-xs px-4"
              >
                Cancel
              </button>
              <button type="submit" class="btn btn-green text-xs px-4">
                {{ isEditing ? "Save Changes" : "Create Trek" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import Sidebar from "@/components/dashboard/Sidebar.vue";
import { useTrekStore } from "@/store";

const store = useTrekStore();

const searchQuery = ref("");
const filterDifficulty = ref("");
const filterStatus = ref("");

const showModal = ref(false);
const isEditing = ref(false);
const editTrekId = ref(null);

const form = ref({
  name: "",
  location: "",
  difficulty: "Easy",
  startDate: "",
  endDate: "",
  availableSlot: 15,
  staffId: "",
  route: "",
  majorStops: [],
  trekTags: [],
  price: "",
  description: "",
  status: "Open",
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

const activeStaff = computed(() => {
  return store.staff.filter((s) => s.is_active);
});

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

const filteredTreks = computed(() => {
  return store.treks.filter((t) => {
    const matchesSearch =
      t.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      t.location.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesDifficulty =
      filterDifficulty.value === "" || t.difficulty === filterDifficulty.value;
    const matchesStatus =
      filterStatus.value === "" || t.status === filterStatus.value;
    return matchesSearch && matchesDifficulty && matchesStatus;
  });
});

onMounted(async () => {
  if (store.treks.length === 0) {
    await store.fetchAdminTreks();
  }
  if (store.staff.length === 0) {
    await store.fetchStaff();
  }
});

const difficultyBadgeClass = (diff) => {
  if (diff === "Easy")
    return "bg-success bg-opacity-10 text-success border border-success-subtle";
  if (diff === "Moderate")
    return "bg-warning bg-opacity-10 text-warning border border-warning-subtle";
  return "bg-danger bg-opacity-10 text-danger border border-danger-subtle";
};

const statusBadgeClass = (status) => {
  if (status === "Open")
    return "bg-success bg-opacity-10 text-success border border-success-subtle";
  return "bg-info bg-opacity-10 text-info border border-info-subtle";
};

const openAddModal = () => {
  isEditing.value = false;
  editTrekId.value = null;
  form.value = {
    name: "",
    location: "",
    difficulty: "Easy",
    startDate: "",
    endDate: "",
    availableSlot: 15,
    staffId: activeStaff.value[0]?.id || "",
    route: "",
    majorStops: [],
    trekTags: [],
    price: "",
    description: "",
    status: "Open",
  };
  showModal.value = true;
};

const openEditModal = (trek) => {
  isEditing.value = true;
  editTrekId.value = trek.id;
  form.value = {
    name: trek.name || "",
    location: trek.location || "",
    difficulty: trek.difficulty || "Easy",
    startDate: trek.start_date || "",
    endDate: trek.end_date || "",
    availableSlot: trek.available_slot || 0,
    staffId: trek.staff_id || "",
    route: trek.route || "",
    majorStops: Array.isArray(trek.major_stops) ? trek.major_stops : [],
    trekTags: Array.isArray(trek.trek_tags) ? trek.trek_tags : [],
    price: trek.price ?? "",
    description: trek.description || "",
    status: trek.status === "Completed" ? "Completed" : "Open",
  };
  showModal.value = true;
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

const closeModal = () => {
  showModal.value = false;
};

const submitForm = async () => {
  if (!trekDuration.value) {
    return;
  }

  if (isEditing.value) {
    await store.editTrek(editTrekId.value, {
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
      status: form.value.status,
    });
  } else {
    await store.addTrek({
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
      status: form.value.status,
    });
  }
  showModal.value = false;
};

const deleteTrek = (trekId) => {
  if (
    confirm(
      "Are you sure you want to delete this trek? This will automatically cancel related bookings.",
    )
  ) {
    store.deleteTrek(trekId);
  }
};
</script>

<style scoped>
.text-xs {
  font-size: 0.8rem;
}

.badge {
  font-size: 0.75rem;
  padding: 0.35em 0.6em;
  border-radius: 6px;
  font-weight: 500;
}

.hover-green-btn:hover {
  color: #10b981 !important;
  background: rgba(16, 185, 129, 0.08) !important;
}

.hover-danger-btn:hover {
  color: #ef4444 !important;
  background: rgba(239, 68, 68, 0.08) !important;
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
  max-width: 650px;
  background: rgba(13, 27, 42, 0.95);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
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
