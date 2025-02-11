import { useState } from "react";
import { Blurhash } from "react-blurhash";

const getRandomSize = () => {
  const sizes = ["200px", "300px", "600px", "500px", "150px", "250px"];
  return sizes[Math.floor(Math.random() * sizes.length)];
};

interface Image {
  id: string;
  url: string;
  blurhash: string;
  description: string;
}
interface ImageWithBlurhashParm {
  image: Image;
}
const ImageWithBlurhash = ({ image }: ImageWithBlurhashParm) => {
  const [isLoaded, setIsLoaded] = useState(false);

  return (
    <div className="p-4 m-2 mb-8 bg-base-light rounded-md relative">
      {/* Blurhash Placeholder */}
      {!isLoaded && (
        <Blurhash
          hash={image.blurhash}
          width="100%"
          height={getRandomSize()} // Adjust as needed
          resolutionX={32}
          resolutionY={32}
          punch={1}
          // className="absolute top-0 left-0 w-full h-full rounded-md"
          className="w-full rounded-md shadow break-inside-avoid transition-opacity duration-500"
        />
      )}

      {/* Actual Image */}
      <img
        key={image.id}
        className={`w-full rounded-md shadow break-inside-avoid transition-opacity duration-500 ${
          isLoaded ? "" : "hidden"
        }`}
        src={image.url}
        alt={image.description}
        onLoad={() =>
          setTimeout(
            () => setIsLoaded(true),
            Math.floor(Math.random() * (5000 - 1000 + 1)) + 1000
          )
        }
      />
    </div>
  );
};

export default ImageWithBlurhash;
