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
            Manage Trekkers
          </h1>
          <p class="text text-xs mb-0">
            Manage registered trekkers and their access
          </p>
        </div>
        <div class="d-flex align-items-center gap-2">
          <span
            class="badge bg-green bg-opacity-10 text-white border border-success-subtle text-xs py-2 px-3"
          >
            Active Trekkers: {{ activeUsersCount }}
          </span>
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
            placeholder="Search users by name, email, contact, ID..."
          />
        </div>
      </section>

      <!-- Users List Table -->
      <section class="glass-panel p-4 mb-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h3 class="h5 fw-bold mb-0 text-white font-display">
            Users (Trekkers) List
          </h3>
          <span class="badge bg-secondary text-xs"
            >Total Users: {{ filteredUsers.length }}</span
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
                <th scope="col">Status</th>
                <th scope="col" class="text-end">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id">
                <td class="fw-semibold text-green font-display">
                  {{ user.id }}
                </td>
                <td class="fw-semibold text-white">{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.phone || "N/A" }}</td>
                <td>
                  <span
                    class="badge"
                    :class="
                      user.is_active
                        ? 'bg-success bg-opacity-10 text-success border border-success-subtle'
                        : 'bg-danger bg-opacity-10 text-danger border border-danger-subtle'
                    "
                  >
                    {{ user.is_active ? "Active" : "Blocked" }}
                  </span>
                </td>
                <td class="text-end">
                  <button
                    v-if="user.is_active"
                    @click="blacklistUser(user.id)"
                    class="btn btn-sm btn-outline-danger px-3 py-1 text-xs font-display"
                  >
                    Blacklist
                  </button>
                  <button
                    v-else
                    @click="whitelistUser(user.id)"
                    class="btn btn-sm btn-outline-success px-3 py-1 text-xs font-display"
                  >
                    Whitelist
                  </button>
                </td>
              </tr>
              <tr v-if="filteredUsers.length === 0">
                <td colspan="6" class="text-center text-muted py-4">
                  No users found.
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
            Blacklisted users cannot log in, browse treks, or book new treks in
            the system.
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
  await store.fetchUsers();
});

const filteredUsers = computed(() => {
  return store.users.filter((u) => {
    const query = searchQuery.value.toLowerCase();
    return (
      (u.username || "").toLowerCase().includes(query) ||
      (u.email || "").toLowerCase().includes(query) ||
      String(u.phone || "")
        .toLowerCase()
        .includes(query) ||
      String(u.id || "")
        .toLowerCase()
        .includes(query)
    );
  });
});

const activeUsersCount = computed(() => {
  return store.users.filter((u) => u.is_active).length;
});

const blacklistUser = (id) => {
  if (
    confirm(
      "Are you sure you want to blacklist this trekker? They will be signed out and unable to log back in.",
    )
  ) {
    store.blacklistUser(id);
  }
};

const whitelistUser = (id) => {
  store.whitelistUser(id);
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
