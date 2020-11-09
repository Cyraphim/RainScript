#pragma once

#include <iostream>
#include <chrono>
#include <ctime>
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


struct Debug
{
	static void Log(std::string m)
	{
		auto start = std::chrono::system_clock::now();
		auto legacyStart = std::chrono::system_clock::to_time_t(start);
		char tmBuff[30];
		tm timer;
		gmtime_s(&timer, &legacyStart);
		strftime(tmBuff, sizeof(tmBuff),"[%R]", &timer);

		std::cout << tmBuff << " DEBUG: " << m << std::endl;
	}
};