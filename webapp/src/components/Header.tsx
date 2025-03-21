import { useNavigate } from "react-router";
import { Link } from "react-router-dom";
import { removeTokenFromStorage } from "../service/token_service";
import { RiLogoutCircleLine, RiMenu2Line } from "@remixicon/react";
import { isUserLoggedIn } from "../service/login_service";
import { ToastContainer } from "react-toastify";
import { toggleUploadContentModel } from "@/lib/utils";

const Header = () => {
  const loggedIn = isUserLoggedIn();
  const toggleMobileMenu = () => {
    const menu = document.querySelector("#mobile_menu");
    if (menu) {
      menu.classList.toggle("h-full");
    }
  };
  return (
    <div className="bg-gray-800  text-white px-4 py-3 w-full sticky z-50 top-0 left-0 right-0">
      <ToastContainer />
      <div className="w-full relative">
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center">
            <Link to="/" className="text-lg font-semibold">
              PinSphere
            </Link>
          </div>

          {/* desktop menu */}
          <div className="w-full items-center hidden md:flex">
            <nav className="flex space-x-6 ml-auto mr-8">
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

            <div className=" flex items-center space-x-4">
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

          {/* mobile menu */}
          <RiMenu2Line
            className="md:hidden cursor-pointer"
            onClick={toggleMobileMenu}
          />
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
