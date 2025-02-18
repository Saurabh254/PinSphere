import { useEffect, useState } from "react";
import { API_URL } from "../constants";
import api_client from "../api_client";
import { Route, Routes, useNavigate } from "react-router";
import Header from "../components/Header";
import ImageWithBlurhash from "../components/ImageWithBlurhash";
import { Content } from "../types";
import ContentWithBlurhash from "../components/ContentWithBlurhash";

type Page<T> = {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
};

const MainView = () => {
  const navigate = useNavigate();
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

  const token = localStorage.getItem("access_token");
  if (!token) {
    navigate("/login");
  }
  return (
    <div className="columns-2 md:columns-4 gap-4 space-y-4 mt-8 mx-4">
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
      </Routes>
    </>
  );
};

export default Home;
