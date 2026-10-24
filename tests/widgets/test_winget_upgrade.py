from unittest.mock import patch

from core.widgets.services.update_check import winget


def _launched_command(package_ids: list[str]) -> str:
    with patch.object(winget.subprocess, "Popen") as popen:
        winget.upgrade_packages(package_ids)
    return popen.call_args.args[0]


def test_git_upgrade_is_guarded_by_in_use_check():
    command = _launched_command(["Git.Git"])
    assert "if ($(Get-Process" in command
    assert "Skipping Git.Git" in command
    assert command.index("Skipping Git.Git") < command.index("gsudo winget upgrade --id 'Git.Git'")


def test_other_packages_are_not_guarded():
    command = _launched_command(["Microsoft.PowerToys"])
    assert "Get-Process" not in command
    assert "gsudo winget upgrade --id 'Microsoft.PowerToys'" in command
