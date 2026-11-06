from weatherkit.records import HourlyReading
from weatherkit.summarize import DailyAggregator
import pytest
@pytest.fixture
def sample_readings():
    return[
        HourlyReading("2026-10-10T01:00", 17.1, 0.4),
        HourlyReading("2026-10-10T02:00", 14.0, 0.9),
        HourlyReading("2026-09-10T01:00", 7.0, 1.4),
        HourlyReading("2026-09-10T02:00", 19.1, 2.3), 
    ]
def test_days(sample_readings):
    aggregator = DailyAggregator(min_hours=2)
    summaries = aggregator.summarize(sample_readings)
    assert len(summaries) == 2
temps= [
    HourlyReading("2025-1-10T01:00",70,2.0),
    HourlyReading("2025-1-10T01:00",4.0,1.9),
    HourlyReading("2025-1-10T01:00",69,3.4),
    HourlyReading("2025-1-10T01:00",9.1,3.3)
]
@pytest.mark.parametrize(
    "expected_max, expected_min",
    [(70, 4.0),]
)
def test_max_min_temp(expected_max, expected_min):
    aggregator = DailyAggregator(min_hours=2)
    summaries = aggregator.summarize(temps)
    assert summaries[0].temp_max == expected_max
    assert summaries[0].temp_min == expected_min
rain_readings = [
    HourlyReading("2016-06-07", 72, 33.2),
    HourlyReading("2016-06-07", 71, 39.1),
    HourlyReading("2016-06-07", 75, 13.55)
]
def test_rain_sum():
    aggregator = DailyAggregator(min_hours=2)
    summaries = aggregator.summarize(rain_readings)
    assert summaries[0].precipitation_sum == pytest.approx(85.85)
def test_fewer_days():
    aggregator = DailyAggregator(min_hours=3)
    incomplete_days = [
        HourlyReading("2019-07-11",29,44),
        HourlyReading("2019-07-11",43,64)
    ]
    summaries = aggregator.summarize(incomplete_days)
    dropped = aggregator.incomplete_days(incomplete_days)
    assert len(summaries) == 0
    assert "2019-07-11" in dropped
def test_lowered_hours():
    aggregator = DailyAggregator(min_hours=2)
    same_days = [
            HourlyReading("2019-07-11",29,44),
            HourlyReading("2019-07-11",43,64)
        ]
    summaries = aggregator.summarize(same_days)
    assert len(summaries) == 1