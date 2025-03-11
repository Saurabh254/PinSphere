import { useNavigate } from "react-router";
import { Link } from "react-router-dom";
import { removeTokenFromStorage } from "../service/token_service";
import { RiLogoutCircleLine } from "@remixicon/react";
import { isUserLoggedIn } from "../service/login_service";
import { toast, ToastContainer } from "react-toastify";
import axios from "axios";
import { API_URL } from "../constants";

const toggleUploadContentModel = async () => {
  try {
    const response = await axios.get(`${API_URL}/users/me`);
    if (response.status === 200) {
      const modal = document.getElementById("my_upload_model");
      if (modal) {
        (modal as HTMLDialogElement).showModal();
      }
    }
  } catch (error) {
    toast.error("Please login to create content");
    console.error(error);
  }
};

const Header = () => {
  const loggedIn = isUserLoggedIn();
  return (
    <div className="bg-gray-800 text-white px-4 py-3 w-full sticky z-50 top-0 left-0 right-0">
      <ToastContainer />
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center">
          <span className="text-lg font-semibold">PinSphere</span>
        </div>

        <nav className="hidden md:flex space-x-6 ml-auto mr-8">
          <Link to="/" className="hover:text-gray-300">
            Home
          </Link>
          <Link to="/profile" className="hover:text-gray-300">
            Profile
          </Link>
          <Link to="#" className="hover:text-gray-300">
            About
          </Link>
          <span
            onClick={toggleUploadContentModel}
            className="hover:text-gray-300 cursor-pointer"
          >
            Create
          </span>
        </nav>
        <span
          onClick={toggleUploadContentModel}
          className="hover:text-gray-300 md:hidden items-center gap-2 flex cursor-pointer"
        >
          <svg
            className="w-6"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="#fff"
          >
            <path d="M4 19H20V12H22V20C22 20.5523 21 21 21 21H3C2.44772 21 2 20 2 20V12H4V19ZM13 9V16H11V9H6L12 3L18 9H13Z"></path>
          </svg>
          Upload
        </span>
        <div className="hidden md:flex items-center space-x-4">
          <div className="relative">
            <input
              type="text"
              placeholder="Search"
              className="bg-gray-700 text-sm text-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
            <div className="absolute inset-y-0 right-2 flex items-center pointer-events-none">
              <svg
                className="w-4 h-4 text-gray-400"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M21 21l-4.35-4.35m1.35-5.65a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
          </div>

          <div className="md:flex hidden">
            {loggedIn ? <LogoutDialog /> : <LoginDialog />}
          </div>
        </div>
      </div>
    </div>
  );
};

const LogoutDialog = () => {
  const navigator = useNavigate();
  const handle_logout = () => {
    removeTokenFromStorage();
    navigator("/login");
  };
  return (
    <>
      <button
        className="btn btn-primary flex items-center justify-center"
        onClick={() => {
          const modal = document.getElementById("logout_model");
          if (modal) {
            (modal as HTMLDialogElement).showModal();
          }
        }}
      >
        Logout
      </button>
      <dialog
        id="logout_model"
        className="modal modal-bottom sm:modal-middle  w-full"
      >
        <div className="modal-box flex flex-col w-fit items-center py-12">
          <div className="h-16 w-16 bg-red-100 rounded-full outline-8 outline-red-100 mb-4 items-center justify-center flex">
            <RiLogoutCircleLine size={48} color="red" className="my-icon" />
          </div>
          <p className=" text-black pb-8 mt-4">
            Are you sure you want to log out?
          </p>
          <div className="flex items-center justify-center p-0 gap-4">
            <div className="modal-action mt-0 ml-auto">
              <form method="dialog">
                <button className="btn btn-primary">Cancel</button>
              </form>
            </div>
            <button
              type="submit"
              onClick={handle_logout}
              className="btn bg-red-500 text-white"
            >
              Logout
            </button>
          </div>
        </div>
      </dialog>
    </>
  );
};

const LoginDialog = () => {
  const navigator = useNavigate();
  return (
    <>
      <button
        className="btn btn-primary flex items-center justify-center"
        onClick={() => {
          navigator("/login");
        }}
      >
        Login
      </button>
    </>
  );
};

export default Header;
