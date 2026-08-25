import argparse
import json

from archpilot.commands import command_exists
from archpilot.detector import analyze_system
from archpilot.planner import create_install_plan
from archpilot.recommender import recommend
from archpilot.render import render_system


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
        "--use-case",
        choices=["gaming", "developer", "everyday",],
        required=True,
    )
    
    recommend_parser.add_argument(
        "--json",
        action="store_true",
    )


    plan_parser = subparsers.add_parser("plan")

    plan_parser.add_argument(
        "--use-case",
        choices=["gaming", "developer", "everyday",],
        required=True,
    )

    plan_parser.add_argument(
        "--json",
        action="store_true",
    )

    plan_parser.add_argument(
        "--output",
    )

    return parser

def run_doctor() -> None:
    required_commands = ["lscpu", "lspci", "lsblk", "systemd-detect-virt",]

    print("ArchPilot doctor\n")

    healthy = True

    for command in required_commands:
        available = command_exists(command)

        status = "OK" if available else "MISSING"

        print(f"{command:20} {status}")

        if not available:
            healthy = False

    print()

    if healthy:
        print("Everything looks good.")

    else:
        print("Some required commands are missing.")

    



def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "doctor":
        run_doctor()

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

    elif args.command == "plan":
        system = analyze_system()

        recommendation = recommend(
            system, args.use_case,
        )

        plan = create_install_plan(recommendation,)

        plan_json = json.dumps(plan.to_dict(), indent=2,)

        if args.output:
            with open(args.output, "w", encoding="utf-8",) as file:
                file.write(plan_json)

            print(f"Plan written to {args.output}")

        else:
            print(plan_json)



if __name__ == "__main__":
    main()