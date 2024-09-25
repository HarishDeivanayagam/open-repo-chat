from agent import Agent
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    folder_path = input("Enter your folder path: ")

    agent = Agent(folder_path=folder_path)

    branch = input("Enter a branch name to start: ")
    agent.switch_branch(branch)

    while True:
        query = input("Enter your query: ")

        if query == "help":
            print("\nAvailable commands:\n-- help (List all commands)\n-- exit (Exit the program)\n-- clear (Clear the agent memory)\n")

        elif query == "exit":
            break

        elif query == "clear":
            pass

        else:
            answer = agent.ask(query)
            print(answer)
