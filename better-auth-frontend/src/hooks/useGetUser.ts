import { useContext } from "react";
import { AuthContext } from "../context/authContext";
import type { UserDetails } from "../types/authTypes";

export const useGetUser = (): UserDetails | undefined => {
  const user = useContext(AuthContext);

  if (!user) {
    console.log("user not loaded yet loaded!");
  } else return user;
};
