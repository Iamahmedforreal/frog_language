"""
Environment Module for Forg Language Compiler

This module provides the Environment class which acts as a symbol table
for managing variable and function scopes during compilation.
"""

from llvmlite import ir
from typing import Optional, Tuple

class Environment:
    """
    Symbol Table for managing variable and function scopes.
    
    This class implements a hierarchical symbol table that supports
    nested scopes through parent-child relationships.
    
    Attributes:
        records: Dictionary mapping names to (value, type) tuples
        parent: Parent environment for nested scopes
        name: Name identifier for this environment scope
    """
    def __init__(self, records: Optional[dict[str, Tuple[ir.Value, ir.Type]]] = None, 
                 parent: Optional['Environment'] = None, name: str = "global") -> None:
        self.records: dict[str, Tuple[ir.Value, ir.Type]] = records if records else {}
        self.parent: Optional['Environment'] = parent
        self.name: str = name

    def define(self, name: str, value: ir.Value, _type: ir.Type) -> ir.Value:
        """
        Define a new symbol in this environment.
        
        Args:
            name: Symbol name
            value: LLVM IR value
            _type: LLVM IR type
            
        Returns:
            The stored value
        """
        self.records[name] = (value, _type)
        return value
    
    def lookup(self, name: str) -> Optional[Tuple[ir.Value, ir.Type]]:
        """
        Look up a symbol in this environment or parent environments.
        
        Args:
            name: Symbol name to look up
            
        Returns:
            Tuple of (value, type) if found, None otherwise
        """
        return self.__resolve(name)
    
    def __resolve(self, name: str) -> Optional[Tuple[ir.Value, ir.Type]]:
        """
        Recursively resolve a symbol name through the environment chain.
        
        Args:
            name: Symbol name to resolve
            
        Returns:
            Tuple of (value, type) if found, None otherwise
        """
        if name in self.records:
            return self.records[name]
        elif self.parent:
            return self.parent.__resolve(name)
        else:
            return None