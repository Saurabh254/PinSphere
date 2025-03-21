import { RiAccountCircleLine } from "@remixicon/react";
import { Content } from "../types";
import { Link } from "react-router";

interface PinProps {
  children: React.ReactNode;
  content: Content;
}

const Pin = ({ children, content }: PinProps) => {
  return (
    <Link
      to={`/content/${content.id}`}
      className=" block hover:bg-gray-200 bg-gray-100 p-2  h-auto break-inside-avoid rounded-xl border-2 border-gray-300 shadow-md w-full aspect-auto"
    >
      {/* User Info */}
      <div className="flex items-center gap-2 mb-2">
        {content.user.url ? (
          <img
            src={content.user.url} // Replace with actual user profile image
            alt="User Avatar"
            className="w-7 h-7 rounded-full"
          />
        ) : (
          <RiAccountCircleLine className="w-5 h-5 rounded-full" />
        )}
        <span className="text-xs font-semibold">{`${
          content.user.name.split(" ")[0]
        } • @${content.user.username}`}</span>
      </div>

      {/* Pin Image */}
      <div className="w-full bg-gray-300 rounded-lg overflow-hidden">
        {children}
      </div>

      {/* Like & Comment Section */}
      <div className="flex items-center justify-left mt-1 text-gray-600 text-sm">
        <div className="flex items-center gap-1">
          <img src="/like.svg" alt="like content" />
          <span>{content.likes}</span>
        </div>
        <div className="flex items-center gap-1 ml-4">
          <img src="/comments.svg" alt="comments " />
          <span>{50}</span>
        </div>
      </div>

      {/* Caption */}
      <p className="text-sm text-gray-700 mt-1 pl-2 ">{content.description}</p>
    </Link>
  );
};

export default Pin;
