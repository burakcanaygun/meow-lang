# 🐱 Meow Lang

A playful, esoteric programming language with cat-themed syntax! Written in Python, Meow Lang is a unique programming language where every keyword is inspired by cat sounds and behaviors. It's a perfect blend of programming concepts and feline charm.

## 🎯 Features

- Cat-themed keywords that mimic cat sounds
- Feline arithmetic operators that make math more playful
- Esoteric yet intuitive syntax for programming concepts
- Variables and functions using cat-inspired keywords
- Control flow statements that purr and meow
- String operations with a cat's playfulness
- Mysterious error messages in pure cat language - your cat might understand them better than you do! 🐱

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- git

### Step 1: Clone the Repository

```bash
git clone https://github.com/burakcanaygun/meow_lang.git
cd meow_lang
```

### Step 2: Create a Virtual Environment

```bash
# Create a new virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install the package in development mode
pip install -e .
```

### Step 4: Verify Installation

```bash
# Run a test program
meow examples/test.meow
```

If you see cat-themed output, congratulations! Meow Lang is successfully installed! 🎉

## 🔤 Syntax Guide

### Keywords

- `meow` - Variable declaration
- `purr` - Print statement
- `grr` - If statement
- `grrr` - Else statement
- `mrrr` - While loop
- `prrr` - Function declaration
- `mew` - Return statement (replaces traditional 'return')

### Arithmetic Operators

- `@` - Addition (PAW_PAW) - Because cats add things by pawing at them
- `%` - Subtraction (SCRATCH) - Cats scratch to take away
- `~` - Multiplication (PURR_PURR) - Happy cats purr twice when things multiply
- `^` - Division (FEED) - Sharing (dividing) food between cats

### Comparison Operators

- `PSPSPS` - Equality (==) - Like calling cats, they come when things are equal
- `HISSS` - Not Equal (!=) - Cats hiss at things that are different
- `TAIL_UP` - Greater Than (>) - A proud cat with tail up
- `TAIL_UP_UP` - Greater or Equal (>=) - A very proud cat with tail high up
- `TAIL_DOWN` - Less Than (<) - A sad cat with tail down
- `TAIL_DOWN_DOWN` - Less or Equal (<=) - A very sad cat with tail low down

### Error Messages

When something goes wrong, your code will communicate with you in authentic cat language:

- "MEOW MEOW HISSS!"
- "MRRROW HISS MEOW!"
- "HISSS MEOW MEOW!"
- "PURRRR HISS MEOW!"
... and other mysterious feline messages. Each error has its own unique cat sound combination!

### Examples

```meow
# Variable declaration
meow x = 5
meow y = 10

# Print statement
purr "Hello World!"

# Arithmetic operations
meow sum = x @ y        # Addition with paw pats
meow diff = x % y       # Subtraction with scratches
meow prod = x ~ y       # Multiplication with happy purrs
meow quot = x ^ y       # Division by sharing food

# If-else statement with cat tail comparison
grr x TAIL_UP y {       # if x > y
    purr "x is greater than y, tail proudly up!"
} grrr {
    purr "y is greater or equal, tail down..."
}

# Equality check using cat calls
grr x PSPSPS y {        # if x == y
    purr "The cats are equal!"
} grrr {
    purr "HISSS! They are different!"
}

# Function declaration
prrr add(a, b) {
    mew a @ b           # Return sum using PAW_PAW
}

# While loop with SCRATCH (subtraction)
meow i = 5
mrrr i TAIL_UP 0 {      # while i > 0
    purr i
    meow i = i % 1      # Countdown using SCRATCH
}
```

## 🐱 Debugging Tips

- When your code produces error messages, try to interpret the cat sounds
- More "HISS" usually means something is very wrong
- "MEOW MEOW" might be a gentler error
- If your cat starts responding to the error messages, you're on the right track! The cake is a lie.

## 🛠️ Development

Want to contribute? Great! Here are some tips:

1. Fork the repository
2. Create a new branch for your feature
3. Write your code
4. Add tests in the `examples` directory
5. Submit a pull request

### Running Tests

```bash
# Run all example programs
meow examples/test.meow
```

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.
