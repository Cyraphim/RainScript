import rain 


while True:
	text = input('rain> ')
	if text == "exit":
		break;

	result, error = rain.run('<stdin>',text)

	if error: 
		print(error.as_string())
	else:
		print(result)
	