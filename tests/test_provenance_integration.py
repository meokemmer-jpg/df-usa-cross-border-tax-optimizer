"""W50-A Batch-2: K12+K13+K16 Tests fuer df-usa-tax provenance_integration [CRUX-MK]."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.provenance_integration import (
    TaxProvenanceRecorder,
    W48_FOUNDATION,
    DEFAULT_K16_LOCK_PATH,
)


@pytest.mark.skipif(not W48_FOUNDATION, reason="W48 foundation modules not installed")
def test_k12_tax_estimate_envelope(tmp_path: Path):
    """K12: tax-estimate gets signed envelope (K_0-HARD)."""
    rec = TaxProvenanceRecorder(audit_dir=tmp_path)
    result = rec.record_tax_estimate(
        operation_id="tax-est-001",
        estimate_payload={
            "treaty_article": "art_10_dividends",
            "gross_income_eur": 100000,
            "estimated_tax_eur": 15000,
            "sandbox_mode": True,
        },
        tenant_id="usa-tax-global",
    )
    assert result is not None
    assert "envelope_path" in result
    env_file = Path(result["envelope_path"])
    assert env_file.exists()
    with open(env_file) as f:
        env = json.load(f)
    assert env["operation_type"] == "df-usa-tax-estimate"
    assert env["issuer"] == "df-usa-cross-border-tax-optimizer"
    assert "signature" in env


@pytest.mark.skipif(not W48_FOUNDATION, reason="W48 foundation modules not installed")
def test_k13_anchor_per_estimate(tmp_path: Path):
    """K13: rfc3161-anchors.jsonl appended per estimate (K_0-HARD pflicht)."""
    rec = TaxProvenanceRecorder(audit_dir=tmp_path)
    rec.record_tax_estimate("tax-anchor-1", {"art": "10", "tax": 100})
    anchor_file = tmp_path / "anchors" / "rfc3161-anchors.jsonl"
    assert anchor_file.exists()
    lines = anchor_file.read_text().strip().split("\n")
    assert len(lines) >= 1


def test_k16_default_lock_path():
    assert "df-usa-tax-optimizer" in str(DEFAULT_K16_LOCK_PATH)
    assert DEFAULT_K16_LOCK_PATH.name.endswith(".lockfile")
