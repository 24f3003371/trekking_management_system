import api from "./api";

export default {
  getDashboard() {
    return api.get("/admin/dashboard");
  },
  createStaff(data) {
    return api.post("/admin/staff", data);
  },
  getAllStaff() {
    return api.get("/admin/staff");
  },
  searchStaff(keyword) {
    return api.get("/admin/staff/search", { params: { keyword } });
  },
  searchUsers(keyword) {
    return api.get("/admin/users/search", { params: { keyword } });
  },
  searchTreks(keyword) {
    return api.get("/admin/treks/search", { params: { keyword } });
  },
  assignTrek(staffId, trekId) {
    return api.post("/admin/assign-trek", {
      staff_id: staffId,
      trek_id: trekId,
    });
  },
  removeStaffFromTrek(trekId, staffId) {
    return api.delete("/admin/remove-trek", {
      data: { trek_id: trekId, staff_id: staffId },
    });
  },
  blacklist(userId) {
    return api.put(`/admin/blacklist/${userId}`);
  },
  unblacklist(userId) {
    return api.put(`/admin/unblacklist/${userId}`);
  },
};
