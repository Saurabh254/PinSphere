import React, { useEffect, useState } from "react";
import { Link, Route, Routes } from "react-router";
import ProfileUpdate from "./ProfileUpdate";
import { FileContentType, Page, SlimContent } from "@/types";
import { User } from "@/types";
import { RiContactsBook2Line } from "@remixicon/react";
import Audio from "../components/Audio";
import { useUser } from "@/hooks/get_user";
import UserProfile from "./UserProfile";
import { API_URL } from "@/constants";
import api_client from "@/api_client";

const ProfileView: React.FC = () => {
  const { user } = useUser();
  const posts: SlimContent[] = [];
  if (user == null) return <h1>loading...</h1>;

  return (
    <>
      {user ? (
        <div className="w-full items-center bg-background justify-center flex  flex-col">
          <div className="p-8 flex items-center flex-col md:flex-row gap-12 md:gap-24">
            {/* User Image */}

            <div>
              <img
                className="rounded-full h-48 w-48 border-2 border-gray-200 md:h-98 md:w-98"
                src={user.url ? user.url : "/person.svg"}
                alt=""
              />
            </div>
            {/* User Info */}
            <div className="flex flex-col items-center md:items-start gap-4">
              <span className="text-lg font-bold ">@{user.username}</span>
              <span className="flex gap-2">
                <span>{user.name}</span>
                <span className="text-gray-500 ">he/him</span>
              </span>
              <div className="flex gap-8">
                <div className="flex flex-col items-center ">
                  <span>{posts.length}</span>
                  <span>posts</span>
                </div>
                <div className="flex flex-col items-center ">
                  <span>{user.likes ? user.likes : 0}</span>
                  <span>likes</span>
                </div>
                <div className="flex flex-col items-center ">
                  <span>{user.comments_count ? user.comments_count : 0}</span>
                  <span>comments</span>
                </div>
              </div>
              <span className="flex gap-2 text-sm text-gray-700">
                <span>Joined</span>
                <span>{new Date(user.created_at).toDateString()}</span>
              </span>

              <div className="flex gap-2">
                <Link to="profile-update" className="btn-primary  btn btn-sm">
                  Edit Profile
                </Link>
                <button className="bg-gray-600 border-gray-600 text-white  btn btn-sm">
                  Share Profile
                </button>
              </div>
            </div>
          </div>
          <h1 className="text-lg font-semibold py-4 w-full pl-12">Posts</h1>
          <hr className="w-full" />
          <div className="my-8 mx-8 ">
            <div className="lg:columns-4 columns-2 gap-4 ">
              <PostComponent user={user} />
            </div>
          </div>
        </div>
      ) : (
        <h1></h1>
      )}
    </>
  );
};

