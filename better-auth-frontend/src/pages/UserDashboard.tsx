import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { useGetUser } from "../hooks/useGetUser";
import type { UserDetails } from "../types/authTypes";
import { useState } from "react";
import { logout } from "../api/auth-api";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";
import Button from "../components/small-components/Button";

const UserDashboard = () => {
  const user: UserDetails | undefined = useGetUser();
  // console.log(user);
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const handleLogout = async () => {
    setLoading(true);

    try {
      const response = await logout();
      if (response) {
        toast.success("Logout successful");
        navigate("/");
      }
    } catch (error) {
      toast.error("Unable to logout");
      console.log(error);
    }
  };

  return (
    <>
      {!user ? (
        <AiOutlineLoading3Quarters className="animate-spin text-5xl text-white" />
      ) : (
        <div className="flex flex-col items-center text-white">
          <h1 className="text-xl mb-10">Welcome {user?.username}</h1>
          <Button
            name="Logout"
            loading={loading}
            loadingText="Logging out..."
            type="submit"
            disabled={loading}
            onClick={handleLogout}
          />
        </div>
      )}
    </>
  );
};

export default UserDashboard;
