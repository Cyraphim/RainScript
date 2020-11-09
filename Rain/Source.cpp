#include "Rain.h"

int main(int argc, char** argv)
{
	std::cout << "Welcome to Rain" << std::endl << "type exit or press Ctrl-C to exit" << std::endl;
	std::string input;
	while(true)
	{
		std::cout << "rain> ";
		std::getline(std::cin, input);

		if(input == "exit")
		{
			std::cout << " ";
			break;
		}
		else
		{
			Rain::Run(input);
		}
	}
	return 0;
}