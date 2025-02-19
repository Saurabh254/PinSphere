import { isValidContentType } from "../service/file_upload_utils";
import FileDropZone from "./FileUploadDropZone";
interface FileUploadPreviewProps {
  file: File | null;
  setFile: (file: File | null) => void;
  setToast: React.Dispatch<
    React.SetStateAction<{ type: string; message: string } | null>
  >;
  description: string;
  setDescription: React.Dispatch<React.SetStateAction<string>>;
}

export default function FileUploadPreview({
  file,
  setFile,
  setToast,
  description,
  setDescription,
}: FileUploadPreviewProps) {
  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    const selectedFile = event.target.files?.[0] || null;
    if (selectedFile && isValidContentType(selectedFile.type)) {
      setFile(selectedFile);
    } else if (!selectedFile) {
      setToast({ type: "error", message: "select a file" });
    } else {
      setToast({ type: "error", message: "Invalid file format" });
    }
  };
  return (
    <div className="flex flex-col items-center p-4 rounded-lg w-auto mx-8 max-h-full">
      {!file && <FileDropZone handleFileChange={handleFileChange} />}
      {file && (
        <div className="mt-4 flex-col flex  items-center max-h-[60vh] ">
          <h3>Preview</h3>
          <img
            src={URL.createObjectURL(file)}
            alt="File Preview"
            className="mt-2 max-h-full   object-cover rounded-lg mx-8 bg-red-300"
          />
        </div>
      )}
      {file && (
        <div className="w-full mt-8 space-y-3">
          <textarea
            className="py-3 px-4 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none max-h-48"
            rows={1}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add a description"
          ></textarea>
        </div>
      )}
    </div>
  );
}
