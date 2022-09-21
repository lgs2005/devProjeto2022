import { User } from "../api/auth";
import createGlobalVariableContextProvider from "../lib/createGlobalStateContext";

export const [AuthControllerContext, AuthController] = 
	createGlobalVariableContextProvider<User | null>(null);