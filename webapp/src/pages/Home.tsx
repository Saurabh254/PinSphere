import { lazy, useEffect, useState } from "react";
import { API_URL } from "../constants";
import api_client from "../api_client";
import { Route, Routes } from "react-router";
import Header from "../components/Header";
import { Content } from "../types";
import ContentWithBlurhash from "../components/ContentWithBlurhash";
const ProfileUpdate = lazy(() => import("./ProfileUpdate.tsx"));

type Page<T> = {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
};

const MainView = () => {
  const [contents, setContents] = useState<Page<Content> | null>(null);
  useEffect(() => {
    const api_call = async () => {
      await api_client
        .get(API_URL + "/content")
        .then((result) => {
          setContents(result.data);
        })
        .catch((err) => {
          console.log(err);
        });
    };
    api_call();
  }, []);

  return (
    <div className="columns-2 w-full md:columns-4 gap-4 space-y-4 mt-8 mx-4 px-8 ">
      {contents &&
        contents.items.map((content) => (
          <ContentWithBlurhash content={content} key={content.id} />
        ))}
    </div>
  );
};

const Home = () => {
  return (
    <>
      <Header />
      <Routes>
        <Route index element={<MainView />} />
        <Route path="profile-update" element={<ProfileUpdate />} />
      </Routes>
    </>
  );
};

export default Home;
