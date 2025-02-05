import { useEffect, useState } from "react";
import { API_URL } from "../constants";
import api_client from "../api_client";
import { Route, Routes, useNavigate } from "react-router";
import Header from "../components/Header";

type Image = {
  id: number;
  url: string;
  title: string;
};

type Page<T> = {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
};

const MainView = () => {
  const navigate = useNavigate();
  const [images, setImages] = useState<Page<Image> | null>(null);
  useEffect(() => {
    const api_call = async () => {
      await api_client
        .get(API_URL + "/images")
        .then((result) => {
          setImages(result.data);
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
      {images &&
        images.items.map((image) => (
          <div className="p-4 m-2 mb-8 bg-base-light rounded-md">
            <img
              key={image.id}
              className="w-full rounded-md shadow break-inside-avoid"
              src={image.url}
              alt={image.title}
            />
          </div>
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
