import { RiChat3Fill, RiHeart2Fill } from "@remixicon/react";

interface PinProps {
  children: React.ReactNode;
}

const Pin = ({ children }: PinProps) => {
  return (
    <div className="bg-gray-100 p-3 break-inside-avoid rounded-xl shadow-md w-fit aspect-auto">
      {/* User Info */}
      <div className="flex items-center gap-2 mb-2">
        <img
          src="http://localhost:9000/pinsphere/content/string/fb7efd66-15ca-46c9-ab66-26d44cb9a329.jpeg" // Replace with actual user profile image
          alt="User Avatar"
          className="w-7 h-7 rounded-full"
        />
        <span className="text-sm font-semibold">dereference__</span>
      </div>

      {/* Pin Image */}
      <div className="w-full bg-gray-300 rounded-lg overflow-hidden">
        {children}
      </div>

      {/* Like & Comment Section */}
      <div className="flex items-center justify-left mt-2 text-gray-600 text-sm">
        <div className="flex items-center gap-1">
          <RiHeart2Fill className="w-5 h-5 text-gray-500" />
          <span>{10}</span>
        </div>
        <div className="flex items-center gap-1 ml-4">
          <RiChat3Fill className="w-5 h-5 text-gray-500" />
          <span>{50}</span>
        </div>
      </div>

      {/* Caption */}
      <p className="text-sm text-gray-700 mt-1">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Est eos debitis
        esse.
      </p>
    </div>
  );
};

export default Pin;
