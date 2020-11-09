#pragma once

#include <iostream>
#include <string>

// OPERATOR DEFINITIONS

#define TT_INT "INT"
#define TT_FLOAT "FLOAT"
#define TT_PLUS "PLUS"
#define TT_MINUS "MINUS"
#define TT_MUL "MUL"
#define TT_DIV "DIV"
#define TT_LPAREN "LPAREN"
#define TT_RPAREN "RPAREN"

// CONSTANTS

#define DIGITS std::string("0123456789")

struct Token
{
	std::string type;
	std::string value;

	Token(std::string t, std::string v = "")
	{
		type = t;
		value = v;
	}

	friend std::ostream& operator<<(std::ostream& os, const Token& dt);

};
