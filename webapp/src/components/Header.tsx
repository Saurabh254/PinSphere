const Header = () => {
  return (
    <div className="bg-gray-800 text-white px-4 py-3">
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center">
          <span className="text-lg font-semibold">PinSphere</span>
        </div>

        <nav className="hidden md:flex space-x-6">
          <a href="#" className="hover:text-gray-300">
            Home
          </a>
          <a href="#" className="hover:text-gray-300">
            Profile
          </a>
          <a href="#" className="hover:text-gray-300">
            About
          </a>
          <a
            onClick={() => {
              const modal = document.getElementById("my_modal_1");
              if (modal) {
                (modal as HTMLDialogElement).showModal();
              }
            }}
            className="hover:text-gray-300"
          >
            Create
          </a>
        </nav>

        <div className="flex items-center space-x-4">
          <div className="relative">
            <input
              type="text"
              placeholder="Search"
              className="bg-gray-700 text-sm text-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
            <div className="absolute inset-y-0 right-2 flex items-center pointer-events-none"></div>
          </div>

          <div className="relative">
            <button className="flex items-center space-x-2 bg-gray-700 text-sm text-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none">
              <span className="flex">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  className="w-4 mr-2"
                >
                  <path d="M12.382 3C12.7607 3 13.107 3.214 13.2764 3.55279L14 5H20C20.5523 5 21 5.44772 21 6V17C21 17.5523 20.5523 18 20 18H13.618C13.2393 18 12.893 17.786 12.7236 17.4472L12 16H5V22H3V3H12.382ZM11.7639 5H5V14H13.2361L14.2361 16H19V7H12.7639L11.7639 5Z"></path>
                </svg>
                English
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Header;
