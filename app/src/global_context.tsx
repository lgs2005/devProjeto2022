import { createContext, PropsWithChildren, useState } from "react";
import { User } from "./api/api_types";

interface GlobalContext<T> {
    value: T,
    setValue: (value: T) => void,
}

// eslint-disable-next-line
function createGlobalContext<T>(init: T) {
    const context = createContext<GlobalContext<T>>(null as unknown as GlobalContext<T>);

    function ContextController({ children }: PropsWithChildren) {
        const [value, setValue] = useState<T>(init);
        const controller = { value, setValue };

        return <context.Provider value={controller} children={children} />
    }

    return [context, ContextController] as const;
}

// export const [UserContext, UserContextController] = createGlobalContext<User | null>(null);
export const UserContext = createContext(null as unknown as User);