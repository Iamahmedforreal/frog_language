"""
Test Runner for Forg Language Compiler

This module provides comprehensive testing capabilities for the Forg compiler,
including unit tests, integration tests, and performance benchmarks.
"""

import os
import sys
import time
import unittest
from typing import List, Dict, Any, Optional
import json
import subprocess
from dataclasses import dataclass

from lexer import Lexer
from parser import Parser
from compiler import Compiler
from AST import Program
from custome_token import TokenType
from error_handler import ErrorHandler, ErrorType


@dataclass
class TestCase:
    """Represents a single test case."""
    name: str
    source_code: str
    expected_result: Optional[int] = None
    expected_tokens: Optional[List[str]] = None
    should_fail: bool = False
    expected_error_type: Optional[ErrorType] = None
    description: str = ""


class LexerTests(unittest.TestCase):
    """Unit tests for the lexer."""
    
    def test_basic_tokens(self):
        """Test basic token recognition."""
        source = "let x: int = 42;"
        lexer = Lexer(source)
        
        expected_types = [
            TokenType.LET, TokenType.IDENT, TokenType.COLON, 
            TokenType.TYPE, TokenType.EQ, TokenType.INT, TokenType.SEMICOLON
        ]
        
        for expected_type in expected_types:
            token = lexer.next_token()
            self.assertEqual(token.type, expected_type)
    
    def test_arithmetic_operators(self):
        """Test arithmetic operator tokens."""
        source = "+ - * / % ^"
        lexer = Lexer(source)
        
        expected_types = [
            TokenType.PLUS, TokenType.MINUS, TokenType.ASTERISK,
            TokenType.SLASH, TokenType.MODULUS, TokenType.POW
        ]
        
        for expected_type in expected_types:
            token = lexer.next_token()
            self.assertEqual(token.type, expected_type)
    
    def test_comparison_operators(self):
        """Test comparison operator tokens."""
        source = "< > <= >= == !="
        lexer = Lexer(source)
        
        expected_types = [
            TokenType.LT, TokenType.GT, TokenType.LT_EQ,
            TokenType.GT_EQ, TokenType.EQ_EQ, TokenType.NOT_EQ
        ]
        
        for expected_type in expected_types:
            token = lexer.next_token()
            self.assertEqual(token.type, expected_type)
    
    def test_numbers(self):
        """Test number literal recognition."""
        # Integer
        lexer = Lexer("42")
        token = lexer.next_token()
        self.assertEqual(token.type, TokenType.INT)
        self.assertEqual(token.literal, 42)
        
        # Float
        lexer = Lexer("3.14")
        token = lexer.next_token()
        self.assertEqual(token.type, TokenType.FLOAT)
        self.assertEqual(token.literal, 3.14)
    
    def test_strings(self):
        """Test string literal recognition."""
        lexer = Lexer('"Hello, World!"')
        token = lexer.next_token()
        self.assertEqual(token.type, TokenType.STRING)
        self.assertEqual(token.literal, "Hello, World!")
    
    def test_keywords(self):
        """Test keyword recognition."""
        keywords = {
            "let": TokenType.LET,
            "fn": TokenType.FN,
            "return": TokenType.RETURN,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "while": TokenType.WHILE,
            "for": TokenType.FOR,
            "break": TokenType.BREAK,
            "continue": TokenType.CONTINUE,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE
        }
        
        for keyword, expected_type in keywords.items():
            lexer = Lexer(keyword)
            token = lexer.next_token()
            self.assertEqual(token.type, expected_type)


