import type { LoginResponse, UserDetails } from "../types/authTypes";
import { axiosInstance } from "./axios-instance";

export const login = async (
  username: string,
  password: string,
): Promise<LoginResponse> => {
  const result = await axiosInstance.post("/auth/login", {
    username,
    password,
  });
  return result.data;
};

export const getUserDetails = async (): Promise<UserDetails> => {
  const result = await axiosInstance.get("/auth/current/user");

  return result.data;
};
