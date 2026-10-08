from dataclasses import dataclass
@dataclass
class DailySummary:
    """Daily summary that will have the date,max/min temperature, precipitation, and hours observed."""
    date: str
    temp_max: float
    temp_min: float
    precipitation_sum: float
    hours_observed: int
    """Method that will get the temperature range and subtract the two to get the temp."""
    def temp_range(self)->float:
        return self.temp_max - self.temp_min
class DailyAggregator:
    def __init__(self,min_hours: int = 24):
        self.min_hours = min_hours
    def summarize(readings: list[HourlyReading]) -> list[DailySummary]:
        pass
    def incomplete_days(readings: list[HourlyReading]) -> list[str]:
        pass