"""
Core XML Generator Components
============================

Contains the base classes and core functionality for the BAS XML generator.
"""

from .generator import XMLGenerator
from .config import GeneratorConfig
from .validator import XMLValidator
from .template_engine import TemplateEngine

__all__ = ['XMLGenerator', 'GeneratorConfig', 'XMLValidator', 'TemplateEngine']