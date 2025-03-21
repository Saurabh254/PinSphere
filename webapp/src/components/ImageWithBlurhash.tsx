import { useState } from "react";
import { Content } from "../types";
import { Blurhash } from "react-blurhash";
interface ImageWithBlurhashParm {
  image: Content;
  key: string;
}

const ImageWithBlurhash = ({ image }: ImageWithBlurhashParm) => {
  const [loaded, setLoaded] = useState(false);
  let aspectRatio = 480 / 480;
  if (image.metadata) {
    aspectRatio = image.metadata.width / image.metadata.height;
  }

  return (
    <div
      className="relative w-full overflow-hidden break-inside-avoid bg-gray-300"
      style={{ aspectRatio }}
    >
      {/* Blurhash Placeholder */}
      {!loaded && (
        <Blurhash
          hash={image.blurhash}
          width="100%"
          height="100%"
          resolutionX={32}
          resolutionY={32}
          punch={1}
          className="absolute top-0 left-0 w-full h-full"
        />
      )}

      {/* Image */}
      <img
        src={image.url}
        onLoad={() => setLoaded(true)}
        alt="Loaded Content"
        className={`absolute top-0 left-0 w-full h-full rounded-xl object-cover transition-opacity duration-500 ${
          loaded ? "opacity-100" : "opacity-0"
        }`}
      />
    </div>
  );
};

export default ImageWithBlurhash;
