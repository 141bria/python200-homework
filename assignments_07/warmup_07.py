#Lesson 02: Tool Definitions and the ReAct Loop#
#Q1#
def celsius_to_fahrenheit(celsius: float) -> str:
    """Convert a Celsius temperature to Fahrenheit and return it as a formatted string."""
    fahrenheit = (celsius * 9 / 5) + 32
    return f"{celsius}°C is {fahrenheit}°F"
tools = [
    {
        "type":"function",
        "function":{
            "name":"celsius_to_fahrenheit",
            "description":"Converts Celsius temperature to Fahrenheit and retrun it as a formatted string.",
            "parameters":{
                "type": "object",
                "properties":{
                    "celsius":{"type":"number"},
                    "required":["celsius"]
                }
            }
        }
    }
]
print(celsius_to_fahrenheit(0))
print(celsius_to_fahrenheit(-40))
print(celsius_to_fahrenheit(100))
#Q2:Time Tool Only#
from dotenv import load_dotenv
from openai import OpenAI
import os
from datetime import datetime

def get_current_time() -> str:
    '''Return the current local time as a formatted string.'''
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

get_current_time()

if load_dotenv("../assignments_06/.env"):
    print('Successfully loaded environment variables from .env')
else:
    print('Warning: could not load environment variables from .env')

client = OpenAI()
print('OpenAI client created.')
import json
#1. I predict that the agent wont trigger a tool call because it only has access to get_current_time,since the celsius function was not listed as a tool in this function.
# 2. I predict it will use its own knowledge and may need only 1 API call.#
tools = [
    {
        'type': 'function',
        'function': {
            'name': 'get_current_time',
            'description': 'Returns the current local time as a string.',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': [],
            },
        },
    }
]
print('Tools list defined with one tool: get_current_time')
def run_agent(user_prompt: str) -> str:
    '''Run a minimal ReAct-style agent for a single user prompt.'''

    SYSTEM_PROMPT = '''You are a simple assistant that can tell the current time.
                     Use the tool get_current_time whenever a user asks about the time.'''
    
    # Step 1: start the conversation with system and user messages
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': user_prompt},
    ]

    # Step 2: first API call - the model decides whether to call a tool
    first_response = client.chat.completions.create(
        model='gpt-4.1-mini',
        messages=messages,
        tools=tools,
        tool_choice='auto',  # model chooses whether to use a tool
    )

    print("First response received from model...")
    print(first_response)
    first_message = first_response.choices[0].message

    # Record what the model said so far
    messages.append(
        {
            'role': 'assistant',
            'content': first_message.content,
            'tool_calls': first_message.tool_calls,
        }
    )

    # Step 3: check if the model requested any tools
    if first_message.tool_calls:
        print("Agentic mode engaged...")
        for tool_call in first_message.tool_calls:
            function_name = tool_call.function.name
            # In this example we only have one tool: get_current_time
            if function_name == 'get_current_time':
                tool_result = get_current_time()
            else:
                tool_result = f'Error: unknown tool {function_name}.'

            # Print for debugging so we can see what happened
            print('Tool called:', function_name)
            print('Tool result:', tool_result)

            # Step 3b: append the tool output so the model can see it
            messages.append(
                {
                    'role': 'tool',
                    'tool_call_id': tool_call.id,
                    'name': function_name,
                    'content': tool_result,
                }
            )

        # Step 4: second API call - model sees the tool result and gives final answer
        second_response = client.chat.completions.create(
            model='gpt-4.1-mini',
            messages=messages,
        )
        print("Second response received from model...")
        print(second_response)

        final_message = second_response.choices[0].message
        return final_message.content or ''
    else:
        print("No tools needed....")

    # If there were no tool calls, the first response was already the final answer
    return first_message.content or ''
print(run_agent("Convert 100 degrees Celsius to Fahrenheit"))
#Surprisinlgy my predicition was right because the agent didn't use a tool and it had only made one API call. I was geniuley surprised because it still ansered the question but it used its own knowledge to get the answer. #
#Q3: Time & Celsisus Tools#
tools_q3 = [
    {
        "type":"function",
        "function":{
            "name":"celsius_to_fahrenheit",
            "description":"Converts Celsius temperature to Fahrenheit and retrun it as a formatted string.",
            "parameters":{
                "type": "object",
                "properties":{
                    "celsius":{"type":"number"}
                },
                    "required":["celsius"]
                }
            },

                'type': 'function',
                'function': {
                    'name': 'get_current_time',
                    'description': 'Returns the current local time as a string.',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                        'required': [],
                        }
                    },
                },
            
]
def run_agent1(user_prompt: str) -> str:
    '''Run a minimal ReAct-style agent for a single user prompt.'''

    SYSTEM_PROMPT = '''You are a simple assistant that can tell the current time.
                     Use the tool get_current_time whenever a user asks about the time.'''
    
    # Step 1: start the conversation with system and user messages
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': user_prompt},
    ]

    # Step 2: first API call - the model decides whether to call a tool
    first_response = client.chat.completions.create(
        model='gpt-4.1-mini',
        messages=messages,
        tools=tools_q3,
        tool_choice='auto',  # model chooses whether to use a tool
    )

    print("First response received from model...")
    print(first_response)
    first_message = first_response.choices[0].message

    # Record what the model said so far
    messages.append(
        {
            'role': 'assistant',
            'content': first_message.content,
            'tool_calls': first_message.tool_calls,
        }
    )

    # Step 3: check if the model requested any tools
    if first_message.tool_calls:
        print("Agentic mode engaged...")
        for tool_call in first_message.tool_calls:
            function_name = tool_call.function.name
            # In this example we only have one tool: get_current_time
            if function_name == 'get_current_time':
                tool_result = get_current_time()
            else:
                tool_result = f'Error: unknown tool {function_name}.'

            # Print for debugging so we can see what happened
            print('Tool called:', function_name)
            print('Tool result:', tool_result)

            # Step 3b: append the tool output so the model can see it
            messages.append(
                {
                    'role': 'tool',
                    'tool_call_id': tool_call.id,
                    'name': function_name,
                    'content': tool_result,
                }
            )

        # Step 4: second API call - model sees the tool result and gives final answer
        second_response = client.chat.completions.create(
            model='gpt-4.1-mini',
            messages=messages,
        )
        print("Second response received from model...")
        print(second_response)

        final_message = second_response.choices[0].message
        return final_message.content or ''
    else:
        print("No tools needed....")

    # If there were no tool calls, the first response was already the final answer
    return first_message.content or ''
response_a = run_agent1("What is 37 degrees Celsius in Fahrenheit?")
print("Response A:", response_a)
#A tool was not called even though it was available to use, it knew how to convert it and reasoned on its own#

response_b = run_agent1("What is the boiling point of water in plain English?")
print("Response B:", response_b)
#A tool was not called because it already knew the boiling point.#
                            #Lesson 03: Multi-Tool Agent#
#Q4#

def compute_correlation(self, col1: str, col2: str):
    """
    Compute the Pearson correlation between two columns in the loaded DataFrame.
    Returns the correlation coefficient and p-value.
    """
    # your code here