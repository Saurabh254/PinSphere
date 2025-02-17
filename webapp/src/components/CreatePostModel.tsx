import { useState } from "react";
import FileUploadPreview from "./FileUploadPreview";
import api_client from "../api_client";
import { upload_file } from "../utils";
import { API_URL } from "../constants";

const CreatePostModel = () => {
  const [file, setFile] = useState<File | null>(null);
  const [fileExt, setFileExt] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ type: string; message: string } | null>(
    null
  );

  const showToast = (type: string, message: string) => {
    setToast({ type, message });
    setTimeout(() => setToast(null), 3000);
  };

  const call_api = async () => {
    if (!file || !fileExt) {
      showToast("info", "Please select a file before uploading.");
      return;
    }
    setLoading(true);
    try {
      const res = await api_client.get(
        `${API_URL}/content/upload_url?ext=${encodeURIComponent(fileExt)}`
      );
      const upload_res = await upload_file(res.data, file);
      if (upload_res.status === 204) {
        const post_res = await api_client.post(
          `${API_URL}/content?content_key=` + res.data.fields.key
        );
        showToast(
          post_res.status === 201 ? "success" : "error",
          post_res.status === 201
            ? "Image uploaded successfully"
            : "Failed to create post"
        );
      } else {
        showToast("error", "Failed to upload image");
      }
    } catch (err) {
      console.error("Error during upload:", err);
      showToast("error", "An error occurred during upload");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {toast && (
        <div className="toast toast-end">
          <div className={`alert alert-${toast.type}`}>
            <span>{toast.message}</span>
          </div>
        </div>
      )}
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
            <button className="btn" onClick={call_api} disabled={loading}>
              {loading ? (
                <span className="loading loading-spinner"></span>
              ) : (
                "Upload Image"
              )}
            </button>
          </div>
        </div>
      </dialog>
    </>
  );
};

export default CreatePostModel;
