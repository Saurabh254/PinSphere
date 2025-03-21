import { post_comments } from "@/service/content_service";
import { RiSendPlaneLine } from "@remixicon/react";
import { useState } from "react";

const PostComments = ({ content_id }: { content_id: string }) => {
  const [comment, setComment] = useState("");
  return (
    <>
      <div className="border-b-2 border-gray-200 ">
        <span className="font-bold px-6 ">Comments</span>
      </div>
      <div className="py-4  gap-4 px-8 w-full flex items-center border-b-2 border-gray-200">
        <div className="join flex items-center gap-2 w-full ">
          <input
            type="text"
            placeholder="Add a comment"
            onChange={(e) => setComment(e.target.value)}
            className=" focus:border-primary border-2 border-gray-200 w-full rounded-lg px-4 py-2"
          />
          <RiSendPlaneLine
            className=""
            onClick={async () => {
              if (comment.length > 0) {
                await post_comments({ content_id: content_id, text: comment });
              }
              setComment("");
            }}
          />
        </div>
      </div>
    </>
  );
};

export default PostComments;
