import { useState } from "react";
import FileUploadPreview from "./FileUploadPreview";
import api_client from "../api_client";
import { upload_file } from "../utils";
import { API_URL } from "../constants";

const toggleUploadContentModel = () => {
  const modal = document.getElementById("my_upload_model");
  if (modal) {
    (modal as HTMLDialogElement).close();
  }
};

const CreatePostModal = () => {
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

  const handleUpload = async () => {
    if (!file || !fileExt)
      return showToast("info", "Please select a file before uploading.");
    setLoading(true);
    try {
      const { data } = await api_client.get(
        `${API_URL}/content/upload_url?ext=${encodeURIComponent(fileExt)}`
      );
      const uploadResponse = await upload_file(data, file);
      const postResponse =
        uploadResponse.status === 204
          ? await api_client.post(
              `${API_URL}/content?content_key=${data.fields.key}`
            )
          : null;
      showToast(
        postResponse?.status === 201 ? "success" : "error",
        postResponse?.status === 201
          ? "Image uploaded successfully"
          : "Failed to create post"
      );
    } catch (error) {
      console.error("Error during upload:", error);
      showToast("error", "An error occurred during upload");
    } finally {
      setLoading(false);
    }
  };
  const handleCancel = async () => {
    setFile(null);
    setFileExt(null);
    setLoading(false);
    toggleUploadContentModel();
  };

  return (
    <>
      <dialog id="my_upload_model" className="modal">
        {toast && (
          <div className="toast toast-end fixed z-50">
            <div className={`alert alert-${toast.type}`}>
              <span>{toast.message}</span>
            </div>
          </div>
        )}
        <div className="modal-box max-h-[80vh] flex flex-col">
          <FileUploadPreview
            file={file}
            fileExt={fileExt}
            setFile={setFile}
            setFileExt={setFileExt}
          />
          <div className="flex justify-between gap-4">
            <button className="btn ml-auto" onClick={handleCancel}>
              Cancel
            </button>
            <button className="btn" onClick={handleUpload} disabled={loading}>
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

export default CreatePostModal;
