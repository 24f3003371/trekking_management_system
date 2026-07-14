import api from "./api";

export default {
  bookTrek(trekId, paymentStatus = "paid") {
    return api.post(`/user/book/${trekId}`, { payment_status: paymentStatus });
  },
  getBookingHistory() {
    return api.get("/user/booking-history");
  },
  cancelBooking(bookingId) {
    return api.delete(`/user/cancel/${bookingId}`);
  },
  getTrekHistory() {
    return api.get("/user/trek-history");
  },
  editProfile(data) {
    return api.put("/user/profile", data);
  },
  getProfile() {
    return api.get("/user/profile");
  },
  requestExport() {
    return api.post("/user/booking-history/export");
  },
  getExportStatus(taskId) {
    return api.get(`/user/booking-history/export/${taskId}`);
  },
};
