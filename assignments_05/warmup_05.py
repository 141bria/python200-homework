import json                       
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
print("\n--- Question 1 ---")
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
#Q2#
reviews = [
"The onboarding process was smooth and the team was welcoming.",
"The software crashes constantly and support never responds.",
"Great price, but the documentation is nearly impossible to follow."
]
print("\n--- Question 2 ---")
for number, review in enumerate(reviews, start=1):
    prompt = """Classifiy the sentiment of each review below as postive,negative, or mixed.",
    Example:
    Review: "Fast shipping but the item arrived damaged.",
    Sentiment: mixed
    """
    ai_check_review = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0,
    messages=[
        {"role":"system", "content": prompt},
        {"role":"user","content":review}
        ]
    )
    print("Review Number:",number, "AI Response:", ai_check_review.choices[0].message.content)
#I noticed that Q2 had a different format than Q2, but the output remained the same.#
#Q3#
reviews1 = [
    "The onboarding process was smooth and the team was welcoming.",
    "The software crashes constantly and support never responds.",
    "Great price, but the documentation is nearly impossible to follow."
    ]
print("\n--- Question 3 ---")
for number, review in enumerate(reviews1, start=1):
        prompt = """Classifiy the sentiment of each review below as postive,negative, or mixed.",
        Example:
        Review: "Fast shipping but the item arrived damaged.",
        Sentiment: mixed
        Review: "Fast shipping great item.",
        Sentiment: positive
        Review: "Slow shipping and the item arrived damaged.",
        Sentiment: negative
        """
        ai_check_review = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role":"system", "content": prompt},
            {"role":"user","content":review}
            ]
        )
        print("Review Number:",number, "AI Response:", ai_check_review.choices[0].message.content)
# Zero-shot asks the model to classify something without giving it any examples. One-shot does the same thing but gives one example to show the model how we want the response formatted. Few-shot gives multiple examples, like positive, negative, and mixed reviews, so the model can better understand the pattern. I would use zero-shot if I wanted to see what the model comes up with on its own, one-shot if I only needed one example to clarify what I wanted, and few-shot if I wanted the model to follow a specific pattern using multiple examples. It really just depends on what I'm trying to accomplish and how much guidance I want to give the model.#
#Q4#
print("\n--- Question 4 ---")
ai_problem_solver = client.chat.completions.create(
     model="gpt-4o-mini",
     messages=[{"role":"system","content": "Solve the following problem and show your reasoning step-by-step before giving a final answer"},
               {"role":"user","content":"""A data engineer earns $85,000 per year. She gets a 12% raise, then 6 months later takes a new job that pays $7,500 more per year that her post-raise salary.
                What is her final annual salary?"""}]
)
print("AI Response:", ai_problem_solver.choices[0].message.content)
#I would say asking the AI to solve the problem step by step helps us understand how it got the answer and makes it easier to catch mistakes.#
#Q5#

review = "I've been using this tool for three months. It handles large datasets well, \
but the UI is clunky and the export options are limited."
ai_analyze_review = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"system",
        "content": "Analyze the review and return the results only as valid JSON with sentiment,confidence,and reason. The sentiment will be one of the following: positivie, negative, or mixed. Confidence will be a float ranging from 0-1.Reason will be one sentence explainiing the explaintion of the decision."
        },
    {
    "role":"user",
    "content":review
    }
    ]
)
try:
    json_load= json.loads(ai_analyze_review.choices[0].message.content)
except json.JSONDecodeError:
    print("Error: response was not valid JSON")
print("Sentiment:", json_load["sentiment"],"Confidence:", json_load["confidence"],"Reason:",json_load["reason"])
#Q6#
user_text = "First boil a pot of water. Once boiling, add a handful of salt and the \
pasta. Cook for 8-10 minutes until al dente. Drain and toss with your sauce of choice."

prompt = f"""
You will be given text inside triple backticks.
If it contains step-by-step instructions, rewrite them as a numbered list.
If it does not contain instructions, respond with exactly: "No steps provided."

```{user_text}```
"""
ai_cooking_instructions = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"system",
            "content": prompt},
        {"role":"user",
        "content":user_text
        }
        ]
)
print(ai_cooking_instructions.choices[0].message.content)

user_text = "Life is about the journey not the destiantion"

prompt = f"""
You will be given text inside triple backticks.
If it contains step-by-step instructions, rewrite them as a numbered list.
If it does not contain instructions, respond with exactly: "No steps provided."

```{user_text}```
"""
ai_cooking_instructions1 = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"system",
            "content": prompt},
        {"role":"user",
        "content":user_text
        }
        ]
)
print(ai_cooking_instructions1.choices[0].message.content)
#Delimeters help AI seperate user text from instructions so it does not get confused.#
                            #Local Models with Ollama#
#Q1#
#Ollama output: "A large language model is a complex AI system that can understand and generate human-like text, learning from vast datasets to improve its knowledge and understanding. It processes and generates natural language, enabling tasks like writing, answering questions, and creating content."#
#Open AI API output: "A large language model (LLM) is an advanced artificial intelligence system designed to understand and generate human language by processing vast amounts of text data. It uses complex algorithms, often based on deep learning techniques, to predict the likelihood of word sequences, enabling it to produce coherent and contextually relevant responses."
ai_explain_model = client.chat.completions.create(
     model="gpt-4o-mini",
     messages=[{"role":"user",
                "content":"Explain what a large language model is in two sentences."}]
)
print(ai_explain_model.choices[0].message.content)
#Both models gave similar answers, but OpenAI's response was more technical and polished.An advatange of running AI locally is that I don't need internet access after downloading the model. A disadvanatge is that local models use my computer's resources which could affect the performance of my computer.#