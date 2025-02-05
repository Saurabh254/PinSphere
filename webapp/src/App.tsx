import { Route, Routes } from "react-router";
import { lazy, Suspense } from "react";

const Home = lazy(() => import("./pages/Home"));
const Login = lazy(() => import("./pages/login"));
const Signup = lazy(() => import("./pages/signup"));
const CreatePostModel = lazy(() => import("./components/CreatePostModel"));

const App = () => {
  return (
    <>
      <Suspense fallback={<h1>Loading</h1>}>
        <CreatePostModel />
      </Suspense>

      <Routes>
        <Route
          path="*"
          element={
            <Suspense fallback={<h1>Loading</h1>}>
              <Home />
            </Suspense>
          }
        />
        <Route
          path="/login"
          element={
            <Suspense fallback={<h1>Loading</h1>}>
              <Login />
            </Suspense>
          }
        />
        <Route
          path="/signup"
          element={
            <Suspense fallback={<h1>Loading</h1>}>
              <Signup />
            </Suspense>
          }
        />
      </Routes>
    </>
  );
};

export default App;
