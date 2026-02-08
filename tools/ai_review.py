import sys
from pathlib import Path

# السماح بالاستيراد من جذر المشروع
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from ai_agent.agent import DebugAgent


def main():
    if len(sys.argv) < 2:
        print("❌ Usage:")
        print("   python tools/ai_review.py <relative_path_to_code> [error_log]")
        sys.exit(1)

    target_code = sys.argv[1]
    error_log = sys.argv[2] if len(sys.argv) > 2 else None

    print("🧠 AI Debug Review Tool")
    print("=" * 60)
    print(f"📄 Target file: {target_code}")

    agent = DebugAgent(target_code_path=target_code)
    prompt = agent.run(error_log=error_log)

    print("\n" + "=" * 60)
    print("🧠 GENERATED REVIEW PROMPT")
    print("=" * 60)
    print(prompt)


if __name__ == "__main__":
    main()
