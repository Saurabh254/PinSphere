import { Link, useParams } from "react-router";
import { RiArrowLeftLine, RiShareLine } from "@remixicon/react";
import RecentComments from "@/components/RecentComments";
import { Content } from "@/types";
import { useEffect, useState } from "react";
import api_client from "@/api_client";
import { API_URL } from "@/constants";

const ContentPage = () => {
  const { content_id } = useParams();
  const [content, setContent] = useState<Content | null>(null);
  useEffect(() => {
    const api_call = async () => {
      try {
        const resp = await api_client.get(API_URL + "/content/" + content_id);
        setContent(resp.data);
      } catch (err) {
        console.log(err);
      }
    };
    api_call();
  }, [content_id]);

  if (!content) return <div>Loading...</div>;
  const tags = ["Decoration", "Art", "Design", "Illustration"];
  if (content_id == undefined) return <div>Content not found</div>;
  return (
    <div className="w-full bg-background lg:px-12">
      <div className="w-full ">
        <div className="">
          <div className="flex items-center py-4 px-4 gap-4 border-b-2 border-gray-400 ">
            <Link to="/">
              <RiArrowLeftLine />
            </Link>
            <Link
              to="/profile/dereference__"
              className="flex items-center gap-2"
            >
              <img
                src={content?.user.url ? content?.user.url : "/profile.svg"}
                alt="back btn"
                className="w-6 h-6 rounded-full"
              />
              <span className="text-sm font-semibold text-foreground">
                {content?.user.name.split(" ")[0]} @{content?.user.username}
              </span>
            </Link>
          </div>
          <div className="w-full flex flex-col md:flex-row items-center justify-center md:gap-24">
            <div className="mx-4 mt-6 w-fit rounded-2xl overflow-hidden border-primary outline-4 outline-background dark:outline-background border-3 md:max-w-1/2 ">
              <img
                className=" w-full h-full max-w-[500px]"
                src={content.url}
                alt="Content Image"
              />
            </div>
            <div className="md:w-1/3 ">
              {/* this is like, comment, share btns  */}
              <div className="flex  items-center justify-left  mx-6 text-gray-600 text-sm mt-4">
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
                  <span className="text-foreground">{content.likes}</span>
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
                  <span className="text-foreground">
                    {content?.comments_count ? content.comments_count : "10k"}
                  </span>
                </div>
                <div className="flex items-center gap-1 ml-auto">
                  <RiShareLine color="var(--foreground)" />
                  <span className="text-foreground">Share</span>
                </div>
              </div>

              {/* This is description  */}
              <span className="px-6 block mt-3 text-sm">
                {content.description}
              </span>

              <span className="text-xs text-gray-500 px-6 mt-4 block">
                Posted on: <strong>17 July 2025</strong>
              </span>
              {/* this is tags */}
              <div className="w-full">
                <span className="w-full border-b-2 block px-6 mt-4 font-bold border-gray-200 pb-2">
                  Tags:
                </span>
                <div className="flex gap-4 px-6 mt-4  flex-wrap">
                  {tags.map((tag) => (
                    <span
                      key={tag}
                      className="bg-primary text-white font-semibold px-3  py-1 rounded-full text-xs"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
        <RecentComments content_id={content_id} />
      </div>
    </div>
  );
};

export default ContentPage;
