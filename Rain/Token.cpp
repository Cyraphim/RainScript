#include "Token.h"

std::ostream& operator<<(std::ostream& os, const Token& t)
{
	return (os << t.type << "::" << t.value);
}