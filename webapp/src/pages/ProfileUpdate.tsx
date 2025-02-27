import { useEffect, useState } from "react";
import { get_user_profile } from "../service/login_service";
import { User } from "../types";
import { RiBook3Line, RiEditLine } from "@remixicon/react";
import {
  FormDataRequestBody,
  update_user_profile,
} from "../service/user_service";
import { upload_file } from "../service/file_handler_service";
import { API_URL } from "../constants";
import api_client from "../api_client";

interface FormDataInterface {
  email: string;
  name: string;
  bio: string;
}
interface ToastType {
  type: "success" | "error" | null;
  message: string;
}

const ProfileEdit = () => {
  const [profile, setProfile] = useState<User | null>(null);
  const [toast, setToast] = useState<ToastType>({ type: null, message: "" });
  const [profile_image, setProfileImage] = useState<File | null>(null);
  const [formdata, setFormdata] = useState<FormDataInterface>({
    email: "",
    name: "",
    bio: "",
  });
  const handleFormSubmit = async () => {
    const request_body: FormDataRequestBody = {};
    if (profile_image) {
      try {
        const upload_url_response = await api_client.get(
          `${API_URL}/users/upload_url?ext=${profile_image.type}`
        );
        await upload_file(upload_url_response.data, profile_image);

        request_body["image_key"] = upload_url_response.data.fields.key;
      } catch (error) {
        console.log(error);
      }
    }
    console.log(profile_image);

    try {
      if (formdata.email.length > 3) request_body["email"] = formdata.email;
      if (formdata.name.length > 3) request_body["name"] = formdata.name;
      if (formdata.bio.length > 3) request_body["bio"] = formdata.bio;
      console.log(request_body);
      await update_user_profile(request_body);
      setToast({ type: "success", message: "Profile Updated Successfully." });
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    const call_api = async () => {
      try {
        const response = await get_user_profile();
        setProfile(response.data);
      } catch (error) {
        console.log(error);
      }
    };
    call_api();
  }, []);
  if (!profile) return <h1>Loading</h1>;
  return (
    <>
      {toast.type == "error" && (
        <div className="toast toast-top toast-end z-50">
          <div className="alert alert-error">
            <div>
              <span>{toast.message}</span>
            </div>
          </div>
        </div>
      )}
      {toast?.type == "success" ? (
        <div className="toast toast-end fixed z-50">
          <div className={`alert alert-${toast.type}`}>
            <span>{toast.message}</span>
          </div>
        </div>
      ) : null}
      <div className="w-full h-[80vh] p-6">
        <h1 className="text-2xl font-bold mb-4">Profile Edit</h1>
        <hr />
        <div className="h-full w-full  flex items-center justify-evenly">
          {/* Image div */}
          <div className="items-center flex flex-col justify-center">
            {profile.url || profile_image ? (
              <img
                src={
                  profile_image != null && profile_image
                    ? URL.createObjectURL(profile_image)
                    : profile.url || undefined
                }
                alt=""
                className="rounded-full w-[450px] h-[450px] ring-1 ring-primary border-4 border-white"
              />
            ) : (
              <span className="w-[450px] h-[450px] rounded-full border-2 flex items-center justify-center">
                NO image
              </span>
            )}
            {/* <div> */}
            <div className="relative inline-block mt-8">
              <button
                type="button"
                className="px-4 py-2 bg-primary text-white rounded-lg"
              >
                Change Photo
              </button>
              <input
                type="file"
                onChange={(e) => {
                  if (e.target.files) {
                    setProfileImage(e.target.files[0]);
                  }
                }}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
            </div>
          </div>

          {/* Profile data div */}
          <div>
            <h1>Update Information</h1>
            <hr className="mb-8 mt-2" />
            <UserDetailsEditForm
              profile={profile}
              formdata={formdata}
              setFormdata={setFormdata}
            />
            <div className="mt-8 flex gap-4 w-full">
              <button type="submit" className="btn ml-auto bg-base-300">
                Reset
              </button>
              <button
                type="submit"
                className="btn btn-primary"
                onClick={handleFormSubmit}
              >
                Update
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

interface UserDetailsEditFormProps {
  profile: User;
  formdata: FormDataInterface;
  setFormdata: React.Dispatch<React.SetStateAction<FormDataInterface>>;
}

const UserDetailsEditForm = ({
  profile,
  formdata,
  setFormdata,
}: UserDetailsEditFormProps) => {
  return (
    <div className="flex flex-col gap-4 w-[600px]">
      <label className="input input-bordered flex items-center gap-2 w-full">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          fill="currentColor"
          className="h-4 w-4 opacity-70"
        >
          <path d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z" />
          <path d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z" />
        </svg>
        <input
          type="text"
          className="grow "
          placeholder={profile.email}
          value={formdata.email}
          onChange={(e) =>
            setFormdata({ ...formdata, email: e.target.value.trim() })
          }
          id="profile_edit_email"
        />
        <RiEditLine
          className="cursor-pointer"
          onClick={() => {
            document.getElementById("profile_edit_email")?.focus();
          }}
        />
      </label>
      <label className="input input-bordered flex items-center gap-2 w-full">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 16 16"
          fill="currentColor"
          className="h-4 w-4 opacity-70"
        >
          <path d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z" />
          <path d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z" />
        </svg>
        <input
          type="text"
          className="grow "
          placeholder={profile.name}
          value={formdata.name}
          onChange={(e) => setFormdata({ ...formdata, name: e.target.value })}
          id="profile_edit_name"
        />
        <RiEditLine
          className="cursor-pointer"
          onClick={() => {
            document.getElementById("profile_edit_name")?.focus();
          }}
        />
      </label>
      <label className="input input-bordered flex items-center gap-2 w-full">
        <RiBook3Line className="h-4 w-4 opacity-70" />
        <input
          type="text"
          className="grow"
          value={formdata.bio}
          onChange={(e) => setFormdata({ ...formdata, bio: e.target.value })}
          placeholder={profile.bio || "Enter You Bio"}
          id="profile_edit_bio"
        />
        <RiEditLine
          className="cursor-pointer"
          onClick={() => {
            document.getElementById("profile_edit_bio")?.focus();
          }}
        />
      </label>
    </div>
  );
};

export default ProfileEdit;
