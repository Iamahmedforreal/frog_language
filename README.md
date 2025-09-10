# 🚀 Forg Language Compiler

A modern, feature-rich compiler for the **Forg** programming language that compiles to LLVM IR with Just-In-Time (JIT) execution capabilities.

[![Language](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org)
[![LLVM](https://img.shields.io/badge/Backend-LLVM-green.svg)](https://llvm.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage Examples](#-usage-examples)
- [Language Features](#-language-features)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

Forg is a statically-typed programming language with a clean syntax that compiles to efficient LLVM IR. The compiler is built in Python and features a complete compilation pipeline from lexical analysis to code generation with JIT execution.

### Key Highlights

- 🔧 **Complete Compiler Pipeline**: Lexer → Parser → AST → LLVM IR → JIT Execution
- ⚡ **High Performance**: LLVM-backed code generation with near-native execution speed
- 🛡️ **Type Safety**: Static typing with comprehensive type checking
- 🔍 **Advanced Debugging**: Rich debug output for every compilation phase
- 📊 **Performance Monitoring**: Built-in benchmarking and profiling tools
- 🧪 **Comprehensive Testing**: Unit tests, integration tests, and performance tests
- 📚 **Extensive Documentation**: Complete guides from beginner to advanced topics

## ✨ Features

### Language Features
- **Static Typing**: All variables and functions are statically typed
- **Functions**: First-class functions with parameters and return types
- **Control Flow**: `if/else`, `while`, `for` loops with `break/continue`
- **Recursion**: Proper support for recursive function calls
- **Operators**: Arithmetic (`+`, `-`, `*`, `/`, `^`), comparison, and logical operators
- **Built-ins**: `printf` for formatted output
- **Comments**: Single-line comments with `//`

### Compiler Features
- **Multi-phase Compilation**: Separate lexical, syntax, and semantic analysis
- **Advanced Error Handling**: Detailed error messages with suggestions
- **LLVM Integration**: Direct compilation to optimized LLVM IR
- **JIT Execution**: Immediate program execution via LLVM JIT
- **Debug Support**: Comprehensive debugging output for all phases
- **Performance Profiling**: Built-in timing and memory monitoring

### Development Features
- **Rich CLI**: Comprehensive command-line interface with multiple options
- **Test Framework**: Custom test runner with detailed reporting
- **Documentation**: Complete API and user documentation
- **Build System**: Makefile with common development tasks
- **Cross-platform**: Support for Windows, Linux, and macOS

## 🚀 Quick Start

### 1. Clone and Install
```bash
git clone <repository-url>
cd compiler
pip install -r requirements.txt
```

### 2. Run Your First Program
```bash
# Compile and run a simple program
python main.py tests/test1.forg

# Output:
# Forg Language Compiler
# Input: tests/test1.forg
# Parser processed 4 statements
# Compilation to LLVM IR successful
# 
# Program executed successfully
#   Return value: 62
```

### 3. Try Advanced Features
```bash
# Enable debug output to see compilation phases
python main.py --debug-all tests/test_factorial.forg

# Run with benchmarking
python main.py --benchmark tests/test3.forg

# Compile without running
python main.py --no-run tests/test2.forg
```

## 📦 Installation

### Prerequisites
- **Python 3.8+** with pip
- **LLVM 14+** (automatically installed via llvmlite)

### Basic Installation
```bash
# Install core dependencies
pip install -r requirements.txt
```

### Development Installation
```bash
# Install with development tools
make dev-setup

# Or manually:
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

### Package Installation
```bash
# Install as a Python package
pip install -e .

# Now you can use forg command anywhere
forg tests/test1.forg
```

## 💡 Usage Examples

### Command Line Options

```bash
# Basic compilation and execution
python main.py program.forg

# Debug specific phases
python main.py --debug-lexer program.forg      # Show lexer tokens
python main.py --debug-parser program.forg     # Save AST to debug/ast.json
python main.py --debug-compiler program.forg   # Save IR to debug/ir.ll
python main.py --debug-all program.forg        # Enable all debug output

# Compilation options
python main.py --no-run program.forg           # Compile only, don't execute
python main.py -O 2 program.forg               # Enable optimizations
python main.py --benchmark program.forg        # Show performance metrics

# Output control
python main.py -v program.forg                 # Verbose output
python main.py -q program.forg                 # Quiet mode (errors only)
```

### Makefile Commands

```bash
make help          # Show all available commands
make run           # Run with default test file
make debug         # Run with full debug output
make test          # Run comprehensive test suite
make clean         # Clean generated files
make benchmark     # Run performance tests
```

## 📝 Language Features

### Hello World
```forg
fn main() -> int {
    printf("Hello, World!\n");
    return 0;
}
```

### Variables and Basic Operations
```forg
fn main() -> int {
    let x: int = 5;
    let y: int = 10;
    let sum: int = x + y;
    
    printf("Sum: %i\n", sum);
    return sum;
}
```

### Functions and Recursion
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

### Control Flow
```forg
fn main() -> int {
    let i: int = 0;
    
    while i < 10 {
        if i % 2 == 0 {
            printf("Even: %i\n", i);
        } else {
            printf("Odd: %i\n", i);
        }
        i = i + 1;
    }
    
    return i;
}
```

### Advanced Features
```forg
fn power(base: int, exp: int) -> int {
    if exp == 0 {
        return 1;
    }
    return base * power(base, exp - 1);
}

fn main() -> int {
    // Using the power operator
    let result1: int = 2 ^ 8;
    
    // Using recursive function
    let result2: int = power(2, 8);
    
    printf("2^8 = %i (operator)\n", result1);
    printf("2^8 = %i (function)\n", result2);
    
    return result1;
}
```

## 📁 Project Structure

```
compiler/
├── 📄 Core Files
│   ├── main.py              # Main compiler entry point
│   ├── lexer.py             # Lexical analysis
│   ├── parser.py            # Syntax analysis
│   ├── compiler.py          # Code generation
│   ├── AST.py               # Abstract syntax tree definitions
│   └── Envorment.py         # Environment and symbol table
│
├── 🛠️ Support Files
│   ├── config.py            # Configuration management
│   ├── error_handler.py     # Error handling system
│   ├── performance.py       # Performance monitoring
│   ├── test_runner.py       # Test framework
│   └── custome_token.py     # Token definitions
│
├── 🧪 Tests
│   ├── tests/               # Test programs (.forg files)
│   │   ├── test1.forg       # Basic arithmetic
│   │   ├── test2.forg       # Variable declarations
│   │   ├── test3.forg       # Functions and loops
│   │   ├── test4.forg       # Complex programs
│   │   ├── test_factorial.forg  # Recursion example
│   │   ├── test_power.forg  # Power operator
│   │   └── test_complex.forg    # Advanced features
│
├── 📚 Documentation
│   ├── docs/                # Comprehensive documentation
│   ├── DOCUMENTATION.md     # Documentation index
│   └── PROJECT_SUMMARY.md   # Detailed project summary
│
├── 🔧 Development
│   ├── Makefile             # Build automation
│   ├── requirements.txt     # Dependencies
│   ├── setup.py             # Package configuration
│   ├── debug/               # Debug output directory
│   └── output/              # Compilation output
```

## 🔧 Development

### Running Tests
```bash
# Run all tests
make test

# Run specific test types
make test-unit          # Unit tests only
make test-files         # Integration tests

# Run individual test files
python main.py tests/test_factorial.forg
```

### Code Quality
```bash
# Format code
make format

# Lint code
make lint

# Type checking (if mypy installed)
mypy *.py
```

### Adding New Features

1. **Language Features**: Modify `lexer.py`, `parser.py`, and `AST.py`
2. **Code Generation**: Update `compiler.py`
3. **Testing**: Add test cases in `tests/` directory
4. **Documentation**: Update relevant docs in `docs/`

### Debug Output

The compiler provides detailed debug information:

```bash
# View lexer tokens
python main.py --debug-lexer tests/test1.forg

# Examine AST structure (saved to debug/ast.json)
python main.py --debug-parser tests/test1.forg

# Inspect LLVM IR (saved to debug/ir.ll)
python main.py --debug-compiler tests/test1.forg
```

## 📚 Documentation

### Available Documentation
- **[Getting Started Guide](docs/getting-started.md)** - Installation and first steps
- **[Language Reference](docs/language-reference.md)** - Complete syntax guide
- **[Compiler Architecture](docs/architecture.md)** - Internal design
- **[API Reference](docs/api-reference.md)** - Detailed API docs
- **[Examples and Tutorials](docs/examples.md)** - Learning resources
- **[Development Guide](docs/development.md)** - Contributing guide
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues

### Quick Links
- 📖 **New Users**: Start with [Getting Started](docs/getting-started.md)
- 🔧 **Developers**: Check [Development Guide](docs/development.md)
- 🐛 **Issues**: See [Troubleshooting](docs/troubleshooting.md)
- 📋 **Reference**: Browse [Language Reference](docs/language-reference.md)

## 🧪 Testing

### Test Categories

1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Full compilation pipeline
3. **Performance Tests**: Benchmarking and profiling
4. **File Tests**: Real Forg program compilation

### Running Tests

```bash
# Comprehensive test suite
python test_runner.py

# Quick integration test
make test-files

# Performance benchmarking
make benchmark
```

### Test Files

| File | Description | Features Tested |
|------|-------------|-----------------|
| `test1.forg` | Basic arithmetic | Variables, expressions |
| `test2.forg` | Function calls | Function definition, calls |
| `test3.forg` | Control flow | While loops, printf |
| `test4.forg` | Complex logic | Multiple functions |
| `test_factorial.forg` | Recursion | Recursive functions |
| `test_power.forg` | Operators | Power operator |
| `test_complex.forg` | Advanced | All language features |

## 🚀 Performance

### Benchmarking

```bash
# Benchmark specific programs
python main.py --benchmark tests/test_factorial.forg

# Performance test suite
python performance.py

# Memory profiling (if memory-profiler installed)
python -m memory_profiler main.py tests/test_complex.forg
```

### Performance Characteristics

- **Compilation Speed**: ~1-10ms for typical programs
- **Execution Speed**: Near-native performance via LLVM JIT
- **Memory Usage**: Minimal overhead, efficient symbol tables
- **Scalability**: Handles programs with thousands of lines

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd compiler

# Set up development environment
make dev-setup

# Run tests to ensure everything works
make test
```

### Contribution Guidelines

1. **Code Style**: Follow PEP 8, use `black` for formatting
2. **Testing**: Add tests for new features
3. **Documentation**: Update docs for user-facing changes
4. **Type Hints**: Use type annotations for all functions
5. **Error Handling**: Use the error handling system for user errors

### Areas for Contribution

- 🔧 **Language Features**: Arrays, structs, modules
- 🚀 **Optimizations**: Advanced LLVM optimizations
- 📚 **Documentation**: Examples, tutorials, guides
- 🧪 **Testing**: More test cases and scenarios
- 🎨 **Tooling**: IDE integration, language server

## 📊 Project Stats

- **Language**: Python 3.8+
- **Backend**: LLVM via llvmlite
- **Test Coverage**: Comprehensive unit and integration tests
- **Documentation**: 100% API documentation coverage
- **Platforms**: Windows, Linux, macOS
- **License**: MIT

## 🎯 Future Roadmap

### Planned Features
- **Arrays and Data Structures**: First-class array support
- **Module System**: Import/export functionality
- **Standard Library**: Built-in functions and utilities
- **IDE Integration**: Language server protocol support
- **Debugger**: Interactive debugging capabilities

### Optimization Goals
- **Multi-pass Compilation**: Separate analysis and generation
- **Advanced Optimizations**: More sophisticated LLVM optimization
- **Incremental Compilation**: Only recompile changed modules
- **Parallel Compilation**: Multi-threaded compilation support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LLVM Project**: For the powerful compilation infrastructure
- **Python Community**: For the excellent development ecosystem
- **Contributors**: Everyone who helped improve this project

## 📞 Support

- 📖 **Documentation**: Check [docs/](docs/) directory
- 🐛 **Bug Reports**: Open an issue on GitHub
- 💡 **Feature Requests**: Start a discussion
- ❓ **Questions**: Check [Troubleshooting Guide](docs/troubleshooting.md)

---

**Happy coding with Forg! 🎉**

Made with ❤️ by the Forg Team
