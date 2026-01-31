import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from parser import parse_odin_output, format_log


def test_parse_progress():
    parsed = parse_odin_output("Sending packet 10/20...")
    assert parsed["type"] == "progress"
    assert parsed["percentage"] == 50


def test_parse_success():
    parsed = parse_odin_output("PASS")
    assert parsed["type"] == "status"
    assert parsed["level"] == "success"


def test_parse_error():
    parsed = parse_odin_output("FAIL")
    assert parsed["type"] == "status"
    assert parsed["level"] == "error"


def test_format_log_timestamp():
    text = format_log({"type": "log", "message": "hello"})
    assert re.match(r"^\[\d{2}:\d{2}:\d{2}\] > hello$", text)
