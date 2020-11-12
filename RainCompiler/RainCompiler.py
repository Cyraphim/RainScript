import rain


while True:
	text = input('rain> ')
	if text == "exit":
		break;

	result, error = rain.run(text)

	if error: 
		print(error)
	else:
		print(result)
	