# IMPORTS


from string_with_arrows import *
import string

# CONSTANTS
DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS


# ERRORS
class Error:
	def __init__(self, position_start, position_end, error_name, details):
		self.position_start = position_start
		self.position_end = position_end
		self.error_name = error_name
		self.details = details
	
	def as_string(self):
		result  = f'{self.error_name}: {self.details}\n'
		result += f'File {self.position_start.fn}, line {self.position_start.ln + 1}'
		result += '\n\n' + string_with_arrows(self.position_start.ftxt, self.position_start, self.position_end)
		return result

class IllegalCharError(Error): #used when lexer doesnt support current character code
	def __init__(self, position_start, position_end, details):
		super().__init__(position_start, position_end, 'Illegal Character', details)

class InvalidSyntaxError(Error):
	def __init__(self, position_start, position_end, details=''):
		super().__init__(position_start, position_end, 'Invalid Syntax', details)

class RuntimeError(Error):
	def __init__(self, position_start, position_end, details, context):
		super().__init__(position_start, position_end, 'Runtime Error', details)
		self.context = context

	def as_string(self):
		result  = self.generate_traceback()
		result += f'{self.error_name}: {self.details}'
		result += '\n\n' + string_with_arrows(self.position_start.ftxt, self.position_start, self.position_end)
		return result

	def generate_traceback(self):
		result = ''
		pos = self.position_start
		ctx = self.context

		while ctx:
			result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
			pos = ctx.parent_entry_pos
			ctx = ctx.parent

		return 'Traceback (most recent call last):\n' + result


# POSITION
# Keep track of line number, current index and column number
class Position:
	def __init__(self, index, ln, col, fn, ftxt):
		self.index = index
		self.ln = ln
		self.col = col
		self.fn = fn
		self.ftxt = ftxt

	def Advance(self, current_char=None):
		self.index += 1
		self.col += 1

		if current_char == '\n':  #if the current character is in new line,it will reset the column to zero and increment the line
			self.ln += 1
			self.col = 0

		return self

	def copy(self):  #it will make copy of position
		return Position(self.index, self.ln, self.col, self.fn, self.ftxt)


# TOKENS
TT_INT			= 'INT'
TT_FLOAT    	= 'FLOAT'
TT_IDENTIFIER	= 'IDENTIFIER'
TT_KEYWORD		= 'KEYWORD'
TT_PLUS     	= 'PLUS'
TT_MINUS    	= 'MINUS'
TT_MUL      	= 'MUL'
TT_DIV      	= 'DIV'
TT_POW			= 'POW'
TT_EQ			= 'EQ'
TT_LPAREN   	= 'LPAREN'
TT_RPAREN   	= 'RPAREN'
TT_EOF			= 'EOF'

KEYWORDS = [
	'var'
]

class Token:
	def __init__(self, type_, value=None, position_start=None, position_end=None):
		self.type = type_
		self.value = value

		if position_start:
			self.position_start = position_start.copy()
			self.position_end = position_start.copy()
			self.position_end.Advance()

		if position_end:
			self.position_end = position_end.copy()

	def matches(self, type_, value):
		return self.type == type_ and self.value == value
	
	def __repr__(self):
		if self.value: return f'{self.type}:{self.value}'
		return f'{self.type}'


