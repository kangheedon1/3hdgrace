#!/usr/bin/env python3
"""
HDGRACE BAS 29.3.1 Premium XML Generator
========================================

Main script to generate comprehensive BAS XML files with 124+ features
supporting up to 700MB output for BrowserAutomationStudio 29.3.1 Premium.

Usage:
    python generate_bas_xml.py [--config config.json] [--output filename.xml] [--size 700]

Features:
- Modular architecture with 124+ automation features
- Full BAS 29.3.1 compatibility  
- Large-scale XML generation (up to 700MB)
- Comprehensive logging and validation
- Statistics and reporting
- Error handling and recovery
"""

import argparse
import sys
import os
import json
from pathlib import Path
from typing import Optional

# Add the xml_generator package to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xml_generator import XMLGenerator, GeneratorConfig


def main():
    """Main entry point for the XML generator."""
    parser = argparse.ArgumentParser(
        description="HDGRACE BAS 29.3.1 Premium XML Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate with default settings (700MB target)
    python generate_bas_xml.py
    
    # Generate with custom config
    python generate_bas_xml.py --config custom_config.json
    
    # Generate with specific output filename and size
    python generate_bas_xml.py --output my_project.xml --size 500
    
    # Generate only specific features
    python generate_bas_xml.py --features live_streaming,youtube_automation
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Path to configuration JSON file (default: auto-generated)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output XML filename (default: auto-generated with timestamp)'
    )
    
    parser.add_argument(
        '--size', '-s',
        type=int,
        default=700,
        help='Target file size in MB (default: 700)'
    )
    
    parser.add_argument(
        '--features', '-f',
        type=str,
        help='Comma-separated list of features to include (default: all)'
    )
    
    parser.add_argument(
        '--threads', '-t',
        type=int,
        default=500,
        help='Maximum number of threads (default: 500)'
    )
    
    parser.add_argument(
        '--validate', '-v',
        action='store_true',
        help='Enable comprehensive XML validation'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress progress output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='HDGRACE BAS XML Generator v1.0.0'
    )
    
    args = parser.parse_args()
    
    try:
        # Print banner
        if not args.quiet:
            print_banner()
        
        # Load or create configuration
        config = load_configuration(args)
        
        # Initialize generator
        generator = XMLGenerator(config)
        
        if not args.quiet:
            print(f"🚀 Initializing HDGRACE BAS XML Generator...")
            print(f"📋 Target size: {config.target_size_mb}MB")
            print(f"🧵 Max threads: {config.max_threads}")
            print(f"🎯 Features: {len(config.enabled_features)}")
            print(f"📁 Output folder: {config.output_folder}")
            print()
        
        # Generate XML
        if args.features:
            # Generate subset of features
            feature_list = [f.strip() for f in args.features.split(',')]
            output_path, stats = generator.generate_feature_subset(feature_list, args.output)
        else:
            # Generate complete XML
            output_path, stats = generator.generate_complete_xml(args.output)
        
        # Validate if requested
        if args.validate:
            if not args.quiet:
                print("🔍 Validating generated XML...")
            validation_result = generator.validator.validate_xml_file(output_path)
            print_validation_results(validation_result, args.quiet)
        
        # Print results
        print_generation_results(output_path, stats, args.quiet)
        
        # Generate additional reports
        generate_reports(generator, output_path, args.quiet)
        
        if not args.quiet:
            print("\n✅ XML generation completed successfully!")
            print(f"📁 Output file: {output_path}")
            print(f"📊 File size: {stats['file_size_mb']:.2f}MB")
            print(f"⏱️  Generation time: {stats['generation_time_seconds']:.2f}s")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n❌ Generation cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error during generation: {str(e)}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        return 1


