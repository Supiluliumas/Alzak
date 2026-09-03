from alzak.data.schema import LevelDataError
from alzak.screens.error_screen import run_error_screen


def test_noninteractive_error_writes_stderr_and_returns_two(monkeypatch, capsys) -> None:
    monkeypatch.setenv("ALZAK_NONINTERACTIVE_ERROR", "1")
    result = run_error_screen(LevelDataError("broken.json", "platforms[0].h", "minimum je 32"))
    captured = capsys.readouterr()
    assert result == 2
    assert "broken.json" in captured.err
    assert "platforms[0].h" in captured.err
