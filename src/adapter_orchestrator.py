"""Adapter-Orchestrator (LaunchAgent-Entry) [CRUX-MK]."""

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class OrchestratorResult:
    estimates_computed: int
    sandbox_mode: bool
    audit_hash: str


def main(argv=None) -> int:
    logging.basicConfig(level=logging.INFO)
    if Path("/tmp/df-usa-cross-border-tax-optimizer.stop").exists():
        return 0

    from .usa_cross_border_tax_optimizer_main import (
        CrossBorderTaxOptimizer, TreatyArticle,
    )
    from .audit_logger import AuditLogger

    o = CrossBorderTaxOptimizer()
    audit = AuditLogger()

    # Sandbox-Demo
    est_dividends = o.estimate_dba_withholding(TreatyArticle.ART_10_DIVIDENDS, 100000.0)
    est_wegzug = o.estimate_wegzugssteuer(500000.0, 200000.0, target_country_eu_eea=False)
    sec883 = o.check_sec_883_eligibility(
        is_us_resident=True, has_us_betriebsstaette=True, hotel_operations_pct=100.0
    )

    audit_hash = audit.append({
        "type": "cross_border_tax_run",
        "dividends_tax_eur": est_dividends.estimated_tax_eur,
        "wegzug_tax_eur": est_wegzug.estimated_tax_eur,
        "sec_883_eligible": sec883["eligible"],
        "sandbox_mode": o.sandbox_mode,
    })

    result = OrchestratorResult(
        estimates_computed=3,
        sandbox_mode=o.sandbox_mode,
        audit_hash=audit_hash,
    )
    logger.info(f"USA-Cross-Border-Tax-Optimizer: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
