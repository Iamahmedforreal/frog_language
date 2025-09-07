# Examples and Tutorials

This document provides comprehensive examples and step-by-step tutorials for learning and using the Forg programming language.

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [Language Features](#language-features)
3. [Advanced Examples](#advanced-examples)
4. [Tutorials](#tutorials)
5. [Common Patterns](#common-patterns)
6. [Best Practices](#best-practices)

## Basic Examples

### Hello World

The simplest Forg program:

```forg
fn main() -> int {
    printf("Hello, World!\n");
    return 0;
}
```

**To run**:
```bash
python main.py hello.forg
```

### Variables and Types

```forg
fn main() -> int {
    // Integer variables
    let age: int = 25;
    let year: int = 2024;
    
    // Float variables
    let pi: float = 3.14159;
    let temperature: float = -5.5;
    
    // Boolean variables
    let is_student: bool = true;
    let has_license: bool = false;
    
    // String variables
    let name: str = "Alice";
    let greeting: str = "Hello there!";
    
    // Print all variables
    printf("Name: %s\n", name);
    printf("Age: %i years\n", age);
    printf("Pi: %f\n", pi);
    printf("Student: %i\n", is_student);
    
    return 0;
}
```

### Basic Arithmetic

```forg
fn main() -> int {
    let a: int = 10;
    let b: int = 3;
    
    printf("a = %i, b = %i\n", a, b);
    printf("a + b = %i\n", a + b);
    printf("a - b = %i\n", a - b);
    printf("a * b = %i\n", a * b);
    printf("a / b = %i\n", a / b);
    printf("a %% b = %i\n", a % b);
    printf("a ^ b = %i\n", a ^ b);  // Power operation
    
    return 0;
}
```

## Language Features

### Functions

#### Simple Function

```forg
fn greet(name: str) -> void {
    printf("Hello, %s!\n", name);
}

fn main() -> int {
    greet("World");
    greet("Alice");
    return 0;
}
```

#### Function with Return Value

```forg
fn add(x: int, y: int) -> int {
    return x + y;
}

fn multiply(x: int, y: int) -> int {
    let result: int = x * y;
    return result;
}

fn main() -> int {
    let sum: int = add(5, 3);
    let product: int = multiply(4, 7);
    
    printf("5 + 3 = %i\n", sum);
    printf("4 * 7 = %i\n", product);
    
    return 0;
}
```

#### Recursive Functions

```forg
fn factorial(n: int) -> int {
    if n <= 1 {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

fn fibonacci(n: int) -> int {
    if n <= 1 {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

fn main() -> int {
    printf("Factorials:\n");
    for (let i: int = 1; i <= 5; i = i + 1) {
        printf("%i! = %i\n", i, factorial(i));
    }
    
    printf("\nFibonacci sequence:\n");
    for (let i: int = 0; i < 8; i = i + 1) {
        printf("F(%i) = %i\n", i, fibonacci(i));
    }
    
    return 0;
}
```

### Control Flow

#### If-Else Statements

```forg
fn check_number(n: int) -> void {
    if n > 0 {
        printf("%i is positive\n", n);
    } else {
        if n < 0 {
            printf("%i is negative\n", n);
        } else {
            printf("%i is zero\n", n);
        }
    }
}

fn main() -> int {
    check_number(10);
    check_number(-5);
    check_number(0);
    return 0;
}
```

#### While Loops

```forg
fn countdown(from: int) -> void {
    let count: int = from;
    
    while count > 0 {
        printf("%i... ", count);
        count = count - 1;
    }
    
    printf("Blast off!\n");
}

fn main() -> int {
    countdown(5);
    return 0;
}
```

#### For Loops

```forg
fn print_multiplication_table(n: int) -> void {
    printf("Multiplication table for %i:\n", n);
    
    for (let i: int = 1; i <= 10; i = i + 1) {
        printf("%i x %i = %i\n", n, i, n * i);
    }
}

fn main() -> int {
    print_multiplication_table(7);
    return 0;
}
```

#### Break and Continue

```forg
fn find_first_multiple(base: int, target: int) -> int {
    for (let i: int = 1; i <= 100; i = i + 1) {
        let product: int = base * i;
        
        if product % 2 != 0 {
            continue;  // Skip odd numbers
        }
        
        if product >= target {
            printf("First even multiple >= %i is %i\n", target, product);
            break;
        }
    }
    
    return 0;
}

fn main() -> int {
    find_first_multiple(3, 20);
    return 0;
}
```

## Advanced Examples

### Mathematical Algorithms

#### Prime Number Checker

```forg
fn is_prime(n: int) -> bool {
    if n <= 1 {
        return false;
    }
    
    if n <= 3 {
        return true;
    }
    
    if n % 2 == 0 {
        return false;
    }
    
    for (let i: int = 3; i * i <= n; i = i + 2) {
        if n % i == 0 {
            return false;
        }
    }
    
    return true;
}

fn find_primes(limit: int) -> void {
    printf("Prime numbers up to %i:\n", limit);
    
    for (let i: int = 2; i <= limit; i = i + 1) {
        if is_prime(i) {
            printf("%i ", i);
        }
    }
    
    printf("\n");
}

fn main() -> int {
    find_primes(50);
    return 0;
}
```

#### Greatest Common Divisor (GCD)

```forg
fn gcd(a: int, b: int) -> int {
    while b != 0 {
        let temp: int = b;
        b = a % b;
        a = temp;
    }
    return a;
}

fn lcm(a: int, b: int) -> int {
    return (a * b) / gcd(a, b);
}

fn main() -> int {
    let x: int = 48;
    let y: int = 18;
    
    printf("GCD(%i, %i) = %i\n", x, y, gcd(x, y));
    printf("LCM(%i, %i) = %i\n", x, y, lcm(x, y));
    
    return 0;
}
```

### Data Processing

#### Array Simulation (Using Variables)

```forg
fn bubble_sort_demo() -> void {
    // Simulate a small array using individual variables
    let a: int = 64;
    let b: int = 34;
    let c: int = 25;
    let d: int = 12;
    let e: int = 22;
    
    printf("Original: %i %i %i %i %i\n", a, b, c, d, e);
    
    // Manual bubble sort for 5 elements
    // Pass 1
    if a > b { let temp: int = a; a = b; b = temp; }
    if b > c { let temp: int = b; b = c; c = temp; }
    if c > d { let temp: int = c; c = d; d = temp; }
    if d > e { let temp: int = d; d = e; e = temp; }
    
    // Pass 2
    if a > b { let temp: int = a; a = b; b = temp; }
    if b > c { let temp: int = b; b = c; c = temp; }
    if c > d { let temp: int = c; c = d; d = temp; }
    
    // Pass 3
    if a > b { let temp: int = a; a = b; b = temp; }
    if b > c { let temp: int = b; b = c; c = temp; }
    
    // Pass 4
    if a > b { let temp: int = a; a = b; b = temp; }
    
    printf("Sorted:   %i %i %i %i %i\n", a, b, c, d, e);
}

fn main() -> int {
    bubble_sort_demo();
    return 0;
}
```

#### Number Pattern Generation

```forg
fn print_triangle(height: int) -> void {
    for (let i: int = 1; i <= height; i = i + 1) {
        // Print spaces
        for (let j: int = 1; j <= height - i; j = j + 1) {
            printf(" ");
        }
        
        // Print numbers
        for (let k: int = 1; k <= i; k = k + 1) {
            printf("%i ", k);
        }
        
        printf("\n");
    }
}

fn print_pascal_triangle(rows: int) -> void {
    for (let i: int = 0; i < rows; i = i + 1) {
        // Print spaces
        for (let j: int = 0; j < rows - i - 1; j = j + 1) {
            printf(" ");
        }
        
        let val: int = 1;
        for (let j: int = 0; j <= i; j = j + 1) {
            printf("%i ", val);
            val = val * (i - j) / (j + 1);
        }
        
        printf("\n");
    }
}

fn main() -> int {
    printf("Number Triangle:\n");
    print_triangle(5);
    
    printf("\nPascal's Triangle:\n");
    print_pascal_triangle(6);
    
    return 0;
}
```

## Tutorials

### Tutorial 1: Building a Calculator

Let's build a simple calculator step by step.

#### Step 1: Basic Operations

```forg
fn add(a: float, b: float) -> float {
    return a + b;
}

fn subtract(a: float, b: float) -> float {
    return a - b;
}

fn multiply(a: float, b: float) -> float {
    return a * b;
}

fn divide(a: float, b: float) -> float {
    if b == 0.0 {
        printf("Error: Division by zero!\n");
        return 0.0;
    }
    return a / b;
}

fn main() -> int {
    let x: float = 10.5;
    let y: float = 3.2;
    
    printf("Calculator Demo\n");
    printf("===============\n");
    printf("x = %f, y = %f\n", x, y);
    printf("x + y = %f\n", add(x, y));
    printf("x - y = %f\n", subtract(x, y));
    printf("x * y = %f\n", multiply(x, y));
    printf("x / y = %f\n", divide(x, y));
    
    return 0;
}
```

#### Step 2: Advanced Operations

```forg
fn power(base: float, exponent: int) -> float {
    let result: float = 1.0;
    
    for (let i: int = 0; i < exponent; i = i + 1) {
        result = result * base;
    }
    
    return result;
}

fn square_root(n: float) -> float {
    // Newton's method for square root
    let guess: float = n / 2.0;
    let epsilon: float = 0.0001;
    
    for (let i: int = 0; i < 10; i = i + 1) {
        let new_guess: float = (guess + n / guess) / 2.0;
        
        if new_guess - guess < epsilon && guess - new_guess < epsilon {
            break;
        }
        
        guess = new_guess;
    }
    
    return guess;
}

fn factorial_float(n: int) -> float {
    let result: float = 1.0;
    
    for (let i: int = 1; i <= n; i = i + 1) {
        result = result * i;  // Will be converted to float
    }
    
    return result;
}

fn main() -> int {
    let base: float = 2.5;
    let exp: int = 3;
    let num: float = 16.0;
    
    printf("Advanced Calculator\n");
    printf("===================\n");
    printf("%f ^ %i = %f\n", base, exp, power(base, exp));
    printf("sqrt(%f) = %f\n", num, square_root(num));
    printf("5! = %f\n", factorial_float(5));
    
    return 0;
}
```

### Tutorial 2: Text Processing

#### Character and String Analysis

```forg
fn count_vowels(text: str) -> int {
    // This is a simplified version since we don't have full string operations
    // In a real implementation, you'd iterate through the string
    printf("Analyzing text: %s\n", text);
    printf("(Vowel counting not fully implemented without string indexing)\n");
    return 0;
}

fn is_palindrome_number(n: int) -> bool {
    let original: int = n;
    let reversed: int = 0;
    
    while n > 0 {
        reversed = reversed * 10 + n % 10;
        n = n / 10;
    }
    
    return original == reversed;
}

fn main() -> int {
    printf("Text Processing Demo\n");
    printf("====================\n");
    
    // Test palindrome numbers
    let numbers: int = 121;
    if is_palindrome_number(numbers) {
        printf("%i is a palindrome\n", numbers);
    } else {
        printf("%i is not a palindrome\n", numbers);
    }
    
    let numbers2: int = 123;
    if is_palindrome_number(numbers2) {
        printf("%i is a palindrome\n", numbers2);
    } else {
        printf("%i is not a palindrome\n", numbers2);
    }
    
    return 0;
}
```

### Tutorial 3: Game Logic

#### Simple Number Guessing Game Logic

```forg
fn linear_congruential_generator(seed: int) -> int {
    // Simple pseudo-random number generator
    return (1103515245 * seed + 12345) % 2147483647;
}

fn simulate_guessing_game() -> void {
    let secret: int = 42;  // In a real game, this would be random
    let max_attempts: int = 5;
    
    printf("Number Guessing Game Simulation\n");
    printf("===============================\n");
    printf("I'm thinking of a number between 1 and 100\n");
    printf("You have %i attempts to guess it!\n", max_attempts);
    
    // Simulate some guesses
    let guesses: int = 25;  // First guess
    
    for (let attempt: int = 1; attempt <= max_attempts; attempt = attempt + 1) {
        printf("Attempt %i: %i\n", attempt, guesses);
        
        if guesses == secret {
            printf("Congratulations! You found it in %i attempts!\n", attempt);
            return;
        } else {
            if guesses < secret {
                printf("Too low! Try higher.\n");
                guesses = guesses + 10;  // Simulate strategy
            } else {
                printf("Too high! Try lower.\n");
                guesses = guesses - 5;   // Simulate strategy
            }
        }
    }
    
    printf("Game over! The number was %i\n", secret);
}

fn main() -> int {
    simulate_guessing_game();
    return 0;
}
```

## Common Patterns

### Input Validation Pattern

```forg
fn validate_positive_integer(n: int) -> bool {
    return n > 0;
}

fn safe_divide(a: int, b: int) -> int {
    if b == 0 {
        printf("Error: Cannot divide by zero\n");
        return 0;
    }
    return a / b;
}

fn process_age(age: int) -> void {
    if !validate_positive_integer(age) {
        printf("Error: Age must be positive\n");
        return;
    }
    
    if age < 18 {
        printf("Minor: %i years old\n", age);
    } else {
        printf("Adult: %i years old\n", age);
    }
}

fn main() -> int {
    process_age(25);
    process_age(-5);
    process_age(0);
    
    printf("10 / 2 = %i\n", safe_divide(10, 2));
    printf("10 / 0 = %i\n", safe_divide(10, 0));
    
    return 0;
}
```

### Counter Pattern

```forg
fn count_occurrences(start: int, end: int, target: int) -> int {
    let count: int = 0;
    
    for (let i: int = start; i <= end; i = i + 1) {
        if i == target {
            count = count + 1;
        }
    }
    
    return count;
}

fn count_digits(n: int) -> int {
    if n == 0 {
        return 1;
    }
    
    let count: int = 0;
    
    while n > 0 {
        count = count + 1;
        n = n / 10;
    }
    
    return count;
}

fn main() -> int {
    printf("Digit count of 12345: %i\n", count_digits(12345));
    printf("Digit count of 0: %i\n", count_digits(0));
    
    return 0;
}
```

### Accumulator Pattern

```forg
fn sum_range(start: int, end: int) -> int {
    let sum: int = 0;
    
    for (let i: int = start; i <= end; i = i + 1) {
        sum = sum + i;
    }
    
    return sum;
}

fn sum_even_numbers(limit: int) -> int {
    let sum: int = 0;
    
    for (let i: int = 2; i <= limit; i = i + 2) {
        sum = sum + i;
    }
    
    return sum;
}

fn product_range(start: int, end: int) -> int {
    let product: int = 1;
    
    for (let i: int = start; i <= end; i = i + 1) {
        product = product * i;
    }
    
    return product;
}

fn main() -> int {
    printf("Sum 1 to 10: %i\n", sum_range(1, 10));
    printf("Sum even numbers up to 20: %i\n", sum_even_numbers(20));
    printf("Product 3 to 6: %i\n", product_range(3, 6));
    
    return 0;
}
```

## Best Practices

### 1. Function Design

**Good**: Small, focused functions
```forg
fn is_even(n: int) -> bool {
    return n % 2 == 0;
}

fn is_odd(n: int) -> bool {
    return !is_even(n);
}
```

**Avoid**: Large, complex functions
```forg
// Avoid this - too many responsibilities
fn process_number_badly(n: int) -> void {
    // Check if even
    // Check if prime
    // Print results
    // Calculate factorial
    // etc.
}
```

### 2. Variable Naming

**Good**: Descriptive names
```forg
fn calculate_area(width: int, height: int) -> int {
    let area: int = width * height;
    return area;
}
```

**Avoid**: Cryptic names
```forg
fn calc(w: int, h: int) -> int {
    let a: int = w * h;
    return a;
}
```

### 3. Error Handling

**Good**: Check for errors
```forg
fn safe_factorial(n: int) -> int {
    if n < 0 {
        printf("Error: Factorial not defined for negative numbers\n");
        return 0;
    }
    
    if n == 0 {
        return 1;
    }
    
    return n * safe_factorial(n - 1);
}
```

### 4. Code Organization

**Good**: Logical grouping
```forg
// Math utilities
fn add(a: int, b: int) -> int { return a + b; }
fn multiply(a: int, b: int) -> int { return a * b; }

// String utilities
fn print_header(title: str) -> void {
    printf("=== %s ===\n", title);
}

// Main program
fn main() -> int {
    print_header("Calculator");
    printf("2 + 3 = %i\n", add(2, 3));
    return 0;
}
```

### 5. Comments

**Good**: Explain why, not what
```forg
fn fibonacci_iterative(n: int) -> int {
    // Use iterative approach to avoid stack overflow for large n
    if n <= 1 {
        return n;
    }
    
    let prev: int = 0;
    let curr: int = 1;
    
    for (let i: int = 2; i <= n; i = i + 1) {
        let next: int = prev + curr;
        prev = curr;
        curr = next;
    }
    
    return curr;
}
```

---

**Next**: [Development Guide](development.md)
**Previous**: [API Reference](api-reference.md)
