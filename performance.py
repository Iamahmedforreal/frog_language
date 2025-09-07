"""
Performance Monitoring and Optimization Module for Forg Compiler

This module provides performance monitoring, profiling, and optimization
capabilities for the Forg language compiler.
"""

import time
import sys
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from contextlib import contextmanager
import json


@dataclass
class PerformanceMetrics:
    """Container for performance metrics."""
    lexing_time: float = 0.0
    parsing_time: float = 0.0
    compilation_time: float = 0.0
    execution_time: float = 0.0
    total_time: float = 0.0
    
    tokens_processed: int = 0
    ast_nodes_created: int = 0
    ir_instructions_generated: int = 0
    
    memory_usage_mb: float = 0.0
    peak_memory_mb: float = 0.0
    
    def __post_init__(self):
        """Calculate derived metrics."""
        self.total_time = (self.lexing_time + self.parsing_time + 
                          self.compilation_time + self.execution_time)
    
    def tokens_per_second(self) -> float:
        """Calculate tokens processed per second."""
        if self.lexing_time > 0:
            return self.tokens_processed / self.lexing_time
        return 0.0
    
    def nodes_per_second(self) -> float:
        """Calculate AST nodes created per second."""
        if self.parsing_time > 0:
            return self.ast_nodes_created / self.parsing_time
        return 0.0
    
    def instructions_per_second(self) -> float:
        """Calculate IR instructions generated per second."""
        if self.compilation_time > 0:
            return self.ir_instructions_generated / self.compilation_time
        return 0.0


