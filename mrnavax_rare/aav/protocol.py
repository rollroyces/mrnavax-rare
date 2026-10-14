"""``AAVVectorDesigner`` protocol — adapter contract for the v0.10 AAV subsystem.

Adapters implement :meth:`AAVVectorDesigner.design` and return a frozen
:class:`~mrnavax_rare.aav.data_types.AAVSpec`. Two adapters are v0.10:

- :class:`~mrnavax_rare.aav.adapters.mock_aav.MockAAVVectorDesigner` — the
  default stdlib-only backend (always available).
- :class:`~mrnavax_rare.aav.adapters.live_aav.LiveAAVVectorDesigner` — a
  :class:`NotImplementedError` stub; reserved for a future integration with
  an external viral vector design tool (e.g. ``aavlearn`` or similar).
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .data_types import AAVSpec


@runtime_checkable
class AAVVectorDesigner(Protocol):
    """Adapter protocol for AAV vector design.

    Concrete adapters (mock / live) implement :meth:`design` with the
    signature shown below. The protocol is ``runtime_checkable`` so tests
    can verify duck-typed adapters without an explicit ``isinstance``.
    """

    def design(
        self,
        target_gene: str,
        cds_wildtype: str,
        hgvs_c: str = "",
        capsid: str = "auto",
        promoter: str = "auto",
        tissue: str = "",
    ) -> AAVSpec:
        """Compose an :class:`AAVSpec` for ``target_gene`` on the chosen capsid.

        Parameters
        ----------
        target_gene:
            Gene symbol (e.g. ``"CFTR"``).
        cds_wildtype:
            Wildtype CDS DNA string (A/C/G/T). The variant-applied CDS is
            computed via :func:`mrnavax_rare.design.variant_injector.apply_hgvs_c`
            when ``hgvs_c`` is non-empty.
        hgvs_c:
            Optional HGVS-C variant (e.g. ``"c.1624G>T"``). Empty string
            means "deliver wildtype CDS".
        capsid:
            One of :data:`~mrnavax_rare.aav.data_types.AAV_CAPSIDS`, or
            ``"auto"`` to pick from ``tissue`` via
            :func:`~mrnavax_rare.aav.data_types.capsid_for_tissue`.
        promoter:
            One of :data:`~mrnavax_rare.aav.data_types.AAV_PROMOTERS`, or
            ``"auto"`` (default ``"CAG"``, or ``"hSyn"`` for CNS / SCN1A).
        tissue:
            Free-text tissue token (e.g. ``"lung"``, ``"liver"``,
            ``"cns"``). Used only when ``capsid == "auto"``.

        Returns
        -------
        AAVSpec
            The composed AAV vector design spec.
        """
        ...


__all__ = ["AAVVectorDesigner"]
