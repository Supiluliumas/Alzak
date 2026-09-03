import ast
from pathlib import Path


def test_sim_package_has_no_presentation_imports() -> None:
    root = Path("src/alzak/sim")
    assert root.is_dir()
    forbidden = {"pygame.display", "pygame.mixer", "pygame.font"}
    for path in root.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)
        assert imports.isdisjoint(forbidden), f"{path}: {imports & forbidden}"
