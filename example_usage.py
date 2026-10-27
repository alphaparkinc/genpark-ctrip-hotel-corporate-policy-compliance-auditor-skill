# -*- coding: utf-8 -*-
"""
Example usage of GenParkCtripHotelCorporatePolicyComplianceAuditor
Demonstrates corporate travel expense audits across varying scenarios.
"""

from client import GenParkCtripHotelCorporatePolicyComplianceAuditor

def main():
    auditor = GenParkCtripHotelCorporatePolicyComplianceAuditor(allowable_overspend_tolerance_pct=0.15)

    cases = [
        {
            "name": "Case 1: Standard Manager Booking in Shanghai (Compliant)",
            "level": "MANAGER", "tier": "TIER_1", "rate": 850.0, "public_rate": 920.0, "carbon": 21.0
        },
        {
            "name": "Case 2: Associate Overspending in Chengdu (Tolerance Override)",
            "level": "ASSOCIATE", "tier": "NEW_TIER_1", "rate": 660.0, "public_rate": 640.0, "carbon": 29.5
        },
        {
            "name": "Case 3: Unreasonable Luxury Overspend (Rejected)",
            "level": "ASSOCIATE", "tier": "TIER_2", "rate": 1150.0, "public_rate": 1200.0, "carbon": 42.0
        }
    ]

    print("================================================================")
    print("GenPark Ctrip Hotel Corporate Policy Auditor - Live Runs")
    print("================================================================\n")

    for c in cases:
        res = auditor.audit_hotel_reservation(
            employee_level=c["level"],
            destination_city_tier=c["tier"],
            hotel_nightly_rate_cny=c["rate"],
            public_ota_consumer_rate_cny=c["public_rate"],
            hotel_carbon_kg_per_night=c["carbon"]
        )
        print(f"[{c['name']}]")
        print(f"  Proposed Rate         : CNY {res['hotel_nightly_rate_cny']:,.2f} vs Policy Ceiling CNY {res['corporate_policy_ceiling_cny']:,.2f}")
        print(f"  Approval Verdict      : {res['approval_verdict']}")
        print(f"  Audit Reason          : {res['audit_reason']}")
        print(f"  Parity Status         : {res['rate_parity_analysis']['parity_status']} ({res['rate_parity_analysis']['parity_notes']})")
        print(f"  ESG Carbon Status     : {res['carbon_esg_metrics']['esg_compliance_tier']} ({res['carbon_esg_metrics']['hotel_carbon_kg_per_night']} kg/night)\n")

if __name__ == "__main__":
    main()