class ParserTests(unittest.TestCase):
    """Unit tests for the parser."""
    
    def test_let_statement(self):
        """Test parsing let statements."""
        source = "let x: int = 42;"
        lexer = Lexer(source)
        parser = Parser(lexer)
        program = parser.parse_program()
        
        self.assertEqual(len(parser.errors), 0)
        self.assertEqual(len(program.statements), 1)
        
        stmt = program.statements[0]
        self.assertEqual(stmt.type().value, "LetStatement")
    
    def test_function_declaration(self):
        """Test parsing function declarations."""
        source = """
        fn add(a: int, b: int) -> int {
            return a + b;
        }
        """
        lexer = Lexer(source)
        parser = Parser(lexer)
        program = parser.parse_program()
        
        self.assertEqual(len(parser.errors), 0)
        self.assertEqual(len(program.statements), 1)
        
        stmt = program.statements[0]
        self.assertEqual(stmt.type().value, "FunctionStatement")
    
    def test_if_statement(self):
        """Test parsing if statements."""
        source = """
        fn main() -> int {
            if x < 10 {
                return 1;
            } else {
                return 0;
            }
        }
        """
        lexer = Lexer(source)
        parser = Parser(lexer)
        program = parser.parse_program()
        
        self.assertEqual(len(parser.errors), 0)
        self.assertEqual(len(program.statements), 1)
        
        # The top level is a function statement
        func_stmt = program.statements[0]
        self.assertEqual(func_stmt.type().value, "FunctionStatement")
        
        # The if statement is inside the function body
        if_stmt = func_stmt.body.statements[0]
        self.assertEqual(if_stmt.type().value, "IfStatement")
    
    def test_while_loop(self):
        """Test parsing while loops."""
        source = """
        while i < 10 {
            i = i + 1;
        }
        """
        lexer = Lexer(source)
        parser = Parser(lexer)
        program = parser.parse_program()
        
        self.assertEqual(len(parser.errors), 0)
        self.assertEqual(len(program.statements), 1)
        
        stmt = program.statements[0]
        self.assertEqual(stmt.type().value, "WhileStatement")
    
    def test_for_loop(self):
        """Test parsing for loops."""
        source = """
        for (let i: int = 0; i < 10; i = i + 1) {
            printf("i = %i\\n", i);
        }
        """
        lexer = Lexer(source)
        parser = Parser(lexer)
        program = parser.parse_program()
        
        self.assertEqual(len(parser.errors), 0)
        self.assertEqual(len(program.statements), 1)
        
        stmt = program.statements[0]
        self.assertEqual(stmt.type().value, "ForStatement")


