import { useEffect } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { getUserDetails } from "../api/auth-api";
import toast from "react-hot-toast";

const ProtectedLoginRoute = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const verifyToken = async () => {
      const user = await getUserDetails();
      if (user) {
        toast.error("Session expired!");
        navigate("/user");
      }
    };

    verifyToken();
  }, []);

  return <Outlet />;
};

export default ProtectedLoginRoute;
