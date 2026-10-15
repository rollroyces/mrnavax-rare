"""Best-effort discovery for ``tdc`` from ``$HOME/.venv-tdc-test``.

Only adds the venv to ``sys.path`` when:

1. ``tdc`` is not already importable, and
2. ``$HOME/.venv-tdc-test`` exists, and
3. The env opt-out ``MRAVANAX_RARE_NO_HOME_PATH`` is *not* set.

Idempotent: re-running the function is a no-op once ``tdc`` resolves
via ``importlib.util.find_spec``.
"""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path


def ensure_tdc_on_path() -> None:
    if os.environ.get("MRAVANAX_RARE_NO_HOME_PATH") == "1":
        return
    if importlib.util.find_spec("tdc") is not None:
        return
    home_venv = Path.home() / ".venv-tdc-test"
    if not home_venv.is_dir():
        return
    site_packages_candidates = [
        home_venv / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages",
        home_venv / "lib" / "site-packages",
    ]
    for site in site_packages_candidates:
        if site.is_dir() and str(site) not in sys.path:
            sys.path.insert(0, str(site))
            break


__all__ = ["ensure_tdc_on_path"]