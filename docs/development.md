# Development Guide

This guide helps developers contribute to the Forg compiler project, extend its functionality, and maintain code quality.

## Table of Contents

1. [Development Setup](#development-setup)
2. [Code Style Guidelines](#code-style-guidelines)
3. [Testing](#testing)
4. [Adding New Features](#adding-new-features)
5. [Debugging](#debugging)
6. [Performance Optimization](#performance-optimization)
7. [Documentation](#documentation)
8. [Release Process](#release-process)

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git (for version control)
- A good text editor or IDE (VS Code, PyCharm, etc.)

### Setting Up the Development Environment

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd compiler
   ```

2. **Create a Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   # Production dependencies
   pip install -r requirements.txt
   
   # Development dependencies
   pip install pytest black flake8 mypy sphinx
   
   # Or use make
   make dev-setup
   ```

4. **Verify Installation**
   ```bash
   python main.py tests/test1.forg
   python test_runner.py
   ```

### Project Structure for Development

```
compiler/
├── src/                    # Main source files
│   ├── lexer.py           # Lexical analyzer
│   ├── parser.py          # Syntax analyzer
│   ├── compiler.py        # Code generator
│   ├── AST.py            # AST definitions
│   └── ...
├── tests/                 # Test files
│   ├── *.forg            # Sample programs
│   └── test_*.py         # Unit tests
├── docs/                  # Documentation
├── debug/                 # Debug output
├── tools/                 # Development tools
└── examples/              # Example programs
```

## Code Style Guidelines

### Python Code Style

We follow **PEP 8** with some modifications:

#### Formatting Rules

- **Line Length**: Maximum 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes for strings, single quotes for character literals
- **Imports**: Group by standard library, third-party, local imports

#### Example

```python
"""
Module docstring describing the purpose.
"""

import os
import sys
from typing import List, Optional, Dict

from llvmlite import ir

from AST import Node, Expression
from error_handler import ErrorHandler


class ExampleClass:
    """Class docstring."""
    
    def __init__(self, name: str, value: int = 0) -> None:
        """Initialize with name and optional value."""
        self.name = name
        self.value = value
    
    def process_data(self, data: List[str]) -> Optional[Dict[str, int]]:
        """Process data and return results."""
        if not data:
            return None
        
        result = {}
        for item in data:
            if len(item) > 0:
                result[item] = len(item)
        
        return result
```

#### Naming Conventions

- **Classes**: `PascalCase` (e.g., `TokenType`, `ASTNode`)
- **Functions/Methods**: `snake_case` (e.g., `parse_expression`, `next_token`)
- **Variables**: `snake_case` (e.g., `current_token`, `line_number`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_ERRORS`, `DEFAULT_TIMEOUT`)
- **Private Members**: prefix with `_` or `__`

#### Type Hints

Always use type hints for function parameters and return values:

```python
def parse_expression(self, precedence: PrecedenceType) -> Optional[Expression]:
    """Parse expression with given precedence."""
    pass

def lookup(self, name: str) -> Optional[Tuple[ir.Value, ir.Type]]:
    """Look up symbol in environment."""
    pass
```

### Forg Code Style

For example Forg programs:

```forg
// Function names: snake_case
fn calculate_average(a: int, b: int) -> float {
    return (a + b) / 2.0;
}

// Variable names: snake_case
fn main() -> int {
    let user_name: str = "Alice";
    let max_attempts: int = 5;
    let is_valid: bool = true;
    
    return 0;
}
```

### Code Quality Tools

#### Automatic Formatting

```bash
# Format all Python files
black --line-length=100 *.py

# Or use make
make format
```

#### Linting

```bash
# Check code style
flake8 --max-line-length=100 --ignore=E203,W503 *.py

# Or use make
make lint
```

#### Type Checking

```bash
# Static type checking
mypy --ignore-missing-imports *.py
```

## Testing

### Test Organization

```
tests/
├── unit/                  # Unit tests
│   ├── test_lexer.py     # Lexer tests
│   ├── test_parser.py    # Parser tests
│   └── test_compiler.py  # Compiler tests
├── integration/           # Integration tests
│   ├── test_pipeline.py  # Full pipeline tests
│   └── test_examples.py  # Example program tests
├── performance/           # Performance tests
│   └── test_benchmarks.py
└── fixtures/              # Test data
    ├── *.forg            # Test programs
    └── expected/         # Expected outputs
```

### Writing Unit Tests

```python
import unittest
from lexer import Lexer
from custome_token import TokenType

class TestLexer(unittest.TestCase):
    """Test cases for the lexer."""
    
    def test_integer_tokens(self):
        """Test integer token recognition."""
        lexer = Lexer("42 123 0")
        
        # First token
        token = lexer.next_token()
        self.assertEqual(token.type, TokenType.INT)
        self.assertEqual(token.literal, 42)
        
        # Second token
        token = lexer.next_token()
        self.assertEqual(token.type, TokenType.INT)
        self.assertEqual(token.literal, 123)
    
    def test_keyword_recognition(self):
        """Test keyword vs identifier recognition."""
        lexer = Lexer("let variable fn function")
        
        # 'let' should be a keyword
        token = lexer.next_token()
        self.assertEqual(token.type, TokenType.LET)
        
        # 'variable' should be an identifier
        token = lexer.next_token()
        self.assertEqual(token.type, TokenType.IDENT)
        
    def setUp(self):
        """Set up test fixtures."""
        self.sample_code = """
        fn add(a: int, b: int) -> int {
            return a + b;
        }
        """
    
    def tearDown(self):
        """Clean up after tests."""
        pass

if __name__ == '__main__':
    unittest.main()
```

### Integration Tests

```python
def test_factorial_program():
    """Test complete factorial program compilation and execution."""
    source = '''
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
    '''
    
    # Compile
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    
    # Check for parse errors
    assert len(parser.errors) == 0
    
    # Compile to IR
    compiler = Compiler()
    compiler.compile(program)
    
    # Check for compile errors
    assert len(compiler.errors) == 0
    
    # Test execution (would require JIT setup)
    # Expected result: 120 (5!)
```

### Running Tests

```bash
# Run all tests
python test_runner.py

# Run specific test file
python -m unittest test_lexer.py

# Run with coverage
python -m pytest --cov=. tests/

# Run performance tests
make benchmark
```

### Test Guidelines

1. **One Concept Per Test**: Each test should verify one specific behavior
2. **Descriptive Names**: Test names should clearly describe what's being tested
3. **Arrange-Act-Assert**: Structure tests with clear setup, action, and verification
4. **Edge Cases**: Test boundary conditions and error cases
5. **Fast Tests**: Unit tests should run quickly (< 1 second each)

## Adding New Features

### Adding a New Token Type

1. **Define the Token** (`custome_token.py`):
   ```python
   class TokenType(Enum):
       # ... existing tokens ...
       NEW_TOKEN = "NEW_TOKEN"
   ```

2. **Update the Lexer** (`lexer.py`):
   ```python
   def next_token(self) -> Token:
       # ... existing cases ...
       match self.current_char:
           case '&':  # Example: new operator
               tok = self.__new_token(TokenType.NEW_TOKEN, self.current_char)
   ```

3. **Add Tests**:
   ```python
   def test_new_token(self):
       lexer = Lexer("&")
       token = lexer.next_token()
       self.assertEqual(token.type, TokenType.NEW_TOKEN)
   ```

### Adding a New AST Node

1. **Define the Node** (`AST.py`):
   ```python
   class NewStatement(Statement):
       def __init__(self, value: Expression) -> None:
           self.value = value
       
       def type(self) -> NodeType:
           return NodeType.NewStatement
       
       def json(self) -> dict:
           return {
               "type": self.type().value,
               "value": self.value.json()
           }
   ```

2. **Update NodeType Enum**:
   ```python
   class NodeType(Enum):
       # ... existing types ...
       NewStatement = "NewStatement"
   ```

3. **Add Parser Support** (`parser.py`):
   ```python
   def __parse_new_statement(self) -> NewStatement:
       stmt = NewStatement()
       # ... parsing logic ...
       return stmt
   ```

### Adding a New Language Feature

Example: Adding a `unless` statement (opposite of `if`)

1. **Add Token and Keyword**:
   ```python
   # In custome_token.py
   UNLESS = "UNLESS"
   
   KEYWORDS = {
       # ... existing keywords ...
       "unless": TokenType.UNLESS,
   }
   ```

2. **Create AST Node**:
   ```python
   class UnlessStatement(Statement):
       def __init__(self, condition: Expression, body: BlockStatement):
           self.condition = condition
           self.body = body
   ```

3. **Add Parser Logic**:
   ```python
   def __parse_unless_statement(self) -> UnlessStatement:
       self.__next_token()  # consume 'unless'
       condition = self.__parse_expression(PrecedenceType.P_LOWEST)
       # ... rest of parsing
   ```

4. **Add Compiler Support**:
   ```python
   def __visit_unless_statement(self, node: UnlessStatement) -> None:
       # Compile as negated if statement
       condition, _ = self.__resolve_value(node.condition)
       negated_condition = self.builder.not_(condition)
       # ... rest of compilation
   ```

5. **Add Tests**:
   ```python
   def test_unless_statement(self):
       source = "unless x > 5 { printf(\"x is small\"); }"
       # ... test parsing and compilation
   ```

## Debugging

### Debugging the Compiler

#### Enable Debug Output

```bash
# Debug lexer
python main.py --debug-lexer program.forg

# Debug parser (saves AST)
python main.py --debug-parser program.forg

# Debug compiler (saves LLVM IR)
python main.py --debug-compiler program.forg

# All debug output
python main.py --debug-all program.forg
```

#### Using the Python Debugger

```python
import pdb

def problematic_function():
    pdb.set_trace()  # Debugger will break here
    # ... code to debug
```

#### Custom Debug Output

```python
def debug_print(*args, **kwargs):
    if DEBUG_ENABLED:
        print("[DEBUG]", *args, **kwargs)

# Usage
debug_print(f"Current token: {self.current_token}")
debug_print(f"AST node count: {len(program.statements)}")
```

### Common Debugging Scenarios

#### Lexer Issues

```python
# Print all tokens
def debug_tokenize(source: str):
    lexer = Lexer(source)
    tokens = []
    while lexer.current_char is not None:
        token = lexer.next_token()
        print(f"Token: {token}")
        tokens.append(token)
    return tokens
```

#### Parser Issues

```python
# Trace parsing
def trace_parsing(self, method_name: str):
    print(f"Entering {method_name}, current_token: {self.current_token}")
    # ... parsing logic
    print(f"Exiting {method_name}")
```

#### Compiler Issues

```python
# Print LLVM IR at each step
def debug_ir_generation(self, node: Node):
    print(f"Before compiling {node.type()}: {len(str(self.module))} characters")
    self.compile(node)
    print(f"After compiling {node.type()}: {len(str(self.module))} characters")
```

## Performance Optimization

### Profiling

#### Built-in Performance Monitoring

```bash
# Enable benchmarking
python main.py --benchmark program.forg

# Run performance suite
python performance.py
```

#### Python Profiling

```bash
# Profile with cProfile
python -m cProfile -o profile.stats main.py program.forg

# Analyze results
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('time').print_stats(10)"
```

#### Memory Profiling

```bash
# Install memory profiler
pip install memory-profiler

# Profile memory usage
python -m memory_profiler main.py program.forg
```

### Optimization Strategies

#### Lexer Optimizations

1. **Character Lookahead Caching**:
   ```python
   def __init__(self):
       self._peek_cache = None
   
   def __peek_char(self):
       if self._peek_cache is None:
           self._peek_cache = self._read_next_char()
       return self._peek_cache
   ```

2. **Token Pooling**:
   ```python
   TOKEN_POOL = {}
   
   def __new_token(self, tt: TokenType, literal: Any):
       key = (tt, literal)
       if key in TOKEN_POOL:
           return TOKEN_POOL[key]
       token = Token(tt, literal, self.line_no, self.position)
       TOKEN_POOL[key] = token
       return token
   ```

#### Parser Optimizations

1. **Precedence Table Caching**:
   ```python
   PRECEDENCE_CACHE = {}
   
   def __get_precedence(self, token_type: TokenType):
       if token_type not in PRECEDENCE_CACHE:
           PRECEDENCE_CACHE[token_type] = PRECEDENCES.get(token_type, P_LOWEST)
       return PRECEDENCE_CACHE[token_type]
   ```

#### Compiler Optimizations

1. **Type Map Caching**:
   ```python
   def __get_llvm_type(self, forg_type: str):
       if forg_type not in self.type_cache:
           self.type_cache[forg_type] = self._create_llvm_type(forg_type)
       return self.type_cache[forg_type]
   ```

### Performance Testing

```python
def benchmark_compilation_speed():
    """Benchmark different aspects of compilation."""
    import time
    
    # Generate test program
    source = generate_large_program(1000)  # 1000 statements
    
    # Measure lexing
    start = time.time()
    lexer = Lexer(source)
    tokens = list(get_all_tokens(lexer))
    lexing_time = time.time() - start
    
    # Measure parsing
    start = time.time()
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    parsing_time = time.time() - start
    
    print(f"Lexing: {lexing_time:.3f}s ({len(tokens)} tokens)")
    print(f"Parsing: {parsing_time:.3f}s ({len(program.statements)} statements)")
```

## Documentation

### Code Documentation

#### Docstring Format

```python
def complex_function(param1: str, param2: int, option: bool = False) -> Dict[str, Any]:
    """
    Brief description of what the function does.
    
    Longer description with more details about the function's behavior,
    edge cases, and important notes.
    
    Args:
        param1: Description of the first parameter
        param2: Description of the second parameter
        option: Description of optional parameter (default: False)
    
    Returns:
        Dictionary containing the results with keys:
        - 'result': The main result
        - 'metadata': Additional information
    
    Raises:
        ValueError: If param1 is empty
        TypeError: If param2 is negative
    
    Example:
        >>> result = complex_function("test", 42, True)
        >>> print(result['result'])
        'processed_test'
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    
    # Implementation here
    return {"result": f"processed_{param1}", "metadata": {"count": param2}}
```

### API Documentation

Use Sphinx for generating API documentation:

```bash
# Install Sphinx
pip install sphinx sphinx-rtd-theme

# Initialize documentation
sphinx-quickstart docs

# Generate documentation
make docs
```

### Writing User Documentation

1. **Clear Structure**: Use consistent headings and organization
2. **Code Examples**: Include working examples for all features
3. **Step-by-step Tutorials**: Guide users through complex tasks
4. **Error Messages**: Document common errors and solutions

## Release Process

### Version Management

Use semantic versioning (MAJOR.MINOR.PATCH):

```python
# version.py
__version__ = "1.2.3"

MAJOR = 1  # Breaking changes
MINOR = 2  # New features (backwards compatible)
PATCH = 3  # Bug fixes
```

### Pre-release Checklist

1. **Code Quality**:
   ```bash
   make lint      # Check code style
   make test      # Run all tests
   make benchmark # Performance regression check
   ```

2. **Documentation**:
   - Update CHANGELOG.md
   - Update version numbers
   - Review and update documentation

3. **Testing**:
   - All tests pass
   - Manual testing of key features
   - Performance benchmarks within acceptable range

### Release Steps

1. **Create Release Branch**:
   ```bash
   git checkout -b release/v1.2.3
   ```

2. **Update Version**:
   ```python
   # Update version in relevant files
   __version__ = "1.2.3"
   ```

3. **Final Testing**:
   ```bash
   make test
   make benchmark
   ```

4. **Create Release**:
   ```bash
   git tag v1.2.3
   git push origin v1.2.3
   ```

5. **Post-release**:
   - Update documentation site
   - Announce release
   - Prepare for next development cycle

### Continuous Integration

Example GitHub Actions workflow:

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest black flake8
    
    - name: Lint
      run: make lint
    
    - name: Test
      run: make test
```

---

**Next**: [Performance Guide](performance.md)
**Previous**: [Examples and Tutorials](examples.md)
