import { useState } from "react";
import { Blurhash } from "react-blurhash";

const getRandomSize = () => {
  const sizes = ["200px", "300px", "600px", "500px", "150px", "250px"];
  return sizes[Math.floor(Math.random() * sizes.length)];
};

const ImageWithBlurhash = ({ image, blurhash, metadata }) => {
  const [isLoaded, setIsLoaded] = useState(false);

  return (
    <div className="p-4 m-2 mb-8 bg-base-light rounded-md relative">
      {/* Blurhash Placeholder */}
      {!isLoaded && (
        <Blurhash
          hash={blurhash}
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
        alt={image.title}
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
