#include "Error.h"

std::ostream& operator<<(std::ostream& os, const Error& e)
{
	return (os << "START: " << e.start_position << "END: " << e.end_position << "\n" << e.error_type << " : " << e.message << std::endl);
}
