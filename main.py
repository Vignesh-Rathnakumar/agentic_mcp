#!/usr/bin/env python3
"""
Main entry point for the Agentic MCP project.

Usage:
    python main.py
"""

from app.agent import create_agent


def main():
    """Run interactive agent loop"""
    print("Initializing agent...")
    agent = create_agent()
    print("Agent ready! Type 'exit' or 'quit' to exit.\n")

    while True:
        try:
            query = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if not query:
            continue

        try:
            result = agent.run(query)
            print(f"\n{result}\n")
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