# LEXER
class Lexer:
	def __init__(self, fn, text):
		self.fn = fn
		self.text = text
		self.pos = Position(-1, 0, -1, fn, text)  #current position
		self.current_char = None #current character
		self.Advance()
	
	def Advance(self): # to  go in Advance character
		self.pos.Advance(self.current_char)
		self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

	def make_tokens(self):
		tokens = []

		while self.current_char != None:
			if self.current_char in ' \t':  #checking there is space or not
				self.Advance()
			elif self.current_char in DIGITS:  #checking if current character is in digits
				tokens.append(self.MakeNumber())
			elif self.current_char in LETTERS:  #checking if current character is in Letters
				tokens.append(self.MakeIdentifier())
			elif self.current_char == '+':
				tokens.append(Token(TT_PLUS, position_start=self.pos))
				self.Advance()
			elif self.current_char == '-':
				tokens.append(Token(TT_MINUS, position_start=self.pos))
				self.Advance()
			elif self.current_char == '*':
				tokens.append(Token(TT_MUL, position_start=self.pos))
				self.Advance()
			elif self.current_char == '/':
				tokens.append(Token(TT_DIV, position_start=self.pos))
				self.Advance()
			elif self.current_char == '^':
				tokens.append(Token(TT_POW, position_start=self.pos))
				self.Advance()
			elif self.current_char == '=':
				tokens.append(Token(TT_EQ, position_start=self.pos))
				self.Advance()
			elif self.current_char == '(':
				tokens.append(Token(TT_LPAREN, position_start=self.pos))
				self.Advance()
			elif self.current_char == ')':
				tokens.append(Token(TT_RPAREN, position_start=self.pos))
				self.Advance()
			else:  #return some error if doesnot find either of these charaters
				position_start = self.pos.copy()
				char = self.current_char
				self.Advance()
				return [], IllegalCharError(position_start, self.pos, "'" + char + "'")

		tokens.append(Token(TT_EOF, position_start=self.pos))
		return tokens, None

	def MakeNumber(self): # it will make either interger token or float token
		number_string = ''
		num_str = ''
		dot_count = 0
		position_start = self.pos.copy()

		while self.current_char != None and self.current_char in DIGITS + '.':
			if self.current_char == '.': #it will generate floating point number
				if dot_count == 1: break
				dot_count += 1
			num_str += self.current_char
			self.Advance()

		if dot_count == 0:  #it will generate integer number
			return Token(TT_INT, int(num_str), position_start, self.pos)
		else:
			return Token(TT_FLOAT, float(num_str), position_start, self.pos)

	def MakeIdentifier(self):
		id_str = ''
		position_start = self.pos.copy()

		while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
			id_str += self.current_char
			self.Advance()

		tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
		return Token(tok_type, id_str, position_start, self.pos)


# NODES
class NumberNode:
	def __init__(self, tok):
		self.tok = tok

		self.position_start = self.tok.position_start
		self.position_end = self.tok.position_end

	def __repr__(self):
		return f'{self.tok}'

class VarAccessNode:
	def __init__(self, var_name_tok):
		self.var_name_tok = var_name_tok

		self.position_start = self.var_name_tok.position_start
		self.position_end = self.var_name_tok.position_end

class VarAssignNode:
	def __init__(self, var_name_tok, value_node):
		self.var_name_tok = var_name_tok
		self.value_node = value_node

		self.position_start = self.var_name_tok.position_start
		self.position_end = self.value_node.position_end

class BinOpNode:
	def __init__(self, left_node, op_tok, right_node):
		self.left_node = left_node
		self.op_tok = op_tok
		self.right_node = right_node

		self.position_start = self.left_node.position_start
		self.position_end = self.right_node.position_end

	def __repr__(self):
		return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
	def __init__(self, op_tok, node):
		self.op_tok = op_tok
		self.node = node

		self.position_start = self.op_tok.position_start
		self.position_end = node.position_end

	def __repr__(self):
		return f'({self.op_tok}, {self.node})'


# PARSE RESULT
class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None
		self.Advance_count = 0  #keep track of how many times it Advanced in this method

	def register_Advancement(self):
		self.Advance_count += 1

	def register(self, res):
		self.Advance_count += res.Advance_count
		if res.error: self.error = res.error
		return res.node

	def success(self, node):
		self.node = node
		return self

	def failure(self, error):  #haven't Advanced since
		if not self.error or self.Advance_count == 0:
			self.error = error
		return self


# PARSER


