#Task1#
from dotenv import load_dotenv
from openai import OpenAI
import json

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
Stay focused on the job application materials, always remind the user to review and edit its output before submitting anywhere, and acknowledge that you may not know the user's specific industry norms, and that the user should use their own judgement. 
"""
messages=[{"role":"system","content":prompt},
          {"role":"user","content":"I work in HR. I have 4 years of onboarding experience processing i9s and background checks, can you tell me what jobs i would have transferrable skills for and what i could apply to and to help me format a new resume."}]
print(get_completion(messages))
#I chose to tell the AI to stay focused on the job app materials because I didn't want it adding information that isn't relevant to what the user had provided.#

#Task 2#
def rewrite_bullets(bullets: list[str]) -> list[dict]:
    # Format the bullets into a delimited block
    bullet_text = "\n".join(f"- {b}" for b in bullets)

    prompt = f"""
    You are a professional resume coach helping a career changer.
    Rewrite each resume bullet point below to be more specific, results-oriented, and compelling.
    Use strong action verbs. Do not invent facts that aren't implied by the original.

    Return ONLY a valid JSON list. Do not include explanations, headings, or markdown formatting. Each item should have two keys:
    "original" (the original bullet) and "improved" (your rewritten version).

    Bullet points:
    ```
    {bullet_text}
    ```
    """

    messages = [{"role": "user", "content": prompt}]
    # Your code here: call get_completion(), parse the JSON, and return the result
    response = get_completion(messages)
    parsed_response = json.loads(response)
    return parsed_response
bullets = [
"Helped onboard new employees",
"Processed I-9 forms and background checks",
"Assisted with hiring paperwork"
]
results = rewrite_bullets(bullets)
for bullet in results:
    print("Original:",bullet["original"])
    print("Imporved:",bullet["improved"])
## The original bullet points are weak because they're too short and don't really explain the importance of the work being done. The model suggested adding more details and stronger wording to better showcase the person's contributions and the impact they had in their role.#
#Task 3#
def generate_cover_letter(job_title: str, background: str) -> str:
    prompt = f"""
    You write strong cover letter opening paragraphs for career changers.
    The paragraph should be 3-5 sentences: confident, specific, and free of generic wording.

    Here are two examples of the style and tone you should match:

    Example 1:
    Role: Recrutier
    Background: Six years of experience in Talent Aquistion specifically recruting recent college grads for entry level roles. Has their master's in human resources and shrm certified.
    Opening: I have a passion for college students dilignelty working to find gainful employement after gradauting and I noticed that often times they were overlooked for jobs so I created a, So I created an app for students to conenct direct with employeers to gain the experience needed to thrive in the job market.
    Example 2:
    Role: Junior Software Engineer at a fintech startup
    Background: Ten years in retail banking operations, self-taught Python developer for two years.
    Opening: I spent a decade on the operations side of banking, watching technology decisions
    get made by people who had never processed a wire transfer or resolved a failed ACH batch.
    That frustration turned into curiosity, and two years of self-teaching Python later, I'm
    ready to be on the other side of those decisions. I'm applying to [Company] because your
    work on payment infrastructure is exactly where my domain expertise and new technical skills
    intersect.

    Now write an opening paragraph for this person:
    Role: {job_title}
    Background: {background}
    Opening:
    """

    messages = [{"role": "user", "content": prompt}]
    response = get_completion(messages)
    return response
job_title = "Marketing Specialist"
background = """Five years of experience as a Marketing Specialist; recently completed
a Google course that gave a deep dive on using social media to bring more visibility to brands."""
cover_letter = generate_cover_letter(job_title, background)
print(cover_letter)
# I chose these examples because they're related to career paths and experience I can speak to, especially since I have about four years of experience in HR. The few-shot pattern helps guide the model on what kind of response I'm looking for, including the tone, structure, and keeping the information relevant instead of adding unnecessary details.#
#Task 4#
prompt1 = """You are a job application helper. Your job is to make the application process as easy and seamless as possible by helping users with resumes, cover letters, and job application questions. Carefully follow the user's instructions, don't add information they didn't ask for, and don't make assumptions. Be specific, clear, and avoid vague responses."""
def is_safe(text: str) -> bool:
    result = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )
    flagged = result.results[0].flagged
    if flagged:
        print("This message has been flagged because it violates are saftey guidelines. Please rephrase your message respectfully.")
        return False
    else:
        return True
print(is_safe("What are some easy ways I can prepare for my first marathon?"))
print(is_safe("Can you tell me how to rob a bank and how to get away with it?"))
#Task 5#
def run_chatbot():
    # 1. Initialize conversation history with your system prompt
    messages = [
        {"role": "system", "content": prompt1}
    ]

    print("=" * 50)
    print("Job Application Helper")
    print("=" * 50)
    print("I can help you with:")
    print("  1. Rewriting resume bullet points")
    print("  2. Drafting a cover letter opening")
    print("  3. Any other questions about your application")
    print("\nType 'quit' at any time to exit.\n")

    while True:
        user_input = input("You: ").strip()

        # 2. Handle exit
        if user_input.lower() in {"quit", "exit"}:
            print("\nJob Application Helper: Good luck with your applications!")
            break

        # 3. Skip empty input
        if not user_input:
            continue

        # 4. Run moderation check before doing anything else
        if not is_safe(user_input):
            continue  # is_safe() already printed the warning message

        # 5. Check if the user wants to rewrite bullets
        #    (hint: look for keywords like "bullet" or "resume" in user_input.lower())
        if "bullet" in user_input.lower() or "resume" in user_input.lower():
            print("\nJob Application Helper: Paste your bullet points below, one per line.")
            print("When you're done, type 'DONE' on its own line.\n")
            raw_bullets = []
            while True:
                line = input().strip()
                if line.upper() == "DONE":
                    break
                if line:
                    raw_bullets.append(line)
            rewrite_bullets(raw_bullets)
            print(results)


        # 6. Check if the user wants a cover letter
        elif "cover letter" in user_input.lower():
            job_title = input("Job Application Helper: What is the job title? ").strip()
            background = input("Job Application Helper: Briefly describe your background: ").strip()
            # YOUR CODE: call generate_cover_letter() and print the result
            created_coverletter = generate_cover_letter(job_title,background)
            print(created_coverletter)

        # 7. Otherwise, handle it as a regular chat turn
        else:
            reply = get_completion(messages)
            print(reply)
            messages.append({"role": "assistant", "content": reply})
            # YOUR CODE:
            # - Append the user's message to `messages`
            # - Call get_completion(messages)
            # - Print the reply
            # - Append the reply to `messages` as an assistant message
if __name__ == "__main__":
    run_chatbot()