#pragma once

#include <iostream>

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

union Value
{
	int i;
	char c;
	float f;
};

struct Token
{
	std::string type;
	Value value;

	Token(std::string t, int v)
	{
		type = t;
		value.i = v;
	}

	Token(std::string t, float v)
	{
		type = t;
		value.f = v;
	}

	friend std::ostream& operator<<(std::ostream& os, const Token& dt);

};
