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
response6= client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Give me a one-sentence fun fact about pandas (the animal, not the library)."}],
    n=3,
    temperature=1.0
)
for response in response6.choices:
    print (response.message.content)
#Q4#
response7 = client.chat.completions.create(
    model= "gpt-4o-mini",
    messages=[{"role":"user","content": "Explain how city officials determine the speed limit on streets vs highways."}],
    temperature= 0.2,
    max_tokens= 15
)
print("AI Response:",response7.choices[0].message.content)
print("Model",response7.model)
#I noticed the response got cut off because of the 15-token limit. This could be useful in a real application when you want to keep AI responses short instead of getting long answers.#
                        #System Messages and Personas#
#Q1#
ai_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages = [
    {"role": "system", "content": "You are a patient, encouraging Python tutor. You always explain things simply and end with a word of encouragement."},
    {"role": "user", "content": "I don't understand what a list comprehension is."}
],
    temperature= 0.1
)
print("AI Response:",ai_response.choices[0].message.content)
print("Model",ai_response.model)

ai_response2 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages = [{"role": "system", "content": "You are a good Python tutor, but you use analogies and metaphors to helo the user understand deeply the information you provide them. You always explain with a short kid like explaintion to ensure the user is able to understand some of the most difficult concepts"},
    {"role": "user", "content": "I don't understand what a list comprehension is."}
],
    temperature= 0.1
)
print("AI Response:",ai_response2.choices[0].message.content)
print("Model",ai_response2.model)
# I noticed the second response was more detailed and broke down Python in a simple, kid-friendly way. It used analogies that made the concept easier to picture, which I believe would help the user understand it better.#
#Q2#
ai_response3 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "My name is Jordan and I'm learning Python."},
    {"role": "assistant", "content": "Nice to meet you, Jordan! Python is a great choice. What would you like to work on?"},
    {"role": "user", "content": "Can you remind me what my name is?"}
],
    temperature= 0.1
)
print("AI Response:",ai_response3.choices[0].message.content)
print("Model",ai_response3.model)
#The model knows Jordan's name because it was included in an earlier user message in the messages list. Even though the API is stateless, it can still see Jordan's name because we provided the conversation history.#
                            #Prompt Engineering#
#Q1#
reviews = [
    "The onboarding process was smooth and the team was welcoming.",
    "The software crashes constantly and support never responds.",
    "Great price, but the documentation is nearly impossible to follow."
    ]
for number, review in enumerate(reviews, start=1):
    prompt = "Classifiy the sentiment of each review below as postive,negative, or mixed."
    ai_check_review = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0,
    messages=[
        {"role":"system", "content": prompt},
        {"role":"user","content":review}
        ]
    )
    print("Review Number:",number, "AI Response:", ai_check_review.choices[0].message.content)