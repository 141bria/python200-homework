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
print(load_happiness_data())
    #tool 2#
@tool
def summarize_column(column: str) -> dict:
    """Summarize one column of the loaded dataset.

    Args:
        column: The name of the column to summarize.

    Returns:
        A dictionary of descriptive statistics or an error.
    """

    if df is None or df.empty:
        return {"error":"DataFrame is not loaded or the file is empty"}
    if column not in df.columns:
        return {"error":"Column doesn't exist in DataFrame"}
    return df[column].describe().to_dict()
print(summarize_column("happiness_score"))
    #tool 3#
from scipy.stats import pearsonr
from pandas.api.types import is_numeric_dtype
@tool
def compute_correlation(col1: str, col2: str) -> dict:
    """Compute the Pearson correlation between two columns in the loaded DataFrame.

    Args:
        col1: The name of the first column.
        col2: The name of the second column.

    Returns:
        The correlation coefficient and p-value.
    """
    if df is None or df.empty:
        return {"error": "DataFrame is not loaded or the file is empty"}
    if col1 not in df.columns or col2 not in df.columns:
        return {"error": "Column not found in CSV"}
    if not is_numeric_dtype(df[col1]) or  not is_numeric_dtype(df[col2]):
        return{"error":"Column is not numeric"}

    data = df[[col1, col2]].dropna()
    pearson_r, p_value = pearsonr(data[col1], data[col2])
    return {
        "col1": col1,
        "col2": col2,
        "pearson_r": round(pearson_r, 4),
        "p_value": round(p_value, 4),
    }
print(compute_correlation ("gdp_per_capita","happiness_score"))
#tool 4#
@tool
def get_top_n_countries(column: str, year: int, n: int = 5) -> dict:
    """Return the top N countries ranked by a given column for a specific year.
    Args:
    column: The column to rank countries by.,
    year: The year to look at.,
    n: How many countries to return.
    Returns:
    Describes the list of country dictionaries or an error message.
    """
    if df is None or df.empty:
        return {"error": "DataFrame is not loaded or the file is empty"}
    if column not in df.columns:
        return {"error": "Column not found in CSV"}
    if year not in df["year"].values:
        return{"error":"this year is not in the dataframe."}
    sorted_column = df[df["year"]==year].sort_values(by=column,ascending=False)
    top_countries= sorted_column.head(n)
    selected_country = top_countries[["country",column]]
    dictionary_of_countries = selected_country.to_dict(orient="records")
    return dictionary_of_countries
print(get_top_n_countries("happiness_score",2024,3))
#Task 2#
from smolagents import CodeAgent, OpenAIServerModel
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent / "assignments_05" / ".env")
api_key = os.getenv("OPENAI_API_KEY")

model = OpenAIServerModel(api_key=api_key, model_id="gpt-4o-mini")

SYSTEM_PROMPT = """
You are a data analyst assistant for the World Happiness dataset.
Use the available tools for loading data, summarizing columns, computing correlations,
and ranking countries. Write Python code directly only when the tools are not sufficient
(for example, when creating custom plots or computing something the tools don't cover).
Be concise and student-friendly in your responses.
"""

agent = CodeAgent(
    tools=[load_happiness_data, summarize_column, compute_correlation, get_top_n_countries],
    model=model,
    instructions=SYSTEM_PROMPT,
    additional_authorized_imports=["pandas", "matplotlib.pyplot", "scipy.stats"],
    max_steps=8,
)

#Task 3#
queries = [
    "Load the happiness data and tell me its shape and column names.",
    "Summarize the happiness_score column.",
    "What is the correlation between gdp_per_capita and happiness_score? Is it statistically significant?",
    "Show me the top 5 happiest countries in 2020.",
    "Plot happiness_score over the years as a line chart, with one line per region. Save the plot to outputs/happiness_by_region.png.",
]

for query in queries:
    print(f"\n--- Query: {query} ---")
    response = agent.run(query, reset=False)
    print(response)

#Task 4#
# My query 1
my_query_1 = "What are the top 3 countires that experienced freedom to make life choices in 2019"   # replace with your question
response_1 = agent.run(my_query_1, reset=False)
print(response_1)
# Comment: Did this trigger tool use, code generation, or both?
# For Query 1 it used a tool, specifically the get_top_n_countries()#
# My query 2
my_query_2 = "What is the average healthy life expectany in the United States in 2019 and 2020? Which year had a higher average?pytho "   # replace with your question
response_2 = agent.run(my_query_2, reset=False)
print(response_2)
# Comment: Did this trigger tool use, code generation, or both?
# For Query 2 it used both.  It used an exsisiting tool to find the data, then wrote its own code and compared the results.#

#Task 5: Refelction #
# 1. The agent gave a Pearson r of 0.6313 and a p-value of 0.0. It also said the results were statistically significant (True). However, it didn't explain the strength or direction of the relationship.

# 2. I was surprised when the agent used an existing tool to find the data for my own question, then wrote its own code to compare the results. I wasn't expecting it to do both.

# 3. I think a tool that looks up data for a specific country and year would be useful. It could help answer questions about a country's healthy life expectancy without ranking other countries.

#AI disclosure#
#I used ChatGPT as a learning resource throughout this assignment to help with debugging, understanding Python syntax, and working through errors in my code. During the project, I used it to help fix issues with my functions, understand error messages, and troubleshoot my API key setup when the agent wasn't connecting properly.I also used ChatGPT to better understand how the CodeAgent works, especially the difference between using an existing tool and generating its own code. It helped me review my results and work through my questions.#