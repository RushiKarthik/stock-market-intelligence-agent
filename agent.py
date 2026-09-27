import json
from groq import Groq
from dotenv import load_dotenv

from agent_tools import TOOLS

load_dotenv()

print("🔥 agent.py started")


# --------------------------------------------------
# Groq client
# --------------------------------------------------

client = Groq()


# --------------------------------------------------
# Tool definitions
# These tell the AI what tools are available
# --------------------------------------------------

tool_definitions = [

    {
        "type": "function",
        "function": {
            "name": "get_market_data",
            "description": (
                "Get current Indian market indicators "
                "such as Nifty 50, Sensex, Bank Nifty "
                "and India VIX."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_global_data",
            "description": (
                "Get global market indicators such as "
                "S&P 500, Nasdaq, Nikkei, crude oil, "
                "gold and USD/INR."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_news",
            "description": (
                "Get recent Indian stock-market news."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }

]


# --------------------------------------------------
# Main Agent
# --------------------------------------------------

def run_agent(user_request):

    print("\n🚀 Starting AI agent...")

    messages = [

        {
            "role": "system",
            "content": (
                "You are an Indian stock market research assistant. "
                "Use the available tools when necessary. "
                "Do not invent market data."
            )
        },

        {
            "role": "user",
            "content": user_request
        }

    ]

    # --------------------------------------------------
    # STEP 1 — Ask AI what tools it needs
    # --------------------------------------------------

    print("📡 Sending request to Groq...")

    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=messages,

        tools=tool_definitions,

        tool_choice="auto",

        temperature=0.2

    )

    print("✅ Groq response received!")

    message = response.choices[0].message


    # --------------------------------------------------
    # STEP 2 — Check whether AI requested tools
    # --------------------------------------------------

    if message.tool_calls:

        print(
            f"\n🔧 AI requested "
            f"{len(message.tool_calls)} tool(s)"
        )

        # Add AI's tool request to conversation
        messages.append(message)


        # --------------------------------------------------
        # STEP 3 — Execute requested tools
        # --------------------------------------------------

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            print(
                f"\n🤖 AI requested tool: "
                f"{tool_name}"
            )

            tool_function = TOOLS.get(tool_name)


            if tool_function:

                print(
                    f"⚙️ Executing {tool_name}..."
                )

                try:

                    result = tool_function()

                    print(
                        f"✅ {tool_name} executed successfully!"
                    )

                    # Send result back to AI
                    messages.append({

                        "role": "tool",

                        "tool_call_id": tool_call.id,

                        "content": json.dumps(
                            result,
                            ensure_ascii=False
                        )

                    })

                except Exception as error:

                    print(
                        f"❌ Error executing "
                        f"{tool_name}: {error}"
                    )

                    messages.append({

                        "role": "tool",

                        "tool_call_id": tool_call.id,

                        "content": json.dumps({
                            "error": str(error)
                        })

                    })

            else:

                print(
                    f"❌ Tool not found: {tool_name}"
                )


        # --------------------------------------------------
        # STEP 4 — Send tool results back to AI
        # --------------------------------------------------

        print(
            "\n🧠 Sending tool results "
            "back to Groq..."
        )

        final_response = client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=messages,

            temperature=0.2

        )


        # --------------------------------------------------
        # STEP 5 — Display final AI analysis
        # --------------------------------------------------

        final_answer = (
            final_response
            .choices[0]
            .message
            .content
        )

        print("\n" + "=" * 70)

        print("🧠 AI FINAL ANALYSIS")

        print("=" * 70)

        print(final_answer)

        print("=" * 70)


    else:

        print("\n🤖 AI did not request any tools.")

        print("\nAI response:")

        print(message.content)


# --------------------------------------------------
# Run the agent
# --------------------------------------------------

if __name__ == "__main__":

    print("\n🚀 Starting Daily Market Research Agent")

    run_agent(
        "Get the latest Indian market data and "
        "recent Indian stock market news."
    )