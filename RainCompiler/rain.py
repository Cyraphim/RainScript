#IMPORTS
import string
from string_with_arrows import *


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
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_EQ = "EQ"

KEYWORDS = [
	'VAR'
	]

class Context:
	def __init__(self,display_name, parent=None,parent_entry_pos=None):
		self.display_name = display_name
		self.parent =parent
		self.parent_entry_pos =parent_entry_pos
		self.symbol_table = None


#SYMBOL TABLE
class SymbolTable:
	def __init__(self):
		self.symbols = {}
		self.parent = None

	def get(self,name):
		value = self.symbols.get(name,None)
		if value == None and self.parent:
			return self.parent.get(name)
		return value

	def set(self,name,value):
		self.symbols[name] = value

	def remove(self,name):
		del self.symbols[name]

	
#CONSTANTS
DIGITS = '1234567890'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS  + DIGITS

#ERROR HANDLING
class Error:
	def __init__(self, error_name, details,  position_start, position_end):
		self.error_name = error_name
		self.details = details
		self.position_start = position_start
		self.position_end = position_end
		
	def as_string(self):
		result  = f'{self.error_name}: {self.details}\n'
		result += f'File {self.position_start.fn}, line {self.position_start.ln + 1}'
		result += '\n\n' + string_with_arrows(self.position_start.ftxt, self.position_start, self.position_end)
		return result
	
class IllegalCharacterError(Error):
	def __init__(self, details, position_start, position_end):
		super().__init__(position_start, position_end,'Illegal Character Error', details)
		
class InvalidSyntaxError(Error):
	def __init__(self, details, position_start, position_end):
		super().__init__(position_start, position_end,'Invalid Syntax Error', details)
		
class RuntimeError(Error):
	
	def __init__(self, details, position_start, position_end,context):
		super().__init__(position_start, position_end,'Runtime Error', details)
		self.context = context
	def generate_traceback(self):
		result = ''
		pos = self.position_start
		ctx = self.context

		while ctx:
			result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
			pos = ctx.parent_entry_pos
			ctx = ctx.parent

		return 'Traceback (most recent call last):\n' + result


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
	def __init__(self, type_, value=None, position_start=None, position_end=None):
		self.type = type_
		self.value = value
		#self.position = position
		if position_start:
			self.position_start = position_start.copy()
			self.position_end = position_start.copy()
			self.position_end.advance 


		if position_end:
			self.position_end = position_end.copy()

	def matches(self,type_,value):
		return self.type == type_ and self.value == value

	def __repr__(self):
		if self.value:
			return f'{self.type}::{self.value}'
		else:
			return f"{self.type}"


class Lexer:
	def __init__(self, text):
		self.text = text
		self.current_position = Position(-1, 0, 1)
		self.current_character = None
		self.Advance()

	def Advance(self):
		self.current_position.advance(self.current_character)
		self.current_character = self.text[self.current_position.index] if self.current_position.index < len(self.text) else None

	def MakeTokens(self):
		tokens = []

		while self.current_character != None:
			if self.current_character in ' \t':
				self.Advance()
			elif self.current_character in DIGITS:
				tokens.append(self.MakeNumberTokens())
			elif self.current_character in LETTERS:
				tokens.append(self.MAKEIDENTIFIER())
			elif self.current_character == '+':
				tokens.append(Token(TT_PLUS, position_start = self.current_position))
				self.Advance()
			elif self.current_character == '-':
				tokens.append(Token(TT_MINUS, position_start = self.current_position))
				self.Advance()
			elif self.current_character == '*':
				tokens.append(Token(TT_MUL, position_start = self.current_position))
				self.Advance()
			elif self.current_character == '/':
				tokens.append(Token(TT_DIV, position_start = self.current_position))
				self.Advance()
			elif self.current_character == '(':
				tokens.append(Token(TT_LPAREN, position_start = self.current_position))
				self.Advance()
			elif self.current_character == ')':
				tokens.append(Token(TT_RPAREN, position_start = self.current_position))
				self.Advance()
			elif self.current_character == '=':
				tokens.append(Token(TT_EQ, position_start = self.current_position))
				self.Advance()
			else:
				position_start = self.current_position.copy()
				char = self.current_character
				self.Advance()
				return [], IllegalCharacterError(position_start, self.current_character,"'" + char + "'")

			
		tokens.append(Token(TT_EOF, position_start = self.current_position))
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
			return Token(TT_INT, int(number_string),position_start, self.current_character)
		else:
			return Token(TT_FLOAT, float(number_string), position_start, self.current_position)

	def MAKEIDENTIFIER(self):
		id_str = ' '
		position_start = self.current_position.copy()


		while self.current_character != None and self.current_character in LETTERS_DIGITS + '_':
			id_str +=  self.current_character
			self.Advance()
		TokenType = TT_KEYWORD if id_str in KEYWORDS else  TT_IDENTIFIER
		return Token(TokenType,id_str,position_start,self.current_position)


				

#NODES

class NumberNode:
	def __init__(self, tok):
		self.tok = tok
		self.position_start = self.tok.position_start
		self.position_end = self.tok.position_end


	def __repr__(self):
		return f'{self.tok}'

class VarAccessNode:
	def __init__(self,var_name_token):
		self.var_name_token = var_name_token

		self.position_start = self.var_name_token.position_start
		self.position_end = self.var_name_token.position_end

class VarAssignNode:
	def __init__(self,var_name_token,value_node):
		self.var_name_token = var_name_token
		self.value_node = value_node

		self.position_start = self.var_name_token.position_start
		self.position_end = self.value_node.position_end
