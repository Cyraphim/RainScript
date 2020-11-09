#pragma once

#include <iostream>

#define LOG(x) std::cout << "DEBUG LOG: " << x << std::endl;


#define ILLEGAL_CHARACTER "ERROR001 :: Illegal Character Detected"

struct Error
{
	std::string message;
	std::string error_type;
	int start_position;
	int end_position;
	
	Error(std::string e, std::string m, int s_p, int s_e)
	{
		message = m;
		error_type = e;
		start_position = s_p;
		end_position = s_e;
	}

	friend std::ostream& operator<<(std::ostream& os, const Error& e);
};


