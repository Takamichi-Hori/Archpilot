import argparse
from archpilot.detector import analyze_system
from archpilot.render import render_system

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="archpilot",
        description="Hardware-aware Arch Linux environment planner",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor")
    subparsers.add_parser("analyze")

    return parser

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "doctor":
        print("ArchPilot doctor")
        print("Everything looks good.")

    elif args.command == "analyze":
        system = analyze_system()
        
        print(render_system(system))

if __name__ == "__main__":
    main()