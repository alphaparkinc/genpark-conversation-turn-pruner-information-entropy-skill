"""
Demonstration of genpark-conversation-turn-pruner-information-entropy-skill
"""

from client import TurnInformationEntropyPrunerClient

def main():
    pruner = TurnInformationEntropyPrunerClient(min_entropy_threshold=2.2)

    history = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi! How can I help you today?"},
        {"role": "user", "content": "Deploy database migration 042 to staging Postgres cluster with SSL."},
        {"role": "assistant", "content": "Executing migration script against postgres://staging-db:5432."},
        {"role": "user", "content": "Thanks!"},
        {"role": "assistant", "content": "You are welcome!"}
    ]

    report = pruner.prune_conversation(history)
    print("=== CONVERSATION TURN ENTROPY PRUNING ===")
    print(f"Retained: {report['retained_turn_count']}/{report['initial_turn_count']} turns")
    print(f"Dropped Noise Turns: {report['dropped_turn_count']}")
    print("\nRetained Context:")
    for t in report["retained_turns"]:
        print(f"[{t['role']} | entropy {t['entropy']}]: {t['content']}")

if __name__ == "__main__":
    main()
