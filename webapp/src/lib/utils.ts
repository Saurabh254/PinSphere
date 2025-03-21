import axios from "@/api_client";
import { API_URL } from "@/constants";
import { toast } from "react-toastify";


export const toggleUploadContentModel = async () => {
  try {
    const response = await axios.get(`${API_URL}/users/me`);
    if (response.status === 200) {
      const modal = document.getElementById("my_upload_model");
      if (modal) {
        (modal as HTMLDialogElement).showModal();
      }
    }
  } catch (error) {
    toast.error("Please login to create content");
    console.error(error);
  }
};
