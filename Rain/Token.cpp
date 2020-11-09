#include "Token.h"

std::ostream& operator<<(std::ostream& os, const Token& t)
{
	std::string val;

	if (t.type == TT_INT)
		val = t.value.i;
	if (t.type == TT_FLOAT)
		val = t.value.f;

	return (os << t.type << "::" << val);
}