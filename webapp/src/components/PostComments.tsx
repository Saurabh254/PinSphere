import { post_comments } from "@/service/content_service";
import { CommentType, Page } from "@/types";
import { RiSendPlaneLine } from "@remixicon/react";
import { useState } from "react";

const PostComments = ({
  content_id,
  comments,
  setComments,
  onCommentAdded, // Add this new prop
}: {
  content_id: string;
  comments: Page<CommentType>;
  setComments: React.Dispatch<React.SetStateAction<Page<CommentType> | null>>;
  onCommentAdded?: () => void; // Optional callback function
}) => {
  const [comment, setComment] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handlePostComment = async () => {
    if (comment.length === 0 || isSubmitting) return;

    setIsSubmitting(true);
    try {
      const resp = await post_comments({
        content_id: content_id,
        text: comment,
      });

      if (resp) {
        // Update the comments state with the new comment
        setComments({
          ...comments,
          items: [resp, ...comments.items],
        });

        // Call the callback to notify parent component
        if (onCommentAdded) {
          onCommentAdded();
        }

        // Clear the input field
        setComment("");
      }
    } catch (error) {
      console.error("Error posting comment:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handlePostComment();
    }
  };

  return (
    <>
      <div className="border-b-2 border-gray-200">
        <span className="font-bold px-6">Comments</span>
      </div>
      <div className="py-4 gap-4 px-8 w-full flex items-center border-b-2 border-gray-200">
        <div className="join flex items-center gap-2 w-full">
          <input
            type="text"
            placeholder="Add a comment"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            onKeyPress={handleKeyPress}
            className="focus:border-primary border-2 border-gray-200 w-full rounded-lg px-4 py-2"
            disabled={isSubmitting}
          />
          <RiSendPlaneLine
            className={`cursor-pointer ${isSubmitting ? "opacity-50" : ""}`}
            onClick={handlePostComment}
          />
        </div>
      </div>
    </>
  );
};

export default PostComments;
