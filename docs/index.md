# Forg Language Compiler Documentation

Welcome to the Forg Language Compiler documentation! Forg is a modern, statically-typed programming language that compiles to LLVM IR for high-performance execution.

## Table of Contents

1. [Getting Started](getting-started.md)
2. [Language Reference](language-reference.md)
3. [Compiler Architecture](architecture.md)
4. [API Reference](api-reference.md)
5. [Examples and Tutorials](examples.md)
6. [Development Guide](development.md)
7. [Performance Guide](performance.md)
8. [Troubleshooting](troubleshooting.md)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Compile and run a Forg program
python main.py examples/hello.forg

# Run with debug output
python main.py --debug-all examples/factorial.forg
```

## Language Overview

Forg is designed to be:
- **Fast**: Compiles to optimized LLVM IR
- **Safe**: Static typing prevents many runtime errors
- **Simple**: Clean, readable syntax
- **Powerful**: Rich feature set including functions, loops, and conditionals

### Example Program

```forg
fn factorial(n: int) -> int {
    if n <= 1 {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

fn main() -> int {
    let result: int = factorial(5);
    printf("5! = %i\n", result);
    return result;
}
```

## Features

- ✅ **Data Types**: `int`, `float`, `bool`, `str`, `void`
- ✅ **Control Flow**: `if`/`else`, `while`, `for` loops
- ✅ **Functions**: First-class functions with parameters and return types
- ✅ **Operators**: Arithmetic, comparison, and assignment operators
- ✅ **Built-ins**: `printf` for formatted output
- ✅ **Comments**: Single-line comments with `//`
- ✅ **Error Handling**: Comprehensive error messages
- ✅ **Debugging**: Multiple debug modes and performance profiling

## Architecture

The Forg compiler follows a traditional compilation pipeline:

```
Source Code → Lexer → Parser → Compiler → LLVM IR → JIT Execution
```

Each stage is modular and can be used independently for analysis or debugging.

## Contributing

We welcome contributions! Please see our [Development Guide](development.md) for details on:
- Setting up the development environment
- Code style guidelines
- Testing procedures
- Submitting pull requests

## License

This project is open source. See the main README for license details.

---

**Next**: [Getting Started Guide](getting-started.md)