class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.tok_index = -1  #keep track of token index
		self.Advance()

	def Advance(self, ):
		self.tok_index += 1
		if self.tok_index < len(self.tokens):
			self.current_tok = self.tokens[self.tok_index]
		return self.current_tok

	def parse(self):
		res = self.expr()
		if not res.error and self.current_tok.type != TT_EOF:
			return res.failure(InvalidSyntaxError(
				self.current_tok.position_start, self.current_tok.position_end,
				"Expected '+', '-', '*', '/' or '^'"
			))
		return res

	

	def Factor(self):
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TT_INT, TT_FLOAT): #check if character is in integer or float 
			res.register_Advancement()
			self.Advance()
			return res.success(NumberNode(tok))

		elif tok.type == TT_IDENTIFIER:
			res.register_Advancement()
			self.Advance()
			return res.success(VarAccessNode(tok))

		elif tok.type == TT_LPAREN:
			res.register_Advancement()
			self.Advance()
			expr = res.register(self.expr())
			if res.error: return res
			if self.current_tok.type == TT_RPAREN:
				res.register_Advancement()
				self.Advance()
				return res.success(expr)
			else:
				return res.failure(InvalidSyntaxError(
					self.current_tok.position_start, self.current_tok.position_end,
					"Expected ')'"
				))

		return res.failure(InvalidSyntaxError(
			tok.position_start, tok.position_end,
			"Expected int, float, identifier, '+', '-' or '('"
		))

	def power(self):
		return self.bin_op(self.Factor, (TT_POW, ), self.factor)

	def factor(self):
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TT_PLUS, TT_MINUS):
			res.register_Advancement()
			self.Advance()
			factor = res.register(self.factor())
			if res.error: return res
			return res.success(UnaryOpNode(tok, factor))

		return self.power()

	def term(self):
		return self.bin_op(self.factor, (TT_MUL, TT_DIV))

	def expr(self):
		res = ParseResult()

		if self.current_tok.matches(TT_KEYWORD, 'var'):
			res.register_Advancement()
			self.Advance()

			if self.current_tok.type != TT_IDENTIFIER:
				return res.failure(InvalidSyntaxError(
					self.current_tok.position_start, self.current_tok.position_end,
					"Expected identifier"
				))

			var_name = self.current_tok
			res.register_Advancement()
			self.Advance()

			if self.current_tok.type != TT_EQ:
				return res.failure(InvalidSyntaxError(
					self.current_tok.position_start, self.current_tok.position_end,
					"Expected '='"
				))

			res.register_Advancement()
			self.Advance()
			expr = res.register(self.expr())
			if res.error: return res
			return res.success(VarAssignNode(var_name, expr))

		node = res.register(self.bin_op(self.term, (TT_PLUS, TT_MINUS)))

		if res.error:
			return res.failure(InvalidSyntaxError(
				self.current_tok.position_start, self.current_tok.position_end,
				"Expected 'VAR', int, float, identifier, '+', '-' or '('"
			))

		return res.success(node)

	

	def bin_op(self, func_a, ops, func_b=None):
		if func_b == None:
			func_b = func_a
		
		res = ParseResult()
		left = res.register(func_a())
		if res.error: return res

		while self.current_tok.type in ops:
			op_tok = self.current_tok
			res.register_Advancement()
			self.Advance()
			right = res.register(func_b())
			if res.error: return res
			left = BinOpNode(left, op_tok, right)

		return res.success(left)


# RUNTIME RESULT


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


# VALUES


class Number:
	def __init__(self, value):
		self.value = value
		self.set_pos()
		self.set_context()

	def set_pos(self, position_start=None, position_end=None):
		self.position_start = position_start
		self.position_end = position_end
		return self

	def set_context(self, context=None):
		self.context = context
		return self

	def added_to(self, other):
		if isinstance(other, Number):
			return Number(self.value + other.value).set_context(self.context), None

	def subbed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value - other.value).set_context(self.context), None

	def multed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value * other.value).set_context(self.context), None

	def dived_by(self, other):
		if isinstance(other, Number):
			if other.value == 0:
				return None, RuntimeError(
					other.position_start, other.position_end,
					'Division by zero',
					self.context
				)

			return Number(self.value / other.value).set_context(self.context), None

	def powed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value ** other.value).set_context(self.context), None

	def copy(self):
		copy = Number(self.value)
		copy.set_pos(self.position_start, self.position_end)
		copy.set_context(self.context)
		return copy
	
	def __repr__(self):
		return str(self.value)


