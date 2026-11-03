                                #API#
#Q1#
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is one thing that makes Python a good language for beginners?"}]
)
print("AI Response:",response.choices[0].message.content)
print("Model:", response.model)
print("Total Tokens Used:", response.usage.total_tokens)
#Q2#
temperatures = 0
response3 = client.chat.completions.create(
model="gpt-4o-mini",
messages = [{"role":"user","content":"Suggest a creative name for a data engineering consultancy."}],
temperature= temperatures
)
print("AI Response:",response3.choices[0].message.content)
print("Model",response3.model)

temperatures = 0.7
response4 = client.chat.completions.create(
model="gpt-4o-mini",
messages = [{"role":"user","content":"Suggest a creative name for a data engineering consultancy."}],
temperature= temperatures
    )
print("AI Response:",response4.choices[0].message.content)
print("Model",response4.model)

temperatures = 1.5
response5 = client.chat.completions.create(
model="gpt-4o-mini",
messages = [{"role":"user","content":"Suggest a creative name for a data engineering consultancy."}],
temperature= temperatures
)
print("AI Response:",response5.choices[0].message.content)
print("Model",response5.model)
#I noticed that the first output gave a list of business-focused names for a data engineering consultancy. The second gave names that could be misleading, like Data Mosaic, which sounds more like creating art with data than consulting. The third only gave one name, and the explanation seemed to go off the deep end. I would use temperature 0 because it's more predictable and consistent, which is what we need in this case.#
#Q3#
