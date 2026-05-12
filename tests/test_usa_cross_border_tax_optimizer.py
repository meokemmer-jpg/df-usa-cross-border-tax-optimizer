"""Tests fuer DF-USA-Cross-Border-Tax-Optimizer [CRUX-MK]. 10 Tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.usa_cross_border_tax_optimizer_main import (
    CrossBorderTaxOptimizer,
    TreatyArticle,
)
from src.audit_logger import AuditLogger
from src.adapter_orchestrator import main as orchestrator_main


# ============== Main: 6 Tests ==============

def test_dividends_withholding_15pct():
    """Test 1: DBA Art.10 Dividends → 15% Withholding."""
    o = CrossBorderTaxOptimizer(sandbox_mode=True)
    est = o.estimate_dba_withholding(TreatyArticle.ART_10_DIVIDENDS, 1000.0)
    assert est.withholding_pct == 15.0
    assert est.estimated_tax_eur == 150.0
    assert est.net_income_eur == 850.0


def test_business_profits_zero_pct_with_betriebsstaette():
    """Test 2: DBA Art.7 Business-Profits → 0% wenn fest. Betriebsstaette."""
    o = CrossBorderTaxOptimizer(sandbox_mode=True)
    est = o.estimate_dba_withholding(TreatyArticle.ART_7_BUSINESS_PROFITS, 1000.0)
    assert est.withholding_pct == 0.0
    assert est.estimated_tax_eur == 0.0


def test_royalties_zero_pct():
    """Test 3: DBA Art.12 Royalties → 0% via DBA."""
    o = CrossBorderTaxOptimizer(sandbox_mode=True)
    est = o.estimate_dba_withholding(TreatyArticle.ART_12_ROYALTIES, 5000.0)
    assert est.estimated_tax_eur == 0.0
    assert est.requires_anwalt_signoff is True


def test_negative_income_raises():
    """Test 4: Negatives Einkommen raises."""
    o = CrossBorderTaxOptimizer(sandbox_mode=True)
    with pytest.raises(ValueError):
        o.estimate_dba_withholding(TreatyArticle.ART_10_DIVIDENDS, -100.0)


def test_wegzugssteuer_computes_capital_gain():
    """Test 5: Wegzugssteuer: Capital-Gain = Asset - Historical-Cost, 26.375%."""
    o = CrossBorderTaxOptimizer(sandbox_mode=True)
    est = o.estimate_wegzugssteuer(500000.0, 200000.0, target_country_eu_eea=False)
    assert est.capital_gain_eur == 300000.0
    # 300000 * 0.26375 = 79125.0
    assert est.estimated_tax_eur == 79125.0
    assert est.can_defer is False  # USA != EU/EEA


def test_sec_883_eligibility_requires_all_three():
    """Test 6: Sec-883 eligibility braucht US-Resident + Betriebsstaette + >=50% Hotel."""
    o = CrossBorderTaxOptimizer(sandbox_mode=True)
    eligible = o.check_sec_883_eligibility(True, True, 80.0)
    not_eligible_no_resident = o.check_sec_883_eligibility(False, True, 80.0)
    not_eligible_low_pct = o.check_sec_883_eligibility(True, True, 30.0)
    assert eligible["eligible"] is True
    assert not_eligible_no_resident["eligible"] is False
    assert not_eligible_low_pct["eligible"] is False


# ============== Orchestrator: 4 Tests ==============

def test_audit_chain_valid(tmp_path):
    """Test 7: Audit-Chain valid."""
    a = AuditLogger(audit_path=tmp_path / "a.jsonl", secret="s")
    a.append({"e": "1"})
    a.append({"e": "2"})
    assert a.verify_chain()["valid"] is True


def test_sandbox_default_via_env(monkeypatch):
    """Test 8: ENV-Var default → sandbox."""
    monkeypatch.delenv("DF_USA_TAX_OPTIMIZER_REAL_ENABLED", raising=False)
    o = CrossBorderTaxOptimizer()
    assert o.sandbox_mode is True


def test_sec_883_invalid_pct_raises():
    """Test 9: hotel_operations_pct > 100 raises."""
    o = CrossBorderTaxOptimizer(sandbox_mode=True)
    with pytest.raises(ValueError):
        o.check_sec_883_eligibility(True, True, 150.0)


def test_orchestrator_main_exits_zero(monkeypatch, tmp_path):
    """Test 10: orchestrator_main() exit-code 0."""
    monkeypatch.setenv("HOME", str(tmp_path))
    rc = orchestrator_main([])
    assert rc == 0
