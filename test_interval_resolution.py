"""
Tests for the custom interval functionality.

This module tests:
- ResolutionEnum functionality and backward compatibility
- IntervalEnum with specific minute intervals
- Utility functions for conversion and validation
- Integration between intervals and resolutions
"""

import unittest
from interval_resolution import (
    ResolutionEnum, IntervalEnum, IntervalConverter,
    create_interval_config, validate_interval_compatibility,
    Resolution  # Test backward compatibility alias
)


class TestResolutionEnum(unittest.TestCase):
    """Test cases for ResolutionEnum."""
    
    def test_resolution_enum_values(self):
        """Test that ResolutionEnum has expected values."""
        self.assertEqual(ResolutionEnum.MINUTE.value, "minute")
        self.assertEqual(ResolutionEnum.HOUR.value, "hour")
        self.assertEqual(ResolutionEnum.DAY.value, "day")
    
    def test_backward_compatibility_alias(self):
        """Test that Resolution alias works for backward compatibility."""
        self.assertIs(Resolution, ResolutionEnum)
        self.assertEqual(Resolution.MINUTE.value, "minute")


class TestIntervalEnum(unittest.TestCase):
    """Test cases for IntervalEnum."""
    
    def test_interval_enum_values(self):
        """Test that IntervalEnum has correct minute values."""
        self.assertEqual(IntervalEnum.MINUTE_1.value, 1)
        self.assertEqual(IntervalEnum.MINUTE_10.value, 10)
        self.assertEqual(IntervalEnum.MINUTE_15.value, 15)
        self.assertEqual(IntervalEnum.MINUTE_30.value, 30)
        self.assertEqual(IntervalEnum.MINUTE_60.value, 60)
    
    def test_interval_minutes_property(self):
        """Test the minutes property."""
        self.assertEqual(IntervalEnum.MINUTE_1.minutes, 1)
        self.assertEqual(IntervalEnum.MINUTE_10.minutes, 10)
        self.assertEqual(IntervalEnum.MINUTE_15.minutes, 15)
        self.assertEqual(IntervalEnum.MINUTE_30.minutes, 30)
        self.assertEqual(IntervalEnum.MINUTE_60.minutes, 60)
    
    def test_interval_seconds_property(self):
        """Test the seconds property."""
        self.assertEqual(IntervalEnum.MINUTE_1.seconds, 60)
        self.assertEqual(IntervalEnum.MINUTE_10.seconds, 600)
        self.assertEqual(IntervalEnum.MINUTE_15.seconds, 900)
        self.assertEqual(IntervalEnum.MINUTE_30.seconds, 1800)
        self.assertEqual(IntervalEnum.MINUTE_60.seconds, 3600)
    
    def test_interval_string_representation(self):
        """Test string representation of intervals."""
        self.assertEqual(str(IntervalEnum.MINUTE_1), "1 minute")
        self.assertEqual(str(IntervalEnum.MINUTE_10), "10 minutes")
        self.assertEqual(str(IntervalEnum.MINUTE_15), "15 minutes")
        self.assertEqual(str(IntervalEnum.MINUTE_30), "30 minutes")
        self.assertEqual(str(IntervalEnum.MINUTE_60), "60 minutes")


class TestIntervalConverter(unittest.TestCase):
    """Test cases for IntervalConverter utility functions."""
    
    def test_from_minutes_valid(self):
        """Test conversion from valid minute values."""
        self.assertEqual(IntervalConverter.from_minutes(1), IntervalEnum.MINUTE_1)
        self.assertEqual(IntervalConverter.from_minutes(10), IntervalEnum.MINUTE_10)
        self.assertEqual(IntervalConverter.from_minutes(15), IntervalEnum.MINUTE_15)
        self.assertEqual(IntervalConverter.from_minutes(30), IntervalEnum.MINUTE_30)
        self.assertEqual(IntervalConverter.from_minutes(60), IntervalEnum.MINUTE_60)
    
    def test_from_minutes_invalid(self):
        """Test conversion from invalid minute values."""
        self.assertIsNone(IntervalConverter.from_minutes(5))
        self.assertIsNone(IntervalConverter.from_minutes(20))
        self.assertIsNone(IntervalConverter.from_minutes(45))
        self.assertIsNone(IntervalConverter.from_minutes(120))
    
    def test_to_resolution_from_interval(self):
        """Test conversion from IntervalEnum to ResolutionEnum."""
        for interval in IntervalEnum:
            result = IntervalConverter.to_resolution(interval)
            self.assertEqual(result, ResolutionEnum.MINUTE)
    
    def test_to_resolution_from_resolution(self):
        """Test that ResolutionEnum passes through unchanged."""
        for resolution in ResolutionEnum:
            result = IntervalConverter.to_resolution(resolution)
            self.assertEqual(result, resolution)
    
    def test_get_supported_intervals(self):
        """Test getting list of supported intervals."""
        supported = IntervalConverter.get_supported_intervals()
        expected = [1, 10, 15, 30, 60]
        self.assertEqual(sorted(supported), expected)
    
    def test_is_valid_interval(self):
        """Test interval validation."""
        # Valid intervals
        self.assertTrue(IntervalConverter.is_valid_interval(1))
        self.assertTrue(IntervalConverter.is_valid_interval(10))
        self.assertTrue(IntervalConverter.is_valid_interval(15))
        self.assertTrue(IntervalConverter.is_valid_interval(30))
        self.assertTrue(IntervalConverter.is_valid_interval(60))
        
        # Invalid intervals
        self.assertFalse(IntervalConverter.is_valid_interval(5))
        self.assertFalse(IntervalConverter.is_valid_interval(20))
        self.assertFalse(IntervalConverter.is_valid_interval(45))
        self.assertFalse(IntervalConverter.is_valid_interval(120))
    
    def test_get_closest_interval(self):
        """Test getting closest supported interval."""
        # Test exact matches
        self.assertEqual(IntervalConverter.get_closest_interval(1), IntervalEnum.MINUTE_1)
        self.assertEqual(IntervalConverter.get_closest_interval(15), IntervalEnum.MINUTE_15)
        
        # Test approximate matches
        self.assertEqual(IntervalConverter.get_closest_interval(2), IntervalEnum.MINUTE_1)
        self.assertEqual(IntervalConverter.get_closest_interval(8), IntervalEnum.MINUTE_10)
        self.assertEqual(IntervalConverter.get_closest_interval(12), IntervalEnum.MINUTE_10)
        self.assertEqual(IntervalConverter.get_closest_interval(18), IntervalEnum.MINUTE_15)
        self.assertEqual(IntervalConverter.get_closest_interval(25), IntervalEnum.MINUTE_30)
        self.assertEqual(IntervalConverter.get_closest_interval(45), IntervalEnum.MINUTE_30)
        self.assertEqual(IntervalConverter.get_closest_interval(90), IntervalEnum.MINUTE_60)


