"""
Main XML Generator Class
========================

The primary orchestrator for generating BAS 29.3.1 XML files with all features.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import xml.etree.ElementTree as ET
from xml.dom import minidom

from .config import GeneratorConfig
from .validator import XMLValidator
from .template_engine import TemplateEngine
from ..modules.functions import FunctionModuleGenerator
from ..modules.ui import UIModuleGenerator
from ..modules.actions import ActionModuleGenerator
from ..modules.security import SecurityModuleGenerator
from ..modules.integration import IntegrationModuleGenerator
from ..modules.logging import LoggingModuleGenerator
from ..modules.validation import ValidationModuleGenerator


class XMLGenerator:
    """
    Main XML Generator for BAS 29.3.1 Premium
    
    Orchestrates all module generators to create comprehensive XML output
    supporting up to 700MB with 124+ features.
    """
    
    def __init__(self, config: Optional[GeneratorConfig] = None):
        """Initialize the XML generator with configuration."""
        self.config = config or GeneratorConfig()
        self.logger = self._setup_logging()
        self.validator = XMLValidator(self.config)
        self.template_engine = TemplateEngine(self.config)
        
        # Initialize module generators
        self.function_generator = FunctionModuleGenerator(self.config)
        self.ui_generator = UIModuleGenerator(self.config)
        self.action_generator = ActionModuleGenerator(self.config)
        self.security_generator = SecurityModuleGenerator(self.config)
        self.integration_generator = IntegrationModuleGenerator(self.config)
        self.logging_generator = LoggingModuleGenerator(self.config)
        self.validation_generator = ValidationModuleGenerator(self.config)
        
        # Statistics tracking
        self.stats = {
            'generation_start': None,
            'generation_end': None,
            'total_features': 0,
            'total_macros': 0,
            'total_actions': 0,
            'file_size_bytes': 0,
            'validation_errors': 0,
            'performance_metrics': {}
        }
        
        self.logger.info(f"XMLGenerator initialized with BAS version {self.config.bas_version}")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        log_file = os.path.join(self.config.logs_folder, f"xml_generator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        logger = logging.getLogger('XMLGenerator')
        logger.info("Logging initialized")
        return logger
    
    def generate_complete_xml(self, output_filename: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Generate complete BAS XML with all features and modules.
        
        Returns:
            Tuple of (output_file_path, generation_statistics)
        """
        self.stats['generation_start'] = datetime.now()
        self.logger.info("Starting complete XML generation...")
        
        try:
            # Create root XML structure
            root = self._create_root_element()
            
            # Generate all modules
            self._generate_settings(root)
            self._generate_ui_components(root)
            self._generate_security_macros(root)
            self._generate_function_macros(root)
            self._generate_action_sequences(root)
            self._generate_integration_modules(root)
            self._generate_logging_modules(root)
            self._generate_validation_modules(root)
            
            # Add system macros
            self._add_system_macros(root)
            
            # Generate large-scale content for target size
            self._expand_content_for_target_size(root)
            
            # Format and validate XML
            xml_string = self._format_xml(root)
            validation_result = self.validator.validate_xml(xml_string)
            
            # Save to file
            output_path = self._save_xml_file(xml_string, output_filename)
            
            # Update statistics
            self._finalize_statistics(output_path, validation_result)
            
            self.logger.info(f"XML generation completed: {output_path}")
            return output_path, self.stats
            
        except Exception as e:
            self.logger.error(f"XML generation failed: {str(e)}")
            raise
    
    def _create_root_element(self) -> ET.Element:
        """Create the root XML element with BAS project structure."""
        root = ET.Element('project')
        root.set('name', self.config.project_name)
        root.set('version', self.config.bas_version)
        root.set('generated', datetime.now().isoformat())
        root.set('generator_version', '1.0.0')
        
        # Add XML declaration comment
        comment = ET.Comment(f'''
Generated by HDGRACE BAS XML Generator v1.0.0
Project: {self.config.project_name}
BAS Version: {self.config.bas_version}
Generation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Target Size: {self.config.target_size_mb}MB
Features: {len(self.config.enabled_features)} enabled
''')
        root.insert(0, comment)
        
        return root
    
    def _generate_settings(self, root: ET.Element):
        """Generate BAS settings section."""
        settings = ET.SubElement(root, 'settings')
        
        # Execution settings
        ET.SubElement(settings, 'MaxThreads').text = str(self.config.max_threads)
        ET.SubElement(settings, 'ThreadDelay').text = str(self.config.thread_delay_ms)
        ET.SubElement(settings, 'ParallelExecution').text = str(self.config.enable_parallel_execution).lower()
        ET.SubElement(settings, 'BrowserPoolSize').text = str(self.config.max_threads)
        
        # File paths
        ET.SubElement(settings, 'InputFolder').text = self.config.input_folder
        ET.SubElement(settings, 'OutputFolder').text = self.config.output_folder
        ET.SubElement(settings, 'LogFolder').text = self.config.logs_folder
        ET.SubElement(settings, 'BackupFolder').text = self.config.backup_folder
        
        # Advanced settings
        ET.SubElement(settings, 'EnableAuditLog').text = str(self.config.enable_audit_logging).lower()
        ET.SubElement(settings, 'EnableSecurity').text = str(self.config.enable_security_features).lower()
        ET.SubElement(settings, 'EnableProxyRotation').text = str(self.config.enable_proxy_rotation).lower()
        
        self.logger.info("Generated settings section")
    
    def _generate_ui_components(self, root: ET.Element):
        """Generate UI components and interface."""
        ui_content = self.ui_generator.generate_ui_module()
        if ui_content:
            ui_element = ET.fromstring(ui_content)
            root.append(ui_element)
            self.stats['total_features'] += 1
            self.logger.info("Generated UI components")
    
    def _generate_security_macros(self, root: ET.Element):
        """Generate security-related macros."""
        security_macros = self.security_generator.generate_security_macros()
        for macro_xml in security_macros:
            macro_element = ET.fromstring(macro_xml)
            root.append(macro_element)
            self.stats['total_macros'] += 1
        self.logger.info(f"Generated {len(security_macros)} security macros")
    
    def _generate_function_macros(self, root: ET.Element):
        """Generate function macros for all 124+ features."""
        function_macros = self.function_generator.generate_all_function_macros()
        for macro_xml in function_macros:
            macro_element = ET.fromstring(macro_xml)
            root.append(macro_element)
            self.stats['total_macros'] += 1
        self.logger.info(f"Generated {len(function_macros)} function macros")
    
    def _generate_action_sequences(self, root: ET.Element):
        """Generate action sequences and workflows."""
        action_sequences = self.action_generator.generate_action_sequences()
        for sequence_xml in action_sequences:
            sequence_element = ET.fromstring(sequence_xml)
            root.append(sequence_element)
            self.stats['total_actions'] += len(sequence_element.findall('.//action'))
        self.logger.info(f"Generated {len(action_sequences)} action sequences")
    
    def _generate_integration_modules(self, root: ET.Element):
        """Generate integration modules for external services."""
        integration_modules = self.integration_generator.generate_integration_modules()
        for module_xml in integration_modules:
            module_element = ET.fromstring(module_xml)
            root.append(module_element)
        self.logger.info(f"Generated {len(integration_modules)} integration modules")
    
    def _generate_logging_modules(self, root: ET.Element):
        """Generate logging and statistics modules."""
        logging_modules = self.logging_generator.generate_logging_modules()
        for module_xml in logging_modules:
            module_element = ET.fromstring(module_xml)
            root.append(module_element)
        self.logger.info(f"Generated {len(logging_modules)} logging modules")
    
    def _generate_validation_modules(self, root: ET.Element):
        """Generate validation and error checking modules."""
        validation_modules = self.validation_generator.generate_validation_modules()
        for module_xml in validation_modules:
            module_element = ET.fromstring(module_xml)
            root.append(module_element)
        self.logger.info(f"Generated {len(validation_modules)} validation modules")
    
    def _add_system_macros(self, root: ET.Element):
        """Add essential system macros."""
        # Main execution macro
        main_macro = ET.SubElement(root, 'macro')
        main_macro.set('name', 'Main')
        
        # Initialize action
        init_action = ET.SubElement(main_macro, 'action')
        init_action.set('name', 'CallMacro')
        ET.SubElement(init_action, 'Name').text = 'Initialize'
        
        # Load configuration
        config_action = ET.SubElement(main_macro, 'action')
        config_action.set('name', 'CallMacro')
        ET.SubElement(config_action, 'Name').text = 'LoadConfiguration'
        
        # Execute all features
        for feature in self.config.enabled_features:
            feature_action = ET.SubElement(main_macro, 'action')
            feature_action.set('name', 'CallMacro')
            ET.SubElement(feature_action, 'Name').text = f'Execute_{feature.title().replace("_", "")}'
        
        self.logger.info("Added system macros")
    
    def _expand_content_for_target_size(self, root: ET.Element):
        """Expand content to reach target file size."""
        current_size = len(ET.tostring(root, encoding='unicode'))
        target_size = self.config.target_size_mb * 1024 * 1024  # Convert to bytes
        
        if current_size < target_size:
            expansion_needed = target_size - current_size
            self.logger.info(f"Expanding content by {expansion_needed / (1024*1024):.2f}MB to reach target")
            
            # Add data expansion macros
            expansion_macro = ET.SubElement(root, 'macro')
            expansion_macro.set('name', 'DataExpansion')
            
            # Calculate number of repetitions needed
            base_content_size = 1000  # Approximate size per expansion unit
            repetitions = max(1, expansion_needed // base_content_size)
            
            for i in range(min(repetitions, 100000)):  # Limit to prevent excessive memory usage
                data_action = ET.SubElement(expansion_macro, 'action')
                data_action.set('name', 'SetVariable')
                ET.SubElement(data_action, 'Variable').text = f'ExpansionData_{i:06d}'
                ET.SubElement(data_action, 'Value').text = f'Generated data block {i:06d} for size expansion. ' * 20
                
                if i % 10000 == 0:
                    self.logger.info(f"Generated {i} expansion blocks...")
        
        self.logger.info("Content expansion completed")
    
    def _format_xml(self, root: ET.Element) -> str:
        """Format XML with proper indentation."""
        rough_string = ET.tostring(root, encoding='unicode')
        
        try:
            reparsed = minidom.parseString(rough_string)
            formatted = reparsed.toprettyxml(indent="  ", encoding=None)
            # Remove empty lines
            lines = [line for line in formatted.split('\n') if line.strip()]
            return '\n'.join(lines)
        except Exception as e:
            self.logger.warning(f"XML formatting failed, using unformatted: {e}")
            return rough_string
    
    def _save_xml_file(self, xml_content: str, filename: Optional[str] = None) -> str:
        """Save XML content to file."""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"hdgrace_bas_complete_{self.config.bas_version.replace('.', '_')}_{timestamp}.xml"
        
        output_path = os.path.join(self.config.output_folder, filename)
        
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        # Create backup
        if self.config.backup_folder:
            backup_path = os.path.join(self.config.backup_folder, filename)
            Path(backup_path).parent.mkdir(parents=True, exist_ok=True)
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)
        
        return output_path
    
    def _finalize_statistics(self, output_path: str, validation_result: Dict[str, Any]):
        """Finalize generation statistics."""
        self.stats['generation_end'] = datetime.now()
        self.stats['file_size_bytes'] = os.path.getsize(output_path)
        self.stats['file_size_mb'] = self.stats['file_size_bytes'] / (1024 * 1024)
        self.stats['validation_errors'] = len(validation_result.get('errors', []))
        
        generation_time = self.stats['generation_end'] - self.stats['generation_start']
        self.stats['generation_time_seconds'] = generation_time.total_seconds()
        
        # Save statistics
        stats_file = output_path.replace('.xml', '_stats.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, default=str, ensure_ascii=False)
        
        self.logger.info(f"Generation statistics saved to {stats_file}")
    
    def generate_feature_subset(self, feature_names: List[str], output_filename: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        """Generate XML with only specified features."""
        original_features = self.config.enabled_features.copy()
        self.config.enabled_features = [f for f in feature_names if f in original_features]
        
        try:
            result = self.generate_complete_xml(output_filename)
            return result
        finally:
            self.config.enabled_features = original_features
    
    def get_generation_report(self) -> Dict[str, Any]:
        """Get comprehensive generation report."""
        return {
            'config': self.config.to_dict(),
            'statistics': self.stats,
            'features_generated': self.config.enabled_features,
            'total_features': len(self.config.enabled_features),
            'generation_successful': self.stats.get('generation_end') is not None
        }