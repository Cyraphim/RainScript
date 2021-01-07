import rain 
import sys
import os

def main(argv):
	if len(argv) != 0:
		try: 
			with open(argv[0], "r") as f:
				script = f.read()
				result, error = rain.run(argv[0], script)
				if error: 
					print(error.as_string())
					input("Press RETURN to continue...")
		except Exception as e:
			print(e)
	else:
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
	
if __name__ == "__main__":
	main(sys.argv[1:])