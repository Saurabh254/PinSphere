import { RiSendPlaneLine } from "@remixicon/react";
import { Link } from "react-router";
import { useEffect, useState } from "react";
import { CommentType } from "@/types";
import api_client from "@/api_client";
import { API_URL } from "@/constants";

const RecentComments = () => {
  const [comments, setComments] = useState<CommentType[]>([]);

  useEffect(() => {
    const api_call = async () => {
      try {
        const resp = await api_client.get(API_URL + "/comments");
        setComments(resp.data);
      } catch (err) {
        console.log(err);
      }
    };
    api_call();
  }, []);

  return (
    <div className="mt-4 w-full mb-8">
      <div className="border-b-2 border-gray-200 ">
        <span className="font-bold px-6 ">Comments</span>
      </div>
      <div className="py-4  gap-4 px-8 w-full flex items-center border-b-2 border-gray-200">
        <div className="join flex items-center gap-2 w-full ">
          <input
            type="text"
            placeholder="Add a comment"
            className=" focus:border-primary border-2 border-gray-200 w-full rounded-lg px-4 py-2"
          />
          <RiSendPlaneLine className="" />
        </div>
      </div>
      <span className="px-6 text-xs font-bold mt-2 block">
        {" "}
        Recent Comments
      </span>
      <div className="px-6 mt-4">
        {comments.map((comment) => (
          <div
            key={comment.id}
            className="border-l-2 border-gray-200 pl-4 py-2"
          >
            <div className="flex items-center">
              <Link
                to={`/profile/${comment.user_id}`}
                className="flex items-center gap-2"
              >
                <img
                  src={comment.user.url ? comment.user.url : "/profile.svg"}
                  alt={`${comment.user_id}'s avatar`}
                  className="w-6 h-6 rounded-full"
                />
                <span className="text-sm font-semibold ">
                  {comment.user_id}
                </span>
              </Link>
              <span className="text-xs font-bold text-gray-400 ml-auto">
                At: {new Date(comment.created_at).toLocaleTimeString()}
              </span>
            </div>
            <span className="text-xs text-gray-500 block mt-2">
              {comment.text}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecentComments;
