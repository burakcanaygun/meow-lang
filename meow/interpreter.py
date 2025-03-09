from typing import Any, Dict, List
from .ast import (
    Expr, Stmt, Binary, Grouping, Literal, Unary, Variable, Expression, Print, Var,
    Logical, Assign, Call, Function, If, Return, While, Block, ExprVisitor, StmtVisitor
)
from .lexer import Token, TokenType

class ReturnException(Exception):
    def __init__(self, value: Any):
        super().__init__()
        self.value = value

class RuntimeError(Exception):
    def __init__(self, token: Token, message: str):
        super().__init__(message)
        self.token = token
        self.message = message

class InterpreterError(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
        super().__init__(f"Line {token.line}: {message}")

class Environment:
    def __init__(self, enclosing: 'Environment' = None):
        self.values: Dict[str, Any] = {}
        self.enclosing = enclosing
    
    def define(self, name: str, value: Any) -> None:
        self.values[name] = value
    
    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        
        if self.enclosing is not None:
            return self.enclosing.get(name)
        
        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
    
    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        
        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")

class MeowCallable:
    def call(self, interpreter: 'Interpreter', arguments: List[Any]) -> Any:
        pass
    
    def arity(self) -> int:
        pass

class MeowFunction(MeowCallable):
    def __init__(self, declaration: Function, closure: Environment):
        self.declaration = declaration
        self.closure = closure
    
    def call(self, interpreter: 'Interpreter', arguments: List[Any]) -> Any:
        environment = Environment(self.closure)
        
        for i in range(len(self.declaration.params)):
            environment.define(
                self.declaration.params[i].lexeme,
                arguments[i]
            )
        
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as return_value:
            return return_value.value
        
        return None
    
    def arity(self) -> int:
        return len(self.declaration.params)

class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
    
    def interpret(self, statements: list[Stmt]) -> None:
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            if hasattr(error, 'token'):
                raise InterpreterError(error.token, str(error))
            raise InterpreterError(Token(TokenType.EOF, "", None, 0), str(error))
        except Exception as error:
            raise InterpreterError(Token(TokenType.EOF, "", None, 0), f"An unexpected error occurred: {str(error)}")
    
    def execute(self, stmt: Stmt) -> None:
        stmt.accept(self)
    
    def execute_block(self, statements: List[Stmt], environment: Environment) -> None:
        previous = self.environment
        try:
            self.environment = environment
            
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous
    
    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)
    
    def visit_block_stmt(self, stmt: Block) -> None:
        self.execute_block(stmt.statements, Environment(self.environment))
    
    def visit_expression_stmt(self, stmt: Expression) -> None:
        self.evaluate(stmt.expression)
    
    def visit_function_stmt(self, stmt: Function) -> None:
        function = MeowFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
    
    def visit_if_stmt(self, stmt: If) -> None:
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)
    
    def visit_print_stmt(self, stmt: Print) -> None:
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
    
    def visit_return_stmt(self, stmt: Return) -> None:
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        
        raise ReturnException(value)
    
    def visit_var_stmt(self, stmt: Var) -> None:
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        
        self.environment.define(stmt.name.lexeme, value)
    
    def visit_while_stmt(self, stmt: While) -> None:
        condition_value = self.evaluate(stmt.condition)
        if not isinstance(condition_value, bool) and not isinstance(condition_value, float):
            raise RuntimeError(stmt.condition.operator, "Condition must evaluate to a boolean or number.")
        
        while self.is_truthy(condition_value):
            self.execute(stmt.body)
            condition_value = self.evaluate(stmt.condition)
    
    def visit_assign_expr(self, expr: Assign) -> Any:
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
    
    def visit_binary_expr(self, expr: Binary) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        
        if expr.operator.type == TokenType.PAW_PAW:  # Addition
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return float(left) + float(right)
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            raise RuntimeError(expr.operator, "Operands must be two numbers or at least one string.")
        elif expr.operator.type == TokenType.SCRATCH:  # Subtraction
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.type == TokenType.PURR_PURR:  # Multiplication
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.type == TokenType.FEED:  # Division
            self.check_number_operands(expr.operator, left, right)
            if float(right) == 0:
                raise RuntimeError(expr.operator, "Division by zero.")
            return float(left) / float(right)
        elif expr.operator.type == TokenType.TAIL_UP:  # Greater than
            if isinstance(left, str) and isinstance(right, str):
                return left > right
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.type == TokenType.TAIL_UP_UP:  # Greater than or equal
            if isinstance(left, str) and isinstance(right, str):
                return left >= right
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.type == TokenType.TAIL_DOWN:  # Less than
            if isinstance(left, str) and isinstance(right, str):
                return left < right
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.type == TokenType.TAIL_DOWN_DOWN:  # Less than or equal
            if isinstance(left, str) and isinstance(right, str):
                return left <= right
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.type == TokenType.PSPSPS:  # Equal
            return self.is_equal(left, right)
        elif expr.operator.type == TokenType.HISSS:  # Not equal
            return not self.is_equal(left, right)
        
        return None
    
    def visit_call_expr(self, expr: Call) -> Any:
        callee = self.evaluate(expr.callee)
        
        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))
        
        if not isinstance(callee, MeowCallable):
            raise RuntimeError(expr.paren, "Can only call functions.")
        
        if len(arguments) != callee.arity():
            raise RuntimeError(
                expr.paren,
                f"Expected {callee.arity()} arguments but got {len(arguments)}."
            )
        
        return callee.call(self, arguments)
    
    def visit_grouping_expr(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expression)
    
    def visit_literal_expr(self, expr: Literal) -> Any:
        return expr.value
    
    def visit_logical_expr(self, expr: Logical) -> Any:
        left = self.evaluate(expr.left)
        
        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        
        return self.evaluate(expr.right)
    
    def visit_unary_expr(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)
        
        if expr.operator.type == TokenType.NOT:
            return not self.is_truthy(right)
        elif expr.operator.type == TokenType.SCRATCH:  # Changed from MINUS to SCRATCH for negation
            self.check_number_operand(expr.operator, right)
            return -float(right)
        
        return None
    
    def visit_variable_expr(self, expr: Variable) -> Any:
        return self.environment.get(expr.name)
    
    def check_number_operand(self, operator: Token, operand: Any) -> None:
        if isinstance(operand, (int, float)):
            return
        raise RuntimeError(operator, "Operand must be a number.")
    
    def check_number_operands(self, operator: Token, left: Any, right: Any) -> None:
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise RuntimeError(operator, "Operands must be numbers.")
    
    def is_truthy(self, object: Any) -> bool:
        if object is None:
            return False
        if isinstance(object, bool):
            return object
        if isinstance(object, float):
            return object != 0
        return True
    
    def is_equal(self, a: Any, b: Any) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b
    
    def stringify(self, value: Any) -> str:
        if value is None:
            return "nil"
        
        if isinstance(value, bool):
            return str(value).lower()
        
        if isinstance(value, (int, float)):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        
        return str(value) 