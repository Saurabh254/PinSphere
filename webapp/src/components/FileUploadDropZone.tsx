const FileDropzone = ({
  handleFileChange,
}: {
  handleFileChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}) => {
  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileChange({
        target: { files: e.dataTransfer.files },
      } as React.ChangeEvent<HTMLInputElement>);
    }
  };

  return (
    <div
      className="border-dashed border-2 border-primary-foreground rounded-lg p-6 text-center cursor-pointer"
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      <div className="flex flex-col items-center">
        <span className="text-gray-500 mb-2">📂</span>
        <p className="font-semibold">Choose a file or drag & drop it here</p>
        <p className="text-sm text-gray-400">
          JPEG, PNG, GIF, and MP4 formats, up to 50MB
        </p>
        <label className="mt-4 inline-block cursor-pointer px-4 py-2 border rounded-lg text-sm font-medium bg-background text-foreground hover:scale-105 duration-300">
          Browse File
          <input
            type="file"
            onChange={handleFileChange}
            className="hidden"
            accept="images/*, videos/*, audios/*"
          />
        </label>
      </div>
    </div>
  );
};

export default FileDropzone;
