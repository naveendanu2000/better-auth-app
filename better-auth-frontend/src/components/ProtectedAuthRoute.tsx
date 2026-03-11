import { useEffect, type ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { getUserDetails } from "../api/auth-api";

const ProtectedAuthRoute = ({ children }: { children: ReactNode }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const verifyToken = async () => {
      const user = await getUserDetails();
      if (!user) {
        toast.error("Session expired!");
        navigate("/");
      }
    };

    verifyToken();
  }, []);

  return children;
};

export default ProtectedAuthRoute;
