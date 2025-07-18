"""
Example usage of the custom interval functionality.

This script demonstrates how to use the interval resolution system
for both backward compatibility and new granular interval features.
"""

from interval_resolution import (
    ResolutionEnum, IntervalEnum, IntervalConverter,
    create_interval_config, validate_interval_compatibility
)


def demonstrate_basic_usage():
    """Demonstrate basic usage of ResolutionEnum and IntervalEnum."""
    print("=== Basic Usage ===")
    
    # Basic ResolutionEnum usage (backward compatibility)
    print(f"ResolutionEnum.MINUTE: {ResolutionEnum.MINUTE.value}")
    print(f"ResolutionEnum.HOUR: {ResolutionEnum.HOUR.value}")
    print(f"ResolutionEnum.DAY: {ResolutionEnum.DAY.value}")
    print()
    
    # IntervalEnum usage
    print("Available intervals:")
    for interval in IntervalEnum:
        print(f"  {interval.name}: {interval.minutes} minutes ({interval.seconds} seconds) - {str(interval)}")
    print()


def demonstrate_converter_utilities():
    """Demonstrate IntervalConverter utility functions."""
    print("=== Converter Utilities ===")
    
    # Convert minutes to intervals
    test_minutes = [1, 5, 10, 12, 15, 20, 30, 45, 60, 90]
    print("Converting minutes to intervals:")
    for minutes in test_minutes:
        interval = IntervalConverter.from_minutes(minutes)
        is_valid = IntervalConverter.is_valid_interval(minutes)
        closest = IntervalConverter.get_closest_interval(minutes)
        
        print(f"  {minutes} min -> Valid: {is_valid}, Exact: {interval}, Closest: {closest}")
    print()
    
    # Supported intervals
    supported = IntervalConverter.get_supported_intervals()
    print(f"Supported intervals: {supported}")
    print()


def demonstrate_configuration():
    """Demonstrate configuration creation."""
    print("=== Configuration Examples ===")
    
    # Default configuration (backward compatible)
    config1 = create_interval_config()
    print("Default config (backward compatible):")
    print(f"  Resolution: {config1['resolution']}")
    print(f"  Interval: {config1['interval']} ({config1['interval_minutes']} min)")
    print()
    
    # Specific interval configuration
    config2 = create_interval_config(
        resolution=ResolutionEnum.MINUTE,
        interval=IntervalEnum.MINUTE_15
    )
    print("15-minute interval config:")
    print(f"  Resolution: {config2['resolution']}")
    print(f"  Interval: {config2['interval']} ({config2['interval_minutes']} min)")
    print(f"  Description: {config2['interval_str']}")
    print()
    
    # Non-minute resolution (no interval)
    config3 = create_interval_config(resolution=ResolutionEnum.HOUR)
    print("Hour resolution config (no interval):")
    print(f"  Resolution: {config3['resolution']}")
    print(f"  Has interval: {'interval' in config3}")
    print()


def demonstrate_compatibility_validation():
    """Demonstrate compatibility validation."""
    print("=== Compatibility Validation ===")
    
    test_cases = [
        (ResolutionEnum.MINUTE, None),
        (ResolutionEnum.MINUTE, IntervalEnum.MINUTE_1),
        (ResolutionEnum.MINUTE, IntervalEnum.MINUTE_30),
        (ResolutionEnum.HOUR, None),
        (ResolutionEnum.HOUR, IntervalEnum.MINUTE_1),  # Should be invalid
        (ResolutionEnum.DAY, IntervalEnum.MINUTE_15),  # Should be invalid
    ]
    
    for resolution, interval in test_cases:
        is_compatible = validate_interval_compatibility(resolution, interval)
        interval_str = str(interval) if interval else "None"
        print(f"  {resolution.value} + {interval_str}: {'✓' if is_compatible else '✗'}")
    print()


def demonstrate_backward_compatibility():
    """Demonstrate backward compatibility scenarios."""
    print("=== Backward Compatibility ===")
    
    # Simulate existing code that uses ResolutionEnum.MINUTE
    def existing_function(resolution: ResolutionEnum = ResolutionEnum.MINUTE):
        """Simulates an existing function that uses resolution parameter."""
        config = create_interval_config(resolution=resolution)
        return config
    
    # Call with default (existing behavior)
    result1 = existing_function()
    print("Existing function with default parameter:")
    print(f"  Gets: {result1['interval']} ({result1['interval_minutes']} min)")
    print()
    
    # Call with explicit ResolutionEnum.MINUTE (existing behavior)
    result2 = existing_function(ResolutionEnum.MINUTE)
    print("Existing function with explicit MINUTE:")
    print(f"  Gets: {result2['interval']} ({result2['interval_minutes']} min)")
    print()
    
    # New enhanced function with interval support
    def enhanced_function(
        resolution: ResolutionEnum = ResolutionEnum.MINUTE,
        interval: IntervalEnum = None
    ):
        """Enhanced function that supports both resolution and interval."""
        config = create_interval_config(resolution=resolution, interval=interval)
        return config
    
    # Enhanced usage with specific intervals
    result3 = enhanced_function(interval=IntervalEnum.MINUTE_15)
    print("Enhanced function with 15-minute interval:")
    print(f"  Gets: {result3['interval']} ({result3['interval_minutes']} min)")
    print()


def demonstrate_real_world_scenarios():
    """Demonstrate real-world usage scenarios."""
    print("=== Real-World Scenarios ===")
    
    # Scenario 1: Data aggregation service
    print("1. Data Aggregation Service:")
    intervals = [IntervalEnum.MINUTE_1, IntervalEnum.MINUTE_15, IntervalEnum.MINUTE_60]
    for interval in intervals:
        config = create_interval_config(interval=interval)
        print(f"   Aggregate data every {config['interval_str']} ({config['interval_seconds']} sec window)")
    print()
    
    # Scenario 2: Chart display options
    print("2. Chart Display Options:")
    user_preferences = [5, 10, 15, 30, 60, 120]  # User wants these intervals
    for pref in user_preferences:
        if IntervalConverter.is_valid_interval(pref):
            interval = IntervalConverter.from_minutes(pref)
            print(f"   {pref} min request -> Use {interval}")
        else:
            closest = IntervalConverter.get_closest_interval(pref)
            print(f"   {pref} min request -> Use closest: {closest}")
    print()
    
    # Scenario 3: API rate limiting
    print("3. API Rate Limiting:")
    for interval in IntervalEnum:
        requests_per_interval = 60 // interval.minutes  # Max 60 requests per hour
        print(f"   {interval}: max {requests_per_interval} requests per {interval.minutes}-minute window")
    print()


if __name__ == "__main__":
    print("Custom Interval Resolution System Demo")
    print("=" * 50)
    print()
    
    demonstrate_basic_usage()
    demonstrate_converter_utilities()
    demonstrate_configuration()
    demonstrate_compatibility_validation()
    demonstrate_backward_compatibility()
    demonstrate_real_world_scenarios()
    
    print("Demo completed successfully! ✓")