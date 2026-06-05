# SPDX-License-Identifier: Apache-2.0
"""Execute the example scripts in CI so they stay working."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = REPO_ROOT / "examples" / "basic_addition.py"


def test_basic_addition_example_runs() -> None:
    result = subprocess.run(
        [sys.executable, str(EXAMPLE)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "add(2, 3)            = 5" in result.stdout
    assert "overflow correctly rejected" in result.stdout
