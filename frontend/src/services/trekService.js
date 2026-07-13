import api from "./api";

export default {
  getAllTreks() {
    return api.get("/treks/");
  },
  getAvailableTreks() {
    return api.get("/user/available-treks");
  },
  getAdminTreks() {
    return api.get("/treks/admin");
  },
  getTrekById(id) {
    return api.get(`/treks/${id}`);
  },
  createTrek(data) {
    return api.post("/treks/", data);
  },
  updateTrek(id, data) {
    return api.put(`/treks/${id}`, data);
  },
  updateAssignedTrek(id, data) {
    return api.patch(`/treks/${id}/staff`, data);
  },
  deleteTrek(id) {
    return api.delete(`/treks/${id}`);
  },
  completeTrek(id) {
    return api.put(`/treks/${id}/complete`);
  },
  getParticipants(trekId) {
    return api.get(`/treks/${trekId}/participants`);
  },
  updateParticipantStatus(bookingId, status) {
    return api.put(`/treks/participants/${bookingId}`, { status });
  },
};
