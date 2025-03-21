import api_client from "@/api_client";
import { API_URL } from "@/constants";

export interface PostCommentType {
  content_id: string;
  text: string;
}
export const post_comments = async (postData: PostCommentType) => {
  try {
    const resp = await api_client.post(API_URL + "/comments", postData);
    return resp.data;
  } catch (err) {
    console.log(err);
  }
};
