from aurora.engine import AuroraEngine
from aurora.modules.status import StatusModule


def test_engine_initializes_and_runs_modules():
    engine = AuroraEngine({"timestamp": "now"})
    engine.register_module(StatusModule())

    result = engine.run()

    assert result[0]["module"] == "status"
    assert result[0]["status"] == "ready"
    assert result[0]["timestamp"] == "now"