class BinOpNode:
	def __init__(self, left_node, token, right_node):
		self.op_token = token
		self.left_node = left_node
		self.right_node = right_node
		self.position_start = self.left_node.position_start
		self.position_end = self.right_node.position_end

	def __repr__(self):
		return f'({self.left_node}, {self.op_token}, {self.right_node})'

class UnaryOpNode:
	def __init__(self, op_token, node):
		self.op_token = op_token
		self.node = node
		self.position_start = self.op_token.position_start
		self.position_end = node.position_end


	def __repr__(self):
		return f'({self.op_token}, {self.node})'


class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None
		self.advance_count = 0

	def register_advancement(self):
    	 self.advance_count += 1

	def register(self, res):
    	
		self.advance_count += res.advance_count
		if res.error: self.error = res.error
		return res.node
		
		

	def success(self, node):
		self.node = node
		return self

	def failure(self, error):
		self.error = error
		return self

#PARSER

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
		res = self.expression()
		if not res.error and self.current_tok.type != TT_EOF:
			return res.failure(InvalidSyntaxError(self.current_tok.position_start, self.current_tok.position_end,
				'Expected \'+\', \'-\', \'*\', or \'/\''))
		return res

	def factor(self):
		res = ParseResult()
		token = self.current_tok

		if token.type in (TT_PLUS, TT_MINUS):
			res.register_advancement()
			self.Advance()

			factor = res.register(self.factor())
			if res.error:
				return res
			return res.success(UnaryOpNode(token, factor))
		
		elif token.type in TT_IDENTIFIER:
			res.register_advancement()
			self.Advance()
			return res.success(VarAccessNode(token))

		elif token.type in (TT_INT, TT_FLOAT):
			res.register_advancement()
			self.Advance()
			return res.success(NumberNode(token))

		elif token.type == TT_LPAREN:
			res.register_advancement()
			self.Advance()
			expr = res.register(self.expression())

			if res.error: 
				return res

			if self.current_tok.type == TT_RPAREN:
				res.register_advancement()
				self.Advance()
				return res.success(expression)
			else:
				return res.failure(InvalidSyntaxError(self.current_tok.position_start,self.current_tok.position_end,'Expected \')\'' ))

			
		return res.failure(InvalidSyntaxError(token.position_start,token.position_end,'Expected Int or Float'))

	def term(self):
		return self.binary_operation(self.factor, (TT_MUL, TT_DIV))


	def expression(self):
		res = ParseResult()

		if self.current_tok.matches(TT_KEYWORD, ' VAR'):
			res.register_advancement()
			self.Advance()

			if self.current_tok.type != TT_IDENTIFIER:
				return res.failure(InvalidSyntaxError(self.current_tok.position_start,self.current_tok.position_end,
										  "EXPECTED IDENTIFIER"))
			var_name = self.current_tok
			res.register_advancement()
			self.Advance()

			if self.current_tok.type != TT_EQ:
				return res.register(InvalidSyntaxError(self.current_tok.position_start,self.current_tok.position_end,"EXPECTED '='"))

		node =  res.register(self.binary_operation(self.term, (TT_PLUS, TT_MINUS)))
		if res.error:
			return res.failure(InvalidSyntaxError(
				self.current_tok.position_start, self.current_tok.position_end,
				"Expected 'VAR', int, float, identifier, '+', '-' or '('"
			))
		return res.success(node)
		

	def binary_operation(self, func, ops):
		res = ParseResult()
		left = res.register(func())

		if res.error: return res

		while self.current_tok.type in ops:
			op_tok = self.current_tok
			res.register_advancement()
			self.Advance()
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
		raise Exception(f"No visit_{type(node).__name__} method defined")
	
	def visit_NumberNode(self, node):
		return RuntimeResult().success(Number(node.tok.value).set_pos(node.position_start, node.position_end))

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

		return res.success(result.set_pos(node.position_start, node.position_end))
	
	def visit_VarAccessNode(self, node, context):

		res = RuntimeResult()
		var_name = node.var_name_token
		value = context.symbol_table.get(var_name)

		if not value:
			return res.failure(RuntimeError(
				node.positon_start, node.position_end,
				f"'{var_name}' is not defined",
				context
			))

		value = value.copy().set_pos(node.pos_start, node.pos_end)
		return res.success(value)
	
	def visit_VarAssignNode(self, node, context):
		res = RuntimeResult()
		var_name = node.var_name_tok.value
		value = res.register(self.visit(node.value_node,context))
		if res.error: return res

		context.symbol_table.set(var_name, value)
		return res.success(value)
	
	def visit_UnaryOpNode(self, node):
		res = RuntimeResult()
		number = res.register(self.visit(node.node))
		if res.error: return res

		if(node.op_tok.type == TT_MINUS):
			number, error = number.multiplied_by(Number(-1))

		if error: return res.failure(error)

		return res.success(number.set_pos(node.position_start, node.position_end))

class Number:
	
	def __init__(self, value):
		
		self.value = value
		self.set_pos()

	def set_pos(self, position_start=None, position_end=None):
		self.position_start = position_start
		self.position_end = position_end
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
			if other.value == 0: return None, RuntimeError( other.position_start,other.position_end,"Cannot divide by zero, please check the denominator values",self.context)
			return Number(self.value / other.value), None

	def __repr__(self):
		return str(self.value)
	
	def copy(self):
		copy = Number(self.value)
		copy.set_pos(self.position_start, self.position_end)
		copy.set_context(self.context)
		return copy


##RUN

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))

def run(text):
    	

	lexer = Lexer(text)
	tokens, error = lexer.MakeTokens()

	if error: return None, error

	parser = Parser(tokens)
	ast = parser.parse()

	if ast.error: return None, ast.error

	interpreter = Interpreter()
	context = Context('<program>')
	context.symbol_table = global_symbol_table
	result = interpreter.visit(ast.node,context)

	return result.value, result.error