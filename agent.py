import json
import os
from llm import call_llm
from tools import TOOLS
from ui import ui
from skills import skills_prompt

ui.banner()

messages = [{
    "role": "system", 
    "content": os.environ["SYSTEM_PROMPT"]
    .replace("{os.getcwd()}", os.getcwd())
    .replace("{skills_prompt()}", skills_prompt())
    }]

while True:
    user_input = ui.ask()
    if not user_input:
        break


    messages.append({"role": "user", "content": user_input})

    while True:
        with ui.working():
            message, usage = call_llm(messages)

        messages.append(message.model_dump(exclude_none=True))
    
    
        ui.usage(usage)

        if message.content:
            ui.agent(message.content)

        if not message.tool_calls:
            break

        for tool_call in message.tool_calls:
            # args = json.loads(tool_call.function.arguments)
            # result = TOOLS[tool_call.function.name](**args)            
            # ui.tool(tool_call.function.name, args, result)

            name = tool_call.function.name
            args = {}
            try:
                args = json.loads(tool_call.function.arguments)
                if name not in TOOLS:
                    raise ValueError(f"'{name}' is not a tool. Your tools are: {', '.join(TOOLS)}")
                result = TOOLS[name](**args)
            except Exception as e:
                result = f"Error: {type(e).__name__}: {e}"
            ui.tool(name, args, result)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

        # print(usage)
ui.summary()