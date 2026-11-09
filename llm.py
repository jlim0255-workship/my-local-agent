import os
import sys
import json
from tools import TOOL_SCHEMAS, TOOLS
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["BASE_URL"],
    api_key=os.environ["API_KEY"],
)

def call_llm(messages):
    response = client.chat.completions.create(
        model=os.environ["MODEL"],
        messages=messages,
        tools=TOOL_SCHEMAS,
    )

    message = response.choices[0].message

    completion_details = response.usage.completion_tokens_details
    prompt_details = response.usage.prompt_tokens_details

    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "reasoning_tokens": getattr(completion_details, "reasoning_tokens", None),
        "cached_tokens": getattr(prompt_details, "cached_tokens", None),
    }

    return message, usage


if __name__ == "__main__":
    user_input = input("Enter your prompt> ")

    message, usage = call_llm([
        {"role": "system", "content": os.environ["SYSTEM_PROMPT"]},
        {"role": "user", "content": user_input},
    ])
    print("\nAgent: ", message.content, "\n")
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        result = TOOLS[tool_call.function.name](**args)
        print("Tool: ", tool_call.function.name, args)
        print(result, "\n")
        print(usage)