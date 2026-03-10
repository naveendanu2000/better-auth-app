import { createContext } from "react";
import type { UserDetails } from "../types/authTypes";

export const AuthContext = createContext<UserDetails | undefined>(undefined);
