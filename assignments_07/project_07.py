#Task 1#
from smolagents import tool
from pathlib import Path
import pandas as pd
df = None

DATA_DIR = Path("happiness_project")

COLUMN_NAMES = {
    "Country": "country",
    "Regional indicator": "region",
    "Happiness score": "happiness_score",
    "Ladder score": "happiness_score",   # the 2024 file uses this name
    "GDP per capita": "gdp_per_capita",
}
@tool
def load_happiness_data() -> dict:
    """Load the World Happiness dataset into memory.
    Returns: A dictionary with shape and column
    """
    global df
    frames = []
    for path in sorted(DATA_DIR.glob("world_happiness_*.csv")):
        year_df = pd.read_csv(path, sep=";", decimal=",")
        year_df = year_df.rename(columns=COLUMN_NAMES)
        year_df["year"] = int(path.stem.split("_")[-1])   # "world_happiness_2020" -> 2020
        frames.append(year_df)

    df = pd.concat(frames, ignore_index=True)
    return{
    "shape":df.shape,
    "columns": df.columns.tolist()}