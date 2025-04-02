import { User } from "@/types";
import { useEffect, useRef, useState } from "react";

interface ProfileImageProps {
  profile: User;
  profile_image?: File | null;
}

const ProfileImage = ({ profile, profile_image }: ProfileImageProps) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [imageUrl, setImageUrl] = useState<string | null>(null);

  useEffect(() => {
    if (profile_image || profile.url) {
      const img = new Image();
      img.crossOrigin = "anonymous";
      img.src = profile_image
        ? URL.createObjectURL(profile_image)
        : profile.url || "";

      img.onload = () => {
        const canvas = canvasRef.current;
        const ctx = canvas?.getContext("2d");
        if (!canvas || !ctx) return;
        const size = Math.min(img.width, img.height);

        canvas.width = size;
        canvas.height = size;

        ctx.drawImage(
          img,
          (img.width - size) / 2,
          (img.height - size) / 2,
          size,
          size,
          0,
          0,
          size,
          size
        );
        setImageUrl(canvas?.toDataURL() || "");
        setImageUrl(canvas.toDataURL());
      };
    }
  }, [profile_image, profile.url]);

  return (
    <div className="relative w-48 h-48 md:w-[450px] md:h-[450px] ring-1 ring-primary border-4 border-white overflow-hidden rounded-full">
      {imageUrl ? (
        <img
          src={imageUrl}
          alt="Profile"
          className="w-full h-full object-cover"
        />
      ) : (
        <span className="flex items-center justify-center w-full h-full">
          NO image
        </span>
      )}
      <canvas ref={canvasRef} className="hidden"></canvas>
    </div>
  );
};

export default ProfileImage;
