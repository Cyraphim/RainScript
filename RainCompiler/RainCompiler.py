import rain 


while True:
	text = input('rain> ')
	if text == "exit":
		break;

	result, error = rain.run('<stdin>',text)

	if error: 
		print('\033[92m' + error.as_string() + '\033[0m')
	else:
		print(result)
	