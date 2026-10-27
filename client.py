# -*- coding: utf-8 -*-
"""
GenPark Ctrip Hotel Corporate Policy Compliance Auditor Client
Automates enterprise travel policy validation, rate parity audits, and carbon ESG compliance.
Zero external dependencies -- Python 3.9+ standard library only.
"""

import math
from typing import Dict, Any, List

class GenParkCtripHotelCorporatePolicyComplianceAuditor:
    """
    携程商旅 (Ctrip Corporate Travel) Agent Core:
    Evaluates hotel room rates against enterprise city tiers, audits OTA rate parity,
    and enforces carbon budget ESG compliance.
    """

    CITY_TIER_CEILINGS_CNY = {
        "TIER_1": 800.0,   # Beijing, Shanghai, Shenzhen, Guangzhou
        "NEW_TIER_1": 600.0, # Hangzhou, Chengdu, Wuhan, Xi'an
        "TIER_2": 450.0,
        "TIER_3_BELOW": 350.0
    }

    def __init__(self, allowable_overspend_tolerance_pct: float = 0.10):
        self.tolerance = allowable_overspend_tolerance_pct

    def audit_hotel_reservation(
        self,
        employee_level: str,
        destination_city_tier: str,
        hotel_nightly_rate_cny: float,
        public_ota_consumer_rate_cny: float,
        hotel_carbon_kg_per_night: float = 24.0,
        ancillary_breakfast_included: bool = True
    ) -> Dict[str, Any]:
        """
        Audits room rate against corporate policy, detects rate parity anomalies, and checks ESG carbon limits.
        """
        base_ceiling = self.CITY_TIER_CEILINGS_CNY.get(destination_city_tier.upper(), 500.0)

        # Seniority multiplier
        level_mult = {
            "EXECUTIVE": 1.75,
            "DIRECTOR": 1.35,
            "MANAGER": 1.15,
            "ASSOCIATE": 1.00
        }.get(employee_level.upper(), 1.0)

        effective_ceiling = round(base_ceiling * level_mult, 2)
        excess_amount = round(hotel_nightly_rate_cny - effective_ceiling, 2)
        excess_pct = round((excess_amount / effective_ceiling) * 100.0, 1) if excess_amount > 0 else 0.0

        # Rate parity check: compare corporate negotiated rate vs open consumer rate
        # If corporate rate > open consumer rate, enterprise is overpaying
        parity_gap_cny = round(hotel_nightly_rate_cny - public_ota_consumer_rate_cny, 2)
        if parity_gap_cny > 20.0:
            parity_status = "NEGATIVE_RATE_PARITY_ALERT"
            parity_note = f"Negotiated corporate rate is CNY {parity_gap_cny:.2f} higher than public consumer rate."
        elif parity_gap_cny < -15.0:
            parity_status = "CORPORATE_DISCOUNT_OPTIMAL"
            parity_note = f"Enterprise saves CNY {abs(parity_gap_cny):.2f}/night compared to open public market."
        else:
            parity_status = "RATE_PARITY_BALANCED"
            parity_note = "Rate is aligned with public OTA market standards."

        # ESG Carbon evaluation (baseline benchmark: 28 kg CO2 / room night)
        carbon_benchmark = 28.0
        carbon_intensity_ratio = hotel_carbon_kg_per_night / carbon_benchmark
        if carbon_intensity_ratio <= 0.75:
            esg_tier = "GREEN_LEADER_ECO_CERTIFIED"
        elif carbon_intensity_ratio <= 1.05:
            esg_tier = "STANDARD_COMPLIANT"
        else:
            esg_tier = "HIGH_CARBON_EMISSION_WARNING"

        # Final Approval Determination
        if hotel_nightly_rate_cny <= effective_ceiling:
            approval_verdict = "AUTO_APPROVED"
            audit_reason = "Reservation strictly satisfies all corporate city-tier room ceilings."
        elif excess_pct <= (self.tolerance * 100.0):
            approval_verdict = "MANAGER_OVERRIDE_REQUIRED"
            audit_reason = f"Rate exceeds ceiling by {excess_pct}% (within {self.tolerance*100}% allowable tolerance)."
        else:
            approval_verdict = "REJECTED_OUT_OF_POLICY"
            audit_reason = f"Rate exceeds policy allowance ceiling by {excess_pct}%; booking blocked."

        potential_savings = max(0.0, excess_amount)

        return {
            "employee_level": employee_level.upper(),
            "destination_city_tier": destination_city_tier.upper(),
            "hotel_nightly_rate_cny": hotel_nightly_rate_cny,
            "corporate_policy_ceiling_cny": effective_ceiling,
            "variance_amount_cny": excess_amount,
            "variance_percentage": excess_pct,
            "approval_verdict": approval_verdict,
            "audit_reason": audit_reason,
            "rate_parity_analysis": {
                "public_ota_rate_cny": public_ota_consumer_rate_cny,
                "parity_status": parity_status,
                "parity_notes": parity_note
            },
            "carbon_esg_metrics": {
                "hotel_carbon_kg_per_night": hotel_carbon_kg_per_night,
                "esg_compliance_tier": esg_tier
            },
            "identified_excess_overspend_cny": potential_savings
        }
