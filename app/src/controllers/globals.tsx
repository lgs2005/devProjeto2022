import { User } from "../api/types";

import createGlobalVariableContextProvider from "../lib/createGlobalStateContext";


export const [AuthControllerContext, AuthController] = 
	createGlobalVariableContextProvider<User | null>(null);