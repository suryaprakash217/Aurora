from aurora.engine import AuroraEngine
from aurora.modules.status import StatusModule


class CountingModule:
    name = "counting"

    def __init__(self) -> None:
        self.initialize_calls = 0

    def initialize(self, context) -> None:
        self.initialize_calls += 1
        self.context = context

    def run(self, context) -> dict[str, object]:
        return {"module": self.name, "initialize_calls": self.initialize_calls, "timestamp": context.get("timestamp", "unknown")}


def test_engine_initializes_and_runs_modules():
    engine = AuroraEngine({"timestamp": "now"})
    engine.register_module(StatusModule())

    result = engine.run()

    assert result[0]["module"] == "status"
    assert result[0]["status"] == "ready"
    assert result[0]["timestamp"] == "now"


def test_engine_initializes_modules_once_per_instance():
    engine = AuroraEngine({"timestamp": "now"})
    module = CountingModule()
    engine.register_module(module)

    first = engine.run()
    second = engine.run()

    assert first[0]["initialize_calls"] == 1
    assert second[0]["initialize_calls"] == 1
