import axios from "axios";
import { useEffect } from "react";
import { useSearchParams } from "react-router-dom";

const googleClientId =
  "738619260855-aad32jgbdkioqjmabv2ot2njssigql3n.apps.googleusercontent.com";
const redirectUri = "http://localhost:5173/auth/google";

export const GoogleAuth = () => {
  const loginWithGoogle = () => {
    const googleAuthUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${googleClientId}&redirect_uri=${redirectUri}&response_type=code&scope=openid%20email%20profile&access_type=offline&prompt=consent`;
    window.location.href = googleAuthUrl;
  };

  return (
    <button
      onClick={loginWithGoogle}
      className="flex-1 bg-base hover:bg-opacity-90 text-primary-content py-2 px-4 rounded-lg flex items-center justify-center text-nowrap font-semibold cursor-pointer hover:bg-[#000]"
    >
      <img
        src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg"
        alt="Google Logo"
        className="h-5 mr-2"
      />
      Log in with Google
    </button>
  );
};

export const GoogleCallback = () => {
  const [searchParams] = useSearchParams();
  const code = searchParams.get("code");
  const error = searchParams.get("error");

  useEffect(() => {
    if (error) {
      console.error("Google Login Failed:", error);
      return;
    }
    if (code) {
      axios
        .post("http://localhost:8000/api/v1/auth/google", { code })
        .then((response) => {
          localStorage.setItem("access_token", response.data.access_token);
          window.location.href = "/";
        })
        .catch((error) => console.error("Error:", error));
    }
  }, [code, error]);

  return <div>{error ? "Login Failed!" : "Logging you in..."}</div>;
};
