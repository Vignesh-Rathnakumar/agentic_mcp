from app.agent import create_agent

agent = create_agent()

while True:
    query = input(">> ")

    if query.lower() in ["exit", "quit"]:
        break

    result = agent.run(query)
    print(result)