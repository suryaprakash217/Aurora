from __future__ import annotations

from aurora.core.application import AuroraApplication
from aurora.core.lifecycle import LifecycleState


def test_lifecycle_transitions():
    app = AuroraApplication(config={})
    assert app.state == LifecycleState.CREATED

    app.initialize()
    assert app.state == LifecycleState.RUNNING

    app.stop()
    assert app.state == LifecycleState.STOPPED
