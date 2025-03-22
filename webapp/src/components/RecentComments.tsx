import { Link } from "react-router";
import { useEffect, useState, useCallback } from "react";
import { CommentType, Page } from "@/types";
import api_client from "@/api_client";
import { API_URL } from "@/constants";
import PostComments from "./PostComments";

const RecentComments = ({ content_id }: { content_id: string }) => {
  const [comments, setComments] = useState<Page<CommentType> | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Create a fetchComments function that can be reused
  const fetchComments = useCallback(async () => {
    setIsLoading(true);
    try {
      const resp = await api_client.get(
        API_URL + `/comments/${content_id}/all`
      );
      setComments(resp.data);
    } catch (err) {
      console.log(err);
    } finally {
      setIsLoading(false);
    }
  }, [content_id]);

  // Initial fetch
  useEffect(() => {
    fetchComments();
  }, [fetchComments]);

  if (isLoading && (!comments || !comments.items.length))
    return <span>Loading comments...</span>;

  return (
    <div className="mt-4 w-full mb-8 lg:max-h-[90vh] lg:overflow-y-scroll">
      {comments && (
        <PostComments
          content_id={content_id}
          setComments={setComments}
          comments={comments}
          onCommentAdded={fetchComments} // Pass the fetchComments function
        />
      )}
      <span className="px-6 text-xs font-bold mt-2 block">Recent Comments</span>
      <div className="px-6 mt-4">
        {comments &&
          comments.items.map((comment) => (
            <div
              key={comment.id}
              className="relative border-l-2 mb-2 border-primary pl-4 py-2"
            >
              <span className="h-4 w-4 rounded-full absolute left-[-9px] bottom-[-1px] bg-primary flex items-center justify-center">
                <span className="h-[1px] w-[50%] block bg-foreground"></span>
              </span>
              <div className="flex items-center">
                <Link
                  to={`/profile/${comment.user_id}`}
                  className="flex items-center gap-2"
                >
                  <img
                    src={comment.user.url ? comment.user.url : "/profile.svg"}
                    alt={`${comment.user.username}'s avatar`}
                    className="w-6 h-6 rounded-full"
                  />
                  <span className="text-xs md:text-sm font-semibold">
                    {comment.user.name.split(" ")[0]} • @{comment.user.username}
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
