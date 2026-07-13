import { defineStore } from "pinia";
import authService from "@/services/authService";
import trekService from "@/services/trekService";
import bookingService from "@/services/bookingService";
import adminService from "@/services/adminService";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: localStorage.getItem("token") || null,
  }),
  actions: {
    setUser(user) {
      this.user = user;
    },
    setToken(token) {
      this.token = token;
      localStorage.setItem("token", token);
    },
    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem("token");
    },
  },
});

export const useTrekStore = defineStore("trek", {
  state: () => ({
    token: localStorage.getItem("token") || null,
    currentUser: JSON.parse(localStorage.getItem("user") || "null"),
    users: [],
    treks: [],
    bookings: [],
    participantsByTrek: {},
    staff: [],
    totalTreks: 0,
    totalUsers: 0,
    totalStaff: 0,
    totalBookings: 0,
  }),

  getters: {
    recentBookings: (state) => [...state.bookings].slice(-5).reverse(),
    // Set of trek IDs the current user has an active (Booked) booking for
    bookedTrekIds: (state) => {
      if (!state.currentUser) return new Set();
      return new Set(
        state.bookings
          .filter(b => (b.status === 'Booked' || b.booking_status === 'booked'))
          .map(b => b.trek_id)
      );
    },
  },

  actions: {
    async login(email, password) {
      try {
        const { data } = await authService.login(email, password);
        this.token = data.access_token;
        this.currentUser = data.user;
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("user", JSON.stringify(data.user));
        return { success: true, user: data.user };
      } catch (err) {
        return {
          success: false,
          message: err.response?.data?.message || "Login failed",
        };
      }
    },

    async register(name, email, password, contact) {
      try {
        await authService.register({
          username: name,
          email,
          password,
          contact,
        });
        return { success: true };
      } catch (err) {
        return {
          success: false,
          message: err.response?.data?.message || "Registration failed",
        };
      }
    },

    logout() {
      this.currentUser = null;
      this.token = null;
      localStorage.removeItem("token");
      localStorage.removeItem("user");
    },

    async fetchTreks() {
      const { data } = await trekService.getAvailableTreks();
      this.treks = data.map((t) => ({
        ...t,
        status: capitalize(t.status),
        difficulty: capitalize(t.difficulty),
        assignedStaffId: t.staff_id,
        startDate: t.start_date,
        endDate: t.end_date,
        progress: t.progress ?? 0,
        availableSlots: t.available_slot,
        slots: t.available_slot,
        checkpoints: (t.major_stops || []).map((stop, idx) => ({
          name: stop,
          elevation: `${idx * 400 + 3400}m`,
        })),
      }));
    },

    async fetchAdminTreks() {
      const { data } = await trekService.getAdminTreks();
      this.treks = data.map((t) => ({
        ...t,
        status: capitalize(t.status),
        difficulty: capitalize(t.difficulty),
        assignedStaffId: t.staff_id,
        startDate: t.start_date,
        endDate: t.end_date,
        progress: t.progress ?? 0,
        availableSlots: t.available_slot,
        slots: t.available_slot,
        checkpoints: (t.major_stops || []).map((stop, idx) => ({
          name: stop,
          elevation: `${idx * 400 + 3400}m`,
        })),
      }));
    },

    async addTrek(data) {
      try {
        await trekService.createTrek(data);
        await this.fetchAdminTreks();
        return { success: true };
      } catch (err) {
        return {
          success: false,
          message: err.response?.data?.message || "Could not create trek",
        };
      }
    },
    async editTrek(id, data) {
      await trekService.updateTrek(id, data);
      await this.fetchAdminTreks();
    },
    async deleteTrek(id) {
      await trekService.deleteTrek(id);
      await this.fetchAdminTreks();
    },
    async completeTrek(id) {
      await trekService.completeTrek(id);
      await this.fetchAdminTreks();
    },

    async bookTrek(trekId) {
      try {
        await bookingService.bookTrek(trekId);
        await this.fetchBookingHistory();
        return { success: true };
      } catch (err) {
        return {
          success: false,
          message: err.response?.data?.message || "Booking failed",
        };
      }
    },

    async cancelBooking(bookingId) {
      try {
        const { data } = await bookingService.cancelBooking(bookingId);
        const cancelledBooking = data.booking;

        // Reflect success immediately. Refresh afterwards to keep all enriched
        // booking details in sync without making a successful cancellation look
        // like a failure if that follow-up request has a temporary issue.
        if (cancelledBooking) {
          this.bookings = this.bookings.map((booking) =>
            booking.id === bookingId
              ? {
                  ...booking,
                  ...cancelledBooking,
                  userId: cancelledBooking.user_id,
                  status: 'Cancelled',
                }
              : booking,
          );
        }
        try {
          await this.fetchBookingHistory();
        } catch (refreshError) {
          console.warn('Booking was cancelled, but the booking list could not be refreshed.', refreshError);
        }
        return { success: true };
      } catch (err) {
        const msg = err.response?.data?.message || err.message || 'Cancellation failed';
        return { success: false, message: msg };
      }
    },

    async fetchBookingHistory() {
      const { data } = await bookingService.getBookingHistory();
      this.bookings = data.map(normalizeBooking);
    },

    async fetchParticipants(trekId) {
      const { data } = await trekService.getParticipants(trekId);
      this.participantsByTrek = {
        ...this.participantsByTrek,
        [trekId]: data.map(normalizeBooking),
      };
    },

    async updateAssignedTrek(trekId, data) {
      const { data: response } = await trekService.updateAssignedTrek(trekId, data);
      await this.fetchAdminTreks();
      return response;
    },

    async createStaff(payload) {
      try {
        await adminService.createStaff(payload);
        await this.fetchStaff();
        return { success: true };
      } catch (err) {
        return {
          success: false,
          message: err.response?.data?.message || "Could not create staff",
        };
      }
    },

    async fetchStaff() {
      const { data } = await adminService.getAllStaff();
      this.staff = data;
    },

    async fetchUsers() {
      const { data } = await adminService.searchUsers("");
      this.users = data;
    },

    async blacklistStaff(id) {
      await adminService.blacklist(id);
      await this.fetchStaff();
    },
    async whitelistStaff(id) {
      await adminService.unblacklist(id);
      await this.fetchStaff();
    },
    async blacklistUser(id) {
      await adminService.blacklist(id);
      await this.fetchUsers();
    },
    async whitelistUser(id) {
      await adminService.unblacklist(id);
      await this.fetchUsers();
    },

    async fetchDashboard() {
      const { data } = await adminService.getDashboard();
      this.totalTreks = data.total_treks;
      this.totalUsers = data.total_users;
      this.totalStaff = data.total_staff;
      this.totalBookings = data.total_bookings;
    },

    updateTrekProgress() {
      // not supported by the backend yet — Trek has no "progress" column/route.
      console.warn("updateTrekProgress: no backend support yet, no-op");
    },

    saveState() {
      // no-op now — persistence lives in the backend DB, not localStorage
    },
  },
});

function capitalize(str) {
  if (!str) return str;
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function normalizeBooking(booking) {
  return {
    ...booking,
    userId: booking.user_id,
    trekId: booking.trek_id,
    userName: booking.user_name || booking.username || 'Trekker',
    status: booking.booking_status
      ? capitalize(booking.booking_status)
      : booking.status || 'Unknown',
    trekName: booking.trek_name || `Trek #${booking.trek_id}`,
    trekDates: (booking.trek_start_date && booking.trek_end_date)
      ? `${booking.trek_start_date} → ${booking.trek_end_date}`
      : '—',
    bookingDate: booking.booking_date ? booking.booking_date.slice(0, 10) : '—',
  };
}
