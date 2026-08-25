from archpilot.models import Recommendation
from archpilot.planner import create_install_plan

def test_destrucvtive_operations_are_disabled():
    recommendation = Recommendation(
        use_case="gaming",
        desktop_environment="KDE Plasma",
    )

    plan = create_install_plan(
        recommendation,
    )

    assert plan.destructive_actions_allowed is False

    assert "format filesystems" in plan.blocked_operations

    assert "delete partitions" in plan.blocked_operations