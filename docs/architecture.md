# Compiler Architecture

This document provides a detailed overview of the Forg compiler's internal architecture, design decisions, and implementation details.

## Table of Contents

1. [Overview](#overview)
2. [Compilation Pipeline](#compilation-pipeline)
3. [Component Architecture](#component-architecture)
4. [Data Structures](#data-structures)
5. [Error Handling](#error-handling)
6. [Performance Considerations](#performance-considerations)
7. [Extension Points](#extension-points)

## Overview

The Forg compiler is designed as a traditional multi-pass compiler with clear separation of concerns. It follows the standard compilation pipeline while providing extensive debugging and profiling capabilities.

### Design Principles

- **Modularity**: Each compilation phase is a separate, testable module
- **Extensibility**: Easy to add new language features or optimizations
- **Robustness**: Comprehensive error handling and recovery
- **Performance**: Efficient algorithms and data structures
- **Debugging**: Rich debugging and introspection capabilities

### Technology Stack

- **Language**: Python 3.8+
- **LLVM Backend**: llvmlite for IR generation and JIT compilation
- **Testing**: Custom test framework with unittest integration
- **Documentation**: Markdown with potential Sphinx integration

## Compilation Pipeline

```
┌─────────────┐    ┌────────────┐    ┌──────────────┐    ┌─────────────┐
│ Source Code │ -> │   Lexer    │ -> │    Parser    │ -> │  Compiler   │
└─────────────┘    └────────────┘    └──────────────┘    └─────────────┘
                         │                  │                    │
                         v                  v                    v
                   ┌──────────┐      ┌─────────────┐      ┌─────────────┐
                   │  Tokens  │      │     AST     │      │  LLVM IR    │
                   └──────────┘      └─────────────┘      └─────────────┘
                                                                 │
                                                                 v
                   ┌─────────────────────────────────────────────────────┐
                   │              JIT Execution Engine                   │
                   └─────────────────────────────────────────────────────┘
```

### Phase 1: Lexical Analysis (Lexer)

**File**: `lexer.py`

The lexer performs tokenization of the source code, converting raw text into a stream of tokens.

**Responsibilities**:
- Character-by-character source code analysis
- Token recognition and classification
- Line and column position tracking
- Comment handling
- Error reporting for invalid characters/tokens

**Key Features**:
- Support for all Forg token types (identifiers, literals, operators, keywords)
- Single-line comment support (`//`)
- Precise error location reporting
- Lookahead capabilities for multi-character tokens

**Algorithm**: Hand-written recursive descent lexer

### Phase 2: Syntax Analysis (Parser)

**File**: `parser.py`

The parser builds an Abstract Syntax Tree (AST) from the token stream using recursive descent parsing with operator precedence.

**Responsibilities**:
- Syntax validation according to Forg grammar
- AST construction
- Operator precedence handling
- Error recovery and reporting

**Key Features**:
- Pratt parser for expression parsing
- Left-recursive elimination
- Error recovery strategies
- Comprehensive error messages

**Algorithm**: Recursive descent parser with Pratt parsing for expressions

### Phase 3: Semantic Analysis & Code Generation (Compiler)

**File**: `compiler.py`

The compiler performs semantic analysis and generates LLVM IR code by traversing the AST.

**Responsibilities**:
- Type checking and inference
- Symbol table management
- Scope resolution
- LLVM IR generation
- Optimization preparation

**Key Features**:
- Environment-based symbol tables
- Hierarchical scoping
- Type safety enforcement
- Built-in function support
- Control flow code generation

**Algorithm**: Tree-walking interpreter pattern adapted for compilation

### Phase 4: JIT Execution

**Integration**: `main.py` with llvmlite

The final phase uses LLVM's JIT compiler to execute the generated IR.

**Responsibilities**:
- LLVM IR validation
- JIT compilation to machine code
- Runtime execution
- Performance monitoring

## Component Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         Main Controller                         │
│                        (main.py)                               │
└─────────────────────┬───────────────────────────────────────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
    v                 v                 v
┌─────────┐    ┌─────────────┐    ┌──────────────┐
│  Lexer  │    │   Parser    │    │   Compiler   │
│         │    │             │    │              │
│ ┌─────┐ │    │ ┌─────────┐ │    │ ┌──────────┐ │
│ │Token│ │    │ │   AST   │ │    │ │   LLVM   │ │
│ │ Def │ │    │ │ Nodes   │ │    │ │    IR    │ │
│ └─────┘ │    │ └─────────┘ │    │ └──────────┘ │
└─────────┘    └─────────────┘    └──────────────┘
```

### Support Components

```
┌─────────────────────────────────────────────────────────────────┐
│                      Support Infrastructure                     │
└─────────────────────────────────────────────────────────────────┘
    │                    │                     │
    v                    v                     v
┌──────────────┐  ┌─────────────────┐  ┌─────────────────┐
│Error Handler │  │  Configuration  │  │  Environment    │
│              │  │                 │  │ (Symbol Table)  │
│ ┌──────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │
│ │  Error   │ │  │ │   Config    │ │  │ │   Scopes    │ │
│ │ Messages │ │  │ │  Settings   │ │  │ │ & Bindings  │ │
│ └──────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │
└──────────────┘  └─────────────────┘  └─────────────────┘
    │                    │                     │
    v                    v                     v
┌──────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Performance  │  │   Test Suite    │  │   Utilities     │
│  Monitor     │  │                 │  │                 │
│              │  │ ┌─────────────┐ │  │ ┌─────────────┐ │
│ ┌──────────┐ │  │ │    Unit     │ │  │ │  File I/O   │ │
│ │ Metrics  │ │  │ │Integration  │ │  │ │ & Helpers   │ │
│ │& Timing  │ │  │ │Performance  │ │  │ └─────────────┘ │
│ └──────────┘ │  │ └─────────────┘ │  └─────────────────┘
└──────────────┘  └─────────────────┘
```

## Data Structures

### Abstract Syntax Tree (AST)

**File**: `AST.py`

The AST represents the hierarchical structure of the program. All nodes inherit from a common `Node` base class.

#### Node Hierarchy

```
Node (Abstract Base)
├── Statement
│   ├── ExpressionStatement
│   ├── LetStatement
│   ├── FunctionStatement
│   ├── BlockStatement
│   ├── ReturnStatement
│   ├── AssignStatement
│   ├── IfStatement
│   ├── WhileStatement
│   ├── ForStatement
│   ├── BreakStatement
│   └── ContinueStatement
├── Expression
│   ├── InfixExpression
│   ├── CallExpression
│   ├── IntegerLiteral
│   ├── FloatLiteral
│   ├── IdentifierLiteral
│   ├── BooleanLiteral
│   └── StringLiteral
└── Program (Root)
```

#### Key Methods

Each AST node implements:
- `type()` - Returns the node type
- `json()` - Serializes to JSON for debugging

### Token System

**File**: `custome_token.py`

Tokens represent the atomic elements of the language.

#### Token Structure

```python
class Token:
    type: TokenType        # Token classification
    literal: Any          # Token value
    line_no: int         # Line number
    position: int        # Character position
```

#### Token Types

- **Literals**: `INT`, `FLOAT`, `STRING`, `IDENT`
- **Keywords**: `LET`, `FN`, `IF`, `WHILE`, etc.
- **Operators**: `PLUS`, `MINUS`, `EQ_EQ`, etc.
- **Delimiters**: `LPAREN`, `RBRACE`, `SEMICOLON`, etc.
- **Special**: `EOF`, `ILLEGAL`

### Environment (Symbol Table)

**File**: `Envorment.py`

The environment manages variable and function scopes using a hierarchical structure.

#### Structure

```python
class Environment:
    records: Dict[str, Tuple[ir.Value, ir.Type]]  # Symbol bindings
    parent: Optional[Environment]                  # Parent scope
    name: str                                     # Scope identifier
```

#### Scope Management

- **Global Scope**: Built-in functions and global variables
- **Function Scope**: Function parameters and local variables
- **Block Scope**: Variables declared in blocks (if, while, for)

### Error System

**File**: `error_handler.py`

Comprehensive error tracking and reporting system.

#### Error Classification

```python
class ErrorType(Enum):
    LEXICAL = "Lexical Error"      # Invalid tokens
    SYNTAX = "Syntax Error"        # Grammar violations  
    SEMANTIC = "Semantic Error"    # Type/scope errors
    TYPE = "Type Error"           # Type mismatches
    RUNTIME = "Runtime Error"     # Execution failures
    INTERNAL = "Internal Error"   # Compiler bugs
```

#### Error Information

Each error includes:
- Error type and message
- Source location (file, line, column)
- Suggested fixes (when available)
- Context information

## Error Handling

### Error Recovery Strategies

1. **Lexer Errors**:
   - Skip invalid characters
   - Continue tokenization
   - Report all errors found

2. **Parser Errors**:
   - Synchronization points (semicolons, braces)
   - Error productions for common mistakes
   - Partial AST construction

3. **Compiler Errors**:
   - Continue after type errors
   - Collect all semantic errors
   - Graceful degradation

### Error Reporting

```
Error Type at file:line:column: Description
  Suggestion: Helpful fix recommendation
  
  Context: Code snippet showing the error location
```

Example:
```
Syntax Error at factorial.forg:Line 5, Column 12: Expected ';' after expression
  Suggestion: Add a semicolon at the end of the statement
  
  Context:
    let result = factorial(5)
                            ^
```

## Performance Considerations

### Compilation Performance

1. **Single-Pass Design**: Each phase processes the entire input once
2. **Efficient Data Structures**: Optimized for common operations
3. **Lazy Evaluation**: Defer expensive operations when possible
4. **Memory Management**: Careful object lifecycle management

### Runtime Performance

1. **LLVM Optimization**: Leverage LLVM's optimization passes
2. **Type System**: Static typing enables optimizations
3. **Efficient Code Generation**: Minimal overhead IR generation
4. **JIT Compilation**: Near-native execution performance

### Profiling and Monitoring

**File**: `performance.py`

- **Phase Timing**: Track time spent in each compilation phase
- **Memory Usage**: Monitor memory consumption
- **Throughput Metrics**: Tokens/second, nodes/second, etc.
- **Benchmark Suite**: Standardized performance tests

## Extension Points

### Adding New Language Features

1. **Lexer Extensions**:
   - Add new token types in `custome_token.py`
   - Implement tokenization logic in `lexer.py`

2. **Parser Extensions**:
   - Add new AST node types in `AST.py`
   - Implement parsing logic in `parser.py`
   - Update grammar and precedence tables

3. **Compiler Extensions**:
   - Add visit methods in `compiler.py`
   - Implement code generation logic
   - Handle new semantic rules

### Adding Built-in Functions

1. Initialize function in `Compiler.__initialize_builtins()`
2. Add call handling in `Compiler.__visit_call_expression()`
3. Update type checking and error handling

### Adding Optimizations

1. **AST-Level**: Constant folding, dead code elimination
2. **IR-Level**: LLVM optimization passes
3. **Runtime**: Profile-guided optimization

### Testing Extensions

1. **Unit Tests**: Add to `test_runner.py`
2. **Integration Tests**: Create new `.forg` files
3. **Performance Tests**: Add benchmarks to `performance.py`

## Future Architecture Improvements

### Planned Enhancements

1. **Multi-Pass Compilation**: Separate semantic analysis phase
2. **Intermediate Representation**: Custom IR before LLVM
3. **Module System**: Support for imports and libraries
4. **Incremental Compilation**: Only recompile changed modules
5. **Better Error Recovery**: More sophisticated error handling
6. **IDE Integration**: Language server protocol support

### Scalability Considerations

1. **Parallel Compilation**: Multi-threaded compilation phases
2. **Caching**: Intermediate result caching
3. **Streaming**: Process large files without loading entirely
4. **Memory Optimization**: Reduce memory footprint for large programs

---

**Next**: [API Reference](api-reference.md)
**Previous**: [Language Reference](language-reference.md)
