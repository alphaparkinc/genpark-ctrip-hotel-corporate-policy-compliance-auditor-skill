# -*- coding: utf-8 -*-
"""
GenPark Ctrip Hotel Corporate Policy Compliance Auditor MCP Server
Exposes corporate travel compliance and rate parity audit tools via JSON-RPC 2.0 over STDIO.
"""

import sys
import json
from client import GenParkCtripHotelCorporatePolicyComplianceAuditor

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-ctrip-hotel-corporate-policy-compliance-auditor", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "audit_hotel_reservation",
                        "description": "Audits hotel room rates against enterprise city tiers, audits OTA rate parity, and enforces carbon budget ESG compliance.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "employee_level": {"type": "string", "description": "Seniority tier (EXECUTIVE, DIRECTOR, MANAGER, ASSOCIATE)"},
                                "destination_city_tier": {"type": "string", "description": "City classification (TIER_1, NEW_TIER_1, TIER_2, TIER_3_BELOW)"},
                                "hotel_nightly_rate_cny": {"type": "number", "description": "Proposed negotiated corporate room rate"},
                                "public_ota_consumer_rate_cny": {"type": "number", "description": "Current open consumer OTA rate for the same room"},
                                "hotel_carbon_kg_per_night": {"type": "number", "description": "Estimated carbon footprint per room night"}
                            },
                            "required": ["employee_level", "destination_city_tier", "hotel_nightly_rate_cny", "public_ota_consumer_rate_cny"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "audit_hotel_reservation":
            auditor = GenParkCtripHotelCorporatePolicyComplianceAuditor()
            res = auditor.audit_hotel_reservation(
                employee_level=args.get("employee_level", "MANAGER"),
                destination_city_tier=args.get("destination_city_tier", "TIER_1"),
                hotel_nightly_rate_cny=args.get("hotel_nightly_rate_cny", 780.0),
                public_ota_consumer_rate_cny=args.get("public_ota_consumer_rate_cny", 850.0),
                hotel_carbon_kg_per_night=args.get("hotel_carbon_kg_per_night", 22.0)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}}
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": f"Method '{method}' not supported"}}

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("MCP Server Discovery Test OK")
        auditor = GenParkCtripHotelCorporatePolicyComplianceAuditor()
        test_res = auditor.audit_hotel_reservation("MANAGER", "TIER_1", 750.0, 820.0)
        print(f"Test Verdict: {test_res['approval_verdict']}")
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
