from abc import ABC, abstractmethod
from typing import Any, List, Optional
from .lexer import Token

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: 'ExprVisitor') -> Any:
        pass

class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: 'StmtVisitor') -> Any:
        pass

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_binary_expr(self)

class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression
    
    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_grouping_expr(self)

class Literal(Expr):
    def __init__(self, value: Any):
        self.value = value
    
    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_literal_expr(self)

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right
    
    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_unary_expr(self)

class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name
    
    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_variable_expr(self)

class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value
    
    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_assign_expr(self)

class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_logical_expr(self)

class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: List[Expr]):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments
    
    def accept(self, visitor: 'ExprVisitor') -> Any:
        return visitor.visit_call_expr(self)

class ExprVisitor(ABC):
    @abstractmethod
    def visit_assign_expr(self, expr: Assign) -> Any:
        pass
    
    @abstractmethod
    def visit_binary_expr(self, expr: Binary) -> Any:
        pass
    
    @abstractmethod
    def visit_call_expr(self, expr: Call) -> Any:
        pass
    
    @abstractmethod
    def visit_grouping_expr(self, expr: Grouping) -> Any:
        pass
    
    @abstractmethod
    def visit_literal_expr(self, expr: Literal) -> Any:
        pass
    
    @abstractmethod
    def visit_logical_expr(self, expr: Logical) -> Any:
        pass
    
    @abstractmethod
    def visit_unary_expr(self, expr: Unary) -> Any:
        pass
    
    @abstractmethod
    def visit_variable_expr(self, expr: Variable) -> Any:
        pass

class Block(Stmt):
    def __init__(self, statements: List[Stmt]):
        self.statements = statements
    
    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_block_stmt(self)

class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression
    
    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_expression_stmt(self)

class Function(Stmt):
    def __init__(self, name: Token, params: List[Token], body: List[Stmt]):
        self.name = name
        self.params = params
        self.body = body
    
    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_function_stmt(self)

class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Optional[Stmt]):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch
    
    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_if_stmt(self)

class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression
    
    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_print_stmt(self)

class Return(Stmt):
    def __init__(self, keyword: Token, value: Optional[Expr]):
        self.keyword = keyword
        self.value = value
    
    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_return_stmt(self)

class Var(Stmt):
    def __init__(self, name: Token, initializer: Optional[Expr]):
        self.name = name
        self.initializer = initializer
    
    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_var_stmt(self)

class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body
    
    def accept(self, visitor: 'StmtVisitor') -> Any:
        return visitor.visit_while_stmt(self)

class StmtVisitor(ABC):
    @abstractmethod
    def visit_block_stmt(self, stmt: Block) -> Any:
        pass
    
    @abstractmethod
    def visit_expression_stmt(self, stmt: Expression) -> Any:
        pass
    
    @abstractmethod
    def visit_function_stmt(self, stmt: Function) -> Any:
        pass
    
    @abstractmethod
    def visit_if_stmt(self, stmt: If) -> Any:
        pass
    
    @abstractmethod
    def visit_print_stmt(self, stmt: Print) -> Any:
        pass
    
    @abstractmethod
    def visit_return_stmt(self, stmt: Return) -> Any:
        pass
    
    @abstractmethod
    def visit_var_stmt(self, stmt: Var) -> Any:
        pass
    
    @abstractmethod
    def visit_while_stmt(self, stmt: While) -> Any:
        pass 