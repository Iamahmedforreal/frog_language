# Troubleshooting Guide

This guide helps you diagnose and resolve common issues when using or developing the Forg compiler.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Compilation Errors](#compilation-errors)
3. [Runtime Errors](#runtime-errors)
4. [Performance Issues](#performance-issues)
5. [Development Issues](#development-issues)
6. [Common Error Messages](#common-error-messages)
7. [Debugging Techniques](#debugging-techniques)
8. [Getting Help](#getting-help)

## Installation Issues

### Python Version Problems

**Problem**: `Python version 3.8+ required`

**Solution**:
```bash
# Check Python version
python --version

# If using an older version, upgrade Python or use pyenv
pyenv install 3.11.0
pyenv local 3.11.0
```

### LLVM Installation Issues

**Problem**: `llvmlite installation failed`

**Solutions**:

1. **Windows**: Install Visual Studio Build Tools
   ```bash
   # Download and install Visual Studio Build Tools
   # Then try installing again
   pip install llvmlite
   ```

2. **Linux**: Install LLVM development packages
   ```bash
   # Ubuntu/Debian
   sudo apt-get install llvm-dev

   # CentOS/RHEL
   sudo yum install llvm-devel

   # Then install llvmlite
   pip install llvmlite
   ```

3. **macOS**: Install LLVM via Homebrew
   ```bash
   brew install llvm
   export LLVM_CONFIG=/usr/local/opt/llvm/bin/llvm-config
   pip install llvmlite
   ```

### Permission Errors

**Problem**: `Permission denied when creating debug files`

**Solution**:
```bash
# Ensure write permissions for debug directory
chmod 755 debug/
mkdir -p debug output

# Or run with elevated permissions (not recommended)
sudo python main.py program.forg
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'llvmlite'`

**Solution**:
```bash
# Verify installation
pip list | grep llvmlite

# Reinstall if necessary
pip uninstall llvmlite
pip install llvmlite

# Check Python path
python -c "import sys; print(sys.path)"
```

## Compilation Errors

### Lexical Errors

#### Invalid Characters

**Error**: `Lexical Error: Invalid character 'ñ' at line 5`

**Solution**: Forg only supports ASCII characters. Replace non-ASCII characters:
```forg
// Bad
let niño: int = 10;

// Good
let nino: int = 10;
```

#### Malformed Numbers

**Error**: `Too many decimals in number`

**Solution**: Check number format:
```forg
// Bad
let pi: float = 3.14.159;

// Good
let pi: float = 3.14159;
```

#### Unterminated Strings

**Error**: `Unterminated string literal`

**Solution**: Ensure strings are properly closed:
```forg
// Bad
let message: str = "Hello, World!;

// Good
let message: str = "Hello, World!";
```

### Syntax Errors

#### Missing Semicolons

**Error**: `Expected next token to be SEMICOLON, got IDENT instead`

**Solution**: Add missing semicolons:
```forg
// Bad
let x: int = 42
let y: int = 24

// Good
let x: int = 42;
let y: int = 24;
```

#### Mismatched Braces

**Error**: `Expected '}' but found EOF`

**Solution**: Check brace matching:
```forg
// Bad
fn main() -> int {
    if true {
        printf("Hello");
    // Missing closing brace

// Good
fn main() -> int {
    if true {
        printf("Hello");
    }
    return 0;
}
```

#### Invalid Function Syntax

**Error**: `Expected function name after 'fn'`

**Solution**: Check function declaration syntax:
```forg
// Bad
fn -> int {
    return 42;
}

// Good
fn get_answer() -> int {
    return 42;
}
```

### Semantic Errors

#### Undefined Variables

**Error**: `Identifier 'x' has not been declared`

**Solution**: Declare variables before use:
```forg
// Bad
fn main() -> int {
    return x + 1;  // x not declared
}

// Good
fn main() -> int {
    let x: int = 42;
    return x + 1;
}
```

#### Type Mismatches

**Error**: `Cannot assign float to int variable`

**Solution**: Ensure type compatibility:
```forg
// Bad
fn main() -> int {
    let x: int = 3.14;  // float assigned to int
    return x;
}

// Good
fn main() -> int {
    let x: float = 3.14;
    let y: int = 3;
    return y;
}
```

#### Function Call Errors

**Error**: `Function 'add' expects 2 arguments, got 1`

**Solution**: Check function signatures:
```forg
fn add(a: int, b: int) -> int {
    return a + b;
}

fn main() -> int {
    // Bad
    // return add(5);

    // Good
    return add(5, 3);
}
```

## Runtime Errors

### LLVM IR Generation Errors

**Error**: `LLVM IR parsing error: expected instruction opcode`

**Common Causes**:
1. Unreachable code blocks
2. Missing return statements
3. Invalid IR structure

**Solution**: Enable compiler debug to inspect IR:
```bash
python main.py --debug-compiler problem.forg
```

Check the generated `debug/ir.ll` file for issues.

### JIT Execution Errors

**Error**: `Execution failed: No 'main' function found`

**Solution**: Ensure your program has a main function:
```forg
// Required
fn main() -> int {
    // Program code here
    return 0;
}
```

### Stack Overflow

**Error**: Program hangs or crashes with deep recursion

**Solution**: 
1. Check for infinite recursion:
```forg
// Bad - infinite recursion
fn bad_factorial(n: int) -> int {
    return n * bad_factorial(n);  // No base case
}

// Good
fn factorial(n: int) -> int {
    if n <= 1 {
        return 1;  // Base case
    }
    return n * factorial(n - 1);
}
```

2. Use iterative approaches for large inputs
3. Increase stack size if necessary

### Division by Zero

**Error**: `Floating point exception` or unexpected results

**Solution**: Add bounds checking:
```forg
fn safe_divide(a: int, b: int) -> int {
    if b == 0 {
        printf("Error: Division by zero!\n");
        return 0;
    }
    return a / b;
}
```

## Performance Issues

### Slow Compilation

**Symptoms**: Compilation takes much longer than expected

**Solutions**:
1. **Profile compilation**:
   ```bash
   python main.py --benchmark slow_program.forg
   ```

2. **Check program size**:
   ```bash
   wc -l slow_program.forg
   ```

3. **Simplify complex expressions**:
   ```forg
   // Avoid deeply nested expressions
   // Break into smaller parts
   ```

### High Memory Usage

**Symptoms**: Compiler uses excessive memory

**Solutions**:
1. **Monitor memory usage**:
   ```bash
   python -m memory_profiler main.py large_program.forg
   ```

2. **Process files in chunks** (for very large programs)
3. **Optimize AST structure** (development)

### Slow Execution

**Symptoms**: Compiled programs run slowly

**Solutions**:
1. **Enable optimizations**:
   ```bash
   python main.py -O2 program.forg
   ```

2. **Profile execution**:
   ```bash
   python main.py --benchmark program.forg
   ```

3. **Optimize algorithms** in your Forg code

## Development Issues

### Test Failures

**Problem**: Tests fail unexpectedly

**Solutions**:
1. **Run specific test**:
   ```bash
   python -m unittest test_runner.TestLexer.test_basic_tokens
   ```

2. **Check for environment issues**:
   ```bash
   python --version
   pip list
   ```

3. **Clear caches**:
   ```bash
   make clean
   rm -rf __pycache__/
   ```

### Import Errors in Development

**Problem**: Local modules not found

**Solutions**:
1. **Check PYTHONPATH**:
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   python main.py
   ```

2. **Use relative imports correctly**:
   ```python
   # Instead of
   import lexer
   
   # Use
   from . import lexer
   ```

### Debug Output Issues

**Problem**: Debug files not generated

**Solutions**:
1. **Check permissions**:
   ```bash
   ls -la debug/
   chmod 755 debug/
   ```

2. **Verify debug flags**:
   ```bash
   python main.py --debug-all --verbose program.forg
   ```

## Common Error Messages

### `Token[EOF : : Line X : Position Y]`

**Meaning**: Unexpected end of file

**Common Causes**:
- Missing closing braces `}`
- Incomplete statements
- Missing semicolons

### `COMPILE ERROR: Identifier 'name' has not been declared`

**Meaning**: Variable or function used before declaration

**Solutions**:
- Declare variable with `let`
- Define function before use
- Check spelling and case

### `Expected instruction opcode`

**Meaning**: Generated LLVM IR is invalid

**Solutions**:
- Check for unreachable code
- Ensure all code paths return values
- Review control flow logic

### `ValueError: LLVM IR parsing error`

**Meaning**: LLVM cannot parse generated IR

**Debug Steps**:
1. Enable IR debug: `--debug-compiler`
2. Check `debug/ir.ll` file
3. Look for malformed IR syntax

## Debugging Techniques

### Progressive Debugging

1. **Start Simple**: Create minimal reproduction case
2. **Add Gradually**: Incrementally add complexity
3. **Isolate Issue**: Remove unrelated code

### Using Debug Flags

```bash
# Step-by-step debugging
python main.py --debug-lexer program.forg     # Check tokens
python main.py --debug-parser program.forg    # Check AST
python main.py --debug-compiler program.forg  # Check IR
```

### Manual Code Inspection

1. **Check Token Stream**:
   ```python
   lexer = Lexer(source)
   while lexer.current_char is not None:
       print(lexer.next_token())
   ```

2. **Inspect AST**:
   ```bash
   python main.py --debug-parser program.forg
   cat debug/ast.json | jq '.'  # If jq available
   ```

3. **Examine LLVM IR**:
   ```bash
   python main.py --debug-compiler program.forg
   cat debug/ir.ll
   ```

### Binary Search Debugging

For large programs with unknown errors:

1. **Comment out half** the code
2. **Test compilation**
3. **Narrow down** the problematic section
4. **Repeat** until issue is isolated

### Comparative Debugging

Compare working vs. non-working programs:

```bash
# Working program
python main.py --debug-all working.forg

# Broken program  
python main.py --debug-all broken.forg

# Compare outputs
diff debug/ast_working.json debug/ast_broken.json
```

## Getting Help

### Before Asking for Help

1. **Search Documentation**: Check this guide and other docs
2. **Review Error Messages**: Read error messages carefully
3. **Create Minimal Example**: Reduce problem to smallest case
4. **Check Recent Changes**: What changed since it last worked?

### Information to Include

When seeking help, provide:

1. **Forg Code**: The problematic program
2. **Error Message**: Complete error output
3. **Environment**: OS, Python version, compiler version
4. **Commands Used**: Exact command line used
5. **Expected vs Actual**: What you expected vs what happened

### Example Help Request

```
Subject: Compilation Error with Recursive Function

Environment:
- OS: Windows 10
- Python: 3.9.7
- Forg Compiler: v1.0.0

Command Used:
python main.py --debug-all factorial.forg

Error Message:
LLVM IR parsing error
<string>:15:1: error: expected instruction opcode

Forg Code:
fn factorial(n: int) -> int {
    if n <= 1 {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

fn main() -> int {
    return factorial(5);
}

Expected: Program compiles and returns 120
Actual: Compilation fails with LLVM error

Additional Info:
- Simple non-recursive functions work fine
- Error occurs with any recursive function
- debug/ir.ll shows unreachable block at end
```

### Community Resources

- **Documentation**: Check the `docs/` directory
- **Examples**: Review `tests/` and `examples/` directories
- **Issues**: Search existing issue reports
- **Discussions**: Join community discussions

### Escalation Path

1. **Self-Help**: Documentation, debugging
2. **Community**: Forums, discussions
3. **Issues**: Bug reports, feature requests
4. **Maintainers**: Direct contact for serious issues

---

**Previous**: [Development Guide](development.md)
**Next**: Return to [Documentation Index](index.md)
