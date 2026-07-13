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
          <h1 class="h3 fw-bold mb-1 font-display text-white">
            Trekking Staff
          </h1>
          <p class="text-muted text-xs mb-0">
            Manage registered guides, leaders, and support crew
          </p>
        </div>
        <div>
          <router-link
            to="/CreateStaff"
            class="btn btn-green d-flex align-items-center gap-2 text-xs py-2 px-3"
          >
            <i class="bi bi-person-plus-fill"></i>
            <span>Add New Staff</span>
          </router-link>
        </div>
      </header>

      <!-- Search Box -->
      <section class="glass-panel p-3 mb-4">
        <div class="input-group">
          <span
            class="input-group-text bg-transparent border-secondary border-end-0 text-white-50"
            ><i class="bi bi-search"></i
          ></span>
          <input
            type="text"
            v-model="searchQuery"
            class="form-control bg-transparent border-secondary border-start-0 text-white text-xs"
            placeholder="Search staff by name, email, or phone..."
          />
        </div>
      </section>

      <!-- Trekking Staff List Table -->
      <section class="glass-panel p-4 mb-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h3 class="h5 fw-bold mb-0 text-white font-display">
            Trekking Staff List
          </h3>
          <span class="badge bg-secondary text-xs"
            >Total Staff: {{ filteredStaff.length }}</span
          >
        </div>

        <div class="table-responsive">
          <table class="table custom-table mb-0">
            <thead>
              <tr>
                <th scope="col">ID</th>
                <th scope="col">Name</th>
                <th scope="col">Email</th>
                <th scope="col">Contact</th>
                <th scope="col">Experience</th>
                <th scope="col">Status</th>
                <th scope="col" class="text-end">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="member in filteredStaff" :key="member.id">
                <td class="fw-semibold text-green font-display">
                  {{ member.id }}
                </td>
                <td>
                  <div class="fw-semibold text-white">
                    {{ member.username }}
                  </div>
                  <div class="text-muted text-xs mt-0.5">
                    <i class="bi bi-star-fill text-warning me-1"></i>
                    Staff member
                  </div>
                </td>
                <td>{{ member.email }}</td>
                <td>{{ member.phone || "N/A" }}</td>
                <td>N/A</td>
                <td>
                  <span
                    class="badge"
                    :class="
                      member.is_active
                        ? 'bg-success bg-opacity-10 text-success border border-success-subtle'
                        : 'bg-danger bg-opacity-10 text-danger border border-danger-subtle'
                    "
                  >
                    {{ member.is_active ? "Active" : "Blocked" }}
                  </span>
                </td>
                <td class="text-end">
                  <button
                    v-if="member.is_active"
                    @click="blacklistStaff(member.id)"
                    class="btn btn-sm btn-outline-danger px-3 py-1 text-xs font-display"
                  >
                    Blacklist
                  </button>
                  <button
                    v-else
                    @click="whitelistStaff(member.id)"
                    class="btn btn-sm btn-outline-success px-3 py-1 text-xs font-display"
                  >
                    Whitelist
                  </button>
                </td>
              </tr>
              <tr v-if="filteredStaff.length === 0">
                <td colspan="7" class="text-center text-white py-4">
                  No trekking staff members found.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div
          class="note-footer d-flex gap-2 text-white-50 mt-4 pt-3 border-top border-secondary-subtle"
          style="font-size: 0.78rem; line-height: 1.4"
        >
          <i class="bi bi-info-circle-fill text-green flex-shrink-0 mt-0.5"></i>
          <div>
            Blacklisted staff members cannot log in, manage treks, or access
            their staff dashboards.
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import Sidebar from "@/components/dashboard/Sidebar.vue";
import { useTrekStore } from "@/store";

const store = useTrekStore();
const searchQuery = ref("");

onMounted(async () => {
  if (store.staff.length === 0) {
    await store.fetchStaff();
  }
});

const filteredStaff = computed(() => {
  return store.staff.filter((s) => {
    const query = searchQuery.value.toLowerCase();
    return (
      (s.username || "").toLowerCase().includes(query) ||
      (s.email || "").toLowerCase().includes(query) ||
      String(s.id || "")
        .toLowerCase()
        .includes(query) ||
      (s.phone || "").toLowerCase().includes(query)
    );
  });
});

const blacklistStaff = (id) => {
  if (
    confirm(
      "Are you sure you want to blacklist this staff member? They will be signed out and unable to access the dashboard.",
    )
  ) {
    store.blacklistStaff(id);
  }
};

const whitelistStaff = (id) => {
  store.whitelistStaff(id);
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
</style>
