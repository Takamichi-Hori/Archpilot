import argparse
from archpilot.detector import analyze_system
from archpilot.render import render_system
import json
from archpilot.recommender import recommend

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

    recommend_parser = subparsers.add_parser("recommend")

    recommend_parser.add_argument(
        "--user-case",
        choices=["gaming", "developer", "everyday",],
        required=True,
    )
    
    recommend_parser.add_argument(
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

    elif args.command == "recommend":
        system = analyze_system()

        recommendation = recommend(system, args.use_case,)

        if args.json:
            print(json.dumps(recommendation.to_dict(), indent=2,))

        else:
            print(f"Use case: {recommendation.use_case}")

            print(f"Desktop: "
                  f"{recommendation.desktop_environment}")

            print("\nPackages:")

            for package in recommendation.packages:
                print(f"  - {package}")

            print("\nServices:")

            for service in recommendation.services:
                print(f"  - {service}")

            if recommendation.warnings:
                print("\nWarnings:")

                for warning in recommendation.warnings:
                    print(f"  - {warning}")



if __name__ == "__main__":
    main()