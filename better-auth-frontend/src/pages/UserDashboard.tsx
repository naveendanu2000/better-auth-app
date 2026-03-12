import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { useGetUser } from "../hooks/useGetUser";
import type { UserDetails } from "../types/authTypes";
import { VscLoading } from "react-icons/vsc";
import { useState } from "react";
import { logout } from "../api/auth-api";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";

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
          <h1 className="text-xl">Welcome {user?.username}</h1>
          <button
            type="submit"
            disabled={loading}
            onClick={handleLogout}
            className="rounded text-black flex gap-2 px-4 py-2 shadow hover:shadow-xl active:shadow-lg cursor-pointer bg-white/50 backdrop-blur-3xl disabled:opacity-65 disabled:hover:shadow disabled:cursor-not-allowed hover:backdrop-blur-lg hover:bg-white/20"
          >
            {loading ? (
              <>
                <VscLoading className="animate-spin text-2xl" /> Logging
                out...{" "}
              </>
            ) : (
              "Logout"
            )}
          </button>
        </div>
      )}
    </>
  );
};

export default UserDashboard;
