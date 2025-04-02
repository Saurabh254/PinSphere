import { lazy, useEffect, useState } from "react";
import { Route, Routes } from "react-router";
import Header from "../components/Header";
import { User } from "../types";
import ContentPage from "./ContentPage.tsx";
import MobileMenu from "@/components/MobileMenu.tsx";
import { getLoggedInUser } from "@/service/user_service.tsx";
import { UserContext } from "@/hooks/get_user.tsx";
import MainView from "@/components/MainView.tsx";
import SearchContent from "./SearchContent.tsx";
const ProfileViewRouter = lazy(() => import("./ProfileView.tsx"));

const Home = () => {
  const [user, setUser] = useState<User | null>(null);
  useEffect(() => {
    const get_user = async () => {
      setUser(await getLoggedInUser());
    };
    get_user();
  }, []);
  return (
    <UserContext.Provider value={{ user, setUser }}>
      <Header />
      <MobileMenu />
      <Routes>
        <Route index element={<MainView />} />
        <Route path="/search" element={<SearchContent />} />
        <Route path="profile/*" element={<ProfileViewRouter />} />
        <Route path="content/:content_id" element={<ContentPage />} />
      </Routes>
    </UserContext.Provider>
  );
};

export default Home;
