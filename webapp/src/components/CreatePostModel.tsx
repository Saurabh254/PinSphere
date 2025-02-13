import { useState } from "react";
import FileUploadPreview from "./FileUploadPreview";
import { API_URL } from "../constants";
import api_client from "../api_client";
import { upload_file } from "../utils";

const CreatePostModel = () => {
  const [file, setFile] = useState<File | null>(null);
  const [fileExt, setFileExt] = useState<string | null>(null);
  const [description, setDescription] = useState<string>("");
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
  const close_dialog = () => {
    setFile(null);
    setFileExt(null);
    setDescription("");
    document.getElementById("my_modal_1")?.close();
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

          {file ? (
            <div className="w-full flex items-center justify-center">
              <input
                className="input"
                type="text"
                placeholder="write your description here"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>
          ) : (
            ""
          )}
          <div className="flex w-full items-center  mt-8 gap-4">
            <button className="btn ml-auto" onClick={close_dialog}>
              Cancel
            </button>
            <button className="btn " onClick={call_api}>
              <span className="loading loading-spinner "></span>
              Upload Image
            </button>
          </div>
        </div>
      </dialog>
    </>
  );
};

export default CreatePostModel;
