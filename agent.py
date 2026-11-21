import ollama

from tools import search_notes, calculate


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_notes",
            "description": "Search the local knowledge base for information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The topic or keyword to search for."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate."
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


def execute_tool(tool_name, arguments):

    if tool_name == "search_notes":
        return search_notes(arguments["query"])

    elif tool_name == "calculate":
        return calculate(arguments["expression"])

    else:
        return "Error: Tool not found."


def run_agent(user_query):

    messages = [
        {
            "role": "system",
            "content": """
You are a helpful research agent.

You have access to two tools:

1. search_notes:
   Search a local knowledge base.

2. calculate:
   Perform mathematical calculations.

Use tools whenever they are useful for answering the user's question.

Do not invent calculation results.

After obtaining the necessary information, provide a concise answer.
"""
        },
        {
            "role": "user",
            "content": user_query
        }
    ]

    max_iterations = 5

    for iteration in range(max_iterations):

        print(f"\n--- Agent iteration {iteration + 1} ---")

        response = ollama.chat(
            model="qwen3.5:4b",
            messages=messages,
            tools=TOOLS
        )

        assistant_message = response.message

        # Add the LLM's response to conversation history
        messages.append(assistant_message)

        # Check whether the LLM requested a tool
        if assistant_message.tool_calls:

            for tool_call in assistant_message.tool_calls:

                tool_name = tool_call.function.name
                arguments = tool_call.function.arguments

                print(f"\nTool requested: {tool_name}")
                print(f"Arguments: {arguments}")

                # Execute the requested tool
                tool_result = execute_tool(
                    tool_name,
                    arguments
                )

                print(f"Tool result: {tool_result}")

                # Return the result to the LLM
                messages.append({
                    "role": "tool",
                    "content": str(tool_result)
                })

        else:

            # No more tools requested
            print("\nAgent finished.")

            return assistant_message.content

    return "Agent stopped because it reached the maximum iteration limit."