#pragma once

#include "Lexer.h"

struct Rain
{
	static void Run(std::string text)
	{
		Lexer* lexer = new Lexer(text);
		auto tokens = lexer->MakeTokens();
		
		for(Token T : tokens)
		{
			std::cout << "TOKEN: ";
			std::cout << T << std::endl;
		}
	}
};

