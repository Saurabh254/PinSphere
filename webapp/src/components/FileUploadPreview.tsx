import FileDropZone from "./FileUploadDropZone";
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
  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    setFileExt(null);
    const selectedFile = event.target.files?.[0] || null;
    if (selectedFile) {
      setFile(selectedFile);
      setFileExt(selectedFile.type);
    }
  };
  console.log(file);
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
    </div>
  );
}
