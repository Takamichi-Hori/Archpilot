from archpilot.models import InstallPlan, Recommendation


def create_install_plan (recommendation: Recommendation,) -> InstallPlan:

    return InstallPlan(
        recommendation=recommendation,
        destructive_actions_allowed=False,
    )