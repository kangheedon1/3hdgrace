"""
Configuration Management for BAS XML Generator
==============================================

Handles all configuration settings for the XML generator including
BAS version compatibility, feature flags, and output parameters.
"""

import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path


@dataclass
class GeneratorConfig:
    """Main configuration class for the XML generator."""
    
    # BAS Version Settings
    bas_version: str = "29.3.1"
    project_name: str = "hdgrace-bas-premium-complete"
    output_format: str = "xml"
    
    # Output Settings
    target_size_mb: int = 700
    enable_compression: bool = True
    enable_minification: bool = False
    
    # Feature Settings
    max_threads: int = 500
    thread_delay_ms: int = 50
    enable_parallel_execution: bool = True
    enable_audit_logging: bool = True
    
    # File Paths
    input_folder: str = "./input/"
    output_folder: str = "./output/"
    logs_folder: str = "./logs/"
    backup_folder: str = "./backup/"
    config_folder: str = "./config/"
    
    # Security Settings
    enable_security_features: bool = True
    encrypt_sensitive_data: bool = True
    enable_proxy_rotation: bool = True
    
    # UI Settings
    enable_emoji_ui: bool = True
    ui_theme: str = "dark"
    enable_progress_bars: bool = True
    
    # Feature Flags
    enabled_features: List[str] = field(default_factory=lambda: [
        "live_streaming", "shorts_optimization", "gmail_management",
        "youtube_automation", "proxy_management", "account_creation",
        "engagement_automation", "analytics", "security", "ui_enhanced"
    ])
    
    # Advanced Settings
    custom_settings: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize configuration after creation."""
        self._ensure_directories()
        self._validate_settings()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        for folder in [self.input_folder, self.output_folder, 
                      self.logs_folder, self.backup_folder, self.config_folder]:
            Path(folder).mkdir(parents=True, exist_ok=True)
    
    def _validate_settings(self):
        """Validate configuration settings."""
        if self.target_size_mb <= 0:
            raise ValueError("Target size must be positive")
        
        if self.max_threads <= 0:
            raise ValueError("Max threads must be positive")
        
        if not self.bas_version:
            raise ValueError("BAS version must be specified")
    
    @classmethod
    def from_file(cls, config_path: str) -> 'GeneratorConfig':
        """Load configuration from JSON file."""
        if not os.path.exists(config_path):
            # Create default config if it doesn't exist
            config = cls()
            config.save_to_file(config_path)
            return config
        
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert dict to dataclass instance
        return cls(**data)
    
    def save_to_file(self, config_path: str):
        """Save configuration to JSON file."""
        Path(config_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, indent=2, ensure_ascii=False)
    
    def update_setting(self, key: str, value: Any):
        """Update a configuration setting."""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            self.custom_settings[key] = value
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a configuration setting."""
        if hasattr(self, key):
            return getattr(self, key)
        return self.custom_settings.get(key, default)
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a specific feature is enabled."""
        return feature in self.enabled_features
    
    def enable_feature(self, feature: str):
        """Enable a specific feature."""
        if feature not in self.enabled_features:
            self.enabled_features.append(feature)
    
    def disable_feature(self, feature: str):
        """Disable a specific feature."""
        if feature in self.enabled_features:
            self.enabled_features.remove(feature)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            **self.__dict__,
            'custom_settings': self.custom_settings
        }
    
    def __repr__(self) -> str:
        """String representation of configuration."""
        return f"GeneratorConfig(bas_version='{self.bas_version}', target_size_mb={self.target_size_mb})"