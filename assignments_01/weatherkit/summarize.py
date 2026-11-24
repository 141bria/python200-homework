from dataclasses import dataclass
from datetime import datetime
from .records import HourlyReading
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
        """Getting the temperature range."""
        return self.temp_max - self.temp_min
class DailyAggregator:
    def __init__(self,min_hours: int = 24):
        """min hours required to consider reading."""
        self.min_hours = min_hours
    def summarize(self,readings: list[HourlyReading]) -> list[DailySummary]:
        """ a list that gathers the hourly reading."""
        summaries = []
        day_reading = {}
        for reading in readings:
            day =  reading.timestamp.split("T")[0]
            if day not in day_reading:
                day_reading[day] = []
            day_reading[day].append(reading)
        for day, daily_readings in day_reading.items():
                temp_min = min(reading.temperature_c for reading in daily_readings)
                temp_max = max(reading.temperature_c for reading in daily_readings)
                total_precipitation = sum(reading.prepcipitation_mm for reading in daily_readings)
                hours_observed = len(daily_readings)
                if hours_observed>= self.min_hours:
                    summary =  DailySummary(
                    date = day,
                    temp_max=temp_max,
                    temp_min = temp_min,
                    precipitation_sum = total_precipitation,
                    hours_observed = hours_observed
                )
                    summaries.append(summary)
        sorted_date = sorted(summaries, key=lambda summary:summary.date)
        return sorted_date
            
    def incomplete_days(self,readings: list[HourlyReading]) -> list[str]:
        """ a list that will get the hourlyreadings that were less than 24hrs."""
        not_a_full_day = {}
        less_than_a_day = []
        for reading in readings:
            day =  reading.timestamp.split("T")[0]
            if day not in not_a_full_day:
                not_a_full_day[day] = []
            not_a_full_day[day].append(reading)
        for day, daily_readings in not_a_full_day.items():
            day_observed = len(daily_readings)
            if day_observed< self.min_hours:
                less_than_a_day.append(day)
        return less_than_a_day

## Intentional Breaking Reflection: test_rain_sum caught the intentional precipitation_sum change.##
                            ## Task 7: Reflections ##
## 1. I don't believe rejecting the whole file is always the best choice becasue one missing temp doesn't mean all the weather data is useless. I would probably want a strict rejection if I needed complete & accurate data for every hour or so. I think I would be okay with the gap if one temp was missing but the rest of the data was still useful. To allow that, I would change the temp field to accept a number or None.##
## 2. Since the min_hours is 24hrs, if the pipeline ran at noon, the current day only had about 12hrs of data & would be treated as incomplete then would be dropped. incompleted_days() helps by showing us which days were dropped,so the missing data does not disappear without some kind of explaintion.##
## 3. Writing weatherkit as a package vs a file makes the code easier to organize and reuse it later. In week 10, the pipeline can import only the pieces it needs, like the schema,records, or aggregator instead of using one big file.##