#Task1#
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def get_completion(messages, model="gpt-4o-mini", temperature=0.7):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=400
    )
    return response.choices[0].message.content

prompt = f"""
You will be given text inside triple backticks.
Stay focused on the job application materials, always remind the user to review and edit its output before submittin anywhere, and acknowledge that you may not know the user's specific industry norms, and that the user should use their own judgement. 
"""
messages=[{"role":"system","content":prompt},
          {"role":"user","content":"I work in HR. I have 4 years of onboarding experience processing i9s and background checks, can you tell me what jobs i would have transferrable skills for and what i could apply to and to help me format a new resume."}]
print(get_completion(messages))