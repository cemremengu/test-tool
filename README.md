# Random Time Series API

A simple FastAPI tool that generates random time series data for any city name. Perfect for testing LLMs with realistic datasets.

## Features

- Generate time series data for any city
- Multiple metrics: temperature, humidity, pressure, wind_speed, rainfall
- Configurable time ranges (1-365 days)
- Realistic patterns with daily cycles and random noise
- Interactive OpenAPI documentation

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
python main.py
```

### Docker

```bash
# Build and run
# Set OPENAPI_SERVER_URL to your desired server URL (optional)
docker build -t timeseries-api .
docker save timeseries-api > timeseries-api.tar
# Example: set OpenAPI server URL to http://myserver:8000
docker run -d -p 8000:8000 -e OPENAPI_SERVER_URL=http://myserver:8000 timeseries-api
# Or use default (http://localhost:8000)
docker run -d -p 8000:8000 timeseries-api
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Example Usage

```bash
# Get 7 days of temperature data for London
curl "http://localhost:8000/timeseries/london"

# Get 30 days of humidity data for Tokyo
curl "http://localhost:8000/timeseries/tokyo?metric=humidity&days=30"

# Get random city name
curl "http://localhost:8000/cities/random"

# List available metrics
curl "http://localhost:8000/metrics"
```

## Endpoints

- `GET /timeseries/{city}` - Generate time series data
- `GET /cities/random` - Get random city name
- `GET /metrics` - List available metrics
- `GET /docs` - API documentation

## Parameters

- **city**: Any city name
- **metric**: temperature, humidity, pressure, wind_speed, rainfall
- **days**: Number of days (1-365)
- **points_per_day**: Data points per day (1-144)

Perfect for testing your LLM with varied time series scenarios!
