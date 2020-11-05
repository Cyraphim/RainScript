#include <iostream>
#include <string>
#include <algorithm>

int main(int argc, char** argv)
{
	std::cout << "Welcome to Rain" << std::endl << "type exit or press Ctrl-C to exit" << std::endl;
	std::string input;
	while(true)
	{
		std::cout << "rain> ";
		std::getline(std::cin, input);
		std::transform(input.begin(), input.end(), input.begin(), std::tolower);


		if(input == "exit")
		{
			std::cout << " ";
			break;
		}
		else
		{
			std::cout << "ERROR001: Could not recognise term: '" << input << "'" << std::endl;
		}
	}
	return 0;
}