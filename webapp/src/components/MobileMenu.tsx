import { useUser } from "@/hooks/get_user";
import { toggleUploadContentModel } from "@/lib/utils";
import {
  RiContrast2Line,
  RiDashboard3Line,
  RiGitRepositoryLine,
  RiHomeSmileLine,
  RiLogoutCircleLine,
  RiPencilLine,
  RiSettings6Line,
  RiSunLine,
  RiUpload2Line,
} from "@remixicon/react";
import { useState } from "react";
import { Link } from "react-router";

const MobileMenu = () => {
  const { user } = useUser();

  const closeMenu = () => {
    document.getElementById("mobile_menu")?.classList.toggle("h-full");
    setWindowPath(window.location.pathname);
  };

  const [windowPath, setWindowPath] = useState(window.location.pathname);

  return (
    <div
      className="bg-background items-left pl-8 md:hidden   flex z-10 flex-col w-full overflow-hidden transition-[height] duration-300 fixed h-0 text-foreground"
      id="mobile_menu"
    >
      {/* profile  */}
      <Link to="/profile" onClick={closeMenu} className="flex mb-8 gap-4 pt-24">
        <div>
          {user && user.url && (
            <img
              src={user.url}
              alt="profile"
              className="w-16 h-16 rounded-full outline-4 outline-primary"
            />
          )}
        </div>
        <div className="flex items-left justify-center flex-col">
          <span className="font-bold">{user && user.name}</span>
          <span className="text-gray-400">{user && user.username} </span>
          <span className="text-xs flex items-center gap-2">
            <RiPencilLine className="w-4" />
            Update Profile
          </span>
        </div>
      </Link>
      {/* title menu */}
      <span className="text-xl font-bold border-b-2 border-gray-600 mr-8 pb-2 pl-2 mt-8 ">
        Menu
      </span>
      <ul className="[&>*]:mb-4 mt-8 flex w-full pr-8 flex-col h-full items-center [&>*]:w-full  text-foreground ">
        <li onClick={closeMenu}>
          <Link
            to="/"
            className={`flex items-center gap-8 px-4 py-2 rounded-3xl ${
              windowPath === "/" || windowPath === ""
                ? "font-bold bg-primary text-white"
                : "font-normal"
            }`}
          >
            <RiHomeSmileLine />
            Home
          </Link>
        </li>
        <li onClick={closeMenu}>
          <Link
            to="/dashboard"
            className={`flex items-center gap-8  px-4  py-2 rounded-3xl ${
              windowPath === "/dashboard"
                ? "font-bold bg-primary text-white"
                : "font-normal"
            }`}
          >
            <RiDashboard3Line />
            Dashboard
          </Link>
        </li>
        <li onClick={closeMenu}>
          <Link
            to="/about"
            className={`flex items-center gap-8  px-4  py-2 rounded-3xl ${
              windowPath === "/about"
                ? "font-bold bg-primary text-white"
                : "font-normal"
            }`}
          >
            <RiGitRepositoryLine /> About
          </Link>
        </li>
        <li
          onClick={() => {
            closeMenu();
            toggleUploadContentModel();
          }}
          className="flex items-center gap-8  px-4  py-2 rounded-3xl"
          style={{
            fontWeight: windowPath === "/upload" ? "bold" : "normal",
            backgroundColor: windowPath === "/upload" ? "var(--primary)" : "",
          }}
        >
          <RiUpload2Line />
          Upload
        </li>
        <li onClick={closeMenu}>
          <Link
            to="/settings"
            className={`flex items-center gap-8  px-4  py-2 rounded-3xl ${
              windowPath === "/settings"
                ? "font-bold bg-primary text-white"
                : "font-normal"
            }`}
          >
            <RiSettings6Line />
            Settings
          </Link>
        </li>
        <li
          onClick={closeMenu}
          className=" border-gray-700 w-full py-2 pl-8 rounded-lg pr-2 border-2 "
        >
          <div className="w-full flex ">
            <span className="ml-0"> Appearance</span>
            <label className="toggle cursor-pointer h-6 text-base-content rounded-lg p-0 mr-4  outline-2 ml-auto  dark:outline-primary w-14 checked:bg-gray-800 py-3">
              <input
                type="checkbox"
                className="rounded-xl h-full "
                onClick={() => {
                  document.querySelector("html")?.classList.toggle("dark");
                  document.querySelector("html")?.classList.toggle("light");
                  if (localStorage.getItem("current_theme") == "light") {
                    localStorage.setItem("current_theme", "dark");
                  } else {
                    localStorage.setItem("current_theme", "light");
                  }
                }}
              />

              <RiContrast2Line aria-label="enabled" className=" " />

              <RiSunLine
                aria-label="disabled"
                className="rounded-full  border-none p-1 outline-none "
              />
            </label>
          </div>
        </li>
        <li onClick={closeMenu} className="border-none mt-auto ">
          <Link to="/login" className="flex items-center gap-4 px-4 py-2 ">
            <RiLogoutCircleLine color="red" />
            {user ? "Logout" : "Login"}
          </Link>
        </li>
      </ul>
    </div>
  );
};

export default MobileMenu;