def print_banner():
    """Print application banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🧩 HDGRACE BAS 29.3.1 Premium XML Generator v1.0.0                       ║
║                                                                              ║
║    ✨ Features:                                                              ║
║    • 124+ Automation Features        • Full BAS 29.3.1 Compatibility      ║
║    • Large-scale Generation (700MB+) • Comprehensive Validation             ║
║    • Modular Architecture            • Advanced Error Handling              ║
║    • Real-time Logging               • Statistics & Reporting               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def load_configuration(args) -> GeneratorConfig:
    """Load configuration from file or create default."""
    if args.config and os.path.exists(args.config):
        config = GeneratorConfig.from_file(args.config)
    else:
        config = GeneratorConfig()
    
    # Override with command line arguments
    if args.size != 700:
        config.target_size_mb = args.size
    
    if args.threads != 500:
        config.max_threads = args.threads
    
    return config


def print_validation_results(validation_result: dict, quiet: bool = False):
    """Print XML validation results."""
    if quiet:
        return
    
    if validation_result['valid']:
        print("✅ XML validation passed")
    else:
        print("❌ XML validation failed")
        
        if validation_result['errors']:
            print("\n🔴 Errors:")
            for error in validation_result['errors'][:5]:  # Show first 5 errors
                print(f"  • {error}")
            if len(validation_result['errors']) > 5:
                print(f"  ... and {len(validation_result['errors']) - 5} more errors")
        
        if validation_result['warnings']:
            print("\n🟡 Warnings:")
            for warning in validation_result['warnings'][:3]:  # Show first 3 warnings
                print(f"  • {warning}")
            if len(validation_result['warnings']) > 3:
                print(f"  ... and {len(validation_result['warnings']) - 3} more warnings")


def print_generation_results(output_path: str, stats: dict, quiet: bool = False):
    """Print generation results and statistics."""
    if quiet:
        return
    
    print("\n📊 Generation Statistics:")
    print(f"  📁 Output file: {os.path.basename(output_path)}")
    print(f"  📏 File size: {stats['file_size_mb']:.2f}MB ({stats['file_size_bytes']:,} bytes)")
    print(f"  🔧 Total macros: {stats['total_macros']:,}")
    print(f"  ⚡ Total actions: {stats['total_actions']:,}")
    print(f"  🎯 Total features: {stats['total_features']:,}")
    print(f"  ⏱️  Generation time: {stats['generation_time_seconds']:.2f} seconds")
    
    if stats['validation_errors'] > 0:
        print(f"  ⚠️  Validation errors: {stats['validation_errors']}")


def generate_reports(generator: XMLGenerator, output_path: str, quiet: bool = False):
    """Generate additional reports and documentation."""
    try:
        if not quiet:
            print("\n📋 Generating additional reports...")
        
        # Generation report
        report = generator.get_generation_report()
        report_path = output_path.replace('.xml', '_report.json')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        if not quiet:
            print(f"  📄 Generation report: {os.path.basename(report_path)}")
        
        # Feature summary
        features_summary = generator.function_generator.get_features_summary()
        summary_path = output_path.replace('.xml', '_features.json')
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(features_summary, f, indent=2, ensure_ascii=False)
        
        if not quiet:
            print(f"  📋 Features summary: {os.path.basename(summary_path)}")
        
        # Create README
        readme_path = output_path.replace('.xml', '_README.md')
        create_readme(readme_path, generator.config, generator.stats, features_summary)
        
        if not quiet:
            print(f"  📖 Documentation: {os.path.basename(readme_path)}")
    
    except Exception as e:
        if not quiet:
            print(f"  ⚠️  Warning: Could not generate reports: {e}")


def create_readme(readme_path: str, config: GeneratorConfig, stats: dict, features_summary: dict):
    """Create README documentation for the generated XML."""
    readme_content = f"""# HDGRACE BAS 29.3.1 Premium XML Project

## 📋 Project Information

- **Generated**: {stats.get('generation_start', 'Unknown')}
- **BAS Version**: {config.bas_version}
- **Project Name**: {config.project_name}
- **File Size**: {stats.get('file_size_mb', 0):.2f}MB
- **Generation Time**: {stats.get('generation_time_seconds', 0):.2f} seconds

## ✨ Features Summary

- **Total Features**: {features_summary.get('total_features', 0)}
- **Feature Categories**: {features_summary.get('total_categories', 0)}
- **Total Macros**: {stats.get('total_macros', 0):,}
- **Total Actions**: {stats.get('total_actions', 0):,}

## 🗂️ Feature Categories

"""
    
    for category, category_info in features_summary.items():
        if category not in ['total_features', 'total_categories']:
            readme_content += f"### {category.replace('_', ' ').title()}\n\n"
            readme_content += f"- **Count**: {category_info.get('count', 0)} features\n"
            readme_content += f"- **Features**: {', '.join([f['name'] for f in category_info.get('features', [])])}\n\n"
    
    readme_content += f"""## ⚙️ Configuration

- **Max Threads**: {config.max_threads}
- **Thread Delay**: {config.thread_delay_ms}ms
- **Parallel Execution**: {config.enable_parallel_execution}
- **Audit Logging**: {config.enable_audit_logging}
- **Security Features**: {config.enable_security_features}

## 📁 Directory Structure

```
{config.input_folder}     # Input files
{config.output_folder}    # Generated XML files
{config.logs_folder}      # Log files
{config.backup_folder}    # Backup files
{config.config_folder}    # Configuration files
```

## 🚀 Usage Instructions

1. **Load in BAS 29.3.1**: Import the generated XML file into BrowserAutomationStudio
2. **Configure Settings**: Adjust thread count and delays as needed
3. **Set File Paths**: Update input/output folder paths in settings
4. **Run Project**: Execute the Main macro to start automation

## 📊 Performance Recommendations

- **Memory**: Minimum 8GB RAM recommended for full feature set
- **CPU**: Multi-core processor recommended for parallel execution
- **Storage**: Ensure sufficient disk space for logs and data
- **Network**: Stable internet connection required for automation

## 🔧 Troubleshooting

1. **High Memory Usage**: Reduce thread count in settings
2. **Slow Performance**: Increase thread delay in configuration
3. **Connection Issues**: Check proxy settings and network connectivity
4. **Validation Errors**: Review logs for specific error details

## 📞 Support

For technical support and updates, refer to the HDGRACE documentation.

---
*Generated by HDGRACE BAS XML Generator v1.0.0*
"""
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)


if __name__ == "__main__":
    sys.exit(main())