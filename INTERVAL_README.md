# Custom Interval Resolution System

This repository implements a custom interval functionality that extends the current `ResolutionEnum.MINUTE` to support specific minute intervals with ranges of 1, 10, 15, 30, and 60 minutes.

## Features

- **ResolutionEnum**: Backward-compatible resolution enumeration with MINUTE, HOUR, and DAY values
- **IntervalEnum**: Granular minute intervals (1, 10, 15, 30, 60 minutes)  
- **IntervalConverter**: Utility functions for interval conversion and validation
- **Configuration helpers**: Functions to create interval-aware configurations
- **Full backward compatibility**: Existing code using `ResolutionEnum.MINUTE` continues to work

## Quick Start

```python
from interval_resolution import ResolutionEnum, IntervalEnum, create_interval_config

# Backward compatible usage
config = create_interval_config(resolution=ResolutionEnum.MINUTE)
print(config['interval'])  # 1 minute (default)

# New granular interval usage  
config = create_interval_config(
    resolution=ResolutionEnum.MINUTE,
    interval=IntervalEnum.MINUTE_15
)
print(config['interval_minutes'])  # 15
```

## IntervalEnum Values

| Enum Value | Minutes | Seconds | String Representation |
|------------|---------|---------|----------------------|
| `MINUTE_1` | 1 | 60 | "1 minute" |
| `MINUTE_10` | 10 | 600 | "10 minutes" |
| `MINUTE_15` | 15 | 900 | "15 minutes" |
| `MINUTE_30` | 30 | 1800 | "30 minutes" |
| `MINUTE_60` | 60 | 3600 | "60 minutes" |

## Utility Functions

### IntervalConverter Methods

- `from_minutes(minutes: int)` - Convert minutes to IntervalEnum if supported
- `to_resolution(interval)` - Convert IntervalEnum to ResolutionEnum for compatibility  
- `get_supported_intervals()` - Get list of supported minute values
- `is_valid_interval(minutes: int)` - Check if a minute value is supported
- `get_closest_interval(minutes: int)` - Get closest supported interval

### Configuration Functions

- `create_interval_config(resolution, interval)` - Create interval-aware configuration
- `validate_interval_compatibility(resolution, interval)` - Validate resolution/interval compatibility

## Usage Examples

### Basic Interval Usage

```python
from interval_resolution import IntervalEnum

# Access interval properties
interval = IntervalEnum.MINUTE_15
print(interval.minutes)  # 15
print(interval.seconds)  # 900  
print(str(interval))     # "15 minutes"
```

### Converter Utilities

```python
from interval_resolution import IntervalConverter

# Convert minutes to intervals
interval = IntervalConverter.from_minutes(15)  # IntervalEnum.MINUTE_15
invalid = IntervalConverter.from_minutes(7)    # None

# Get closest supported interval
closest = IntervalConverter.get_closest_interval(12)  # IntervalEnum.MINUTE_10

# Validate intervals
is_valid = IntervalConverter.is_valid_interval(30)  # True
is_invalid = IntervalConverter.is_valid_interval(7)  # False
```

### Configuration Creation

```python
from interval_resolution import ResolutionEnum, IntervalEnum, create_interval_config

# Default configuration (backward compatible)
config = create_interval_config()
# Returns: resolution=MINUTE, interval=MINUTE_1

# Specific interval configuration
config = create_interval_config(
    resolution=ResolutionEnum.MINUTE,
    interval=IntervalEnum.MINUTE_30
)
# Returns: resolution=MINUTE, interval=MINUTE_30, interval_minutes=30, etc.

# Non-minute resolution (no interval support)
config = create_interval_config(resolution=ResolutionEnum.HOUR)
# Returns: resolution=HOUR (no interval fields)
```

### Backward Compatibility

```python
from interval_resolution import ResolutionEnum, create_interval_config

# Existing code pattern - still works!
def existing_function(resolution: ResolutionEnum = ResolutionEnum.MINUTE):
    config = create_interval_config(resolution=resolution)
    return config

result = existing_function()  # Gets MINUTE_1 interval automatically
```

## Real-World Use Cases

### Data Aggregation

```python
# Configure different aggregation intervals
intervals = [IntervalEnum.MINUTE_1, IntervalEnum.MINUTE_15, IntervalEnum.MINUTE_60]

for interval in intervals:
    config = create_interval_config(interval=interval)
    print(f"Aggregate every {config['interval_str']}")
```

### Chart Display Options

```python
# Handle user-requested intervals with fallback to closest supported
user_requests = [5, 10, 15, 25, 60]

for minutes in user_requests:
    if IntervalConverter.is_valid_interval(minutes):
        interval = IntervalConverter.from_minutes(minutes)
    else:
        interval = IntervalConverter.get_closest_interval(minutes)
    
    print(f"User wants {minutes}min -> Use {interval}")
```

### API Rate Limiting

```python
# Configure rate limits based on intervals
for interval in IntervalEnum:
    max_requests = 60 // interval.minutes  # 60 requests per hour max
    print(f"{interval}: {max_requests} requests per {interval.minutes}-minute window")
```

## Compatibility

- **Backward Compatible**: All existing `ResolutionEnum.MINUTE` usage continues to work
- **Type Safe**: Full type hints for better IDE support
- **Validation**: Built-in compatibility validation between resolutions and intervals
- **Extensible**: Easy to add new intervals or extend functionality

## Testing

Run the comprehensive test suite:

```bash
python -m unittest test_interval_resolution -v
```

## Example Script

See `example_usage.py` for a complete demonstration:

```bash
python example_usage.py
```

This will show all features in action with real-world scenarios and output examples.

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## License

This project is part of the TUTUT MARTAMTI profile repository.