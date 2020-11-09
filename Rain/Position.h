#pragma once

struct Position
{
	int index;
	int column;
	int line;

	Position(int i, int c, int l)
	{
		index = i;
		column = c;
		line = l;
	}

	void Advance(char current_char)
	{
		index++;
		column++;

		if(current_char == '\n')
		{
			line++;
			column = 0;
		}
	}

	Position* clone()
	{
		return new Position(index, column, line);
	}
};

