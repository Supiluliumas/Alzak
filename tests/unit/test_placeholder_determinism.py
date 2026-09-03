import subprocess
import sys


def test_placeholder_generator_verify_mode() -> None:
    result = subprocess.run(
        [sys.executable, "tools/generate_placeholders.py", "--verify"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "19 images, 1 music loop, 5 SFX" in result.stdout
