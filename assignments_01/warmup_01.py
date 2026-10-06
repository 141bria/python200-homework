##Part 1: Warmup Exercises##
## --- Classes --- ##
##Q1##

class Thermometer:
    def __init__(self,location):
        self.location = location
        self.readings = []
    def add(self,reading):
        self.readings.append(reading)
    def average(self):
        if len (self.readings) == 0:
            return None
        else:
            average = sum(self.readings)/len(self.readings)
            return average
            ## return the highest reading or none if there are none
    def hottest(self):
        if len(self.readings) == 0:
            return None
        else:
            hottest_temp= max(self.readings)
            return hottest_temp
    def __repr__(self):
        return f"Thermometer(location='{self.location}',n_readings={len(self.readings)},average={self.average()}"
        
        
Location1 = Thermometer("Memphis")
Location1.add(79)
Location1.add(85)
Location1.add(93)
Location1.add(97)
print(Location1.average())
print(Location1.hottest())
## Average needs to handle empty cases should you not get any readings which would result in 0, and can cause and error message because you can't divide by 0!

##Q2##
print(Location1)
Location2 = Thermometer("Atlanta")
Location2.add(80)
Location2.add(83)
Location2.add(84)
Location2.add(85)
print(Location2)
## When python doesn't have a __repr__ it prints a generic object description instead of useful details like in this problem average, hottest temperature,etc. Not utilizing __repr__ when debugging can make it harder because you can't easily tell what information the object has.##
##Q3##
class TemperatureAlert:
    def __init__(self,threshold=30.0):
        self.threshold = threshold
    def breaches (self,thermometer):
        temps_over_threshold = []
        for temp in thermometer.readings:
            if temp >self.threshold:
                temps_over_threshold.append(temp)
        return temps_over_threshold
Alert_1 = TemperatureAlert(33)
Alert_2 = TemperatureAlert(29.9)
print(Alert_1.breaches(Location1))
print(Alert_2.breaches(Location1))
##Threshold is stored in TemperatureAlert because we wanted that specifc temp to be our threshold instead of assigning it each time.##
## This would be useful because we can reuse it mutliple times which means there could be fewer chances of making a mistake.##

##Dataclasses, Type Hints, and Docstrings##
##Q1##
from dataclasses import dataclass, field, FrozenInstanceError
@dataclass(frozen=True)
class Station:
    """ A location that is defined by it's elevation, cordinates, and name.
    Attributes:
        station_id : a unique value that identifies the station
        name : the name of station 
        latitude : it is the north and south position 
        longitude : it is the west and east postion
        elevation : how high the location is
    
    """
    station_id : str
    name : str
    latitude : float
    longitude : float
    elevation : float
station_a = Station("Pop-267","Popular",29.456,35.998,41.051)
station_b = Station("Pop-267","Popular",29.456,35.998,41.051)
print(station_a==station_b)
## We got the result "True" becasue we asked Python to compare the two and see if they're equal to each other, in this case it is true because they have the same values. With a dataclass, Python automatically creates the instructions to compare the information inside the objects when I use ==. With the regular way of writing a handwritten class, Python doesn't automatically know to compare the information inside of it unless I add code telling it how to do so.##

##Q2##
station_c = Station("Uni-903","Union",12.222,32.321,34.567)
station_d = Station("Uni-903","Union",12.222,32.321,34.567)
station_e = Station("Wal-305","Walnut",49.890,2.21,4.657)
stations = {station_c,station_d,station_e}
try:
    station_c.name = "new_station_name"
except FrozenInstanceError as e:
    print("Cannot modify:",e)
print(len(stations))
## In this instance frozen allows us to make a set of stations and cacluate how many we have that are unique. We created 3 but set showed us only 2 have unique values.##
##Q3##
@dataclass
class StationBatch:
    region : str
    stations :list[Station] = field(default_factory=list)
    def add(self,station:Station) -> None:
        """ Adds a station to the list of stations."""
        self.stations.append(station)
    def highest(self) -> Station | None:
        ##Go thru station & find greatest elevation or return none if the batch is empty##
        if self.stations:
            return max(self.stations, key= lambda station: station.elevation)
        else:
            return None
# AI assistance: I used ChatGPT for help with the syntax for checking
# whether stations is empty and using max() with key=lambda to compare elevation.



