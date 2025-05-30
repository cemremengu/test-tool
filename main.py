import math
import random
from datetime import datetime, timedelta
from typing import List

import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(
    title="Weather Time Series API",
    description="Generate random time series data for any city - Perfect for testing with realistic time series datasets",
    servers=[
        {"url": "http://localhost:8000", "description": "Local server"},
    ],
    version="1.0.0",
    openapi_tags=[
        {"name": "timeseries", "description": "Time series data generation endpoints"},
        {"name": "utilities", "description": "Helper endpoints for testing"},
    ],
)


class DataPoint(BaseModel):
    timestamp: str
    value: float


class TimeSeriesResponse(BaseModel):
    city: str
    metric: str
    data: List[DataPoint]
    total_points: int


@app.get(
    "/timeseries/{city}",
    response_model=TimeSeriesResponse,
    tags=["timeseries"],
    operation_id="timeseries",
    description="Generate a time series dataset for a given city and metric",
)
def get_timeseries(
    city: str,
    metric: str = Query(
        default="temperature",
        description="Metric type to generate",
        examples={
            "temperature": "temperature",
            "humidity": "humidity",
            "pressure": "pressure",
            "wind_speed": "wind_speed",
            "rainfall": "rainfall",
        },
    ),
    days: int = Query(
        default=7,
        ge=1,
        le=365,
        description="Number of days of historical data to generate",
        examples={
            "1 day": 1,
            "7 days": 7,
            "30 days": 30,
            "365 days": 365,
        },
    ),
    points_per_day: int = Query(
        default=24,
        ge=1,
        le=144,
        description="Data points per day (24=hourly, 144=every 10 minutes)",
        examples={
            "hourly": 24,
            "every 10 minutes": 144,
            "every 15 minutes": 96,
            "every 30 minutes": 48,
        },
    ),
):
    # Generate base value range based on metric type
    base_ranges = {
        "temperature": (15, 35),
        "humidity": (30, 90),
        "pressure": (980, 1030),
        "wind_speed": (0, 25),
        "rainfall": (0, 10),
    }

    base_min, base_max = base_ranges.get(metric.lower(), (0, 100))

    # Generate time series data
    data_points = []
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)

    total_points = days * points_per_day
    time_interval = timedelta(days=days) / total_points

    # Create a realistic trend with some randomness
    base_value = random.uniform(base_min, base_max)

    for i in range(total_points):
        current_time = start_time + (time_interval * i)

        # Add some realistic patterns
        daily_cycle = 5 * math.sin(2 * math.pi * (i % points_per_day) / points_per_day)
        weekly_trend = 2 * math.sin(2 * math.pi * i / (points_per_day * 7))
        random_noise = random.uniform(-3, 3)

        value = base_value + daily_cycle + weekly_trend + random_noise

        # Keep within reasonable bounds
        value = max(base_min - 10, min(base_max + 10, value))

        data_points.append(
            DataPoint(timestamp=current_time.isoformat(), value=round(value, 2))
        )

    return TimeSeriesResponse(
        city=city.title(),
        metric=metric.lower(),
        data=data_points,
        total_points=len(data_points),
    )


@app.get("/metrics", tags=["utilities"], operation_id="available_metrics")
def get_available_metrics():
    return {
        "metrics": ["temperature", "humidity", "pressure", "wind_speed", "rainfall"]
    }


# Import math after the endpoints are defined

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
