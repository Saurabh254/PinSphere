interface ImagePreviewParams {
  preview: string;
}

const ImagePreview = ({ preview }: ImagePreviewParams) => {
  return (
    <div className="mt-4 flex flex-col items-center max-h-[80vh] h-full w-full overflow-hidden p-0">
      <h3 className="m-0 p-0">Preview</h3>
      <div className="flex justify-center items-center w-full h-full">
        <img
          src={preview}
          alt="File Preview"
          className="max-h-[60vh] max-w-full object-contain rounded-lg bg-red-300"
        />
      </div>
    </div>
  );
};

export default ImagePreview;
