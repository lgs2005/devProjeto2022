import { useState } from "react";

export default function useFormData<T extends {}>(init: T) {
	const [data, setData] = useState(init);
	const onFieldChanged: React.ChangeEventHandler<HTMLFormElement> = (e) => {
		if (e.target.name in data) {
			setData({
				...data,
				[e.target.name]: e.target.value
			});
		} else {
			console.error(`Form data entry with name ${e.target.name} does not exist.`);
		}

	}
	
	return [data, setData, onFieldChanged] as [typeof data, typeof setData, typeof onFieldChanged];
}