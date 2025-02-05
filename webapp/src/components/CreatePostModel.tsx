import { useState } from "react";
import FileUploadPreview from "./FileUploadPreview";
import { API_URL } from "../constants";
import api_client from "../api_client";
import { upload_file } from "../utils";

const CreatePostModel = () => {
  const [file, setFile] = useState<File | null>(null);
  const [fileExt, setFileExt] = useState<string | null>(null);
  const call_api = async () => {
    if (file) {
      try {
        const res = await api_client.get(
          API_URL + "/images/upload_url?ext=" + fileExt
        );
        const upload_res = await upload_file(res.data, file);
        if (upload_res.status === 204) {
          console.log(res.data);
          const post_res = await api_client.post(
            API_URL + "/images?image_key=" + res.data.fields.key
          );
          if (post_res.status === 201) {
            alert("Image uploaded successfully");
          }
        }
      } catch (err) {
        console.log(err);
      }
    }
  };

  return (
    <>
      <dialog id="my_modal_1" className="modal">
        <div className="modal-box max-w-fit">
          <FileUploadPreview
            file={file}
            fileExt={fileExt}
            setFile={setFile}
            setFileExt={setFileExt}
          />
          <div className="flex w-full items-baseline gap-4">
            <div className="modal-action w-fit ml-auto">
              <form method="dialog">
                <button className="btn">Cancel</button>
              </form>
            </div>
            <button className="btn" onClick={call_api}>
              <span className="loading loading-spinner"></span>
              Upload Image
            </button>
          </div>
        </div>
      </dialog>
    </>
  );
};

export default CreatePostModel;
