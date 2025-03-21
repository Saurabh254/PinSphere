import { Link } from "react-router";
import { RiArrowLeftLine, RiShareLine } from "@remixicon/react";
import RecentComments from "@/components/RecentComments";

const ContentPage = () => {
  const tags = ["Decoration", "Art", "Design", "Illustration"];
  return (
    <div className="w-full lg:px-12">
      <div className="w-full ">
        <div className="">
          <div className="flex items-center py-4 px-4 gap-4 border-b-2 border-gray-400 ">
            <Link to="/">
              <RiArrowLeftLine />{" "}
            </Link>
            <Link
              to="/profile/dereference__"
              className="flex items-center gap-2"
            >
              <img
                src="http://192.168.13.146:9000/pinsphere/content/dereference__/98d9f30e-a4ac-4de3-9723-70ef23d7c503.png"
                alt="back btn"
                className="w-6 h-6 rounded-full"
              />
              <span>dereference__</span>
            </Link>
          </div>
          <div className="w-full flex flex-col md:flex-row items-center justify-center md:gap-24">
            <div className="mx-4 mt-6 w-fit rounded-2xl overflow-hidden border-white outline-4 outline-primary border-3 md:max-w-1/2 ">
              <img
                className=" w-full h-full max-w-[500px]"
                src="http://192.168.13.146:9000/pinsphere/content/dereference__/98d9f30e-a4ac-4de3-9723-70ef23d7c503.png"
                alt="Content Image"
              />
            </div>
            <div className="md:w-1/3">
              {/* this is like, comment, share btns  */}
              <div className="flex  items-center justify-left  mx-6 text-gray-600 text-sm mt-4">
                <div className="flex items-center gap-1">
                  <img src="/like.svg" alt="like btn" className="w-7" />
                  <span className="font-bold">10</span>
                </div>
                <div className="flex items-center gap-1 ml-4">
                  <img src="/comments.svg" alt="" className="w-7" />
                  <span className="font-bold">{50}</span>
                </div>
                <div className="flex items-center gap-1 ml-auto">
                  <RiShareLine />
                  <span className="font-bold">Share</span>
                </div>
              </div>

              {/* This is description  */}
              <span className="px-6 block mt-3 text-sm">
                Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                Tenetur nemo tempora temporibus sunt sit neque labore eum fugit
                in? Ad, obcaecati.
              </span>

              <span className="text-xs text-gray-500 px-6 mt-4 block">
                Posted on: <strong>17 July 2025</strong>
              </span>
              {/* this is tags */}
              <div className="w-full">
                <span className="w-full border-b-2 block px-6 mt-4 font-bold border-gray-200 pb-2">
                  Tags:
                </span>
                <div className="flex gap-4 px-6 mt-2  flex-wrap">
                  {tags.map((tag) => (
                    <span
                      key={tag}
                      className="bg-primary text-white font-bold px-3  py-1 rounded-full text-xs"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
        <RecentComments />
      </div>
    </div>
  );
};

export default ContentPage;
