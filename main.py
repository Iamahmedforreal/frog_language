"""
Forg Language Compiler - Main Entry Point

A custom programming language compiler that lexes, parses, and compiles
Forg source code to LLVM IR with JIT execution capabilities.

Usage:
    python main.py [options] [input_file]
    
Examples:
    python main.py tests/test3.forg
    python main.py --debug-all tests/test1.forg
    python main.py --no-run --output program.exe tests/test2.forg
"""

import argparse
import json
import os
import sys
import time
from ctypes import CFUNCTYPE, c_int
from typing import Optional

from llvmlite import ir
import llvmlite.binding as llvm

from lexer import Lexer 
from parser import Parser
from compiler import Compiler
from AST import Program
from config import CompilerConfig, OptimizationLevel
from error_handler import error_handler, ErrorType

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Forg Language Compiler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s tests/test3.forg                    # Compile and run
  %(prog)s --debug-all tests/test1.forg       # Enable all debug output
  %(prog)s --no-run -o program tests/test2.forg  # Compile only
  %(prog)s --benchmark tests/test4.forg       # Run with benchmarking
        """
    )
    
    # Input/Output
    parser.add_argument('input', nargs='?', default="tests/test3.forg",
                       help='Input Forg source file (default: tests/test3.forg)')
    parser.add_argument('-o', '--output', 
                       help='Output file name')
    
    # Debug options
    debug_group = parser.add_argument_group('debug options')
    debug_group.add_argument('--debug-lexer', action='store_true',
                           help='Enable lexer debug output')
    debug_group.add_argument('--debug-parser', action='store_true',
                           help='Enable parser debug output (saves AST to debug/ast.json)')
    debug_group.add_argument('--debug-compiler', action='store_true',
                           help='Enable compiler debug output (saves IR to debug/ir.ll)')
    debug_group.add_argument('--debug-all', action='store_true',
                           help='Enable all debug output')
    
    # Execution options
    exec_group = parser.add_argument_group('execution options')
    exec_group.add_argument('--no-run', action='store_true',
                          help='Compile only, do not execute')
    exec_group.add_argument('--benchmark', action='store_true',
                          help='Enable benchmarking output')
    
    # Optimization
    parser.add_argument('-O', '--optimization', type=int, choices=[0, 1, 2, 3],
                       default=0, help='Optimization level (default: 0)')
    
    # Output control
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='Quiet output (errors only)')
    
    args = parser.parse_args()
    
    # Handle --debug-all flag
    if args.debug_all:
        args.debug_lexer = True
        args.debug_parser = True
        args.debug_compiler = True
    
    return args


def load_source_file(file_path: str) -> Optional[str]:
    """Load source code from file with error handling."""
    try:
        if not os.path.exists(file_path):
            error_handler.add_error(
                ErrorType.INTERNAL,
                f"Source file '{file_path}' not found",
                0,
                source_file=file_path,
                suggestion="Check the file path and ensure the file exists"
            )
            return None
            
        with open(file_path, "r", encoding='utf-8') as f:
            return f.read()
            
    except IOError as e:
        error_handler.add_error(
            ErrorType.INTERNAL,
            f"Failed to read source file: {e}",
            0,
            source_file=file_path
        )
        return None


def run_lexer_debug(source: str, config: CompilerConfig) -> None:
    """Run lexer in debug mode."""
    if config.should_print("debug"):
        print("==== LEXER DEBUG ====")
        
    debug_lex = Lexer(source=source)
    token_count = 0
    
    while debug_lex.current_char is not None:
        token = debug_lex.next_token()
        if config.should_print("debug"):
            print(f"  {token}")
        token_count += 1
        
    if config.should_print("info"):
        print(f"Lexer processed {token_count} tokens")


def run_parser(source: str, config: CompilerConfig) -> Optional[Program]:
    """Run parser with error handling."""
    lexer = Lexer(source=source)
    parser = Parser(lexer=lexer)
    
    program = parser.parse_program()
    
    # Handle parser errors
    if len(parser.errors) > 0:
        for err in parser.errors:
            error_handler.add_error(
                ErrorType.SYNTAX,
                err,
                0,  # Parser errors don't have line numbers yet
                source_file=config.input_file
            )
        return None
    
    # Save AST debug output
    if config.parser_debug:
        try:
            ast_path = config.get_ast_output_path()
            with open(ast_path, "w") as f:
                json.dump(program.json(), f, indent=4)
            
            if config.should_print("info"):
                print(f"AST saved to {ast_path}")
        except IOError as e:
            error_handler.add_warning(
                f"Failed to save AST debug output: {e}",
                0,
                source_file=config.input_file
            )
    
    if config.should_print("info"):
        print(f"Parser processed {len(program.statements)} statements")
    
    return program


def run_compiler(program: Program, config: CompilerConfig) -> Optional[ir.Module]:
    """Run compiler with error handling."""
    compiler = Compiler()
    compiler.compile(node=program)
    
    # Handle compiler errors
    if len(compiler.errors) > 0:
        for err in compiler.errors:
            error_handler.add_error(
                ErrorType.SEMANTIC,
                err,
                0,
                source_file=config.input_file
            )
        return None
    
    module = compiler.module
    module.triple = llvm.get_default_triple()
    
    # Save IR debug output
    if config.compiler_debug:
        try:
            ir_path = config.get_ir_output_path()
            with open(ir_path, "w") as f:
                f.write(str(module))
            
            if config.should_print("info"):
                print(f"LLVM IR saved to {ir_path}")
        except IOError as e:
            error_handler.add_warning(
                f"Failed to save IR debug output: {e}",
                0,
                source_file=config.input_file
            )
    
    if config.should_print("info"):
        print("Compilation to LLVM IR successful")
    
    return module


def execute_program(module: ir.Module, config: CompilerConfig) -> Optional[int]:
    """Execute the compiled program with JIT."""
    if not config.run_code:
        return None
        
    try:
        # Initialize LLVM
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        
        # Parse and verify IR
        llvm_ir_parsed = llvm.parse_assembly(str(module))
        llvm_ir_parsed.verify()
        
        # Create execution engine
        target_machine = llvm.Target.from_default_triple().create_target_machine()
        engine = llvm.create_mcjit_compiler(llvm_ir_parsed, target_machine)
        engine.finalize_object()
        
        # Get main function
        entry = engine.get_function_address('main')
        if entry == 0:
            error_handler.add_error(
                ErrorType.SEMANTIC,
                "No 'main' function found in program",
                0,
                source_file=config.input_file,
                suggestion="Add a 'main' function that returns an integer"
            )
            return None
        
        efunc = CFUNCTYPE(c_int)(entry)
        
        # Execute with timing
        start_time = time.time()
        result = efunc()
        end_time = time.time()
        
        execution_time_ms = round((end_time - start_time) * 1000, 2)
        
        if config.should_print("info"):
            print(f"\nProgram executed successfully")
            print(f"  Return value: {result}")
            
        if config.benchmark or config.should_print("debug"):
            print(f"  Execution time: {execution_time_ms} ms")
        
        return result
        
    except Exception as e:
        error_handler.add_error(
            ErrorType.RUNTIME,
            f"Execution failed: {e}",
            0,
            source_file=config.input_file
        )
        return None


def main() -> int:
    """Main compiler entry point."""
    args = parse_arguments()
    config = CompilerConfig.from_args(args)
    
    if config.should_print("info"):
        print(f"Forg Language Compiler")
        print(f"Input: {config.input_file}")
    
    # Load source file
    source = load_source_file(config.input_file)
    if source is None:
        error_handler.print_summary()
        return 1
    
    # Run lexer debug if requested
    if config.lexer_debug:
        run_lexer_debug(source, config)
    
    # Parse source code
    program = run_parser(source, config)
    if program is None:
        error_handler.print_summary()
        return 1
    
    # Compile to LLVM IR
    module = run_compiler(program, config)
    if module is None:
        error_handler.print_summary()
        return 1
    
    # Execute program
    result = execute_program(module, config)
    
    # Print summary
    error_handler.print_summary()
    
    if error_handler.has_errors():
        return 1
    
    return 0 if result is None else result


if __name__ == '__main__':
    sys.exit(main())
