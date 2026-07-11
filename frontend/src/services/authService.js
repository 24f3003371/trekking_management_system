import api from "./api";

export default {
  login(email, password) {
    return api.post("/auth/login", { email, password });
  },
  register({ username, email, password }) {
    return api.post("/auth/register", { username, email, password });
  },
};
