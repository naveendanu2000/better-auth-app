import { useEffect, type ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import { getUserDetails } from "../api/auth-api";
import toast from "react-hot-toast";

const ProtectedAuthRoute = ({ children }: { children: ReactNode }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const verifyToken = async () => {
      try {
        await getUserDetails();
      } catch (error) {
        toast.error("Session expired!");
        console.log(error);
        navigate("/");
      }
    };

    verifyToken();
  }, [navigate]);

  return children;
};

export default ProtectedAuthRoute;
