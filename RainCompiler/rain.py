#TOKENS

TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_EOF = "EOF"

#CONSTANTS
DIGITS = '1234567890'

#ERROR HANDLING
class Error:
	def __init__(self, error_name, details, position):
		self.error_name = error_name
		self.details = details
		self.position = position
		
	def __repr__(self):
		return f'{self.position}\n{self.error_name}:{self.details}'
	
	def as_string(self):
		return f'{self.position}\n{self.error_name}:{self.details}'
	
class IllegalCharacterError(Error):
	def __init__(self, details, position):
		super().__init__('Illegal Character Error', details, position)
		
class InvalidSyntaxError(Error):
	def __init__(self, details, position):
		super().__init__('Invalid Syntax Error', details, position)
		
class RuntimeError(Error):
	def __init__(self, details, position):
		super().__init__('Runtime Error', details, position)


class RuntimeResult:
	def __init__(self):
		self.value = None
		self.error = None

	def register(self, res):
		if res.error: self.error = res.error
		return res.value

	def success(self, value):
		self.value = value
		return self

	def failure(self, error):
		self.error = error
		return self


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
	def __init__(self, type_, value=None, position=None):
		self.type = type_
		self.value = value
		self.position = position

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
				tokens.append(Token(TT_PLUS, position = self.current_position))
				self.Advance()
			elif self.current_character == '-':
				tokens.append(Token(TT_MINUS, position = self.current_position))
				self.Advance()
			elif self.current_character == '*':
				tokens.append(Token(TT_MUL, position = self.current_position))
				self.Advance()
			elif self.current_character == '/':
				tokens.append(Token(TT_DIV, position = self.current_position))
				self.Advance()
			elif self.current_character == '(':
				tokens.append(Token(TT_LPAREN, position = self.current_position))
				self.Advance()
			elif self.current_character == ')':
				tokens.append(Token(TT_RPAREN, position = self.current_position))
				self.Advance()
			else:
				char = self.current_character
				self.Advance()
				return [], IllegalCharacterError("'" + char + "'", self.current_position)
			
		tokens.append(Token(TT_EOF, position = self.current_position))
		return tokens, None

	def MakeNumberTokens(self):
		number_string = ''
		dots = 0
		position_start = self.current_position

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
			return Token(TT_INT, int(number_string), position = position_start)
		else:
			return Token(TT_FLOAT, float(number_string), position = position_start);

				

#NODES

class NumberNode:
	def __init__(self, tok):
		self.tok = tok
		self.position = self.tok.position


	def __repr__(self):
		return f'{self.tok}'

class BinOpNode:
	def __init__(self, left_node, tok, right_node):
		self.op_tok = tok
		self.left_node = left_node
		self.right_node = right_node
		self.position = self.op_tok.position

	def __repr__(self):
		return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
	def __init__(self, op_tok, node):
		self.op_tok = op_tok
		self.node = node
		self.position = self.op_tok.position

	def __repr__(self):
		return f'({self.op_tok}, {self.node})';


class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None

	def register(self, res):
		if isinstance(res, ParseResult):
			if res.error: self.error = res.error
			return res.node
		
		return res

	def success(self, node):
		self.node = node;
		return self

	def failure(self, error):
		self.error = error
		return self


class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.token_index = -1
		self.Advance()

	def Advance(self):
		self.token_index += 1
		if self.token_index < len(self.tokens):
			self.current_tok = self.tokens[self.token_index]
		return self.current_tok

	def parse(self):
		res = self.expression();
		if not res.error and self.current_tok.type != TT_EOF:
			return res.failure(InvalidSyntaxError(
				'Expected \'+\', \'-\', \'*\', or \'/\'', 
				self.current_tok.position))
		return res

	def factor(self):
		res = ParseResult()
		token = self.current_tok

		if token.type in (TT_PLUS, TT_MINUS):
			res.register(self.Advance())
			factor = res.register(self.factor())
			if res.error:
				return res
			return res.success(UnaryOpNode(token, factor))

		elif token.type in (TT_INT, TT_FLOAT):
			res.register(self.Advance())
			return res.success(NumberNode(token))

		elif token.type == TT_LPAREN:
			res.register(self.Advance())
			expr = res.register(self.expression())

			if res.error: 
				return res

			if self.current_tok.type == TT_RPAREN:
				res.register(self.Advance())
				return res.success(expr)
			else:
				return res.failure(InvalidSyntaxError('Expected \')\'', token.position))

			
		return res.failure(InvalidSyntaxError('Expected Int or Float', token.position))

	def term(self):
		return self.binary_operation(self.factor, (TT_MUL, TT_DIV))

	def expression(self):
		return self.binary_operation(self.term, (TT_PLUS, TT_MINUS))
		

	def binary_operation(self, func, ops):
		res = ParseResult()
		left = res.register(func())

		if res.error: return res

		while self.current_tok.type in ops:
			op_tok = self.current_tok
			res.register(self.Advance())
			right = res.register(func())
			if res.error: return res
			left = BinOpNode(left, op_tok, right)

		return res.success(left)


class Interpreter:
	def visit(self, node):
		method_name = f"visit_{type(node).__name__}"
		method = getattr(self, method_name, self.no_visit_method)
		return method(node)

	def no_visit_method(self, node):
		raise Exception(f"No visit_{type(Node).__name__} method defined");
	
	def visit_NumberNode(self, node):
		return RuntimeResult().success(Number(node.tok.value).set_pos(node.position))

	def visit_BinOpNode(self, node):
		res = RuntimeResult()
		left = res.register(self.visit(node.left_node))
		if res.error: return res
		right = res.register(self.visit(node.right_node))
		if res.error: return res

		if node.op_tok.type == TT_PLUS:
			result, error = left.added_to(right)
		if node.op_tok.type == TT_MINUS:
			result, error = left.subtracted_by(right)
		if node.op_tok.type == TT_MUL:
			result, error = left.multiplied_by(right)
		if node.op_tok.type == TT_DIV:
			result, error = left.divided_by(right)

		if error: return res.failure(error)

		return res.success(result.set_pos(node.position));
	
	def visit_UnaryOpNode(self, node):
		res = RuntimeResult()
		number = res.register(self.visit(node.node))
		if res.error: return res

		if(node.op_tok.type == TT_MINUS):
			number, error = number.multiplied_by(Number(-1))

		if error: return res.failure(error)

		return res.success(number.set_pos(node.position))

class Number:
	def __init__(self, value):
		self.value = value
		self.set_pos()

	def set_pos(self, position = None):
		self.position = position
		return self
	
	def added_to(self, other):
		if isinstance(other, Number):
			return Number(self.value + other.value), None
		
	def subtracted_by(self, other):
		if isinstance(other, Number):
			return Number(self.value - other.value), None
		
	def multiplied_by(self, other):
		if isinstance(other, Number):
			return Number(self.value * other.value), None

	def divided_by(self, other):
		if isinstance(other, Number):
			if other.value == 0: return None, RuntimeError("Cannot divide by zero, please check the denominator values", other.position)
			return Number(self.value / other.value), None

	def __repr__(self):
		return str(self.value)


def run(text):
	lexer = Lexer(text)
	tokens, error = lexer.MakeTokens()

	if error: return None, error

	parser = Parser(tokens)
	ast = parser.parse()

	if ast.error: return None, ast.error

	interpreter = Interpreter();

	result = interpreter.visit(ast.node)

	return result.value, result.error