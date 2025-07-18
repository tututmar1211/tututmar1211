"""
Custom interval functionality that extends ResolutionEnum.MINUTE to support specific minute intervals.

This module provides:
- ResolutionEnum with MINUTE support for backward compatibility
- IntervalEnum with specific minute intervals (1, 10, 15, 30, 60 minutes)
- Utility functions for interval conversion and validation
"""

from enum import Enum
from typing import Union, Optional


class ResolutionEnum(Enum):
    """
    Resolution enumeration for backward compatibility.
    
    This enum maintains compatibility with existing code that uses ResolutionEnum.MINUTE.
    """
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"


class IntervalEnum(Enum):
    """
    Interval enumeration for specific minute intervals.
    
    Supports granular minute intervals: 1, 10, 15, 30, and 60 minutes.
    """
    MINUTE_1 = 1
    MINUTE_10 = 10
    MINUTE_15 = 15
    MINUTE_30 = 30
    MINUTE_60 = 60

    @property
    def minutes(self) -> int:
        """Return the interval value in minutes."""
        return self.value

    @property
    def seconds(self) -> int:
        """Return the interval value in seconds."""
        return self.value * 60

    def __str__(self) -> str:
        """String representation of the interval."""
        if self.value == 1:
            return "1 minute"
        return f"{self.value} minutes"


class IntervalConverter:
    """Utility class for interval conversion and validation."""
    
    @staticmethod
    def from_minutes(minutes: int) -> Optional[IntervalEnum]:
        """
        Convert minutes to IntervalEnum if supported.
        
        Args:
            minutes: Number of minutes
            
        Returns:
            IntervalEnum if the minutes value is supported, None otherwise
        """
        for interval in IntervalEnum:
            if interval.value == minutes:
                return interval
        return None
    
    @staticmethod
    def to_resolution(interval: Union[IntervalEnum, ResolutionEnum]) -> ResolutionEnum:
        """
        Convert IntervalEnum to ResolutionEnum for backward compatibility.
        
        Args:
            interval: IntervalEnum or ResolutionEnum instance
            
        Returns:
            ResolutionEnum.MINUTE for all IntervalEnum values, 
            or the original ResolutionEnum value
        """
        if isinstance(interval, IntervalEnum):
            return ResolutionEnum.MINUTE
        return interval
    
    @staticmethod
    def get_supported_intervals() -> list[int]:
        """
        Get list of supported interval values in minutes.
        
        Returns:
            List of supported minute intervals
        """
        return [interval.value for interval in IntervalEnum]
    
    @staticmethod
    def is_valid_interval(minutes: int) -> bool:
        """
        Check if a minute value is a supported interval.
        
        Args:
            minutes: Number of minutes to validate
            
        Returns:
            True if the interval is supported, False otherwise
        """
        return minutes in IntervalConverter.get_supported_intervals()
    
    @staticmethod
    def get_closest_interval(minutes: int) -> IntervalEnum:
        """
        Get the closest supported interval to the given minutes.
        
        Args:
            minutes: Target minutes value
            
        Returns:
            The closest supported IntervalEnum
        """
        supported = IntervalConverter.get_supported_intervals()
        closest = min(supported, key=lambda x: abs(x - minutes))
        return IntervalConverter.from_minutes(closest)


def create_interval_config(
    resolution: ResolutionEnum = ResolutionEnum.MINUTE,
    interval: Optional[IntervalEnum] = None
) -> dict:
    """
    Create a configuration dictionary for interval-aware processing.
    
    This function maintains backward compatibility while allowing for granular interval control.
    
    Args:
        resolution: ResolutionEnum for backward compatibility (default: MINUTE)
        interval: Optional IntervalEnum for specific minute intervals
        
    Returns:
        Dictionary containing resolution and interval configuration
    """
    config = {
        "resolution": resolution,
        "resolution_value": resolution.value
    }
    
    if interval is not None:
        config.update({
            "interval": interval,
            "interval_minutes": interval.minutes,
            "interval_seconds": interval.seconds,
            "interval_str": str(interval)
        })
    elif resolution == ResolutionEnum.MINUTE:
        # Default to 1-minute interval for backward compatibility
        config.update({
            "interval": IntervalEnum.MINUTE_1,
            "interval_minutes": 1,
            "interval_seconds": 60,
            "interval_str": "1 minute"
        })
    
    return config


def validate_interval_compatibility(
    resolution: ResolutionEnum,
    interval: Optional[IntervalEnum] = None
) -> bool:
    """
    Validate that the interval is compatible with the resolution.
    
    Args:
        resolution: ResolutionEnum value
        interval: Optional IntervalEnum value
        
    Returns:
        True if compatible, False otherwise
    """
    if interval is None:
        return True
    
    # IntervalEnum is only compatible with MINUTE resolution
    if resolution != ResolutionEnum.MINUTE:
        return False
    
    return True


# Backward compatibility aliases
Resolution = ResolutionEnum  # For existing code that might use 'Resolution'