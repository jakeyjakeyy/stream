import Cookies from "js-cookie";
import { server } from "typescript";

async function RefreshToken() {
  const serverURL = import.meta.env.VITE_BACKEND_URL;
  const refresh = Cookies.get("refresh_token");
  try {
    const response = await fetch(`http://${serverURL}:8000/api/token/refresh`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh }),
    });

    const data = await response.json();

    if (data.detail === "Token is invalid or expired") {
      Cookies.remove("refresh_token");
      Cookies.remove("access_token");
      return { message: "Expired token" };
    }

    if (data.access) {
      Cookies.set("access_token", data.access);
      return { message: "Token refreshed" };
    } else {
      return { message: "Please log in again" };
    }
  } catch (err) {
    console.log(err);
  }
}

export default RefreshToken;
