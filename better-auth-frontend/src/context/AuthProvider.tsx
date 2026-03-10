import { type ReactNode, useState, useEffect } from "react";
import { getUserDetails } from "../api/auth-api";
import { type UserDetails } from "../types/authTypes";
import toast from "react-hot-toast";
import { AuthContext } from "./authContext";

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<UserDetails | undefined>(undefined);

  useEffect(() => {
    const updateUser = async () => {
      try {
        const response = await getUserDetails();
        setUser(response);
      } catch (error) {
        toast.error(`Unable to load details ${error}`);
      }
    };

    updateUser();

    return () => {
      setUser(undefined);
    };
  });

  return <AuthContext.Provider value={user}>{children}</AuthContext.Provider>;
};
