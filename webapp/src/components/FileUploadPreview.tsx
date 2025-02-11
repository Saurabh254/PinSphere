import { useState } from "react";

interface FileUploadPreviewProps {
  file: File | null;
  setFile: (file: File | null) => void;
  fileExt: string | null;
  setFileExt: (fileExt: string | null) => void;
}

export default function FileUploadPreview({
  setFile,
  setFileExt,
}: FileUploadPreviewProps) {
  const [preview, setPreview] = useState<string | null>(null);

  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    setFileExt(null);
    const selectedFile = event.target.files?.[0] || null;
    if (selectedFile) {
      setFile(selectedFile);
      setFileExt(selectedFile.type);
      setPreview(URL.createObjectURL(selectedFile));
    }
  };
  return (
    <div className="flex flex-col items-center p-4 rounded-lg w-auto mx-8">
      <input
        type="file"
        onChange={handleFileChange}
        className="mb-4 file-input "
      />
      {preview && (
        <div className="mt-4 flex-col flex  items-center">
          <h3>Preview</h3>
          <img
            src={preview}
            alt="File Preview"
            className="mt-2 max-h-[80vh] max-w-[80vw] object-cover rounded-lg mx-8 bg-red-300"
          />
        </div>
      )}
    </div>
  );
}
