from typing import List, Optional
from .lexer import Token, TokenType
from .ast import (
    Expr, Stmt, Binary, Grouping, Literal, Unary, Variable, Expression, Print, Var,
    Logical, Assign, Call, Function, If, Return, While, Block
)

class ParseError(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = self._random_meow()
        super().__init__(f"{self.message}")
    
    def _random_meow(self) -> str:
        import random
        cat_sounds = [
            "MEOW MEOW HISSS!",
            "MRRROW HISS MEOW!",
            "HISSS MEOW MEOW!",
            "PURRRR HISS MEOW!",
            "MEOW HISS HISS!",
            "MRRROW PURR HISS!",
            "HISS HISS MEOW!",
            "PURR MEOW HISS!",
            "MEOW PURR MEOW!"
        ]
        return random.choice(cat_sounds)

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0
        self.had_error = False
    
    def parse(self) -> List[Stmt]:
        statements = []
        while not self.is_at_end():
            if self.match(TokenType.NEWLINE):
                continue
            stmt = self.declaration()
            if stmt:
                statements.append(stmt)
                # Consume any trailing newlines
                while self.match(TokenType.NEWLINE):
                    continue
        return statements
    
    def declaration(self) -> Optional[Stmt]:
        try:
            if self.match(TokenType.PRRR):
                return self.function("function")
            if self.match(TokenType.MEOW):
                return self.var_declaration()
            return self.statement()
        except ParseError as error:
            self.synchronize()
            return None
    
    def function(self, kind: str) -> Function:
        name = self.consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters.")
                
                parameters.append(
                    self.consume(TokenType.IDENTIFIER, "Expect parameter name.")
                )
                
                if not self.match(TokenType.COMMA):
                    break
        
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        
        self.consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body = self.block()
        return Function(name, parameters, body)
    
    def var_declaration(self) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        
        initializer = None
        if self.match(TokenType.EQUALS):
            initializer = self.expression()
        
        if not self.is_at_end():
            self.consume(TokenType.NEWLINE, "Expect 'newline' after variable declaration.")
        return Var(name, initializer)
    
    def statement(self) -> Stmt:
        if self.match(TokenType.GRR):
            return self.if_statement()
        if self.match(TokenType.MRRR):
            return self.while_statement()
        if self.match(TokenType.PURR):
            return self.print_statement()
        if self.match(TokenType.MEW):
            return self.return_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        return self.expression_statement()
    
    def if_statement(self) -> Stmt:
        condition = self.expression()
        
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before if statement body.")
        then_branch = Block(self.block())
        
        else_branch = None
        if self.match(TokenType.GRRR):
            self.consume(TokenType.LEFT_BRACE, "Expect '{' before else statement body.")
            else_branch = Block(self.block())
        
        return If(condition, then_branch, else_branch)
    
    def while_statement(self) -> Stmt:
        condition = self.expression()
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before while loop body.")
        body = Block(self.block())
        return While(condition, body)
    
    def block(self) -> List[Stmt]:
        statements = []
        
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            if self.match(TokenType.NEWLINE):
                continue
            stmt = self.declaration()
            if stmt:
                statements.append(stmt)
        
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements
    
    def print_statement(self) -> Stmt:
        value = self.expression()
        if not self.is_at_end():
            self.consume(TokenType.NEWLINE, "Expect 'newline' after value.")
        return Print(value)
    
    def return_statement(self) -> Stmt:
        keyword = self.previous()
        value = None
        if not self.check(TokenType.NEWLINE):
            value = self.expression()
        
        if not self.is_at_end():
            self.consume(TokenType.NEWLINE, "Expect 'newline' after return value.")
        return Return(keyword, value)
    
    def expression_statement(self) -> Stmt:
        expr = self.expression()
        if not self.is_at_end():
            self.consume(TokenType.NEWLINE, "Expect 'newline' after expression.")
        return Expression(expr)
    
    def expression(self) -> Expr:
        return self.assignment()
    
    def assignment(self) -> Expr:
        expr = self.or_()
        
        if self.match(TokenType.EQUALS):
            equals = self.previous()
            value = self.assignment()
            
            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            
            self.error(equals, "Invalid assignment target.")
        
        return expr
    
    def or_(self) -> Expr:
        expr = self.and_()
        
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_()
            expr = Logical(expr, operator, right)
        
        return expr
    
    def and_(self) -> Expr:
        expr = self.equality()
        
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        
        return expr
    
    def equality(self) -> Expr:
        expr = self.comparison()
        
        while self.match(TokenType.PSPSPS, TokenType.HISSS):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def comparison(self) -> Expr:
        expr = self.term()
        
        while self.match(TokenType.TAIL_UP, TokenType.TAIL_UP_UP,
                        TokenType.TAIL_DOWN, TokenType.TAIL_DOWN_DOWN):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def term(self) -> Expr:
        expr = self.factor()
        
        while self.match(TokenType.PAW_PAW, TokenType.SCRATCH):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def factor(self) -> Expr:
        expr = self.unary()
        
        while self.match(TokenType.PURR_PURR, TokenType.FEED):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def unary(self) -> Expr:
        if self.match(TokenType.NOT, TokenType.SCRATCH):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        
        return self.call()
    
    def call(self) -> Expr:
        expr = self.primary()
        
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            else:
                break
        
        return expr
    
    def finish_call(self, callee: Expr) -> Expr:
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        
        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        
        return Call(callee, paren, arguments)
    
    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        
        raise self.error(self.peek(), "Expect expression.")
    
    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type
    
    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()
    
    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF
    
    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current - 1]
    
    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)
    
    def error(self, token: Token, message: str) -> ParseError:
        self.had_error = True
        return ParseError(token, message)
    
    def synchronize(self) -> None:
        self.advance()
        
        while not self.is_at_end():
            if self.previous().type == TokenType.NEWLINE:
                return
            
            if self.peek().type in {
                TokenType.MEOW,
                TokenType.PURR,
                TokenType.GRR,
                TokenType.GRRR,
                TokenType.MRRR,
                TokenType.PRRR,
                TokenType.MEW,
            }:
                return
            
            self.advance() 