import React, { useEffect, useState } from "react";
import { Link, Route, Routes } from "react-router";
import ProfileUpdate from "./ProfileUpdate";
import { getLoggedInUser, getUserContents } from "@/service/user_service";
import { FileContentType, Page, SlimContent } from "@/types";
import { User } from "@/types";
import { RiContactsBook2Line } from "@remixicon/react";
import Audio from "../components/Audio";

const ProfileView: React.FC = () => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  useEffect(() => {
    const call_api = async () => {
      const user_data = await getLoggedInUser();
      setCurrentUser(user_data);
    };
    call_api();
  }, []);
  const posts: SlimContent[] = [];
  if (currentUser == null) return <h1>loading...</h1>;

  return (
    <>
      {currentUser ? (
        <div className="w-full items-center justify-center flex flex-col">
          <div className="p-8 flex items-center gap-24">
            {/* User Image */}
            <div>
              <img
                className="rounded-full h-98 w-98"
                src={currentUser.url ? currentUser.url : "/person.svg"}
                alt=""
              />
            </div>

            {/* User Info */}
            <div className="flex flex-col gap-4">
              <span className="text-lg font-bold ">
                @{currentUser.username}
              </span>
              <span className="flex gap-2">
                <span>{currentUser.name}</span>
                <span className="text-gray-500 ">he/him</span>
              </span>
              <div className="flex gap-8">
                <div className="flex flex-col items-center ">
                  <span>{posts.length}</span>
                  <span>posts</span>
                </div>
                <div className="flex flex-col items-center ">
                  <span>15</span>
                  <span>likes</span>
                </div>
              </div>
              <span className="flex gap-2 text-sm text-gray-700">
                <span>Joined</span>
                <span>{new Date(currentUser.created_at).toDateString()}</span>
              </span>

              <div className="flex gap-2">
                <Link to="profile-update" className="btn-primary btn btn-sm">
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
              <PostComponent currentUser={currentUser} />
            </div>
          </div>
        </div>
      ) : (
        <h1></h1>
      )}
    </>
  );
};

const PostComponent: React.FC<{ currentUser: User }> = ({ currentUser }) => {
  const [posts, setPosts] = useState<Page<SlimContent> | null>(null);

  useEffect(() => {
    const call_api = async () => {
      const posts_data = await getUserContents();
      setPosts(posts_data);
    };
    call_api();
  }, []);

  if (posts == null) return <h1>loading posts ...</h1>;
  return (
    <>
      {posts.items.map((post) => (
        <ContentComponent user={currentUser} post={post} />
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
      <div className="border-2 aspect-auto break-inside-avoid mb-4 border-gray-200 bg-indigo-200  rounded-lg px-4 py-2">
        <div className="flex items-center gap-2 mb-2 font-semibold">
          {user.url ? (
            <img src={user.url} className="h-8 w-8  rounded-full" />
          ) : (
            <RiContactsBook2Line />
          )}
          <span className="text-sm">{user.name}</span>
        </div>

        <img src={post.url} alt="" className="rounded-[10px] w-full" />
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
      <Route path="profile-update" element={<ProfileUpdate />} />
    </Routes>
  );
};
export default ProfileViewRouter;
