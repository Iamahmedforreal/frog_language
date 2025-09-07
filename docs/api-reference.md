# API Reference

This document provides comprehensive API documentation for the Forg compiler's internal components. This is useful for developers who want to extend the compiler or integrate it into other tools.

## Table of Contents

1. [Lexer API](#lexer-api)
2. [Parser API](#parser-api)
3. [AST Nodes](#ast-nodes)
4. [Compiler API](#compiler-api)
5. [Environment API](#environment-api)
6. [Error Handling API](#error-handling-api)
7. [Configuration API](#configuration-api)
8. [Performance API](#performance-api)
9. [Utility Functions](#utility-functions)

## Lexer API

### Class: `Lexer`

**File**: `lexer.py`

Tokenizes Forg source code into a stream of tokens.

#### Constructor

```python
def __init__(self, source: str) -> None
```

**Parameters**:
- `source`: The source code string to tokenize

**Example**:
```python
lexer = Lexer("let x: int = 42;")
```

#### Methods

##### `next_token() -> Token`

Returns the next token from the source code.

**Returns**: `Token` object or `EOF` token when finished

**Example**:
```python
while lexer.current_char is not None:
    token = lexer.next_token()
    print(token)
```

#### Properties

##### `current_char: str | None`

The current character being processed. `None` when at end of input.

##### `position: int`

Current position in the source string.

##### `line_no: int`

Current line number (1-indexed).

##### `read_position: int`

Next position to read from.

## Parser API

### Class: `Parser`

**File**: `parser.py`

Parses tokens into an Abstract Syntax Tree (AST).

#### Constructor

```python
def __init__(self, lexer: Lexer) -> None
```

**Parameters**:
- `lexer`: A `Lexer` instance

**Example**:
```python
lexer = Lexer(source_code)
parser = Parser(lexer)
```

#### Methods

##### `parse_program() -> Program`

Parses the entire program and returns the root AST node.

**Returns**: `Program` AST node

**Example**:
```python
program = parser.parse_program()
if len(parser.errors) == 0:
    print("Parsing successful")
else:
    for error in parser.errors:
        print(f"Parse error: {error}")
```

#### Properties

##### `errors: List[str]`

List of parsing errors encountered.

##### `current_token: Token`

The current token being processed.

##### `peek_token: Token`

The next token to be processed.

## AST Nodes

### Base Classes

#### `Node` (Abstract Base Class)

**File**: `AST.py`

Base class for all AST nodes.

##### Abstract Methods

```python
def type(self) -> NodeType
def json(self) -> dict
```

#### `Statement(Node)`

Base class for all statement nodes.

#### `Expression(Node)`

Base class for all expression nodes.

### Program Node

#### `Program(Node)`

Root node of the AST representing the entire program.

##### Properties

```python
statements: List[Statement]
```

##### Methods

```python
def type(self) -> NodeType  # Returns NodeType.Program
def json(self) -> dict     # Serializes to JSON
```

### Statement Nodes

#### `LetStatement(Statement)`

Represents variable declarations.

##### Properties

```python
name: IdentifierLiteral     # Variable name
value: Expression          # Initial value
value_type: str           # Type annotation
```

#### `FunctionStatement(Statement)`

Represents function declarations.

##### Properties

```python
name: IdentifierLiteral                 # Function name
parameters: List[FunctionParameter]     # Parameters
body: BlockStatement                   # Function body
return_type: str                      # Return type
```

#### `ReturnStatement(Statement)`

Represents return statements.

##### Properties

```python
return_value: Expression  # Value to return (optional)
```

#### `IfStatement(Statement)`

Represents conditional statements.

##### Properties

```python
condition: Expression              # Condition to test
consequence: BlockStatement        # If-true block
alternative: BlockStatement | None # Else block (optional)
```

#### `WhileStatement(Statement)`

Represents while loops.

##### Properties

```python
condition: Expression      # Loop condition
body: BlockStatement      # Loop body
```

#### `ForStatement(Statement)`

Represents for loops.

##### Properties

```python
var_declaration: LetStatement   # Loop variable
condition: Expression          # Loop condition
action: AssignStatement       # Loop increment
body: BlockStatement         # Loop body
```

### Expression Nodes

#### `InfixExpression(Expression)`

Represents binary operations.

##### Properties

```python
left_node: Expression   # Left operand
operator: str          # Operator (+, -, *, etc.)
right_node: Expression # Right operand
```

#### `CallExpression(Expression)`

Represents function calls.

##### Properties

```python
function: Expression          # Function to call
arguments: List[Expression]   # Arguments
```

#### Literal Nodes

##### `IntegerLiteral(Expression)`

```python
value: int  # Integer value
```

##### `FloatLiteral(Expression)`

```python
value: float  # Float value
```

##### `StringLiteral(Expression)`

```python
value: str  # String value
```

##### `BooleanLiteral(Expression)`

```python
value: bool  # Boolean value
```

##### `IdentifierLiteral(Expression)`

```python
value: str  # Identifier name
```

## Compiler API

### Class: `Compiler`

**File**: `compiler.py`

Compiles AST to LLVM IR.

#### Constructor

```python
def __init__(self) -> None
```

#### Methods

##### `compile(node: Node) -> None`

Compiles an AST node to LLVM IR.

**Parameters**:
- `node`: AST node to compile

**Example**:
```python
compiler = Compiler()
compiler.compile(program)
module = compiler.module
```

#### Properties

##### `module: ir.Module`

The LLVM module containing generated code.

##### `builder: ir.IRBuilder`

Current LLVM IR builder.

##### `env: Environment`

Current symbol table environment.

##### `errors: List[str]`

List of compilation errors.

##### `type_map: Dict[str, ir.Type]`

Mapping from Forg types to LLVM types.

```python
{
    'int': ir.IntType(32),
    'float': ir.FloatType(),
    'bool': ir.IntType(1),
    'void': ir.VoidType(),
    'str': ir.PointerType(ir.IntType(8))
}
```

## Environment API

### Class: `Environment`

**File**: `Envorment.py`

Symbol table for managing variable and function scopes.

#### Constructor

```python
def __init__(self, 
             records: Optional[Dict[str, Tuple[ir.Value, ir.Type]]] = None,
             parent: Optional['Environment'] = None, 
             name: str = "global") -> None
```

**Parameters**:
- `records`: Initial symbol bindings
- `parent`: Parent environment (for nested scopes)
- `name`: Environment name (for debugging)

#### Methods

##### `define(name: str, value: ir.Value, _type: ir.Type) -> ir.Value`

Define a new symbol in this environment.

**Parameters**:
- `name`: Symbol name
- `value`: LLVM IR value
- `_type`: LLVM IR type

**Returns**: The stored value

##### `lookup(name: str) -> Optional[Tuple[ir.Value, ir.Type]]`

Look up a symbol in this environment or parent environments.

**Parameters**:
- `name`: Symbol name to look up

**Returns**: Tuple of (value, type) if found, None otherwise

**Example**:
```python
env = Environment()
env.define("x", int_value, ir.IntType(32))

result = env.lookup("x")
if result:
    value, type_info = result
    print(f"Found symbol: {value} of type {type_info}")
```

## Error Handling API

### Class: `ErrorHandler`

**File**: `error_handler.py`

Centralized error handling and reporting.

#### Constructor

```python
def __init__(self) -> None
```

#### Methods

##### `add_error(error_type: ErrorType, message: str, line_no: int, position: int = 0, source_file: Optional[str] = None, suggestion: Optional[str] = None) -> None`

Add a new error to the error list.

##### `add_warning(message: str, line_no: int, position: int = 0, source_file: Optional[str] = None) -> None`

Add a new warning to the warning list.

##### `has_errors() -> bool`

Check if any errors have been recorded.

##### `has_warnings() -> bool`

Check if any warnings have been recorded.

##### `print_summary() -> None`

Print a summary of all errors and warnings.

### Class: `CompilerError`

Represents a single compiler error.

#### Properties

```python
error_type: ErrorType        # Type of error
message: str                # Error description
line_no: int               # Line number
position: int              # Character position
source_file: Optional[str] # Source file name
suggestion: Optional[str]  # Suggested fix
```

### Enum: `ErrorType`

```python
class ErrorType(Enum):
    LEXICAL = "Lexical Error"
    SYNTAX = "Syntax Error"
    SEMANTIC = "Semantic Error"
    TYPE = "Type Error"
    RUNTIME = "Runtime Error"
    INTERNAL = "Internal Compiler Error"
```

## Configuration API

### Class: `CompilerConfig`

**File**: `config.py`

Configuration management for the compiler.

#### Constructor

```python
def __init__(self) -> None
```

#### Class Methods

##### `from_args(cls, args) -> 'CompilerConfig'`

Create configuration from command line arguments.

#### Properties

```python
# Input/Output
input_file: Optional[str]
output_file: Optional[str]
output_format: OutputFormat

# Debug flags
lexer_debug: bool
parser_debug: bool
compiler_debug: bool
ast_debug: bool
ir_debug: bool

# Execution settings
run_code: bool
benchmark: bool

# Optimization
optimization_level: OptimizationLevel

# Directories
debug_dir: str
output_dir: str

# Error handling
max_errors: int
warnings_as_errors: bool
```

#### Methods

##### `get_ast_output_path() -> str`

Get the path for AST debug output.

##### `get_ir_output_path() -> str`

Get the path for LLVM IR debug output.

##### `should_print(level: str = "info") -> bool`

Check if output should be printed based on verbosity settings.

## Performance API

### Class: `PerformanceProfiler`

**File**: `performance.py`

Performance monitoring and profiling.

#### Constructor

```python
def __init__(self) -> None
```

#### Methods

##### `enable() -> None`

Enable performance profiling.

##### `disable() -> None`

Disable performance profiling.

##### `time_phase(phase_name: str) -> ContextManager`

Context manager for timing compilation phases.

**Example**:
```python
profiler = PerformanceProfiler()
profiler.enable()

with profiler.time_phase("lexing"):
    # Lexing code here
    pass

profiler.print_summary()
```

##### `record_tokens(count: int) -> None`

Record number of tokens processed.

##### `record_ast_nodes(count: int) -> None`

Record number of AST nodes created.

##### `print_summary(verbose: bool = False) -> None`

Print performance summary.

### Class: `PerformanceMetrics`

Container for performance metrics.

#### Properties

```python
lexing_time: float
parsing_time: float
compilation_time: float
execution_time: float
total_time: float

tokens_processed: int
ast_nodes_created: int
ir_instructions_generated: int

memory_usage_mb: float
peak_memory_mb: float
```

#### Methods

##### `tokens_per_second() -> float`

Calculate tokens processed per second.

##### `nodes_per_second() -> float`

Calculate AST nodes created per second.

## Utility Functions

### Token Utilities

#### `lookup_ident(ident: str) -> TokenType`

**File**: `custome_token.py`

Look up identifier to determine if it's a keyword or regular identifier.

**Parameters**:
- `ident`: Identifier string

**Returns**: Appropriate `TokenType`

### File Utilities

#### `load_source_file(file_path: str) -> Optional[str]`

**File**: `main.py`

Load source code from file with error handling.

**Parameters**:
- `file_path`: Path to source file

**Returns**: Source code string or None if error

### Benchmark Utilities

#### `benchmark_file(file_path: str, iterations: int = 5) -> Dict[str, float]`

**File**: `performance.py`

Benchmark compilation of a specific file.

**Parameters**:
- `file_path`: Path to Forg source file
- `iterations`: Number of iterations to run

**Returns**: Dictionary with average timing results

## Usage Examples

### Complete Compilation Pipeline

```python
from lexer import Lexer
from parser import Parser
from compiler import Compiler
from error_handler import error_handler

# Load source code
source = "fn main() -> int { return 42; }"

# Lexical analysis
lexer = Lexer(source)

# Syntax analysis
parser = Parser(lexer)
program = parser.parse_program()

if parser.errors:
    for error in parser.errors:
        print(f"Parse error: {error}")
    exit(1)

# Code generation
compiler = Compiler()
compiler.compile(program)

if compiler.errors:
    for error in compiler.errors:
        print(f"Compile error: {error}")
    exit(1)

# Get LLVM module
module = compiler.module
print(str(module))
```

### Custom Error Handling

```python
from error_handler import ErrorHandler, ErrorType

error_handler = ErrorHandler()

# Add custom errors
error_handler.add_error(
    ErrorType.SEMANTIC,
    "Custom semantic error",
    line_no=10,
    position=5,
    source_file="test.forg",
    suggestion="Try using a different variable name"
)

# Check for errors
if error_handler.has_errors():
    error_handler.print_summary()
```

### Performance Monitoring

```python
from performance import PerformanceProfiler

profiler = PerformanceProfiler()
profiler.enable()

# Time different phases
with profiler.time_phase("lexing"):
    lexer = Lexer(source)
    tokens = []
    while lexer.current_char is not None:
        tokens.append(lexer.next_token())

profiler.record_tokens(len(tokens))
profiler.print_summary(verbose=True)
```

### Configuration Management

```python
from config import CompilerConfig

# Create default configuration
config = CompilerConfig()
config.lexer_debug = True
config.optimization_level = OptimizationLevel.O2

# Use configuration
if config.should_print("debug"):
    print("Debug output enabled")

ast_path = config.get_ast_output_path()
```

---

**Next**: [Examples and Tutorials](examples.md)
**Previous**: [Compiler Architecture](architecture.md)
