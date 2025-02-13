import { useState } from "react";
import ImagePreview from "./ImagePreview";

interface FileUploadPreviewProps {
  file: File | null;
  setFile: (file: File | null) => void;
  fileExt: string | null;
  setFileExt: (fileExt: string | null) => void;
}

export default function FileUploadPreview({
  file,
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
      {preview && file && <ImagePreview preview={preview} />}
    </div>
  );
}