class TestConfigurationFunctions(unittest.TestCase):
    """Test cases for configuration and validation functions."""
    
    def test_create_interval_config_default(self):
        """Test creating config with default parameters."""
        config = create_interval_config()
        
        self.assertEqual(config["resolution"], ResolutionEnum.MINUTE)
        self.assertEqual(config["resolution_value"], "minute")
        self.assertEqual(config["interval"], IntervalEnum.MINUTE_1)
        self.assertEqual(config["interval_minutes"], 1)
        self.assertEqual(config["interval_seconds"], 60)
        self.assertEqual(config["interval_str"], "1 minute")
    
    def test_create_interval_config_with_interval(self):
        """Test creating config with specific interval."""
        config = create_interval_config(
            resolution=ResolutionEnum.MINUTE,
            interval=IntervalEnum.MINUTE_15
        )
        
        self.assertEqual(config["resolution"], ResolutionEnum.MINUTE)
        self.assertEqual(config["resolution_value"], "minute")
        self.assertEqual(config["interval"], IntervalEnum.MINUTE_15)
        self.assertEqual(config["interval_minutes"], 15)
        self.assertEqual(config["interval_seconds"], 900)
        self.assertEqual(config["interval_str"], "15 minutes")
    
    def test_create_interval_config_non_minute_resolution(self):
        """Test creating config with non-minute resolution."""
        config = create_interval_config(resolution=ResolutionEnum.HOUR)
        
        self.assertEqual(config["resolution"], ResolutionEnum.HOUR)
        self.assertEqual(config["resolution_value"], "hour")
        self.assertNotIn("interval", config)
        self.assertNotIn("interval_minutes", config)
        self.assertNotIn("interval_seconds", config)
        self.assertNotIn("interval_str", config)
    
    def test_validate_interval_compatibility(self):
        """Test interval compatibility validation."""
        # Compatible combinations
        self.assertTrue(validate_interval_compatibility(ResolutionEnum.MINUTE, None))
        self.assertTrue(validate_interval_compatibility(ResolutionEnum.MINUTE, IntervalEnum.MINUTE_1))
        self.assertTrue(validate_interval_compatibility(ResolutionEnum.MINUTE, IntervalEnum.MINUTE_30))
        self.assertTrue(validate_interval_compatibility(ResolutionEnum.HOUR, None))
        self.assertTrue(validate_interval_compatibility(ResolutionEnum.DAY, None))
        
        # Incompatible combinations
        self.assertFalse(validate_interval_compatibility(ResolutionEnum.HOUR, IntervalEnum.MINUTE_1))
        self.assertFalse(validate_interval_compatibility(ResolutionEnum.DAY, IntervalEnum.MINUTE_15))


class TestBackwardCompatibility(unittest.TestCase):
    """Test cases for backward compatibility."""
    
    def test_existing_minute_resolution_usage(self):
        """Test that existing ResolutionEnum.MINUTE usage still works."""
        # This simulates existing code that uses resolution=ResolutionEnum.MINUTE
        resolution = ResolutionEnum.MINUTE
        config = create_interval_config(resolution=resolution)
        
        # Should automatically get 1-minute interval for backward compatibility
        self.assertEqual(config["resolution"], ResolutionEnum.MINUTE)
        self.assertEqual(config["interval"], IntervalEnum.MINUTE_1)
        self.assertEqual(config["interval_minutes"], 1)
    
    def test_resolution_enum_maintains_interface(self):
        """Test that ResolutionEnum maintains its interface."""
        # Test that existing code using ResolutionEnum still works
        resolution = ResolutionEnum.MINUTE
        self.assertEqual(resolution.value, "minute")
        
        # Test string representation and comparison
        self.assertEqual(str(resolution), "ResolutionEnum.MINUTE")
        self.assertTrue(resolution == ResolutionEnum.MINUTE)


if __name__ == "__main__":
    unittest.main()