# CONTEXT


class Context:
	def __init__(self, display_name, parent=None, parent_entry_pos=None):
		self.display_name = display_name
		self.parent = parent
		self.parent_entry_pos = parent_entry_pos
		self.symbol_table = None


# SYMBOL TABLE


class SymbolTable:
	def __init__(self):
		self.symbols = {}
		self.parent = None

	def get(self, name):
		value = self.symbols.get(name, None)
		if value == None and self.parent:
			return self.parent.get(name)
		return value

	def set(self, name, value):
		self.symbols[name] = value

	def remove(self, name):
		del self.symbols[name]


# INTERPRETER


class Interpreter:
	def visit(self, node, context):
		method_name = f'visit_{type(node).__name__}'
		method = getattr(self, method_name, self.no_visit_method)
		return method(node, context)

	def no_visit_method(self, node, context):
		raise Exception(f'No visit_{type(node).__name__} method defined')

	

	def visit_NumberNode(self, node, context):
		return RuntimeResult().success(
			Number(node.tok.value).set_context(context).set_pos(node.position_start, node.position_end)
		)

	def visit_VarAccessNode(self, node, context):
		res = RuntimeResult()
		var_name = node.var_name_tok.value
		value = context.symbol_table.get(var_name)

		if not value:
			return res.failure(RuntimeError(
				node.position_start, node.position_end,
				f"'{var_name}' is not defined",
				context
			))

		value = value.copy().set_pos(node.position_start, node.position_end)
		return res.success(value)

	def visit_VarAssignNode(self, node, context):
		res = RuntimeResult()
		var_name = node.var_name_tok.value
		value = res.register(self.visit(node.value_node, context))
		if res.error: return res

		context.symbol_table.set(var_name, value)
		return res.success(value)

	def visit_BinOpNode(self, node, context):
		res = RuntimeResult()
		left = res.register(self.visit(node.left_node, context))
		if res.error: return res
		right = res.register(self.visit(node.right_node, context))
		if res.error: return res

		if node.op_tok.type == TT_PLUS:
			result, error = left.added_to(right)
		elif node.op_tok.type == TT_MINUS:
			result, error = left.subbed_by(right)
		elif node.op_tok.type == TT_MUL:
			result, error = left.multed_by(right)
		elif node.op_tok.type == TT_DIV:
			result, error = left.dived_by(right)
		elif node.op_tok.type == TT_POW:
			result, error = left.powed_by(right)

		if error:
			return res.failure(error)
		else:
			return res.success(result.set_pos(node.position_start, node.position_end))

	def visit_UnaryOpNode(self, node, context):
		res = RuntimeResult()
		number = res.register(self.visit(node.node, context))
		if res.error: return res

		error = None

		if node.op_tok.type == TT_MINUS:
			number, error = number.multed_by(Number(-1))

		if error:
			return res.failure(error)
		else:
			return res.success(number.set_pos(node.position_start, node.position_end))


# RUN


global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))

def run(fn, text):
	# Generate tokens
	lexer = Lexer(fn, text)
	tokens, error = lexer.make_tokens()
	if error: return None, error
	
	# Generate AST
	parser = Parser(tokens)
	ast = parser.parse()
	if ast.error: return None, ast.error

	# Run program
	interpreter = Interpreter()
	context = Context('<program>')
	context.symbol_table = global_symbol_table
	result = interpreter.visit(ast.node, context)

	return result.value, result.error