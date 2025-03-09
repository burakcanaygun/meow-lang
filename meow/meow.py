import sys
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter

def run(source: str) -> None:
    try:
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        
        parser = Parser(tokens)
        statements = parser.parse()
        
        if not statements:
            return
        
        interpreter = Interpreter()
        interpreter.interpret(statements)
    except Exception as e:
        print(f"Error: {e}")

def run_file(path: str) -> None:
    with open(path, 'r') as file:
        source = file.read()
    
    run(source)

def run_prompt() -> None:
    while True:
        try:
            line = input("meow> ")
            if line.strip() == "":
                continue
            run(line)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

def main() -> None:
    if len(sys.argv) > 2:
        print("Usage: meow [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()

if __name__ == "__main__":
    main() 