class PerformanceProfiler:
    """
    Performance profiler for the Forg compiler.
    
    Provides timing, memory usage tracking, and performance analysis.
    """
    
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.phase_times: Dict[str, float] = {}
        self.start_times: Dict[str, float] = {}
        self.enabled = False
        
    def enable(self):
        """Enable performance profiling."""
        self.enabled = True
        
    def disable(self):
        """Disable performance profiling."""
        self.enabled = False
    
    @contextmanager
    def time_phase(self, phase_name: str):
        """Context manager for timing compilation phases."""
        if not self.enabled:
            yield
            return
            
        start_time = time.time()
        try:
            yield
        finally:
            end_time = time.time()
            elapsed = end_time - start_time
            self.phase_times[phase_name] = elapsed
            
            # Update metrics based on phase
            if phase_name == "lexing":
                self.metrics.lexing_time = elapsed
            elif phase_name == "parsing":
                self.metrics.parsing_time = elapsed
            elif phase_name == "compilation":
                self.metrics.compilation_time = elapsed
            elif phase_name == "execution":
                self.metrics.execution_time = elapsed
    
    def record_tokens(self, count: int):
        """Record number of tokens processed."""
        self.metrics.tokens_processed = count
    
    def record_ast_nodes(self, count: int):
        """Record number of AST nodes created."""
        self.metrics.ast_nodes_created = count
    
    def record_ir_instructions(self, count: int):
        """Record number of IR instructions generated."""
        self.metrics.ir_instructions_generated = count
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            memory_mb = process.memory_info().rss / 1024 / 1024
            self.metrics.memory_usage_mb = memory_mb
            if memory_mb > self.metrics.peak_memory_mb:
                self.metrics.peak_memory_mb = memory_mb
            return memory_mb
        except ImportError:
            # psutil not available, return 0
            return 0.0
    
    def print_summary(self, verbose: bool = False):
        """Print performance summary."""
        if not self.enabled:
            return
            
        print("\n" + "="*50)
        print("PERFORMANCE SUMMARY")
        print("="*50)
        
        # Timing breakdown
        print(f"Lexing:      {self.metrics.lexing_time*1000:8.2f} ms")
        print(f"Parsing:     {self.metrics.parsing_time*1000:8.2f} ms")
        print(f"Compilation: {self.metrics.compilation_time*1000:8.2f} ms")
        print(f"Execution:   {self.metrics.execution_time*1000:8.2f} ms")
        print(f"Total:       {self.metrics.total_time*1000:8.2f} ms")
        
        # Throughput metrics
        if verbose:
            print("\nThroughput:")
            if self.metrics.tokens_processed > 0:
                print(f"Tokens/sec:       {self.metrics.tokens_per_second():8.0f}")
            if self.metrics.ast_nodes_created > 0:
                print(f"AST nodes/sec:    {self.metrics.nodes_per_second():8.0f}")
            if self.metrics.ir_instructions_generated > 0:
                print(f"IR instrs/sec:    {self.metrics.instructions_per_second():8.0f}")
        
        # Memory usage
        if self.metrics.memory_usage_mb > 0:
            print(f"\nMemory Usage:")
            print(f"Current:     {self.metrics.memory_usage_mb:8.2f} MB")
            print(f"Peak:        {self.metrics.peak_memory_mb:8.2f} MB")
        
        print("="*50)
    
    def save_metrics(self, filename: str):
        """Save metrics to JSON file."""
        if not self.enabled:
            return
            
        metrics_dict = {
            'timing': {
                'lexing_ms': self.metrics.lexing_time * 1000,
                'parsing_ms': self.metrics.parsing_time * 1000,
                'compilation_ms': self.metrics.compilation_time * 1000,
                'execution_ms': self.metrics.execution_time * 1000,
                'total_ms': self.metrics.total_time * 1000
            },
            'throughput': {
                'tokens_processed': self.metrics.tokens_processed,
                'ast_nodes_created': self.metrics.ast_nodes_created,
                'ir_instructions_generated': self.metrics.ir_instructions_generated,
                'tokens_per_second': self.metrics.tokens_per_second(),
                'nodes_per_second': self.metrics.nodes_per_second(),
                'instructions_per_second': self.metrics.instructions_per_second()
            },
            'memory': {
                'current_mb': self.metrics.memory_usage_mb,
                'peak_mb': self.metrics.peak_memory_mb
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(metrics_dict, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save metrics to {filename}: {e}")


class CompilerOptimizer:
    """
    Compiler optimization utilities.
    
    Provides various optimization techniques for the Forg compiler.
    """
    
    @staticmethod
    def optimize_ast(program):
        """
        Apply AST-level optimizations.
        
        This is a placeholder for future optimizations like:
        - Constant folding
        - Dead code elimination
        - Expression simplification
        """
        # TODO: Implement AST optimizations
        return program
    
    @staticmethod
    def optimize_ir(module):
        """
        Apply LLVM IR-level optimizations.
        
        Uses LLVM's built-in optimization passes.
        """
        try:
            import llvmlite.binding as llvm
            
            # Create pass manager
            pmb = llvm.create_pass_manager_builder()
            pmb.opt_level = 2  # -O2 optimization level
            pmb.size_level = 0  # Don't optimize for size
            
            # Create module pass manager
            pm = llvm.create_module_pass_manager()
            pmb.populate(pm)
            
            # Run optimization passes
            pm.run(module)
            
            return module
        except Exception as e:
            print(f"Warning: IR optimization failed: {e}")
            return module


# Global profiler instance
profiler = PerformanceProfiler()


def benchmark_file(file_path: str, iterations: int = 5) -> Dict[str, float]:
    """
    Benchmark compilation of a specific file.
    
    Args:
        file_path: Path to the Forg source file
        iterations: Number of iterations to run
        
    Returns:
        Dictionary with average timing results
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Benchmark file not found: {file_path}")
    
    print(f"Benchmarking {file_path} ({iterations} iterations)...")
    
    times = {
        'lexing': [],
        'parsing': [],
        'compilation': [],
        'total': []
    }
    
    for i in range(iterations):
        # Import here to avoid circular imports
        from lexer import Lexer
        from parser import Parser
        from compiler import Compiler
        
        # Read source
        with open(file_path, 'r') as f:
            source = f.read()
        
        # Time lexing
        start = time.time()
        lexer = Lexer(source)
        tokens = []
        while lexer.current_char is not None:
            tokens.append(lexer.next_token())
        lexing_time = time.time() - start
        times['lexing'].append(lexing_time)
        
        # Time parsing
        start = time.time()
        lexer = Lexer(source)
        parser = Parser(lexer)
        program = parser.parse_program()
        parsing_time = time.time() - start
        times['parsing'].append(parsing_time)
        
        if len(parser.errors) > 0:
            print(f"Parsing errors in iteration {i+1}: {parser.errors}")
            continue
        
        # Time compilation
        start = time.time()
        compiler = Compiler()
        compiler.compile(program)
        compilation_time = time.time() - start
        times['compilation'].append(compilation_time)
        
        total_time = lexing_time + parsing_time + compilation_time
        times['total'].append(total_time)
    
    # Calculate averages
    averages = {}
    for phase, phase_times in times.items():
        if phase_times:
            averages[phase] = sum(phase_times) / len(phase_times)
        else:
            averages[phase] = 0.0
    
    # Print results
    print(f"Average times over {iterations} iterations:")
    print(f"  Lexing:      {averages['lexing']*1000:6.2f} ms")
    print(f"  Parsing:     {averages['parsing']*1000:6.2f} ms")
    print(f"  Compilation: {averages['compilation']*1000:6.2f} ms")
    print(f"  Total:       {averages['total']*1000:6.2f} ms")
    
    return averages


def run_performance_suite():
    """Run a comprehensive performance test suite."""
    print("Forg Compiler Performance Suite")
    print("="*40)
    
    test_files = [
        "tests/test1.forg",
        "tests/test2.forg", 
        "tests/test3.forg",
        "tests/test4.forg"
    ]
    
    # Add new test files if they exist
    additional_tests = [
        "tests/test_power.forg",
        "tests/test_factorial.forg",
        "tests/test_complex.forg"
    ]
    
    for test_file in additional_tests:
        if os.path.exists(test_file):
            test_files.append(test_file)
    
    results = {}
    
    for test_file in test_files:
        if os.path.exists(test_file):
            try:
                results[test_file] = benchmark_file(test_file, iterations=3)
                print()
            except Exception as e:
                print(f"Error benchmarking {test_file}: {e}")
                print()
    
    # Summary
    if results:
        print("Performance Summary:")
        print("-" * 40)
        total_avg = 0
        count = 0
        
        for file_path, timings in results.items():
            filename = os.path.basename(file_path)
            total_time = timings.get('total', 0) * 1000
            print(f"{filename:20} {total_time:6.2f} ms")
            total_avg += total_time
            count += 1
        
        if count > 0:
            print("-" * 40)
            print(f"{'Average:':20} {total_avg/count:6.2f} ms")


if __name__ == '__main__':
    run_performance_suite()

