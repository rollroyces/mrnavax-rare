"""Top-level pytest conftest.

Runs *before* any test module is imported. We use it to apply the
``$HOME/.venv-boltz-test`` and ``$HOME/.venv-tdc-test`` sys-path
augmentations for ``boltz`` and ``tdc`` so the ``pytest.importorskip(…)``
markers in the relevant test modules resolve to "importable" and the
gated tests actually run (instead of silently skipping on this Mac). The
same hooks are no-op on any box where ``boltz``/``tdc`` are already
importable from system Python.

See :mod:`mrnavax_rare.config.boltz_discovery` and
:mod:`mrnavax_rare.config.tdc_discovery` for the environment-variable
opt-out (``MRAVANAX_RARE_NO_HOME_PATH=1``).
"""
from __future__ import annotations

from mrnavax_rare.config.boltz_discovery import ensure_boltz_on_path
from mrnavax_rare.config.tdc_discovery import ensure_tdc_on_path

# Augment sys.path with the canonical $HOME site-packages directories
# if needed. Idempotent — does nothing once the packages resolve via
# find_spec.
ensure_boltz_on_path()
ensure_tdc_on_path()
