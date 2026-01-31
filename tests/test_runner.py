import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import runner


def test_build_flash_command_basic():
    firmware = {
        "BL": "/tmp/bl.tar.md5",
        "AP": "/tmp/ap.tar.md5",
        "CP": "/tmp/cp.tar.md5",
        "CSC": "/tmp/csc.tar.md5",
    }
    options = {
        "nand_erase": True,
        "home_validation": True,
        "reboot": True,
        "device_path": "/dev/usb1",
    }
    cmd = runner.build_flash_command(firmware, options)
    assert cmd[0] == runner.ODIN_BIN_PATH
    assert cmd[1:] == [
        "-b", firmware["BL"],
        "-a", firmware["AP"],
        "-c", firmware["CP"],
        "-s", firmware["CSC"],
        "-e",
        "-V",
        "--reboot",
        "-d", options["device_path"],
    ]


def test_build_flash_command_optional_fields():
    firmware = {"AP": "/tmp/ap.tar"}
    options = {"nand_erase": False, "home_validation": False, "reboot": False, "device_path": None}
    cmd = runner.build_flash_command(firmware, options)
    assert cmd == [runner.ODIN_BIN_PATH, "-a", firmware["AP"]]


def test_run_device_list_command_file_not_found(monkeypatch):
    def fake_run(*args, **kwargs):
        raise FileNotFoundError()

    monkeypatch.setattr(runner.subprocess, "run", fake_run)
    devices = runner.run_device_list_command()
    assert devices and devices[0].startswith(runner.ERROR_PREFIX)

