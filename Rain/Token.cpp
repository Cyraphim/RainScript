#include "Token.h"

std::ostream& operator<<(std::ostream& os, const Token& t)
{
	if(t.value == "")
	{
		return (os << t.type);
	}
	else
	{
		return (os << t.type << "::" << t.value);
	}
}