export const PostComponent: React.FC<{ user: User }> = ({ user }) => {
  const [posts, setPosts] = useState<Page<SlimContent> | null>(null);

  useEffect(() => {
    const call_api = async () => {
      const contents = await api_client.get(
        API_URL + "/content?username=" + user.username
      );
      setPosts(contents.data);
    };
    call_api();
  }, [user.username]);

  if (posts == null) return <h1>loading posts ...</h1>;
  return (
    <>
      {posts.items.map((post) => (
        <ContentComponent user={user} post={post} />
      ))}
    </>
  );
};
const ContentComponent: React.FC<{ post: SlimContent; user: User }> = ({
  post,
  user,
}) => {
  if (
    (post.metadata.content_type &&
      post.metadata.content_type == FileContentType.JPEG) ||
    post.metadata.content_type == FileContentType.PNG ||
    post.metadata.content_type == FileContentType.GIF
  ) {
    return (
      <Link
        to={`/content/${post.id}`}
        className="border-2 block border-primary aspect-auto break-inside-avoid mb-4  bg-background rounded-lg px-4 py-2"
      >
        <div className="flex items-center gap-2 mb-2 font-semibold">
          {user.url ? (
            <img src={user.url} className="h-6 w-6  rounded-full" />
          ) : (
            <RiContactsBook2Line />
          )}
          <span className="text-xs md:text-sm">
            {user.name.split(" ")[0]} @{user.username}
          </span>
        </div>

        <img src={post.url} alt="" className="rounded-[10px] w-full" />
        <div className="flex items-center font-semibold text-sm gap-2 mt-1">
          <div className="flex items-center gap-1">
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              color="white"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <mask
                id="mask0_1_37"
                // style="mask-type:luminance"
                maskUnits="userSpaceOnUse"
                x="5"
                y="6"
                width="16"
                height="14"
              >
                <path
                  d="M9.85 7C7.72375 7 6 8.70281 6 10.8032C6 14.6064 10.55 18.0639 13 18.8681C15.45 18.0639 20 14.6064 20 10.8032C20 8.70281 18.2762 7 16.15 7C14.848 7 13.6965 7.6386 13 8.61602C12.6449 8.11655 12.1733 7.70892 11.625 7.42763C11.0767 7.14634 10.4678 6.99966 9.85 7Z"
                  fill="#555555"
                  stroke="white"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </mask>
              <g mask="url(#mask0_1_37)">
                <path
                  d="M4.6 4.23401H21.4V20.8299H4.6V4.23401Z"
                  fill="var(--foreground)"
                />
              </g>
            </svg>
            <span className="text-foreground">{post.likes}</span>
          </div>
          <div className="flex items-center gap-1 ml-4">
            <svg
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                opacity="0.5"
                d="M15.655 14.0692C16.2883 13.355 16.6667 12.4467 16.6667 11.4583C16.6667 9.15749 14.615 7.29166 12.0833 7.29166C9.55167 7.29166 7.5 9.15749 7.5 11.4583C7.5 13.7592 9.55167 15.625 12.0833 15.625C12.7108 15.6255 13.3327 15.5079 13.9167 15.2783L16.25 16.25L15.655 14.0692Z"
                fill="var(--foreground)"
              />
              <path
                fillRule="evenodd"
                clipRule="evenodd"
                d="M7.91667 3.125C5.0975 3.125 2.70834 5.21583 2.70834 7.91667C2.7107 8.91569 3.0442 9.88574 3.65667 10.675L3.14667 12.5442C3.01334 13.0358 3.52 13.4817 3.99 13.2858L6.32334 12.3133C6.47639 12.2496 6.59784 12.1276 6.66098 11.9743C6.72412 11.821 6.72376 11.6489 6.66 11.4958C6.59624 11.3428 6.47429 11.2213 6.32098 11.1582C6.16767 11.0951 5.99555 11.0954 5.8425 11.1592L4.68917 11.64L4.9475 10.6925C4.97488 10.5923 4.97687 10.4869 4.9533 10.3858C4.92973 10.2847 4.88134 10.1911 4.8125 10.1133C4.2725 9.50417 3.95834 8.74167 3.95834 7.91667C3.95834 6.015 5.67334 4.375 7.91667 4.375C9.65 4.375 11.0758 5.36083 11.6283 6.685C9.01167 6.89583 6.875 8.90417 6.875 11.4583C6.875 14.1592 9.26417 16.25 12.0833 16.25C12.7217 16.25 13.3358 16.1442 13.9033 15.95L16.01 16.8267C16.48 17.0233 16.9867 16.5767 16.8533 16.085L16.3433 14.2167C16.9558 13.4274 17.2893 12.4574 17.2917 11.4583C17.2917 9.04417 15.3833 7.11833 12.9658 6.73583C12.3875 4.6275 10.3125 3.125 7.91667 3.125ZM8.125 11.4583C8.125 9.5575 9.84 7.91667 12.0833 7.91667C14.3267 7.91667 16.0417 9.5575 16.0417 11.4583C16.0417 12.2825 15.7275 13.0458 15.1875 13.655C15.1187 13.7327 15.0703 13.8264 15.0467 13.9275C15.0231 14.0286 15.0251 14.134 15.0525 14.2342L15.3108 15.1817L14.1575 14.7008C14.007 14.6384 13.838 14.6372 13.6867 14.6975C13.1762 14.8989 12.6321 15.0016 12.0833 15C9.84 15 8.125 13.36 8.125 11.4583Z"
                fill="var(--foreground)"
              />
            </svg>
            <span className="text-foreground">{user?.comments_count}</span>
          </div>
        </div>
        <span className="text-foreground text-xs md:text-xs">
          {post.description.slice(0, 50)}
        </span>
      </Link>
    );
  } else if (
    post.metadata.content_type == FileContentType.MP3 ||
    post.metadata.content_type == FileContentType.WAV ||
    post.metadata.content_type == FileContentType.OGG
  ) {
    return (
      <div className="border-2 aspect-auto break-inside-avoid mb-4 border-gray-200 bg-indigo-200  rounded-lg px-4 py-2">
        <div className="flex items-center gap-2 mb-2 font-semibold">
          {user.url ? (
            <img src={user.url} className="h-8 w-8  rounded-full" />
          ) : (
            <RiContactsBook2Line />
          )}
          <span className="text-sm">{user.name}</span>
        </div>
        <Audio content={post} />
        <div className="flex items-center font-semibold text-sm gap-2 mt-1">
          <span className="flex items-center">
            <img src="/like.svg" alt="" />
            <span>{post.likes}</span>
          </span>
          <span className="flex items-center">
            <img src="/comments.svg" alt="" />
            <span>32</span>
          </span>
        </div>
        <span className="text-gray-900 text-sm">
          Lorem ipsum dolor sit amet.
        </span>
      </div>
    );
  } else {
    return (
      <div className="border-2 aspect-auto break-inside-avoid mb-4 border-gray-200 bg-indigo-200  rounded-lg px-4 py-2">
        <div className="flex items-center gap-2 mb-2 font-semibold">
          {user.url ? (
            <img src={user.url} className="h-8 w-8  rounded-full" />
          ) : (
            <RiContactsBook2Line />
          )}
          <span className="text-sm">{user.name}</span>
        </div>

        <video src={post.url} controls className="rounded-lg" />
        <div className="flex items-center font-semibold text-sm gap-2 mt-1">
          <span className="flex items-center">
            <img src="/like.svg" alt="" />
            <span>{post.likes}</span>
          </span>
          <span className="flex items-center">
            <img src="/comments.svg" alt="" />
            <span>32</span>
          </span>
        </div>
        <span className="text-gray-900 text-sm">
          Lorem ipsum dolor sit amet.
        </span>
      </div>
    );
  }
};

const ProfileViewRouter: React.FC = () => {
  return (
    <Routes>
      <Route index element={<ProfileView />} />
      <Route path=":username" element={<UserProfile />} />
      <Route path="profile-update" element={<ProfileUpdate />} />
    </Routes>
  );
};
export default ProfileViewRouter;
