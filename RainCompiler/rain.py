#TOKENS

TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"

#CONSTANTS
DIGITS = '1234567890'

#ERROR HANDLING
class Error:
	def __init__(self, error_name, details, position):
		self.error_name = error_name
		self.details = details
		self.position = position

	def as_string(self):
		return f':{self.position}\n{self.error_name}:{self.details}'

class IllegalCharacterError(Error):
	def __init__(self, details, position):
		super().__init__('Illegal Character Error', details, position)


#POSITION
class Position:
	def __init__(self, i, c, l):
		self.index = i
		self.column = c
		self.line = l

	def advance(self, char):
		self.index += 1
		self.column += 1

		if char == '\n':
			self.index += 1
			self.column = 0

		return self

	def copy(self):
		return Position(self.index, self.column, self.line)

	def __repr__(self):
		return f'Line:{self.line} Column:{self.column}'

			


#TOKEN [TYPE:VALUE]
class Token:
	def __init__(self, type_, value=None):
		self.type = type_
		self.value = value

	def __repr__(self):
		if self.value:
			return f'{self.type}::{self.value}'
		else:
			return f"{self.type}"


class Lexer:
	def __init__(self, text):
		self.text = text;
		self.current_position = Position(-1, 0, 1)
		self.current_character = None
		self.Advance()

	def Advance(self):
		self.current_position.advance(self.current_character)
		self.current_character = self.text[self.current_position.index] if self.current_position.index < len(self.text) else None;

	def MakeTokens(self):
		tokens = []

		while self.current_character != None:
			if self.current_character in ' \t':
				self.Advance()
			elif self.current_character in DIGITS:
				tokens.append(self.MakeNumberTokens())
			elif self.current_character == '+':
				tokens.append(Token(TT_PLUS))
				self.Advance()
			elif self.current_character == '-':
				tokens.append(Token(TT_MINUS))
				self.Advance()
			elif self.current_character == '*':
				tokens.append(Token(TT_MUL))
				self.Advance()
			elif self.current_character == '/':
				tokens.append(Token(TT_DIV))
				self.Advance()
			elif self.current_character == '(':
				tokens.append(Token(TT_LPAREN))
				self.Advance()
			elif self.current_character == ')':
				tokens.append(Token(TT_RPAREN))
				self.Advance()
			else:
				char = self.current_character
				self.Advance()
				return [], IllegalCharacterError("'" + char + "'", self.current_position)
			
			
		return tokens, None

	def MakeNumberTokens(self):
		number_string = ''
		dots = 0

		while self.current_character != None and self.current_character in DIGITS + '.':
			if self.current_character == '.':
				if dots == 1: 
					break
				dots += 1
				number_string += '.'
			else:
				number_string += self.current_character

			self.Advance()

		if dots == 0:
			return Token(TT_INT, int(number_string))
		else:
			return Token(TT_FLOAT, float(number_string));

				

def run(text):
	lexer = Lexer(text)
	tokens, error = lexer.MakeTokens()

	return tokens, error