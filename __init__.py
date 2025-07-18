"""
Custom Interval Resolution System

This package provides custom interval functionality that extends ResolutionEnum.MINUTE
to support specific minute intervals with ranges of 1, 10, 15, 30, and 60 minutes.

Main exports:
- ResolutionEnum: Backward-compatible resolution enumeration
- IntervalEnum: Granular minute intervals  
- IntervalConverter: Utility functions for conversion and validation
- create_interval_config: Configuration helper function
- validate_interval_compatibility: Compatibility validation
"""

from .interval_resolution import (
    ResolutionEnum,
    IntervalEnum, 
    IntervalConverter,
    create_interval_config,
    validate_interval_compatibility,
    Resolution  # Backward compatibility alias
)

__version__ = "1.0.0"
__author__ = "TUTUT MARTAMTI"

__all__ = [
    "ResolutionEnum",
    "IntervalEnum",
    "IntervalConverter", 
    "create_interval_config",
    "validate_interval_compatibility",
    "Resolution"
]