import argparse
from archpilot.detector import analyze_system
from archpilot.render import render_system
import json

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="archpilot",
        description="Hardware-aware Arch Linux environment planner",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor")
    analyze_parser = subparsers.add_parser("analyze")

    analyze_parser.add_argument(
        "--json",
        action="store_true",
    )

    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "doctor":
        print("ArchPilot doctor")
        print("Everything looks good.")

    elif args.command == "analyze":
        system = analyze_system()
        
        if args.json:
            print(json.dumps(system.to_dict(), indent=2))
        else:
            print(render_system(system))

if __name__ == "__main__":
    main()