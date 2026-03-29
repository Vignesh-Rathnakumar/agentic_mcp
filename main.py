from app.agent import create_agent

def main():
    print("🔥 Agentic MCP AI (Type 'exit' to quit)")
    
    agent = create_agent()

    while True:
        try:
            query = input(">> ").strip()

            if not query:
                continue

            if query.lower() in ["exit", "quit"]:
                print("👋 Exiting...")
                break

            result = agent.run(query)

            print("\n🤖 Result:")
            print(result)
            print("-" * 40)

        except KeyboardInterrupt:
            print("\n👋 Interrupted. Exiting...")
            break

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()