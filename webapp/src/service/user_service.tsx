import { Page, SlimContent } from "@/types";
import api_client from "../api_client";
import { API_URL } from "../constants";

export const checkUserNameAvailablity = async (userName: string) => {
  const response = await api_client.get(
    `${API_URL}/users/check-username/${userName}`
  );
  return response.data;
};

export interface FormDataRequestBody {
  image_key?: string;
  email?: string;
  username?: string;
  name?: string;
  bio?: string;
}
export const update_user_profile = async (data: FormDataRequestBody) => {
  const response = await api_client.put(`${API_URL}/users`, data);
  return response.data;
};

export const getLoggedInUser = async () => {
  const response = await api_client.get(`${API_URL}/users/me`);
  return response.data;
};
export const getUserContents = async (): Promise<Page<SlimContent>> => {
  const response = await api_client.get(`${API_URL}/content/me`);
  return response.data;
};
