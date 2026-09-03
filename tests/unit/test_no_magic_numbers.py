import ast
from pathlib import Path


MODULES = (
    Path("src/alzak/sim/laser.py"),
    Path("src/alzak/sim/player.py"),
    Path("src/alzak/sim/enemy.py"),
    Path("src/alzak/render/world.py"),
    Path("src/alzak/render/hud.py"),
)
STRUCTURAL_NUMBERS = {-1, 0, 1, 2}


def test_gameplay_modules_keep_tuning_values_in_config() -> None:
    violations: list[str] = []
    for path in MODULES:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Constant) or isinstance(node.value, bool):
                continue
            if isinstance(node.value, (int, float)) and node.value not in STRUCTURAL_NUMBERS:
                violations.append(f"{path}:{node.lineno}: {node.value}")
    assert violations == [], "Move gameplay tuning values to alzak.config:\n" + "\n".join(violations)
