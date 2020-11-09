#pragma once

#include "Token.h"
#include "Error.h"
#include "Position.h"
#include <vector>
#include <string>

struct Lexer
{
	std::string text;
	Position* current_position;
	char current_character;

	Lexer(std::string t)
	{
		Debug::Log("Testing");
		text = t;
		current_position = new Position(1, 0, -1);
		current_character = NULL;
		this->Advance();
	}

	void Advance()
	{
		current_position->Advance(NULL);
		current_character = (current_position->index < text.length())?text[current_position->index]:NULL;

	}

	Token MakeNumber()
	{
		std::string number_string;
		int dot_count = 0;

		while (this->current_character != NULL && (DIGITS.find(this->current_character) != std::string::npos || std::string(".").find(this->current_character) != std::string::npos))
		{
			if(this->current_character == '.')
			{
				if(dot_count == 1)
				{
					break;
				}

				dot_count++;
				number_string.append(1,'.');
			}
			else
			{
				number_string.append(1, this->current_character);
			}
			this->Advance();
		}
				

		number_string.append("\0");

		if (dot_count == 0)
		{
			return Token(TT_INT, number_string);
		}
		else
		{
			return Token(TT_FLOAT, number_string);
		}
	}

	std::vector<Token> MakeTokens()
	{
		std::vector<Token> toReturn;

		while(this->current_character != NULL)
		{
			if(std::string(" \t").find(this->current_character) != std::string::npos)
			{
				this->Advance();
			}
			else if (DIGITS.find(this->current_character) != std::string::npos)
			{
				toReturn.push_back(this->MakeNumber());
			}
			else if (this->current_character == '+')
			{
				toReturn.push_back(Token(TT_PLUS));
				this->Advance();
			}
			else if (this->current_character == '-')
			{
				toReturn.push_back(Token(TT_MINUS));
				this->Advance();
			}
			else if (this->current_character == '*')
			{
				toReturn.push_back(Token(TT_MUL));
				this->Advance();
			}
			else if (this->current_character == '/')
			{
				toReturn.push_back(Token(TT_DIV));
				this->Advance();
			}
			else if (this->current_character == '(')
			{
				toReturn.push_back(Token(TT_LPAREN));
				this->Advance();
			}
			else if (this->current_character == ')')
			{
				toReturn.push_back(Token(TT_RPAREN));
				this->Advance();
			}
			else
			{
				char c = this->current_character;
				this->Advance();
				std::cout << Error(ILLEGAL_CHARACTER, std::string(1, c), current_position->line, current_position->column);
				return std::vector<Token>();
			}
		}
		return toReturn;
	}
};