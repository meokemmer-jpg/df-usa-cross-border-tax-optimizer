"""USA Cross-Border Tax Optimizer Core [CRUX-MK].

DE-USA DBA + Sec-883 + E-2-Visa Mock-Calc.
K_0-DIREKT: KEINE Real-Tax-Calc ohne PHRONESIS_TICKET.

[CRUX-MK]
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TreatyArticle(str, Enum):
    ART_7_BUSINESS_PROFITS = "art_7_business_profits"
    ART_10_DIVIDENDS = "art_10_dividends"
    ART_12_ROYALTIES = "art_12_royalties"
    SEC_883_HOTEL = "sec_883_hotel_operations"


@dataclass(frozen=True)
class TaxEstimate:
    """Mock-Estimate. NICHT-Production-Ready ohne Anwalt-Signoff."""
    treaty_article: TreatyArticle
    gross_income_eur: float
    withholding_pct: float
    estimated_tax_eur: float
    net_income_eur: float
    requires_anwalt_signoff: bool
    sandbox_mode: bool
    disclaimer: str


@dataclass(frozen=True)
class WegzugssteuerEstimate:
    """§ 6 AStG Wegzugssteuer-Mock."""
    asset_value_eur: float
    historical_cost_eur: float
    capital_gain_eur: float
    estimated_tax_eur: float
    can_defer: bool          # EU/EWR-Verschmelzung
    requires_anwalt_signoff: bool


# DE-USA-DBA-Witholding-Rates (Stand 2026, Mock-Werte)
DBA_RATES = {
    TreatyArticle.ART_7_BUSINESS_PROFITS: 0.0,    # Befreit bei feste Betriebsstaette
    TreatyArticle.ART_10_DIVIDENDS: 0.15,         # Reduziert von 30% via DBA
    TreatyArticle.ART_12_ROYALTIES: 0.0,          # Befreit via DBA
    TreatyArticle.SEC_883_HOTEL: 0.0,             # Carve-Out wenn US-Resident
}

DISCLAIMER = (
    "MOCK-CALCULATION. Sandbox-Mode. KEINE Steuerberatung. "
    "Real-Tax-Decisions erfordern Anwalt + Steuerberater + PHRONESIS_TICKET."
)


class CrossBorderTaxOptimizer:
    def __init__(self, sandbox_mode: Optional[bool] = None):
        if sandbox_mode is None:
            sandbox_mode = (
                os.environ.get("DF_USA_TAX_OPTIMIZER_REAL_ENABLED", "false").lower() != "true"
            )
        self.sandbox_mode = sandbox_mode

    def estimate_dba_withholding(
        self,
        treaty_article: TreatyArticle,
        gross_income_eur: float,
    ) -> TaxEstimate:
        """Mock-Estimate fuer DBA-Quellensteuer."""
        if gross_income_eur < 0:
            raise ValueError("gross_income_eur must be >= 0")
        rate = DBA_RATES.get(treaty_article, 0.30)  # Default fallback 30% IRS
        tax = gross_income_eur * rate
        return TaxEstimate(
            treaty_article=treaty_article,
            gross_income_eur=gross_income_eur,
            withholding_pct=rate * 100,
            estimated_tax_eur=round(tax, 2),
            net_income_eur=round(gross_income_eur - tax, 2),
            requires_anwalt_signoff=True,
            sandbox_mode=self.sandbox_mode,
            disclaimer=DISCLAIMER,
        )

    def estimate_wegzugssteuer(
        self,
        asset_value_eur: float,
        historical_cost_eur: float,
        target_country_eu_eea: bool = False,
    ) -> WegzugssteuerEstimate:
        """§ 6 AStG Mock."""
        if asset_value_eur < 0 or historical_cost_eur < 0:
            raise ValueError("asset_value + historical_cost must be >= 0")
        gain = max(0.0, asset_value_eur - historical_cost_eur)
        # Mock 26.375% (KapErtSt + Soli) auf Capital-Gain
        tax = gain * 0.26375
        return WegzugssteuerEstimate(
            asset_value_eur=asset_value_eur,
            historical_cost_eur=historical_cost_eur,
            capital_gain_eur=round(gain, 2),
            estimated_tax_eur=round(tax, 2),
            can_defer=target_country_eu_eea,  # USA = nein
            requires_anwalt_signoff=True,
        )

    def check_sec_883_eligibility(
        self,
        is_us_resident: bool,
        has_us_betriebsstaette: bool,
        hotel_operations_pct: float,
    ) -> dict:
        """Sec-883-Carve-Out Eligibility-Mock."""
        if hotel_operations_pct < 0 or hotel_operations_pct > 100:
            raise ValueError("hotel_operations_pct must be 0-100")
        eligible = (
            is_us_resident
            and has_us_betriebsstaette
            and hotel_operations_pct >= 50.0
        )
        return {
            "eligible": eligible,
            "is_us_resident": is_us_resident,
            "has_us_betriebsstaette": has_us_betriebsstaette,
            "hotel_operations_pct": hotel_operations_pct,
            "requires_anwalt_signoff": True,
            "sandbox_mode": self.sandbox_mode,
            "disclaimer": DISCLAIMER,
        }
