# Getting Started with Forg

This guide will help you get up and running with the Forg language compiler in just a few minutes.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** installed on your system
- **pip** package manager
- A text editor or IDE of your choice

You can check your Python version with:
```bash
python --version
```

## Installation

### 1. Download the Compiler

Download or clone the Forg compiler to your local machine:

```bash
# If you have git
git clone <repository-url>
cd compiler

# Or download and extract the ZIP file
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

The main dependency is `llvmlite`, which provides LLVM bindings for Python.

### 3. Verify Installation

Test that everything is working by running a simple example:

```bash
python main.py tests/test1.forg
```

You should see output similar to:
```
Forg Language Compiler
Input: tests/test1.forg
Compilation to LLVM IR successful

Program executed successfully
  Return value: 62
No errors or warnings found.
```

## Your First Forg Program

Let's create a simple "Hello, World!" program in Forg.

### 1. Create a New File

Create a file called `hello.forg` with the following content:

```forg
fn main() -> int {
    printf("Hello, World!\n");
    return 0;
}
```

### 2. Compile and Run

Execute your program with:

```bash
python main.py hello.forg
```

You should see:
```
Forg Language Compiler
Input: hello.forg
Compilation to LLVM IR successful
Hello, World!

Program executed successfully
  Return value: 0
No errors or warnings found.
```

## Command-Line Options

The Forg compiler provides several useful command-line options:

### Basic Usage
```bash
python main.py [options] input_file
```

### Common Options

| Option | Description |
|--------|-------------|
| `-h, --help` | Show help message |
| `-o OUTPUT` | Specify output file name |
| `--no-run` | Compile only, don't execute |
| `-v, --verbose` | Enable verbose output |
| `-q, --quiet` | Minimal output (errors only) |

### Debug Options

| Option | Description |
|--------|-------------|
| `--debug-lexer` | Show lexer token output |
| `--debug-parser` | Save AST to `debug/ast.json` |
| `--debug-compiler` | Save LLVM IR to `debug/ir.ll` |
| `--debug-all` | Enable all debug outputs |

### Performance Options

| Option | Description |
|--------|-------------|
| `--benchmark` | Show execution timing |
| `-O {0,1,2,3}` | Set optimization level |

## Examples

Here are some example commands to get you started:

```bash
# Basic compilation and execution
python main.py examples/factorial.forg

# Compile without running
python main.py --no-run examples/fibonacci.forg

# Debug the compilation process
python main.py --debug-all examples/primes.forg

# Benchmark performance
python main.py --benchmark examples/complex.forg

# Quiet mode (minimal output)
python main.py --quiet examples/simple.forg
```

## Project Structure

Understanding the project layout will help you navigate the codebase:

```
compiler/
├── main.py              # Main entry point
├── lexer.py             # Lexical analyzer
├── parser.py            # Syntax analyzer
├── compiler.py          # LLVM IR generator
├── AST.py              # Abstract Syntax Tree definitions
├── custome_token.py    # Token definitions
├── Envorment.py        # Symbol table
├── config.py           # Configuration management
├── error_handler.py    # Error handling
├── test_runner.py      # Test suite
├── performance.py      # Performance monitoring
├── requirements.txt    # Dependencies
├── Makefile           # Build commands
├── tests/             # Example Forg programs
├── debug/             # Debug output
├── docs/              # Documentation
└── output/            # Compiled output
```

## Using Make Commands

If you have `make` available, you can use convenient shortcuts:

```bash
# Show all available commands
make help

# Run with default test file
make run

# Run with debug output
make debug

# Run all tests
make test

# Clean generated files
make clean

# Install dependencies
make install
```

## Development Setup

If you plan to contribute to the compiler or modify it:

```bash
# Install development dependencies
make dev-setup

# Or manually
pip install pytest black flake8 mypy

# Run tests
make test

# Format code
make format

# Check code quality
make lint
```

## Next Steps

Now that you have Forg up and running, you can:

1. **Learn the Language**: Read the [Language Reference](language-reference.md)
2. **Try Examples**: Explore the example programs in the `tests/` directory
3. **Build Something**: Create your own Forg programs
4. **Understand Internals**: Check out the [Architecture Guide](architecture.md)
5. **Contribute**: See the [Development Guide](development.md)

## Troubleshooting

If you encounter issues:

1. **Check Prerequisites**: Ensure Python 3.8+ is installed
2. **Verify Dependencies**: Run `pip install -r requirements.txt` again
3. **Check Permissions**: Ensure you have write permissions for debug output
4. **Read Error Messages**: Forg provides detailed error information
5. **Consult Documentation**: See [Troubleshooting Guide](troubleshooting.md)

## Getting Help

- **Documentation**: Browse the docs in the `docs/` directory
- **Examples**: Check the `tests/` directory for sample programs
- **Issues**: Report bugs or request features through the project's issue tracker
- **Community**: Join discussions and get help from other users

---

**Next**: [Language Reference](language-reference.md)
**Previous**: [Documentation Index](index.md)
