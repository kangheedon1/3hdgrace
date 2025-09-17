"""
Function Module Generator
========================

Generates function macros for all 124+ BAS automation features
including live streaming, shorts optimization, Gmail management, etc.
"""

from typing import Dict, List, Any
import logging
from ...core.config import GeneratorConfig
from ...core.template_engine import TemplateEngine


class FunctionModuleGenerator:
    """Generates function macros for all automation features."""
    
    def __init__(self, config: GeneratorConfig):
        """Initialize function generator with configuration."""
        self.config = config
        self.logger = logging.getLogger('FunctionGenerator')
        self.template_engine = TemplateEngine(config)
        
        # Load all 124+ features definition
        self.features = self._load_all_features()
        
        self.logger.info(f"Initialized with {len(self.features)} features")
    
    def _load_all_features(self) -> List[Dict[str, Any]]:
        """Load comprehensive list of all 124+ features."""
        features = []
        
        # 1. Live Streaming Management (12 features)
        live_streaming_features = [
            {
                "id": "ls001", "name": "고정 시청자 500명 유지", "emoji": "👥",
                "category": "live_streaming", "type": "viewer_management",
                "description": "500개 브라우저로 24시간 라이브 시청자 유지",
                "default_count": 500, "default_duration": 86400, "default_threads": 50
            },
            {
                "id": "ls002", "name": "조회수 반복 입장이탈", "emoji": "🔄",
                "category": "live_streaming", "type": "view_manipulation",
                "description": "조회수 증가를 위한 반복 시청/이탈",
                "default_count": 1000, "default_duration": 3600, "default_threads": 20
            },
            {
                "id": "ls003", "name": "라이브 방송 자동 시청", "emoji": "📺",
                "category": "live_streaming", "type": "auto_watch",
                "description": "특정 라이브 방송 자동 시청",
                "default_count": 100, "default_duration": 7200, "default_threads": 10
            },
            {
                "id": "ls004", "name": "동시시청자 유지", "emoji": "🎯",
                "category": "live_streaming", "type": "concurrent_viewers",
                "description": "여러 라이브 방송 동시 시청",
                "default_count": 50, "default_duration": 3600, "default_threads": 25
            },
            {
                "id": "ls005", "name": "조회수 시청자 동시 증가", "emoji": "📈",
                "category": "live_streaming", "type": "dual_boost",
                "description": "조회수와 시청자 수 동시 향상",
                "default_count": 200, "default_duration": 1800, "default_threads": 15
            },
            {
                "id": "ls006", "name": "라이브 스트림 조회수 증가", "emoji": "🎪",
                "category": "live_streaming", "type": "view_boost",
                "description": "라이브 조회수 알고리즘 기반 증가",
                "default_count": 500, "default_duration": 3600, "default_threads": 30
            },
            {
                "id": "ls007", "name": "LIVE 고정 시청자 유지", "emoji": "🟢",
                "category": "live_streaming", "type": "persistent_viewers",
                "description": "라이브 시청자 자동 유지",
                "default_count": 300, "default_duration": 7200, "default_threads": 20
            },
            {
                "id": "ls008", "name": "Shorts 시청 최적화", "emoji": "⚡",
                "category": "live_streaming", "type": "shorts_optimization",
                "description": "쇼츠 시청 최적화 알고리즘",
                "default_count": 1000, "default_duration": 1800, "default_threads": 40
            },
            {
                "id": "ls009", "name": "댓글좋아요구독 자동화", "emoji": "❤️",
                "category": "live_streaming", "type": "engagement",
                "description": "라이브 방송 내 자동 상호작용",
                "default_count": 100, "default_duration": 3600, "default_threads": 10
            },
            {
                "id": "ls010", "name": "키워드 1등 만들기", "emoji": "🏆",
                "category": "live_streaming", "type": "seo_boost",
                "description": "키워드 검색 시 1등 순위로 노출",
                "default_count": 50, "default_duration": 7200, "default_threads": 5
            },
            {
                "id": "ls011", "name": "고정 시청자 시스템 ElitePlus", "emoji": "💎",
                "category": "live_streaming", "type": "elite_system",
                "description": "고급 고정 시청자 시스템",
                "default_count": 1000, "default_duration": 14400, "default_threads": 100
            },
            {
                "id": "ls012", "name": "조회수 유입 알고리즘", "emoji": "🌊",
                "category": "live_streaming", "type": "traffic_algorithm",
                "description": "자연스러운 조회수 유입 시뮬레이션",
                "default_count": 800, "default_duration": 5400, "default_threads": 60
            }
        ]
        features.extend(live_streaming_features)
        
        # 2. Shorts and Video Management (10 features)
        shorts_features = [
            {
                "id": "sv001", "name": "Shorts 시청 최적화", "emoji": "🟣",
                "category": "shorts_videos", "type": "optimization",
                "description": "쇼츠 자동 시청 최적화",
                "default_count": 500, "default_duration": 900, "default_threads": 25
            },
            {
                "id": "sv002", "name": "모바일프록시 자동 전환", "emoji": "📱",
                "category": "shorts_videos", "type": "mobile_proxy",
                "description": "모바일 디바이스 유형으로 프록시 전환",
                "default_count": 100, "default_duration": 1800, "default_threads": 10
            },
            {
                "id": "sv003", "name": "고정 프록시 Google 계정 없이", "emoji": "🔒",
                "category": "shorts_videos", "type": "proxy_management",
                "description": "프록시 고정 사용",
                "default_count": 200, "default_duration": 3600, "default_threads": 15
            },
            {
                "id": "sv004", "name": "IMEI 회전 프록시 설정", "emoji": "📡",
                "category": "shorts_videos", "type": "imei_rotation",
                "description": "IMEI 기반 프록시 회전",
                "default_count": 150, "default_duration": 2700, "default_threads": 12
            },
            {
                "id": "sv005", "name": "영상 반복 재생 알고리즘", "emoji": "🔁",
                "category": "shorts_videos", "type": "repeat_algorithm",
                "description": "동영상 반복 재생",
                "default_count": 300, "default_duration": 1800, "default_threads": 20
            },
            {
                "id": "sv006", "name": "키워드 기반 검색 유입 시청", "emoji": "🔍",
                "category": "shorts_videos", "type": "keyword_search",
                "description": "키워드 검색 후 자동 시청",
                "default_count": 250, "default_duration": 2400, "default_threads": 18
            },
            {
                "id": "sv007", "name": "키워드 순위 개선", "emoji": "📊",
                "category": "shorts_videos", "type": "ranking_boost",
                "description": "키워드 순위 상승",
                "default_count": 100, "default_duration": 5400, "default_threads": 8
            },
            {
                "id": "sv008", "name": "일반 영상 자동 시청", "emoji": "🎬",
                "category": "shorts_videos", "type": "general_watch",
                "description": "일반 유튜브 영상 자동 시청",
                "default_count": 400, "default_duration": 3600, "default_threads": 30
            },
            {
                "id": "sv009", "name": "쇼츠 자동 시청", "emoji": "⚡",
                "category": "shorts_videos", "type": "shorts_watch",
                "description": "쇼츠 영상 자동 시청",
                "default_count": 800, "default_duration": 1200, "default_threads": 50
            },
            {
                "id": "sv010", "name": "타겟 채널 방문", "emoji": "🎯",
                "category": "shorts_videos", "type": "channel_visit",
                "description": "특정 채널 자동 방문",
                "default_count": 150, "default_duration": 2700, "default_threads": 15
            }
        ]
        features.extend(shorts_features)
        
        # 3. Gmail Account Management (12 features)
        gmail_features = [
            {
                "id": "gm001", "name": "지메일 계정 생성", "emoji": "📩",
                "category": "gmail_management", "type": "account_creation",
                "description": "자동 지메일 계정 생성",
                "default_count": 50, "default_duration": 1800, "default_threads": 5
            },
            {
                "id": "gm002", "name": "대량 계정 생성", "emoji": "🏭",
                "category": "gmail_management", "type": "bulk_creation",
                "description": "대량 지메일 계정 생성",
                "default_count": 500, "default_duration": 7200, "default_threads": 20
            },
            {
                "id": "gm003", "name": "계정 검증 자동화", "emoji": "✅",
                "category": "gmail_management", "type": "verification",
                "description": "계정 검증 자동화",
                "default_count": 100, "default_duration": 3600, "default_threads": 10
            },
            {
                "id": "gm004", "name": "프로필 설정 자동화", "emoji": "👤",
                "category": "gmail_management", "type": "profile_setup",
                "description": "프로필 자동 설정",
                "default_count": 200, "default_duration": 2700, "default_threads": 15
            },
            {
                "id": "gm005", "name": "복구 이메일 설정", "emoji": "🔐",
                "category": "gmail_management", "type": "recovery_setup",
                "description": "복구 이메일 자동 설정",
                "default_count": 150, "default_duration": 1800, "default_threads": 12
            },
            {
                "id": "gm006", "name": "SMS 인증 자동화", "emoji": "📱",
                "category": "gmail_management", "type": "sms_verification",
                "description": "SMS 인증 자동화",
                "default_count": 100, "default_duration": 1200, "default_threads": 8
            },
            {
                "id": "gm007", "name": "계정 보안 설정", "emoji": "🛡️",
                "category": "gmail_management", "type": "security_setup",
                "description": "계정 보안 설정 자동화",
                "default_count": 200, "default_duration": 2400, "default_threads": 15
            },
            {
                "id": "gm008", "name": "계정 상태 모니터링", "emoji": "📊",
                "category": "gmail_management", "type": "monitoring",
                "description": "계정 상태 실시간 모니터링",
                "default_count": 1000, "default_duration": 86400, "default_threads": 5
            },
            {
                "id": "gm009", "name": "계정 로그인 테스트", "emoji": "🔑",
                "category": "gmail_management", "type": "login_test",
                "description": "계정 로그인 자동 테스트",
                "default_count": 500, "default_duration": 3600, "default_threads": 25
            },
            {
                "id": "gm010", "name": "계정 백업 관리", "emoji": "💾",
                "category": "gmail_management", "type": "backup_management",
                "description": "계정 정보 백업 관리",
                "default_count": 200, "default_duration": 1800, "default_threads": 10
            },
            {
                "id": "gm011", "name": "계정 복구 자동화", "emoji": "🔄",
                "category": "gmail_management", "type": "recovery_automation",
                "description": "계정 복구 자동화",
                "default_count": 50, "default_duration": 2700, "default_threads": 5
            },
            {
                "id": "gm012", "name": "계정 그룹 관리", "emoji": "👥",
                "category": "gmail_management", "type": "group_management",
                "description": "계정 그룹별 관리",
                "default_count": 100, "default_duration": 3600, "default_threads": 8
            }
        ]
        features.extend(gmail_features)
        
        # Add more categories to reach 124+ features
        # 4. YouTube Automation (15 features)
        youtube_features = self._generate_youtube_features()
        features.extend(youtube_features)
        
        # 5. Proxy Management (10 features)
        proxy_features = self._generate_proxy_features()
        features.extend(proxy_features)
        
        # 6. Account Creation & Management (15 features)
        account_features = self._generate_account_features()
        features.extend(account_features)
        
        # 7. Engagement Automation (20 features)
        engagement_features = self._generate_engagement_features()
        features.extend(engagement_features)
        
        # 8. Analytics & Monitoring (15 features)
        analytics_features = self._generate_analytics_features()
        features.extend(analytics_features)
        
        # 9. Security & Privacy (10 features)
        security_features = self._generate_security_features()
        features.extend(security_features)
        
        # 10. Advanced Features (15 features)
        advanced_features = self._generate_advanced_features()
        features.extend(advanced_features)
        
        return features
    
    def _generate_youtube_features(self) -> List[Dict[str, Any]]:
        """Generate YouTube automation features."""
        return [
            {"id": "yt001", "name": "유튜브 채널 생성", "emoji": "📷", "category": "youtube_automation", "type": "channel_creation"},
            {"id": "yt002", "name": "채널 프로필 설정", "emoji": "🎨", "category": "youtube_automation", "type": "profile_setup"},
            {"id": "yt003", "name": "동영상 업로드 자동화", "emoji": "📤", "category": "youtube_automation", "type": "upload_automation"},
            {"id": "yt004", "name": "썸네일 자동 생성", "emoji": "🖼️", "category": "youtube_automation", "type": "thumbnail_creation"},
            {"id": "yt005", "name": "제목 최적화", "emoji": "📝", "category": "youtube_automation", "type": "title_optimization"},
            {"id": "yt006", "name": "설명 자동 생성", "emoji": "📄", "category": "youtube_automation", "type": "description_generation"},
            {"id": "yt007", "name": "태그 자동 추가", "emoji": "🏷️", "category": "youtube_automation", "type": "tag_automation"},
            {"id": "yt008", "name": "플레이리스트 관리", "emoji": "📋", "category": "youtube_automation", "type": "playlist_management"},
            {"id": "yt009", "name": "커뮤니티 포스트", "emoji": "📢", "category": "youtube_automation", "type": "community_posting"},
            {"id": "yt010", "name": "스케줄 업로드", "emoji": "⏰", "category": "youtube_automation", "type": "scheduled_upload"},
            {"id": "yt011", "name": "라이브 스트림 설정", "emoji": "🔴", "category": "youtube_automation", "type": "livestream_setup"},
            {"id": "yt012", "name": "채널 최적화", "emoji": "⚙️", "category": "youtube_automation", "type": "channel_optimization"},
            {"id": "yt013", "name": "SEO 최적화", "emoji": "🔍", "category": "youtube_automation", "type": "seo_optimization"},
            {"id": "yt014", "name": "분석 데이터 수집", "emoji": "📊", "category": "youtube_automation", "type": "analytics_collection"},
            {"id": "yt015", "name": "수익화 설정", "emoji": "💰", "category": "youtube_automation", "type": "monetization_setup"}
        ]
    
    def _generate_proxy_features(self) -> List[Dict[str, Any]]:
        """Generate proxy management features."""
        return [
            {"id": "px001", "name": "프록시 자동 로테이션", "emoji": "🔄", "category": "proxy_management", "type": "rotation"},
            {"id": "px002", "name": "프록시 상태 체크", "emoji": "✅", "category": "proxy_management", "type": "health_check"},
            {"id": "px003", "name": "고속 프록시 선별", "emoji": "⚡", "category": "proxy_management", "type": "speed_filtering"},
            {"id": "px004", "name": "지역별 프록시 관리", "emoji": "🌍", "category": "proxy_management", "type": "geo_management"},
            {"id": "px005", "name": "프록시 풀 관리", "emoji": "🏊", "category": "proxy_management", "type": "pool_management"},
            {"id": "px006", "name": "프록시 인증 자동화", "emoji": "🔐", "category": "proxy_management", "type": "auth_automation"},
            {"id": "px007", "name": "프록시 성능 모니터링", "emoji": "📊", "category": "proxy_management", "type": "performance_monitoring"},
            {"id": "px008", "name": "프록시 장애 복구", "emoji": "🔧", "category": "proxy_management", "type": "failure_recovery"},
            {"id": "px009", "name": "프록시 비용 최적화", "emoji": "💰", "category": "proxy_management", "type": "cost_optimization"},
            {"id": "px010", "name": "프록시 보안 검증", "emoji": "🛡️", "category": "proxy_management", "type": "security_validation"}
        ]
    
    def _generate_account_features(self) -> List[Dict[str, Any]]:
        """Generate account creation and management features."""
        return [
            {"id": "ac001", "name": "계정 대량 생성", "emoji": "🏭", "category": "account_creation", "type": "bulk_creation"},
            {"id": "ac002", "name": "신원 정보 생성", "emoji": "🆔", "category": "account_creation", "type": "identity_generation"},
            {"id": "ac003", "name": "전화번호 인증", "emoji": "📞", "category": "account_creation", "type": "phone_verification"},
            {"id": "ac004", "name": "이메일 인증", "emoji": "✉️", "category": "account_creation", "type": "email_verification"},
            {"id": "ac005", "name": "계정 웜업", "emoji": "🔥", "category": "account_creation", "type": "account_warming"},
            {"id": "ac006", "name": "계정 에이징", "emoji": "⏳", "category": "account_creation", "type": "account_aging"},
            {"id": "ac007", "name": "계정 활동 시뮬레이션", "emoji": "🎭", "category": "account_creation", "type": "activity_simulation"},
            {"id": "ac008", "name": "계정 신뢰도 구축", "emoji": "🏆", "category": "account_creation", "type": "trust_building"},
            {"id": "ac009", "name": "계정 그룹 관리", "emoji": "👥", "category": "account_creation", "type": "group_management"},
            {"id": "ac010", "name": "계정 상태 추적", "emoji": "📍", "category": "account_creation", "type": "status_tracking"},
            {"id": "ac011", "name": "계정 복구 시스템", "emoji": "🔄", "category": "account_creation", "type": "recovery_system"},
            {"id": "ac012", "name": "계정 보안 강화", "emoji": "🔒", "category": "account_creation", "type": "security_enhancement"},
            {"id": "ac013", "name": "계정 생명주기 관리", "emoji": "🔄", "category": "account_creation", "type": "lifecycle_management"},
            {"id": "ac014", "name": "계정 품질 관리", "emoji": "⭐", "category": "account_creation", "type": "quality_management"},
            {"id": "ac015", "name": "계정 자동화 스케줄링", "emoji": "📅", "category": "account_creation", "type": "automation_scheduling"}
        ]
    
    def _generate_engagement_features(self) -> List[Dict[str, Any]]:
        """Generate engagement automation features."""
        engagement_features = []
        feature_types = [
            ("자동 댓글봇", "🧠", "comment_bot"),
            ("좋아요 자동화", "👍", "like_automation"),
            ("구독 자동화", "📺", "subscribe_automation"),
            ("공유 자동화", "🔗", "share_automation"),
            ("댓글 응답 봇", "💬", "reply_bot"),
            ("감정 분석 댓글", "😊", "sentiment_comments"),
            ("키워드 기반 댓글", "🔍", "keyword_comments"),
            ("자연어 처리 댓글", "🤖", "nlp_comments"),
            ("다국어 댓글", "🌐", "multilang_comments"),
            ("상황별 댓글", "🎯", "contextual_comments"),
            ("인플루언서 타겟팅", "⭐", "influencer_targeting"),
            ("브랜드 멘션", "🏷️", "brand_mentions"),
            ("해시태그 활용", "#️⃣", "hashtag_usage"),
            ("트렌드 분석", "📈", "trend_analysis"),
            ("경쟁사 분석", "🔍", "competitor_analysis"),
            ("사용자 행동 분석", "👤", "user_behavior"),
            ("참여율 최적화", "⚡", "engagement_optimization"),
            ("시간대별 최적화", "🕐", "timing_optimization"),
            ("콘텐츠 추천", "💡", "content_recommendation"),
            ("자동 스토리 생성", "📖", "story_generation")
        ]
        
        for i, (name, emoji, type_name) in enumerate(feature_types, 1):
            engagement_features.append({
                "id": f"en{i:03d}",
                "name": name,
                "emoji": emoji,
                "category": "engagement_automation",
                "type": type_name,
                "description": f"{name} 자동화 시스템",
                "default_count": 100 + (i * 10),
                "default_duration": 1800 + (i * 300),
                "default_threads": min(20, 5 + i)
            })
        
        return engagement_features
    
    def _generate_analytics_features(self) -> List[Dict[str, Any]]:
        """Generate analytics and monitoring features."""
        return [
            {"id": "an001", "name": "실시간 분석", "emoji": "⚡", "category": "analytics", "type": "realtime_analytics"},
            {"id": "an002", "name": "성과 추적", "emoji": "📊", "category": "analytics", "type": "performance_tracking"},
            {"id": "an003", "name": "ROI 분석", "emoji": "💰", "category": "analytics", "type": "roi_analysis"},
            {"id": "an004", "name": "트래픽 분석", "emoji": "🚦", "category": "analytics", "type": "traffic_analysis"},
            {"id": "an005", "name": "사용자 분석", "emoji": "👥", "category": "analytics", "type": "user_analysis"},
            {"id": "an006", "name": "콘텐츠 분석", "emoji": "📄", "category": "analytics", "type": "content_analysis"},
            {"id": "an007", "name": "키워드 추적", "emoji": "🔍", "category": "analytics", "type": "keyword_tracking"},
            {"id": "an008", "name": "경쟁사 모니터링", "emoji": "👁️", "category": "analytics", "type": "competitor_monitoring"},
            {"id": "an009", "name": "트렌드 예측", "emoji": "🔮", "category": "analytics", "type": "trend_prediction"},
            {"id": "an010", "name": "보고서 자동화", "emoji": "📋", "category": "analytics", "type": "report_automation"},
            {"id": "an011", "name": "알림 시스템", "emoji": "🔔", "category": "analytics", "type": "notification_system"},
            {"id": "an012", "name": "대시보드 생성", "emoji": "📺", "category": "analytics", "type": "dashboard_creation"},
            {"id": "an013", "name": "데이터 시각화", "emoji": "📈", "category": "analytics", "type": "data_visualization"},
            {"id": "an014", "name": "예측 모델링", "emoji": "🧮", "category": "analytics", "type": "predictive_modeling"},
            {"id": "an015", "name": "비즈니스 인텔리전스", "emoji": "🧠", "category": "analytics", "type": "business_intelligence"}
        ]
    
    def _generate_security_features(self) -> List[Dict[str, Any]]:
        """Generate security and privacy features."""
        return [
            {"id": "sc001", "name": "브라우저 핑거프린트 위장", "emoji": "🎭", "category": "security", "type": "fingerprint_spoofing"},
            {"id": "sc002", "name": "IP 추적 방지", "emoji": "🛡️", "category": "security", "type": "ip_protection"},
            {"id": "sc003", "name": "CAPTCHA 자동 해결", "emoji": "🔓", "category": "security", "type": "captcha_solving"},
            {"id": "sc004", "name": "봇 탐지 우회", "emoji": "👻", "category": "security", "type": "bot_detection_bypass"},
            {"id": "sc005", "name": "SSL 인증서 관리", "emoji": "🔒", "category": "security", "type": "ssl_management"},
            {"id": "sc006", "name": "데이터 암호화", "emoji": "🔐", "category": "security", "type": "data_encryption"},
            {"id": "sc007", "name": "로그 보안", "emoji": "📝", "category": "security", "type": "log_security"},
            {"id": "sc008", "name": "접근 제어", "emoji": "🚪", "category": "security", "type": "access_control"},
            {"id": "sc009", "name": "보안 감사", "emoji": "🔍", "category": "security", "type": "security_audit"},
            {"id": "sc010", "name": "침입 탐지", "emoji": "🚨", "category": "security", "type": "intrusion_detection"}
        ]
    
    def _generate_advanced_features(self) -> List[Dict[str, Any]]:
        """Generate advanced features."""
        return [
            {"id": "ad001", "name": "AI 기반 최적화", "emoji": "🤖", "category": "advanced", "type": "ai_optimization"},
            {"id": "ad002", "name": "머신러닝 예측", "emoji": "🧠", "category": "advanced", "type": "ml_prediction"},
            {"id": "ad003", "name": "자동 스케일링", "emoji": "📈", "category": "advanced", "type": "auto_scaling"},
            {"id": "ad004", "name": "로드 밸런싱", "emoji": "⚖️", "category": "advanced", "type": "load_balancing"},
            {"id": "ad005", "name": "분산 처리", "emoji": "🌐", "category": "advanced", "type": "distributed_processing"},
            {"id": "ad006", "name": "클러스터 관리", "emoji": "🔗", "category": "advanced", "type": "cluster_management"},
            {"id": "ad007", "name": "자동 복구", "emoji": "🔄", "category": "advanced", "type": "auto_recovery"},
            {"id": "ad008", "name": "성능 최적화", "emoji": "⚡", "category": "advanced", "type": "performance_optimization"},
            {"id": "ad009", "name": "리소스 관리", "emoji": "💾", "category": "advanced", "type": "resource_management"},
            {"id": "ad010", "name": "API 통합", "emoji": "🔌", "category": "advanced", "type": "api_integration"},
            {"id": "ad011", "name": "웹훅 처리", "emoji": "🎣", "category": "advanced", "type": "webhook_processing"},
            {"id": "ad012", "name": "이벤트 스트리밍", "emoji": "🌊", "category": "advanced", "type": "event_streaming"},
            {"id": "ad013", "name": "실시간 동기화", "emoji": "🔄", "category": "advanced", "type": "realtime_sync"},
            {"id": "ad014", "name": "클라우드 통합", "emoji": "☁️", "category": "advanced", "type": "cloud_integration"},
            {"id": "ad015", "name": "마이크로서비스", "emoji": "🧩", "category": "advanced", "type": "microservices"}
        ]
    
    def generate_all_function_macros(self) -> List[str]:
        """Generate all function macros for enabled features."""
        macros = []
        
        for feature in self.features:
            if self._is_feature_enabled(feature):
                try:
                    macro_xml = self.template_engine.render_feature_macro(feature)
                    macros.append(macro_xml)
                    self.logger.debug(f"Generated macro for feature: {feature['name']}")
                except Exception as e:
                    self.logger.error(f"Failed to generate macro for {feature['name']}: {e}")
                    continue
        
        self.logger.info(f"Generated {len(macros)} function macros")
        return macros
    
    def _is_feature_enabled(self, feature: Dict[str, Any]) -> bool:
        """Check if a feature is enabled in configuration."""
        category = feature.get('category', '')
        
        # Check if category is enabled
        if category in self.config.enabled_features:
            return True
        
        # Check for specific feature enablement
        feature_key = f"{category}_{feature.get('type', '')}"
        if feature_key in self.config.enabled_features:
            return True
        
        # Default to enabled if no specific configuration
        return True
    
    def generate_feature_category_macros(self, category: str) -> List[str]:
        """Generate macros for a specific feature category."""
        category_features = [f for f in self.features if f.get('category') == category]
        macros = []
        
        for feature in category_features:
            try:
                macro_xml = self.template_engine.render_feature_macro(feature)
                macros.append(macro_xml)
            except Exception as e:
                self.logger.error(f"Failed to generate macro for {feature['name']}: {e}")
                continue
        
        self.logger.info(f"Generated {len(macros)} macros for category: {category}")
        return macros
    
    def get_features_summary(self) -> Dict[str, Any]:
        """Get summary of all features by category."""
        summary = {}
        
        for feature in self.features:
            category = feature.get('category', 'unknown')
            if category not in summary:
                summary[category] = {
                    'count': 0,
                    'features': []
                }
            
            summary[category]['count'] += 1
            summary[category]['features'].append({
                'id': feature.get('id'),
                'name': feature.get('name'),
                'emoji': feature.get('emoji'),
                'type': feature.get('type')
            })
        
        # Add total count
        summary['total_features'] = len(self.features)
        summary['total_categories'] = len([k for k in summary.keys() if k != 'total_features'])
        
        return summary
    
    def generate_main_controller_macro(self) -> str:
        """Generate main controller macro that orchestrates all features."""
        controller_template = '''
  <macro name="MainController">
    <action name="LogEvent">
      <Type>SYSTEM_START</Type>
      <Level>INFO</Level>
      <Details>🚀 HDGRACE BAS System Started - {total_features} features available</Details>
    </action>
    
    <action name="InitializeSystem">
      <Features>{total_features}</Features>
      <Categories>{total_categories}</Categories>
      <Version>{bas_version}</Version>
    </action>
    
    <!-- Execute all enabled feature categories -->
{feature_calls}
    
    <action name="LogEvent">
      <Type>SYSTEM_COMPLETE</Type>
      <Level>INFO</Level>
      <Details>✅ All features executed successfully</Details>
    </action>
  </macro>'''
        
        # Generate feature calls
        summary = self.get_features_summary()
        feature_calls = []
        
        for category in summary:
            if category not in ['total_features', 'total_categories']:
                call_xml = f'''    <action name="CallMacro">
      <Name>Execute_{category.title().replace("_", "")}</Name>
    </action>'''
                feature_calls.append(call_xml)
        
        formatted_calls = '\n'.join(feature_calls)
        
        return controller_template.format(
            total_features=summary['total_features'],
            total_categories=summary['total_categories'],
            bas_version=self.config.bas_version,
            feature_calls=formatted_calls
        )