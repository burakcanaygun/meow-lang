from enum import Enum, auto
from typing import List, Optional
import random

class TokenType(Enum):
    # Keywords
    MEOW = auto()      # var
    PURR = auto()      # print
    HISS = auto()      # grouping
    GRR = auto()       # if
    GRRR = auto()      # else
    MRRR = auto()      # while
    PRRR = auto()      # function
    MEW = auto()       # return
    AND = auto()
    OR = auto()
    TRUE = auto()
    FALSE = auto()
    NIL = auto()
    
    # Operators
    PAW_PAW = auto()     # plus (+)
    SCRATCH = auto()     # minus (-)
    PURR_PURR = auto()   # multiply (*)
    FEED = auto()        # divide (/)
    EQUALS = auto()      # =
    PSPSPS = auto()      # == (cats come when equal)
    HISSS = auto()       # != (cats hiss when different)
    TAIL_UP = auto()     # > (proud tail up)
    TAIL_UP_UP = auto()  # >= (very proud tail)
    TAIL_DOWN = auto()   # < (sad tail down)
    TAIL_DOWN_DOWN = auto() # <= (very sad tail)
    NOT = auto()
    
    # Delimiters
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()

class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: Optional[object], line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __str__(self) -> str:
        return f"{self.type}: {self.lexeme}"

class LexerError(Exception):
    def __init__(self, line: int, message: str):
        self.line = line
        self.message = self._random_meow()
        super().__init__(f"{self.message}")
    
    def _random_meow(self) -> str:
        cat_sounds = [
            "MEOW MEOW HISSS!",
            "MRRROW HISS MEOW!",
            "HISSS MEOW MEOW!",
            "PURRRR HISS MEOW!",
            "MEOW HISS HISS!",
            "MRRROW PURR HISS!"
        ]
        return random.choice(cat_sounds)

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        
        self.keywords = {
            "meow": TokenType.MEOW,
            "purr": TokenType.PURR,
            "hiss": TokenType.HISS,
            "grr": TokenType.GRR,
            "grrr": TokenType.GRRR,
            "mrrr": TokenType.MRRR,
            "prrr": TokenType.PRRR,
            "mew": TokenType.MEW,
            "and": TokenType.AND,
            "or": TokenType.OR,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "nil": TokenType.NIL,
            "TAIL_UP": TokenType.TAIL_UP,
            "TAIL_UP_UP": TokenType.TAIL_UP_UP,
            "TAIL_DOWN": TokenType.TAIL_DOWN,
            "TAIL_DOWN_DOWN": TokenType.TAIL_DOWN_DOWN,
            "PSPSPS": TokenType.PSPSPS,
            "HISSS": TokenType.HISSS,
        }
    
    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    
    def scan_token(self) -> None:
        c = self.advance()
        
        if c == ' ' or c == '\r' or c == '\t':
            return
        elif c == '\n':
            self.line += 1
            if self.tokens and self.tokens[-1].type != TokenType.NEWLINE:
                self.add_token(TokenType.NEWLINE)
        elif c == '#':  # Comment
            while self.peek() != '\n' and not self.is_at_end():
                self.advance()
        elif c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '@':  # PAW_PAW for addition
            self.add_token(TokenType.PAW_PAW)
        elif c == '%':  # SCRATCH for subtraction
            self.add_token(TokenType.SCRATCH)
        elif c == '~':  # PURR_PURR for multiplication
            self.add_token(TokenType.PURR_PURR)
        elif c == '^':  # FEED for division
            self.add_token(TokenType.FEED)
        elif c == '=':
            self.add_token(TokenType.EQUALS)  # =
        elif c == '!':
            self.add_token(TokenType.NOT)
        elif c == '"':
            self.string()
        elif c.isdigit():
            self.number()
        elif c.isalpha() or c == '_':  # Allow underscore in identifiers
            self.identifier()
        else:
            raise LexerError(self.line, f"Unexpected character: {c}")
    
    def identifier(self) -> None:
        while self.peek().isalnum():
            self.advance()
        
        text = self.source[self.start:self.current]
        type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(type)
    
    def string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        
        if self.is_at_end():
            raise LexerError(self.line, "Unterminated string - missing closing quote")
        
        # The closing ".
        self.advance()
        
        # Trim the surrounding quotes.
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)
    
    def number(self) -> None:
        while self.peek().isdigit():
            self.advance()
        
        # Look for a fractional part.
        if self.peek() == '.' and self.peek_next().isdigit():
            # Consume the "."
            self.advance()
            
            while self.peek().isdigit():
                self.advance()
        
        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)
    
    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        
        self.current += 1
        return True
    
    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]
    
    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]
    
    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c
    
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
    
    def add_token(self, type: TokenType, literal: Optional[object] = None) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line)) 