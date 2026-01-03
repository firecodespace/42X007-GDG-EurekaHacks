from enum import Enum
from pydantic import BaseModel
from typing import Optional, List


class PlatformType(str, Enum):
    INDEX = "index"
    CANONICAL = "canonical"
    EXTERNAL = "external"


class Platform(BaseModel):
    name: str
    domain: str
    base_url: str
    platform_type: PlatformType
    
    requires_authentication: bool = False
    has_api: bool = False
    
    rate_limit_requests: Optional[int] = None
    rate_limit_period: Optional[int] = None
    
    supports_pagination: bool = True
    max_pages: Optional[int] = None
    
    css_selectors: Optional[dict] = None
    
    notes: Optional[str] = None


SUPPORTED_PLATFORMS = {
    "unstop": Platform(
        name="Unstop",
        domain="unstop.com",
        base_url="https://unstop.com",
        platform_type=PlatformType.INDEX,
        supports_pagination=True,
        notes="Index platform that links to external organizer sites"
    ),
    "devpost": Platform(
        name="Devpost",
        domain="devpost.com",
        base_url="https://devpost.com",
        platform_type=PlatformType.INDEX,
        supports_pagination=True,
        notes="Index platform with mixed internal/external events"
    ),
    "devfolio": Platform(
        name="Devfolio",
        domain="devfolio.co",
        base_url="https://devfolio.co",
        platform_type=PlatformType.CANONICAL,
        supports_pagination=True,
        notes="Canonical source with structured event data"
    ),
    "hack2skill": Platform(
        name="Hack2Skill",
        domain="hack2skill.com",
        base_url="https://www.hack2skill.com",
        platform_type=PlatformType.CANONICAL,
        supports_pagination=True,
        notes="Canonical source with consistent layout"
    ),
    "devnovate": Platform(
        name="Devnovate",
        domain="devnovate.com",
        base_url="https://devnovate.com",
        platform_type=PlatformType.CANONICAL,
        supports_pagination=True,
        notes="Canonical source for competitions"
    )
}


def get_platform_by_domain(domain: str) -> Optional[Platform]:
    """Get platform configuration by domain"""
    domain = domain.lower().replace('www.', '')
    
    for platform_key, platform in SUPPORTED_PLATFORMS.items():
        if platform.domain in domain:
            return platform
    
    return None
