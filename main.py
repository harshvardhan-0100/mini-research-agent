from agent import run_agent


while True:

    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:

        print("Agent shutting down.")
        break

    response = run_agent(user_input)

    print("\nAgent:", response)