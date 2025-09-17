"""
Template Engine for BAS XML Generation
======================================

Provides templating and content generation capabilities for creating
dynamic XML content based on patterns and data.
"""

import re
import json
from typing import Dict, List, Any, Optional
from string import Template
import logging
from .config import GeneratorConfig


class TemplateEngine:
    """Template engine for generating dynamic XML content."""
    
    def __init__(self, config: GeneratorConfig):
        """Initialize template engine with configuration."""
        self.config = config
        self.logger = logging.getLogger('TemplateEngine')
        self.templates = {}
        self.variables = {}
        
        # Load built-in templates
        self._load_builtin_templates()
    
    def _load_builtin_templates(self):
        """Load built-in XML templates for common patterns."""
        
        # Basic macro template
        self.templates['basic_macro'] = Template('''
  <macro name="$macro_name">
    $macro_content
  </macro>''')
        
        # Action template
        self.templates['action'] = Template('''
    <action name="$action_name">
      $action_parameters
    </action>''')
        
        # Parameter template
        self.templates['parameter'] = Template('''
      <$param_name>$param_value</$param_name>''')
        
        # UI component template
        self.templates['ui_component'] = Template('''
    <$component_type id="$component_id" $attributes>
      $component_content
    </$component_type>''')
        
        # Settings section template
        self.templates['settings_section'] = Template('''
  <settings>
    $settings_content
  </settings>''')
        
        # Feature macro template with full structure
        self.templates['feature_macro'] = Template('''
  <!-- $emoji $description -->
  <macro name="$macro_name">
    <parameter name="target_url"/>
    <parameter name="count" default="$default_count"/>
    <parameter name="duration" default="$default_duration"/>
    <parameter name="threads" default="$default_threads"/>
    
    <!-- Initialization -->
    <action name="LogEvent">
      <Type>FEATURE_START</Type>
      <Level>INFO</Level>
      <Details>$emoji $feature_name started - ID: $feature_id</Details>
    </action>
    
    <action name="SetVariable">
      <Variable>Feature_$feature_id_Status</Variable>
      <Value>running</Value>
    </action>
    
    <!-- Feature-specific actions -->
    $feature_actions
    
    <!-- Completion -->
    <action name="SetVariable">
      <Variable>Feature_$feature_id_Status</Variable>
      <Value>completed</Value>
    </action>
    
    <action name="LogEvent">
      <Type>FEATURE_COMPLETE</Type>
      <Level>INFO</Level>
      <Details>$emoji $feature_name completed - Result: {Feature_$feature_id_Result}</Details>
    </action>
    
    <action name="AuditLog">
      <Action>FEATURE_EXECUTION</Action>
      <FeatureId>$feature_id</FeatureId>
      <FeatureName>$feature_name</FeatureName>
      <Category>$category</Category>
      <Result>{Feature_$feature_id_Result}</Result>
    </action>
  </macro>''')
        
        # Expansion template for large content generation
        self.templates['expansion_block'] = Template('''
    <action name="SetVariable">
      <Variable>ExpansionData_$block_id</Variable>
      <Value>$expansion_content</Value>
    </action>''')
        
        self.logger.info("Built-in templates loaded")
    
    def register_template(self, name: str, template_content: str):
        """Register a new template."""
        self.templates[name] = Template(template_content)
        self.logger.debug(f"Template '{name}' registered")
    
    def set_variable(self, name: str, value: Any):
        """Set a template variable."""
        self.variables[name] = value
    
    def set_variables(self, variables: Dict[str, Any]):
        """Set multiple template variables."""
        self.variables.update(variables)
    
    def render_template(self, template_name: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """Render a template with variables."""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = self.templates[template_name]
        render_vars = {**self.variables}
        
        if variables:
            render_vars.update(variables)
        
        try:
            return template.substitute(render_vars)
        except KeyError as e:
            self.logger.error(f"Missing template variable: {e}")
            # Return template with safe substitution (missing vars become empty)
            return template.safe_substitute(render_vars)
    
    def render_feature_macro(self, feature_data: Dict[str, Any]) -> str:
        """Render a complete feature macro from feature data."""
        # Generate feature-specific actions based on category
        actions = self._generate_feature_actions(feature_data)
        
        template_vars = {
            'emoji': feature_data.get('emoji', '🔧'),
            'description': feature_data.get('description', 'Feature'),
            'macro_name': f"Feature_{feature_data.get('id', 'Unknown')}_{feature_data.get('name', 'Unknown').replace(' ', '_')}",
            'feature_name': feature_data.get('name', 'Unknown Feature'),
            'feature_id': feature_data.get('id', 'unknown'),
            'category': feature_data.get('category', 'general'),
            'default_count': feature_data.get('default_count', 1000),
            'default_duration': feature_data.get('default_duration', 3600),
            'default_threads': feature_data.get('default_threads', 4),
            'feature_actions': actions
        }
        
        return self.render_template('feature_macro', template_vars)
    
    def _generate_feature_actions(self, feature_data: Dict[str, Any]) -> str:
        """Generate specific actions based on feature category and type."""
        category = feature_data.get('category', 'general').lower()
        feature_type = feature_data.get('type', 'basic').lower()
        
        actions = []
        
        if category == 'live_streaming':
            actions.extend(self._generate_live_streaming_actions(feature_data))
        elif category == 'shorts_videos':
            actions.extend(self._generate_shorts_actions(feature_data))
        elif category == 'gmail_management':
            actions.extend(self._generate_gmail_actions(feature_data))
        elif category == 'youtube_automation':
            actions.extend(self._generate_youtube_actions(feature_data))
        elif category == 'proxy_management':
            actions.extend(self._generate_proxy_actions(feature_data))
        elif category == 'account_creation':
            actions.extend(self._generate_account_actions(feature_data))
        elif category == 'engagement':
            actions.extend(self._generate_engagement_actions(feature_data))
        elif category == 'analytics':
            actions.extend(self._generate_analytics_actions(feature_data))
        elif category == 'security':
            actions.extend(self._generate_security_actions(feature_data))
        else:
            actions.extend(self._generate_generic_actions(feature_data))
        
        return '\n    '.join(actions)
    
    def _generate_live_streaming_actions(self, feature_data: Dict[str, Any]) -> List[str]:
        """Generate actions for live streaming features."""
        return [
            '''<action name="InitializeBrowser">
      <Engine>Chromium</Engine>
      <Headless>false</Headless>
    </action>''',
            '''<action name="SetProxy">
      <Source>API</Source>
      <RotationInterval>300</RotationInterval>
    </action>''',
            '''<action name="Navigate">
      <Url>https://www.youtube.com/watch?v={target_url}</Url>
    </action>''',
            '''<action name="WaitFor">
      <Selector>video</Selector>
      <Timeout>15000</Timeout>
    </action>''',
            '''<action name="Click">
      <Selector>video</Selector>
    </action>''',
            '''<action name="Delay">
      <Min>{duration}</Min>
      <Max>{duration}</Max>
    </action>'''
        ]
    
    def _generate_shorts_actions(self, feature_data: Dict[str, Any]) -> List[str]:
        """Generate actions for shorts optimization features."""
        return [
            '''<action name="Navigate">
      <Url>https://www.youtube.com/shorts/{target_url}</Url>
    </action>''',
            '''<action name="WaitFor">
      <Selector>[data-shorts-player]</Selector>
      <Timeout>10000</Timeout>
    </action>''',
            '''<action name="RandomizeViewTime">
      <MinSeconds>15</MinSeconds>
      <MaxSeconds>60</MaxSeconds>
    </action>''',
            '''<action name="SimulateEngagement">
      <LikeChance>0.3</LikeChance>
      <CommentChance>0.1</CommentChance>
      <SubscribeChance>0.05</SubscribeChance>
    </action>'''
        ]
    
    def _generate_gmail_actions(self, feature_data: Dict[str, Any]) -> List[str]:
        """Generate actions for Gmail management features."""
        return [
            '''<action name="Navigate">
      <Url>https://accounts.google.com/signup</Url>
    </action>''',
            '''<action name="GenerateRandomIdentity">
      <NameFormat>FirstLast</NameFormat>
      <CountryCode>US</CountryCode>
    </action>''',
            '''<action name="FillRegistrationForm">
      <FirstName>{GeneratedFirstName}</FirstName>
      <LastName>{GeneratedLastName}</LastName>
      <Username>{GeneratedUsername}</Username>
      <Password>{GeneratedPassword}</Password>
    </action>''',
            '''<action name="HandleVerification">
      <Method>SMS</Method>
      <RecoveryEmail>{RecoveryEmail}</RecoveryEmail>
    </action>'''
        ]
    
    def _generate_youtube_actions(self, feature_data: Dict[str, Any]) -> List[str]:
        """Generate actions for YouTube automation features."""
        return [
            '''<action name="LoginYoutube">
      <Email>{AccountEmail}</Email>
      <Password>{AccountPassword}</Password>
    </action>''',
            '''<action name="NavigateToChannel">
      <ChannelUrl>{target_url}</ChannelUrl>
    </action>''',
            '''<action name="PerformChannelActions">
      <Subscribe>true</Subscribe>
      <EnableNotifications>true</EnableNotifications>
      <LikeRecentVideos>5</LikeRecentVideos>
    </action>''',
            '''<action name="WatchVideosDuration">
      <MinWatchTime>30</MinWatchTime>
      <MaxWatchTime>300</MaxWatchTime>
      <VideoCount>{count}</VideoCount>
    </action>'''
        ]
    
    def _generate_proxy_actions(self, feature_data: Dict[str, Any]) -> List[str]:
        """Generate actions for proxy management features."""
        return [
            '''<action name="LoadProxyList">
      <Source>./config/proxies.txt</Source>
      <Format>ip:port:user:pass</Format>
    </action>''',
            '''<action name="TestProxyConnection">
      <Timeout>5000</Timeout>
      <TestUrl>https://httpbin.org/ip</TestUrl>
    </action>''',
            '''<action name="RotateProxy">
      <Interval>300</Interval>
      <Strategy>Random</Strategy>
    </action>''',
            '''<action name="ValidateProxyHealth">
      <MaxFailures>3</MaxFailures>
      <HealthCheckInterval>60</HealthCheckInterval>
    </action>'''
        ]
    
    def _generate_account_actions(self, feature_data: Dict[str, Any]) -> List[str]:
        """Generate actions for account creation features."""
        return [
            '''<action name="GenerateAccountData">
      <NameDatabase>./data/names.json</NameDatabase>
      <CountryCode>US</CountryCode>
      <AgeRange>18-65</AgeRange>
    </action>''',
            '''<action name="CreateEmailAccount">
      <Provider>Gmail</Provider>
      <VerificationMethod>SMS</VerificationMethod>
    </action>''',
            '''<action name="SetupAccountProfile">
      <ProfilePicture>Random</ProfilePicture>
      <Bio>Generated</Bio>
      <Interests>Random</Interests>
    </action>''',
            '''<action name="VerifyAccountSetup">
      <LoginTest>true</LoginTest>
      <ProfileCheck>true</ProfileCheck>
    </action>'''
        ]
    
    def _generate_engagement_actions(self, feature_data: Dict[str, Any]) -> List[str]:
        """Generate actions for engagement automation features."""
        return [
            '''<action name="LoadCommentTemplates">
      <File>./data/comments.json</File>
      <Language>en</Language>
    </action>''',
            '''<action name="AnalyzeVideoContent">
      <ExtractKeywords>true</ExtractKeywords>
      <AnalyzeSentiment>true</AnalyzeSentiment>
    </action>''',
            '''<action name="GenerateRelevantComment">
      <MaxLength>280</MaxLength>
      <Tone>Positive</Tone>
      <IncludeEmoji>true</IncludeEmoji>
    </action>''',
            '''<action name="PostEngagementActions">
      <Like>true</Like>
      <Comment>true</Comment>
      <Subscribe>0.1</Subscribe>
    </action>'''
        ]
    
    def _generate_analytics_actions(self, feature_data: Dict[str, Any]) -> List[str]:
        """Generate actions for analytics features."""
        return [
            '''<action name="CollectMetrics">
      <ViewCount>true</ViewCount>
      <LikeCount>true</LikeCount>
      <CommentCount>true</CommentCount>
      <SubscriberCount>true</SubscriberCount>
    </action>''',
            '''<action name="TrackEngagement">
      <WatchTime>true</WatchTime>
      <ClickThroughRate>true</ClickThroughRate>
      <RetentionRate>true</RetentionRate>
    </action>''',
            '''<action name="GenerateReport">
      <Format>JSON</Format>
      <OutputFile>./reports/analytics_{TIMESTAMP}.json</OutputFile>
    </action>''',
            '''<action name="UpdateDatabase">
      <Table>analytics_data</Table>
      <Timestamp>{CURRENT_TIME}</Timestamp>
    </action>'''
        ]
    
    def _generate_security_actions(self, feature_data: Dict[str, Any]) -> List[str]:
        """Generate actions for security features."""
        return [
            '''<action name="RandomizeFingerprint">
      <UserAgent>true</UserAgent>
      <Resolution>true</Resolution>
      <Timezone>true</Timezone>
      <Language>true</Language>
    </action>''',
            '''<action name="EnablePrivacyMode">
      <DisableWebRTC>true</DisableWebRTC>
      <DisableGeolocation>true</DisableGeolocation>
      <BlockTrackers>true</BlockTrackers>
    </action>''',
            '''<action name="EncryptSensitiveData">
      <Algorithm>AES256</Algorithm>
      <KeySource>Environment</KeySource>
    </action>''',
            '''<action name="AuditSecuritySettings">
      <CheckCookies>true</CheckCookies>
      <CheckLocalStorage>true</CheckLocalStorage>
      <CheckFingerprint>true</CheckFingerprint>
    </action>'''
        ]
    
    def _generate_generic_actions(self, feature_data: Dict[str, Any]) -> List[str]:
        """Generate generic actions for undefined categories."""
        return [
            '''<action name="ExecuteCustomLogic">
      <Script>./scripts/custom_feature.js</Script>
      <Parameters>{feature_parameters}</Parameters>
    </action>''',
            '''<action name="WaitForCompletion">
      <Timeout>30000</Timeout>
      <CheckInterval>1000</CheckInterval>
    </action>''',
            '''<action name="LogProgress">
      <Message>Generic feature executed successfully</Message>
      <Level>INFO</Level>
    </action>'''
        ]
    
    def generate_expansion_content(self, target_size_bytes: int) -> str:
        """Generate content blocks to reach target file size."""
        content_blocks = []
        block_size = 1000  # Approximate size per block
        num_blocks = max(1, target_size_bytes // block_size)
        
        for i in range(num_blocks):
            block_data = {
                'block_id': f"{i:06d}",
                'expansion_content': f"Generated expansion data block {i:06d} for size optimization. " * 10
            }
            block_xml = self.render_template('expansion_block', block_data)
            content_blocks.append(block_xml)
        
        return '\n'.join(content_blocks)
    
    def create_ui_component(self, component_type: str, component_id: str, 
                          attributes: Dict[str, str], content: str = "") -> str:
        """Create a UI component from template."""
        attr_string = ' '.join([f'{k}="{v}"' for k, v in attributes.items()])
        
        variables = {
            'component_type': component_type,
            'component_id': component_id,
            'attributes': attr_string,
            'component_content': content
        }
        
        return self.render_template('ui_component', variables)
    
    def batch_render_features(self, features_data: List[Dict[str, Any]]) -> List[str]:
        """Render multiple features in batch."""
        rendered_features = []
        
        for feature_data in features_data:
            try:
                rendered_feature = self.render_feature_macro(feature_data)
                rendered_features.append(rendered_feature)
            except Exception as e:
                self.logger.error(f"Failed to render feature {feature_data.get('name', 'Unknown')}: {e}")
                # Continue with other features
                continue
        
        return rendered_features