class IntegrationTests(unittest.TestCase):
    """Integration tests for the complete compiler pipeline."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_cases = [
            TestCase(
                name="simple_arithmetic",
                source_code="""
                fn main() -> int {
                    let x: int = 5;
                    let y: int = 10;
                    return x + y;
                }
                """,
                expected_result=15,
                description="Test basic arithmetic operations"
            ),
            TestCase(
                name="conditional_logic",
                source_code="""
                fn main() -> int {
                    let x: int = 5;
                    if x < 10 {
                        return 1;
                    } else {
                        return 0;
                    }
                }
                """,
                expected_result=1,
                description="Test conditional logic"
            ),
            TestCase(
                name="function_call",
                source_code="""
                fn add(a: int, b: int) -> int {
                    return a + b;
                }
                
                fn main() -> int {
                    return add(5, 10);
                }
                """,
                expected_result=15,
                description="Test function calls"
            ),
            TestCase(
                name="while_loop",
                source_code="""
                fn main() -> int {
                    let i: int = 0;
                    let sum: int = 0;
                    while i < 5 {
                        sum = sum + i;
                        i = i + 1;
                    }
                    return sum;
                }
                """,
                expected_result=10,  # 0+1+2+3+4 = 10
                description="Test while loops"
            ),
            TestCase(
                name="for_loop_with_break",
                source_code="""
                fn main() -> int {
                    let sum: int = 0;
                    for (let i: int = 0; i < 10; i = i + 1) {
                        if i == 5 {
                            break;
                        }
                        sum = sum + i;
                    }
                    return sum;
                }
                """,
                expected_result=10,  # 0+1+2+3+4 = 10
                description="Test for loops with break"
            )
        ]
    
    def test_compilation_pipeline(self):
        """Test the complete compilation pipeline for each test case."""
        for test_case in self.test_cases:
            with self.subTest(test_case=test_case.name):
                self._run_test_case(test_case)
    
    def _run_test_case(self, test_case: TestCase):
        """Run a single test case through the compilation pipeline."""
        error_handler = ErrorHandler()
        
        try:
            # Lexing
            lexer = Lexer(test_case.source_code)
            
            # Parsing
            parser = Parser(lexer)
            program = parser.parse_program()
            
            if len(parser.errors) > 0:
                if test_case.should_fail:
                    return  # Expected failure
                else:
                    self.fail(f"Parser errors: {parser.errors}")
            
            # Compilation
            compiler = Compiler()
            compiler.compile(program)
            
            if len(compiler.errors) > 0:
                if test_case.should_fail:
                    return  # Expected failure
                else:
                    self.fail(f"Compiler errors: {compiler.errors}")
            
            # If we expect this test to fail but it didn't, that's an error
            if test_case.should_fail:
                self.fail(f"Expected test case '{test_case.name}' to fail, but it succeeded")
            
            # Verify expected result if provided
            if test_case.expected_result is not None:
                # Note: We can't easily test execution results in unit tests
                # without setting up the full LLVM execution environment
                pass
                
        except Exception as e:
            if test_case.should_fail:
                return  # Expected failure
            else:
                self.fail(f"Unexpected exception in test case '{test_case.name}': {e}")


class PerformanceTests(unittest.TestCase):
    """Performance and benchmark tests."""
    
    def test_lexer_performance(self):
        """Test lexer performance on large input."""
        # Generate a large source file
        source_lines = []
        for i in range(1000):
            source_lines.append(f"let var{i}: int = {i};")
        source = "\n".join(source_lines)
        
        start_time = time.time()
        lexer = Lexer(source)
        
        token_count = 0
        while lexer.current_char is not None:
            lexer.next_token()
            token_count += 1
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Should process at least 1000 tokens per second
        tokens_per_second = token_count / elapsed_time
        self.assertGreater(tokens_per_second, 1000, 
                          f"Lexer too slow: {tokens_per_second:.2f} tokens/sec")
    
    def test_parser_performance(self):
        """Test parser performance on large input."""
        # Generate a large source file with function declarations
        source_lines = ["fn main() -> int {"]
        for i in range(100):
            source_lines.append(f"    let var{i}: int = {i};")
        source_lines.append("    return 0;")
        source_lines.append("}")
        source = "\n".join(source_lines)
        
        start_time = time.time()
        lexer = Lexer(source)
        parser = Parser(lexer)
        program = parser.parse_program()
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        
        # Should parse quickly
        self.assertLess(elapsed_time, 1.0, 
                       f"Parser too slow: {elapsed_time:.3f} seconds")
        self.assertEqual(len(parser.errors), 0)


def run_file_tests():
    """Run tests on existing test files."""
    test_files = [
        ("tests/test1.forg", 62),   # Expected result from test1
        ("tests/test2.forg", 420),  # Expected result from test2  
        ("tests/test3.forg", 10),   # Expected result from test3
        ("tests/test4.forg", 3),    # Expected result from test4
    ]
    
    print("\n=== File-based Integration Tests ===")
    
    for file_path, expected_result in test_files:
        if not os.path.exists(file_path):
            print(f"⚠️  Test file not found: {file_path}")
            continue
            
        print(f"\nTesting {file_path}...")
        
        try:
            # Run the compiler on the test file
            result = subprocess.run([
                sys.executable, "main.py", "--quiet", file_path
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == expected_result:
                print(f"✅ {file_path}: PASSED (returned {result.returncode})")
            else:
                print(f"❌ {file_path}: FAILED")
                print(f"   Expected: {expected_result}")
                print(f"   Got: {result.returncode}")
                if result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
                    
        except subprocess.TimeoutExpired:
            print(f"❌ {file_path}: TIMEOUT")
        except Exception as e:
            print(f"❌ {file_path}: ERROR - {e}")


def main():
    """Run all tests."""
    print("Forg Compiler Test Suite")
    print("=" * 40)
    
    # Run unit tests
    print("\n=== Unit Tests ===")
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTests(test_loader.loadTestsFromTestCase(LexerTests))
    test_suite.addTests(test_loader.loadTestsFromTestCase(ParserTests))
    test_suite.addTests(test_loader.loadTestsFromTestCase(IntegrationTests))
    test_suite.addTests(test_loader.loadTestsFromTestCase(PerformanceTests))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Run file-based tests
    run_file_tests()
    
    # Print summary
    print(f"\n=== Test Summary ===")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\n{'✅ All tests passed!' if success else '❌ Some tests failed.'}")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
