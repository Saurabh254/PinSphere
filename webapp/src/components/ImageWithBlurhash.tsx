import { useState } from "react";
import { Image } from "../types";
import { Blurhash } from "react-blurhash";
interface ImageWithBlurhashParm {
  image: Image;
  key: string;
}

const ImageWithBlurhash = ({ image }: ImageWithBlurhashParm) => {
  const [loaded, setLoaded] = useState(false);
  const aspectRatio = image.metadata.width / image.metadata.height;

  return (
    <div>
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
          className={`absolute top-0 left-0 w-full h-full object-cover transition-opacity duration-500 ${
            loaded ? "opacity-100" : "opacity-0"
          }`}
        />
      </div>
      <div>{image.description}</div>
    </div>
  );
};

export default ImageWithBlurhash;
