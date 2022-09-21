import { createContext, PropsWithChildren, useState } from "react";

interface GlobalController<T> {
	value: T,
	setValue: (value: T) => void,
}

export default function createGlobalVariableContextProvider<T>(init: T) {
	const context = createContext<GlobalController<T>>(null as unknown as GlobalController<T>);
	
	function ContextProvider({ children }: PropsWithChildren) {
		const [value, setValue] = useState<T>(init);
		const controller = {
			value,
			setValue,
		};

		return <context.Provider value={controller} children={children} />
	}

	return [context, ContextProvider] as const;
}