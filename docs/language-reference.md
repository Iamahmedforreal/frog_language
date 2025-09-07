# Forg Language Reference

This document provides a comprehensive reference for the Forg programming language syntax, semantics, and features.

## Table of Contents

1. [Basic Syntax](#basic-syntax)
2. [Data Types](#data-types)
3. [Variables](#variables)
4. [Functions](#functions)
5. [Control Flow](#control-flow)
6. [Operators](#operators)
7. [Built-in Functions](#built-in-functions)
8. [Comments](#comments)
9. [Keywords](#keywords)
10. [Grammar](#grammar)

## Basic Syntax

Forg uses a C-like syntax with explicit type annotations and semicolon-terminated statements.

### Program Structure

Every Forg program must have a `main` function that returns an integer:

```forg
fn main() -> int {
    // Program code here
    return 0;
}
```

### Case Sensitivity

Forg is case-sensitive. `variable` and `Variable` are different identifiers.

### Whitespace

Whitespace (spaces, tabs, newlines) is generally ignored except for separating tokens.

## Data Types

Forg supports the following built-in data types:

### Integer (`int`)

32-bit signed integers.

```forg
let count: int = 42;
let negative: int = -10;
```

**Range**: -2,147,483,648 to 2,147,483,647

### Floating Point (`float`)

Single-precision floating-point numbers.

```forg
let pi: float = 3.14159;
let temperature: float = -273.15;
```

### Boolean (`bool`)

Boolean values: `true` or `false`.

```forg
let is_valid: bool = true;
let is_complete: bool = false;
```

### String (`str`)

String literals enclosed in double quotes.

```forg
let message: str = "Hello, World!";
let name: str = "Forg";
```

**Escape Sequences**:
- `\n` - Newline
- `\"` - Double quote
- `\\` - Backslash

### Void (`void`)

Used for functions that don't return a value.

```forg
fn print_header() -> void {
    printf("=== Header ===\n");
}
```

## Variables

Variables must be declared with explicit types using the `let` keyword.

### Declaration and Initialization

```forg
let variable_name: type = initial_value;
```

Examples:
```forg
let age: int = 25;
let height: float = 5.9;
let name: str = "Alice";
let is_student: bool = true;
```

### Assignment

After declaration, variables can be reassigned using the assignment operator:

```forg
let count: int = 0;
count = 10;      // Reassignment
count = count + 1; // Using current value
```

### Scope

Variables have block scope - they're only accessible within the block where they're declared:

```forg
fn example() -> int {
    let outer: int = 1;
    
    if true {
        let inner: int = 2;  // Only accessible in this block
        outer = outer + inner; // Can access outer variable
    }
    
    // inner is not accessible here
    return outer;
}
```

## Functions

Functions are declared using the `fn` keyword and must specify parameter types and return type.

### Function Declaration

```forg
fn function_name(param1: type1, param2: type2) -> return_type {
    // Function body
    return value;
}
```

### Examples

```forg
// Function with no parameters
fn get_answer() -> int {
    return 42;
}

// Function with parameters
fn add(a: int, b: int) -> int {
    return a + b;
}

// Function with no return value
fn greet(name: str) -> void {
    printf("Hello, %s!\n", name);
}

// Recursive function
fn factorial(n: int) -> int {
    if n <= 1 {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
```

### Function Calls

```forg
let result: int = add(5, 3);
greet("World");
let fact: int = factorial(5);
```

### The Main Function

Every program must have a `main` function:

```forg
fn main() -> int {
    // Program entry point
    return 0;  // Exit code
}
```

## Control Flow

Forg provides standard control flow constructs.

### If Statements

```forg
if condition {
    // Code executed if condition is true
}

if condition {
    // True branch
} else {
    // False branch
}
```

Example:
```forg
let age: int = 18;

if age >= 18 {
    printf("You are an adult\n");
} else {
    printf("You are a minor\n");
}
```

### While Loops

```forg
while condition {
    // Code executed while condition is true
}
```

Example:
```forg
let count: int = 0;
while count < 5 {
    printf("Count: %i\n", count);
    count = count + 1;
}
```

### For Loops

```forg
for (initialization; condition; update) {
    // Loop body
}
```

Example:
```forg
for (let i: int = 0; i < 10; i = i + 1) {
    printf("i = %i\n", i);
}
```

### Break and Continue

```forg
// Break - exit the loop immediately
for (let i: int = 0; i < 10; i = i + 1) {
    if i == 5 {
        break;
    }
    printf("%i ", i);
}

// Continue - skip to next iteration
for (let i: int = 0; i < 10; i = i + 1) {
    if i % 2 == 0 {
        continue;
    }
    printf("%i ", i);  // Only prints odd numbers
}
```

## Operators

### Arithmetic Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Addition | `a + b` |
| `-` | Subtraction | `a - b` |
| `*` | Multiplication | `a * b` |
| `/` | Division | `a / b` |
| `%` | Modulus | `a % b` |
| `^` | Exponentiation | `a ^ b` |

### Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `==` | Equal to | `a == b` |
| `!=` | Not equal to | `a != b` |
| `<` | Less than | `a < b` |
| `>` | Greater than | `a > b` |
| `<=` | Less than or equal | `a <= b` |
| `>=` | Greater than or equal | `a >= b` |

### Assignment Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Assignment | `a = b` |

### Operator Precedence

From highest to lowest precedence:

1. Function calls
2. Exponentiation (`^`)
3. Multiplication, Division, Modulus (`*`, `/`, `%`)
4. Addition, Subtraction (`+`, `-`)
5. Comparison (`<`, `>`, `<=`, `>=`)
6. Equality (`==`, `!=`)
7. Assignment (`=`)

Use parentheses to override precedence:
```forg
let result: int = (a + b) * c;  // Addition happens first
```

## Built-in Functions

### printf

Formatted output function (similar to C's printf):

```forg
printf(format_string, arguments...);
```

**Format Specifiers**:
- `%i` - Integer
- `%f` - Float
- `%s` - String
- `%%` - Literal %
- `\n` - Newline

Examples:
```forg
printf("Hello, World!\n");
printf("Number: %i\n", 42);
printf("Pi: %f\n", 3.14159);
printf("Name: %s, Age: %i\n", "Alice", 25);
```

## Comments

Single-line comments start with `//` and continue to the end of the line:

```forg
// This is a comment
let x: int = 42; // Comment at end of line

// Multi-line comments can be created
// by using multiple single-line comments
```

## Keywords

The following words are reserved keywords in Forg:

- `fn` - Function declaration
- `let` - Variable declaration
- `return` - Return statement
- `if` - Conditional statement
- `else` - Alternative branch
- `while` - While loop
- `for` - For loop
- `break` - Break statement
- `continue` - Continue statement
- `true` - Boolean literal
- `false` - Boolean literal

### Type Keywords

- `int` - Integer type
- `float` - Float type
- `bool` - Boolean type
- `str` - String type
- `void` - Void type

## Grammar

This section provides the formal grammar for Forg in EBNF notation.

### Lexical Elements

```ebnf
Program = { Statement } ;

Statement = LetStatement
          | FunctionStatement
          | ReturnStatement
          | ExpressionStatement
          | BlockStatement
          | IfStatement
          | WhileStatement
          | ForStatement
          | BreakStatement
          | ContinueStatement
          | AssignStatement ;

LetStatement = "let" Identifier ":" Type "=" Expression ";" ;

FunctionStatement = "fn" Identifier "(" [ ParameterList ] ")" "->" Type BlockStatement ;

ParameterList = Parameter { "," Parameter } ;

Parameter = Identifier ":" Type ;

ReturnStatement = "return" [ Expression ] ";" ;

IfStatement = "if" Expression BlockStatement [ "else" BlockStatement ] ;

WhileStatement = "while" Expression BlockStatement ;

ForStatement = "for" "(" LetStatement Expression ";" AssignStatement ")" BlockStatement ;

BreakStatement = "break" ";" ;

ContinueStatement = "continue" ";" ;

AssignStatement = Identifier "=" Expression ";" ;

BlockStatement = "{" { Statement } "}" ;

ExpressionStatement = Expression ";" ;

Expression = OrExpression ;

OrExpression = AndExpression { "||" AndExpression } ;

AndExpression = EqualityExpression { "&&" EqualityExpression } ;

EqualityExpression = RelationalExpression { ( "==" | "!=" ) RelationalExpression } ;

RelationalExpression = AdditiveExpression { ( "<" | ">" | "<=" | ">=" ) AdditiveExpression } ;

AdditiveExpression = MultiplicativeExpression { ( "+" | "-" ) MultiplicativeExpression } ;

MultiplicativeExpression = ExponentiationExpression { ( "*" | "/" | "%" ) ExponentiationExpression } ;

ExponentiationExpression = UnaryExpression { "^" UnaryExpression } ;

UnaryExpression = ( "!" | "-" ) UnaryExpression
                | CallExpression ;

CallExpression = PrimaryExpression { "(" [ ArgumentList ] ")" } ;

ArgumentList = Expression { "," Expression } ;

PrimaryExpression = Identifier
                  | IntegerLiteral
                  | FloatLiteral
                  | StringLiteral
                  | BooleanLiteral
                  | "(" Expression ")" ;

Type = "int" | "float" | "bool" | "str" | "void" ;

Identifier = Letter { Letter | Digit | "_" } ;

IntegerLiteral = Digit { Digit } ;

FloatLiteral = Digit { Digit } "." Digit { Digit } ;

StringLiteral = '"' { Character } '"' ;

BooleanLiteral = "true" | "false" ;

Letter = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;

Digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
```

## Error Handling

Forg provides comprehensive error reporting:

### Compile-Time Errors

- **Lexical Errors**: Invalid tokens, malformed numbers
- **Syntax Errors**: Invalid grammar, missing tokens
- **Semantic Errors**: Type mismatches, undefined variables

### Example Error Messages

```
Syntax Error at example.forg:Line 5: Expected next token to be SEMICOLON, got IDENT instead.

Semantic Error at example.forg:Line 8: Identifier 'undefined_var' has not been declared.

Type Error at example.forg:Line 12: Cannot assign float to int variable.
```

## Best Practices

1. **Use Descriptive Names**: Choose clear, meaningful variable and function names
2. **Consistent Formatting**: Use consistent indentation and spacing
3. **Comment Your Code**: Explain complex logic with comments
4. **Type Safety**: Leverage the type system to catch errors early
5. **Error Handling**: Check for potential runtime errors
6. **Function Design**: Keep functions focused and single-purpose

## Examples

### Complete Program Examples

**Fibonacci Sequence**:
```forg
fn fibonacci(n: int) -> int {
    if n <= 1 {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

fn main() -> int {
    for (let i: int = 0; i < 10; i = i + 1) {
        printf("fib(%i) = %i\n", i, fibonacci(i));
    }
    return 0;
}
```

**Prime Number Checker**:
```forg
fn is_prime(n: int) -> bool {
    if n <= 1 {
        return false;
    }
    
    for (let i: int = 2; i * i <= n; i = i + 1) {
        if n % i == 0 {
            return false;
        }
    }
    
    return true;
}

fn main() -> int {
    for (let i: int = 2; i <= 20; i = i + 1) {
        if is_prime(i) {
            printf("%i is prime\n", i);
        }
    }
    return 0;
}
```

---

**Next**: [Compiler Architecture](architecture.md)
**Previous**: [Getting Started](getting-started.md)
