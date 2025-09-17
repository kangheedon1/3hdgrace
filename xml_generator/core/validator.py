"""
XML Validator for BAS 29.3.1
============================

Validates generated XML against BAS standards and checks for common errors.
"""

import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Tuple
import logging
from .config import GeneratorConfig


class XMLValidator:
    """Validates BAS XML files for correctness and compatibility."""
    
    def __init__(self, config: GeneratorConfig):
        """Initialize validator with configuration."""
        self.config = config
        self.logger = logging.getLogger('XMLValidator')
        
        # Define BAS-specific validation rules
        self.required_elements = {'project', 'settings', 'macro'}
        self.valid_action_types = {
            'CallMacro', 'SetVariable', 'Click', 'Type', 'Navigate', 'WaitFor',
            'LoadAccounts', 'LoadShortsLinks', 'CreateUI', 'AddToggleButton',
            'RandomizeBrowser', 'SetProxy', 'Delay', 'LogEvent', 'AuditLog',
            'InitializeBrowser', 'ParseAccount', 'CreateInput', 'CreateFolder'
        }
        
        # Common XML error patterns
        self.error_patterns = {
            'mismatched_tag': r'<(\w+)[^>]*>.*?</(?!\1>)\w+>',
            'unclosed_tag': r'<(\w+)[^/>]*(?<!/)>(?!.*</\1>)',
            'malformed_attribute': r'<\w+[^>]*\s+\w+\s*=\s*[^"\'][^>]*>',
            'invalid_entity': r'&(?!amp;|lt;|gt;|quot;|apos;)[^;]+;',
        }
    
    def validate_xml(self, xml_content: str) -> Dict[str, Any]:
        """
        Comprehensive XML validation.
        
        Returns:
            Dictionary with validation results including errors and warnings
        """
        results = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'statistics': {},
            'recommendations': []
        }
        
        try:
            # Basic XML parsing validation
            self._validate_xml_syntax(xml_content, results)
            
            # BAS-specific validation
            if results['valid']:
                root = ET.fromstring(xml_content)
                self._validate_bas_structure(root, results)
                self._validate_bas_actions(root, results)
                self._validate_bas_settings(root, results)
                self._validate_macro_structure(root, results)
            
            # Performance and size validation
            self._validate_performance_metrics(xml_content, results)
            
            # Generate recommendations
            self._generate_recommendations(results)
            
        except ET.ParseError as e:
            results['errors'].append(f"XML Parse Error: {str(e)}")
            results['valid'] = False
        except Exception as e:
            results['errors'].append(f"Validation Error: {str(e)}")
            results['valid'] = False
        
        # Final validation status
        results['valid'] = len(results['errors']) == 0
        
        self.logger.info(f"Validation completed: {'PASSED' if results['valid'] else 'FAILED'}")
        return results
    
    def _validate_xml_syntax(self, xml_content: str, results: Dict[str, Any]):
        """Validate basic XML syntax."""
        try:
            ET.fromstring(xml_content)
            results['valid'] = True
        except ET.ParseError as e:
            results['errors'].append(f"XML Syntax Error: {str(e)}")
            results['valid'] = False
            
            # Try to identify specific error patterns
            for error_type, pattern in self.error_patterns.items():
                matches = re.findall(pattern, xml_content, re.IGNORECASE | re.DOTALL)
                if matches:
                    results['errors'].append(f"{error_type.replace('_', ' ').title()}: {len(matches)} instances found")
    
    def _validate_bas_structure(self, root: ET.Element, results: Dict[str, Any]):
        """Validate BAS-specific XML structure."""
        # Check root element
        if root.tag != 'project':
            results['errors'].append("Root element must be 'project'")
        
        # Check required attributes
        required_attrs = ['name', 'version']
        for attr in required_attrs:
            if attr not in root.attrib:
                results['errors'].append(f"Missing required attribute '{attr}' in project element")
        
        # Check BAS version compatibility
        version = root.get('version', '')
        if not version.startswith('29.'):
            results['warnings'].append(f"BAS version '{version}' may not be compatible with 29.3.1")
        
        # Check for required sections
        settings = root.find('settings')
        if settings is None:
            results['errors'].append("Missing required 'settings' section")
        
        macros = root.findall('macro')
        if not macros:
            results['warnings'].append("No macros found in project")
        
        # Validate project structure
        results['statistics']['total_macros'] = len(macros)
        results['statistics']['total_actions'] = len(root.findall('.//action'))
    
    def _validate_bas_actions(self, root: ET.Element, results: Dict[str, Any]):
        """Validate BAS action elements."""
        actions = root.findall('.//action')
        invalid_actions = []
        
        for action in actions:
            action_name = action.get('name', '')
            if action_name and action_name not in self.valid_action_types:
                invalid_actions.append(action_name)
        
        if invalid_actions:
            unique_invalid = list(set(invalid_actions))
            results['warnings'].append(f"Unknown action types found: {', '.join(unique_invalid)}")
        
        # Check for empty actions
        empty_actions = [action for action in actions if not action.get('name')]
        if empty_actions:
            results['errors'].append(f"Found {len(empty_actions)} actions without 'name' attribute")
    
    def _validate_bas_settings(self, root: ET.Element, results: Dict[str, Any]):
        """Validate BAS settings configuration."""
        settings = root.find('settings')
        if settings is None:
            return
        
        # Check critical settings
        max_threads = settings.find('MaxThreads')
        if max_threads is not None:
            try:
                threads = int(max_threads.text)
                if threads <= 0:
                    results['errors'].append("MaxThreads must be positive")
                elif threads > 1000:
                    results['warnings'].append(f"MaxThreads ({threads}) is very high, may cause performance issues")
            except (ValueError, TypeError):
                results['errors'].append("MaxThreads must be a valid integer")
        
        # Check thread delay
        thread_delay = settings.find('ThreadDelay')
        if thread_delay is not None:
            try:
                delay = int(thread_delay.text)
                if delay < 0:
                    results['errors'].append("ThreadDelay cannot be negative")
            except (ValueError, TypeError):
                results['errors'].append("ThreadDelay must be a valid integer")
    
    def _validate_macro_structure(self, root: ET.Element, results: Dict[str, Any]):
        """Validate macro structure and organization."""
        macros = root.findall('macro')
        macro_names = []
        
        for macro in macros:
            name = macro.get('name')
            if not name:
                results['errors'].append("Macro found without 'name' attribute")
                continue
                
            if name in macro_names:
                results['errors'].append(f"Duplicate macro name: '{name}'")
            macro_names.append(name)
            
            # Check macro actions
            actions = macro.findall('action')
            if not actions:
                results['warnings'].append(f"Macro '{name}' has no actions")
        
        results['statistics']['macro_names'] = macro_names
    
    def _validate_performance_metrics(self, xml_content: str, results: Dict[str, Any]):
        """Validate performance and size metrics."""
        file_size = len(xml_content.encode('utf-8'))
        file_size_mb = file_size / (1024 * 1024)
        
        results['statistics']['file_size_bytes'] = file_size
        results['statistics']['file_size_mb'] = file_size_mb
        
        # Check file size
        if file_size_mb > self.config.target_size_mb * 1.1:  # 10% tolerance
            results['warnings'].append(f"File size ({file_size_mb:.2f}MB) exceeds target ({self.config.target_size_mb}MB)")
        elif file_size_mb < self.config.target_size_mb * 0.5:  # Below 50% of target
            results['warnings'].append(f"File size ({file_size_mb:.2f}MB) is significantly below target ({self.config.target_size_mb}MB)")
        
        # Count lines and complexity
        lines = xml_content.split('\n')
        results['statistics']['total_lines'] = len(lines)
        results['statistics']['non_empty_lines'] = len([line for line in lines if line.strip()])
        
        # Check for overly complex elements
        complex_lines = [line for line in lines if len(line) > 200]
        if complex_lines:
            results['warnings'].append(f"Found {len(complex_lines)} very long lines that may impact readability")
    
    def _generate_recommendations(self, results: Dict[str, Any]):
        """Generate recommendations based on validation results."""
        recommendations = []
        
        if results['statistics'].get('total_macros', 0) == 0:
            recommendations.append("Consider adding macros to implement automation logic")
        
        if results['statistics'].get('total_actions', 0) < 10:
            recommendations.append("Project has very few actions - consider adding more automation steps")
        
        file_size_mb = results['statistics'].get('file_size_mb', 0)
        if file_size_mb < 1:
            recommendations.append("File size is small - consider adding more features or content")
        elif file_size_mb > 100:
            recommendations.append("Large file size - consider optimizing or splitting into modules")
        
        if len(results['warnings']) > 10:
            recommendations.append("Many warnings found - review and address to improve quality")
        
        if len(results['errors']) > 0:
            recommendations.append("Critical errors found - must be fixed before deployment")
        
        results['recommendations'] = recommendations
    
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """Validate XML file from disk."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
            return self.validate_xml(xml_content)
        except FileNotFoundError:
            return {
                'valid': False,
                'errors': [f"File not found: {file_path}"],
                'warnings': [],
                'statistics': {},
                'recommendations': []
            }
        except Exception as e:
            return {
                'valid': False,
                'errors': [f"Error reading file: {str(e)}"],
                'warnings': [],
                'statistics': {},
                'recommendations': []
            }
    
    def batch_validate(self, file_paths: List[str]) -> Dict[str, Dict[str, Any]]:
        """Validate multiple XML files."""
        results = {}
        for file_path in file_paths:
            results[file_path] = self.validate_file(file_path)
        return results
    
    def fix_common_errors(self, xml_content: str) -> Tuple[str, List[str]]:
        """Attempt to fix common XML errors automatically."""
        fixed_content = xml_content
        fixes_applied = []
        
        # Fix unclosed tags (basic cases)
        self_closing_tags = ['input', 'img', 'br', 'hr']
        for tag in self_closing_tags:
            pattern = f'<{tag}([^>]*)>(?!</{tag}>)'
            replacement = f'<{tag}\\1/>'
            if re.search(pattern, fixed_content, re.IGNORECASE):
                fixed_content = re.sub(pattern, replacement, fixed_content, flags=re.IGNORECASE)
                fixes_applied.append(f"Auto-closed {tag} tags")
        
        # Fix entity encoding issues
        entity_fixes = {
            r'&(?!amp;|lt;|gt;|quot;|apos;)': '&amp;',
            r'<(?![!/?\w])': '&lt;',
            r'>(?<![!/?\w])': '&gt;'
        }
        
        for pattern, replacement in entity_fixes.items():
            if re.search(pattern, fixed_content):
                fixed_content = re.sub(pattern, replacement, fixed_content)
                fixes_applied.append(f"Fixed entity encoding: {pattern}")
        
        return fixed_content, fixes_applied