##"ValueError: mutable default <class 'list'> for field stations is not allowed: use default_factory." Python gives us this error message and refuses the 1st version because not using defualt_factory could cause us to accidentally have list with the same information and doing this tells python to make a new list everytime. ##

##Pydantic##
##Q1##
from pydantic import BaseModel,Field, model_validator,ValidationError
class Reading(BaseModel):
   station_id : str = Field(min_length=3)
   timestamp : str
   temperature_c : float = Field(ge=-90,le=60)
   humidity : float = Field(ge=0,le=100)
   @model_validator(mode="after")
   def check_humidty(self):
       """The humidty cannot be 0."""
       if self.humidity == 0 and self.temperature_c <  -40:
           raise ValueError(
               f"humidity ({self.humidity}) cannot be 0 and ({self.temperature_c})cannot be less than -40)"
           )
       return self


reading_1 = Reading(
    station_id= "Flo-235",
    timestamp = "three o'clock",
    temperature_c = 45,
    humidity = 38
    )
print(reading_1)
##Q2##
try:
    reading_2 = Reading(station_id= "bloom-222",
    timestamp = "two o'clock",
    temperature_c = 150,
    humidity = 90)
except ValidationError as e:
    print("Temp is outside range",e)

try:
    reading_3 = Reading(station_id= "Prop-909",
    timestamp = "four o'clock",
    temperature_c = 50,
    humidity = "very humid")
except ValidationError as e:
    print("Can't be a word",e)
try:
    reading_4 = Reading(station_id= "flower-841",
    temperature_c = 150,
    humidity = 89)
except ValidationError as e:
    print("Missing value",e)
reading_5 = Reading(
    station_id= "TN-901",
    timestamp = "six o'clock",
    temperature_c = "21.5",
    humidity = 40)
print(reading_5)
type(reading_5.temperature_c)
type(reading_5.humidity)
## Pydantic was able to accept temperature_c because it saw the string could be changed to a float, but humidity required a float but there wasn't a numeric value in sight##
##Q3##
try:
    reading_6 = Reading(
    station_id= "NY",
    temperature_c = "twenty",
    humidity = 70
)
except ValidationError as e:
    for error in e.errors():
        print(error["loc"],error["msg"])
## There were a total of three errors reported. Being able to read all errors at once may make debugging easier instead of reading what went wrong one line at a time.##
##Q4##
##model_validator added to Q1. Field constraints alone aren't enough because it's limited to one field vs model validator can has a guard for mutliple fields not just one#
reading_7 = Reading(
    station_id= "MS-662",
        timestamp = "seven o'clock",
        temperature_c = 55,
        humidity = 30
)
try:
    reading_8 = Reading(
    station_id= "ATL-404",
        timestamp = "six o'clock",
        temperature_c = -41,
        humidity = 0
)
except ValidationError as e:
    print("Humidity can't be 0 & Temperature can't be less than -40:",e)
import pytest
def celsius_to_fahrenheit(celsius: float) -> float:
    """ testing conversion of Celsisus to Farehient"""
    return celsius * 9/5 + 32
def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit (0) == 32
    assert celsius_to_fahrenheit (100) == 212
    assert celsius_to_fahrenheit (37) == pytest.approx(98.6)
    ## 98.6 was a float that could've had small precision differences like 98.600003, we needed pytest.approx to indicate close to the value and not an exact value that == would've required.##
    ##Q2##
def mean(values: list[float]) -> float:
        if len(values) == 0:
            raise ValueError("Can't have an empty list!")
        else:
            return sum(values)/len(values)
def test_mean_of_empty_raises():
    with pytest.raises(ValueError,match="empty"):
        mean([])
## ValueError checks that the type of error we expected occured,match checks to see that the error message has what we expected##
##Q3##
@pytest.mark.parametrize(
        "values,output",
    [
    ([7],7),
    ([-3,-9,-4,-20],-9),
    ([-7,3,-25,21],-2),
    ([0,3,2,1,5,-1],pytest.approx(1.6666666667))
    ],
)
def test_mean_values(values,output):
    assert mean(values) == output
##6 passed in 0.08s##
##Q4##
##FAILED warmup_01.py::test_celsius_to_fahrenheit - assert 257.0 == 212##
## pytest showed the value was now 257 instead of 212, this is far more useful than assertion failed because assert looks to see if the values equal each other but pytest shows you the actual and expected values so we can see what went wrong.##