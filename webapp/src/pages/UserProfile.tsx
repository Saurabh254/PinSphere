import api_client from "@/api_client";
import { API_URL } from "@/constants";
import { User } from "@/types";
import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { PostComponent } from "./ProfileView";

const ProfileView: React.FC = () => {
  const { username } = useParams();
  const [user, setUser] = useState<User | null>(null);
  useEffect(() => {
    const api_call = async () => {
      try {
        const user_data = await api_client.get(API_URL + "/users/" + username);
        setUser(user_data.data);
      } catch (err) {
        console.log(err);
      }
    };
    api_call();
  }, [username]);
  if (user == null) return <h1>loading...</h1>;

  if (username == null) return <h1>profile doesn't exists...</h1>;
  return (
    <div className="w-full bg-background lg:px-12">
      <div className="flex gap-4 items-center flex-col mt-8">
        <img
          src={user.url ? user.url : "/profile.svg"}
          alt="profile"
          className="w-40 h-40 rounded-full"
        />
        <div>
          <h1 className="text-2xl font-semibold">{user.name}</h1>
          <div className="flex items-center gap-4 justify-evenly mt-4">
            <span className="flex  flex-col items-center w-fit gap-2 text-sm ">
              <span>{0}</span>
              <span>likes</span>
            </span>
            <span className="flex  flex-col items-center w-fit gap-2 text-sm">
              <span>{0}</span>
              <span>comments</span>
            </span>
            <span className="flex flex-col items-center w-fit gap-2 text-sm ">
              <span>{8}</span>
              <span>Posts</span>
            </span>
          </div>
          <span className="flex gap-2 w-full items-center justify-center mt-4 text-sm text-foreground">
            <span>Joined</span>
            <span>{new Date(user.created_at).toDateString()}</span>
          </span>
          <div className="flex gap-2 items-center justify-evenly mt-4">
            <button className="bg-primary font-bold  text-white  btn btn-sm">
              Share Profile
            </button>
            <button className="bg-red-700 font-bold   text-white  btn btn-sm">
              Report
            </button>
          </div>
        </div>
      </div>
      <h1 className="text-lg font-semibold py-4 w-full pl-12">Posts</h1>
      <hr className="w-full border-primary border-1" />
      <div className="my-8 mx-4 ">
        <div className="lg:columns-4 columns-2 gap-4 ">
          <PostComponent user={user} />
        </div>
      </div>
    </div>
  );
};

export default ProfileView;
