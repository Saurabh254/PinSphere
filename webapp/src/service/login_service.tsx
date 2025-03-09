import api_client from "../api_client";
import { API_URL } from "../constants";
import { getTokenFromStorage } from "./token_service";

export function isUserLoggedIn() {
  return getTokenFromStorage() !== null;
}

export const get_user_profile = async () => {
  return await api_client.get(`${API_URL}/users/me`);
};
