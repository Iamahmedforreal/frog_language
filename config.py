"""
Configuration Module for Forg Language Compiler

This module provides centralized configuration management for the compiler,
including debug flags, optimization levels, and output settings.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import os


class OptimizationLevel(Enum):
    """LLVM optimization levels."""
    O0 = 0  # No optimization
    O1 = 1  # Basic optimization
    O2 = 2  # Standard optimization
    O3 = 3  # Aggressive optimization


class OutputFormat(Enum):
    """Supported output formats."""
    EXECUTABLE = "executable"
    OBJECT = "object"
    ASSEMBLY = "assembly"
    LLVM_IR = "llvm-ir"
    BITCODE = "bitcode"


@dataclass
class CompilerConfig:
    """
    Comprehensive configuration for the Forg compiler.
    
    This class centralizes all compiler settings and provides
    sensible defaults for all configuration options.
    """
    
    # Input/Output settings
    input_file: Optional[str] = None
    output_file: Optional[str] = None
    output_format: OutputFormat = OutputFormat.EXECUTABLE
    
    # Debug flags
    lexer_debug: bool = False
    parser_debug: bool = False
    compiler_debug: bool = False
    ast_debug: bool = False
    ir_debug: bool = False
    
    # Execution settings
    run_code: bool = True
    benchmark: bool = False
    
    # Optimization settings
    optimization_level: OptimizationLevel = OptimizationLevel.O0
    
    # Output directories
    debug_dir: str = "debug"
    output_dir: str = "output"
    
    # File extensions
    source_extension: str = ".forg"
    
    # Verbose output
    verbose: bool = False
    quiet: bool = False
    
    # Error handling
    max_errors: int = 10
    warnings_as_errors: bool = False
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        # Create debug directory if it doesn't exist
        if not os.path.exists(self.debug_dir):
            os.makedirs(self.debug_dir)
            
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    @classmethod
    def from_args(cls, args) -> 'CompilerConfig':
        """Create configuration from command line arguments."""
        config = cls()
        
        # Set values from args if they exist
        if hasattr(args, 'input') and args.input:
            config.input_file = args.input
        if hasattr(args, 'output') and args.output:
            config.output_file = args.output
        if hasattr(args, 'debug_lexer'):
            config.lexer_debug = args.debug_lexer
        if hasattr(args, 'debug_parser'):
            config.parser_debug = args.debug_parser
        if hasattr(args, 'debug_compiler'):
            config.compiler_debug = args.debug_compiler
        if hasattr(args, 'verbose'):
            config.verbose = args.verbose
        if hasattr(args, 'quiet'):
            config.quiet = args.quiet
        if hasattr(args, 'optimization'):
            config.optimization_level = OptimizationLevel(args.optimization)
        if hasattr(args, 'no_run'):
            config.run_code = not args.no_run
        if hasattr(args, 'benchmark'):
            config.benchmark = args.benchmark
            
        return config
    
    def get_ast_output_path(self) -> str:
        """Get the path for AST debug output."""
        return os.path.join(self.debug_dir, "ast.json")
    
    def get_ir_output_path(self) -> str:
        """Get the path for LLVM IR debug output."""
        return os.path.join(self.debug_dir, "ir.ll")
    
    def get_output_path(self) -> str:
        """Get the final output path based on configuration."""
        if self.output_file:
            return self.output_file
            
        if self.input_file:
            base_name = os.path.splitext(os.path.basename(self.input_file))[0]
            
            if self.output_format == OutputFormat.EXECUTABLE:
                extension = ".exe" if os.name == 'nt' else ""
            elif self.output_format == OutputFormat.OBJECT:
                extension = ".o"
            elif self.output_format == OutputFormat.ASSEMBLY:
                extension = ".s"
            elif self.output_format == OutputFormat.LLVM_IR:
                extension = ".ll"
            elif self.output_format == OutputFormat.BITCODE:
                extension = ".bc"
            else:
                extension = ""
                
            return os.path.join(self.output_dir, f"{base_name}{extension}")
        
        return os.path.join(self.output_dir, "output")
    
    def should_print(self, level: str = "info") -> bool:
        """Check if output should be printed based on verbosity settings."""
        if self.quiet:
            return level == "error"
        if self.verbose:
            return True
        return level in ["info", "warning", "error"]


# Default global configuration
config = CompilerConfig()
