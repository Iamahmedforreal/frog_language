"""
Error Handling Module for Forg Language Compiler

This module provides comprehensive error handling and reporting
capabilities for the Forg compiler pipeline.
"""

from enum import Enum
from typing import List, Optional
from dataclasses import dataclass


class ErrorType(Enum):
    """Types of errors that can occur during compilation."""
    LEXICAL = "Lexical Error"
    SYNTAX = "Syntax Error"
    SEMANTIC = "Semantic Error"
    TYPE = "Type Error"
    RUNTIME = "Runtime Error"
    INTERNAL = "Internal Compiler Error"


@dataclass
class CompilerError:
    """
    Represents a compiler error with detailed information.
    
    Attributes:
        error_type: Type of error
        message: Error description
        line_no: Line number where error occurred
        position: Character position in line
        source_file: Source file name (optional)
        suggestion: Suggested fix (optional)
    """
    error_type: ErrorType
    message: str
    line_no: int
    position: int = 0
    source_file: Optional[str] = None
    suggestion: Optional[str] = None
    
    def __str__(self) -> str:
        """Format error for display."""
        location = f"Line {self.line_no}"
        if self.position > 0:
            location += f", Column {self.position}"
        if self.source_file:
            location = f"{self.source_file}:{location}"
            
        error_msg = f"{self.error_type.value} at {location}: {self.message}"
        
        if self.suggestion:
            error_msg += f"\n  Suggestion: {self.suggestion}"
            
        return error_msg


class ErrorHandler:
    """
    Centralized error handling and reporting system.
    """
    
    def __init__(self):
        self.errors: List[CompilerError] = []
        self.warnings: List[CompilerError] = []
        
    def add_error(self, error_type: ErrorType, message: str, line_no: int, 
                  position: int = 0, source_file: Optional[str] = None,
                  suggestion: Optional[str] = None) -> None:
        """Add a new error to the error list."""
        error = CompilerError(
            error_type=error_type,
            message=message,
            line_no=line_no,
            position=position,
            source_file=source_file,
            suggestion=suggestion
        )
        self.errors.append(error)
        
    def add_warning(self, message: str, line_no: int, 
                   position: int = 0, source_file: Optional[str] = None) -> None:
        """Add a new warning to the warning list."""
        warning = CompilerError(
            error_type=ErrorType.SEMANTIC,  # Warnings are typically semantic
            message=message,
            line_no=line_no,
            position=position,
            source_file=source_file
        )
        self.warnings.append(warning)
        
    def has_errors(self) -> bool:
        """Check if any errors have been recorded."""
        return len(self.errors) > 0
        
    def has_warnings(self) -> bool:
        """Check if any warnings have been recorded."""
        return len(self.warnings) > 0
        
    def get_error_count(self) -> int:
        """Get the total number of errors."""
        return len(self.errors)
        
    def get_warning_count(self) -> int:
        """Get the total number of warnings."""
        return len(self.warnings)
        
    def print_errors(self) -> None:
        """Print all errors to stdout."""
        if self.has_errors():
            print(f"\n{self.get_error_count()} error(s) found:")
            for error in self.errors:
                print(f"  {error}")
                
    def print_warnings(self) -> None:
        """Print all warnings to stdout."""
        if self.has_warnings():
            print(f"\n{self.get_warning_count()} warning(s) found:")
            for warning in self.warnings:
                print(f"  {warning}")
                
    def print_summary(self) -> None:
        """Print a summary of all errors and warnings."""
        self.print_errors()
        self.print_warnings()
        
        if not self.has_errors() and not self.has_warnings():
            print("No errors or warnings found.")
        elif not self.has_errors():
            print("Compilation successful with warnings.")
        else:
            print("Compilation failed due to errors.")
            
    def clear(self) -> None:
        """Clear all errors and warnings."""
        self.errors.clear()
        self.warnings.clear()


# Global error handler instance
error_handler = ErrorHandler()
