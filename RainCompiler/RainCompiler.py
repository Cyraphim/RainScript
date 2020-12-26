import rain 


while True:
	text = input('rain> ')
	if text.strip()=="": continue

	if text == "exit":
		break;

	result, error = rain.run('<stdin>',text)

	if error: 
		print(error.as_string())
	elif result:
		if len(result.elements)==1:
			print(repr(result.elements[0]))
	else:
		print(result)
	