class HackFlixException(Exception):
    """Base exception for HackFlix"""
    pass


class ConfigurationError(HackFlixException):
    """Configuration related errors"""
    pass


class ExtractionError(HackFlixException):
    """Extraction engine errors"""
    pass


class ScraperError(ExtractionError):
    """Scraper specific errors"""
    pass


class NormalizationError(HackFlixException):
    """Normalization errors"""
    pass


class PersistenceError(HackFlixException):
    """Database/storage errors"""
    pass


class ValidationError(HackFlixException):
    """Data validation errors"""
    pass


class RateLimitError(HackFlixException):
    """Rate limiting errors"""
    pass


class PlatformUnavailableError(HackFlixException):
    """Platform temporarily unavailable"""
    pass
