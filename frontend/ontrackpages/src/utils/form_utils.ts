const validateFormFields = (fields: {}) => {
	let isFilled = true;	

	for (let field in fields) {
		if (fields[field as keyof typeof fields] === '') {
			isFilled = false;
		};
	};

	return isFilled;
};

export default validateFormFields;