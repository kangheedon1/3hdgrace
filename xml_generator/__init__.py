"""
BAS 29.3.1 Premium XML Generator System
=======================================

A modular, high-performance XML generator for BrowserAutomationStudio 29.3.1 Premium
supporting large-scale automation projects with up to 700MB output capability.

Features:
- Modular architecture for maintainability
- Full BAS 29.3.1 compatibility
- 124+ automation features
- Large-scale XML generation
- Comprehensive logging and validation
- Statistics and reporting
"""

__version__ = "1.0.0"
__author__ = "HDGRACE Team"
__license__ = "MIT"

from .core.generator import XMLGenerator
from .core.config import GeneratorConfig
from .core.validator import XMLValidator

__all__ = ['XMLGenerator', 'GeneratorConfig', 'XMLValidator']