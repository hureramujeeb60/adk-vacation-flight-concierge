from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings


# Initialize FastMCP with DNS rebinding protection disabled for Docker networking
mcp = FastMCP(
    "Vacation-Flight-Concierge-Server",
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)


FLIGHTS = [
    {
        "flight_id": "VAC-DXB-101",
        "origin": "Karachi",
        "destination": "Dubai",
        "departure_date": "2026-06-12",
        "return_date": "2026-06-17",
        "airline": "SkyBridge Holidays",
        "fare_class": "Saver",
        "base_price_usd": 310,
        "layovers": 0,
        "total_duration_hours": 2.3,
        "arrival_time_local": "13:20",
        "overnight_connection": False,
        "included_checked_baggage_kg": 20,
        "tags": ["beach", "weekend", "family"],
    },
    {
        "flight_id": "VAC-DXB-204",
        "origin": "Karachi",
        "destination": "Dubai",
        "departure_date": "2026-06-12",
        "return_date": "2026-06-17",
        "airline": "Pearl Air",
        "fare_class": "Flex",
        "base_price_usd": 380,
        "layovers": 0,
        "total_duration_hours": 2.5,
        "arrival_time_local": "11:10",
        "overnight_connection": False,
        "included_checked_baggage_kg": 30,
        "tags": ["beach", "family", "refundable"],
    },
    {
        "flight_id": "VAC-DXB-330",
        "origin": "Karachi",
        "destination": "Dubai",
        "departure_date": "2026-06-12",
        "return_date": "2026-06-17",
        "airline": "Orbit Wings",
        "fare_class": "Basic",
        "base_price_usd": 250,
        "layovers": 1,
        "total_duration_hours": 6.8,
        "arrival_time_local": "18:45",
        "overnight_connection": False,
        "included_checked_baggage_kg": 15,
        "tags": ["budget", "city-break"],
    },
    {
        "flight_id": "VAC-BKK-410",
        "origin": "Karachi",
        "destination": "Bangkok",
        "departure_date": "2026-07-04",
        "return_date": "2026-07-10",
        "airline": "SunTrail Air",
        "fare_class": "Value",
        "base_price_usd": 540,
        "layovers": 1,
        "total_duration_hours": 8.2,
        "arrival_time_local": "14:35",
        "overnight_connection": False,
        "included_checked_baggage_kg": 25,
        "tags": ["beach", "summer", "couples"],
    },
    {
        "flight_id": "VAC-IST-515",
        "origin": "Karachi",
        "destination": "Istanbul",
        "departure_date": "2026-09-15",
        "return_date": "2026-09-22",
        "airline": "Crescent Atlantic",
        "fare_class": "Flex",
        "base_price_usd": 610,
        "layovers": 0,
        "total_duration_hours": 5.7,
        "arrival_time_local": "12:40",
        "overnight_connection": False,
        "included_checked_baggage_kg": 30,
        "tags": ["city-break", "history", "family", "refundable"],
    },
]

FARE_RULES = {
    "Basic": {
        "change_fee_usd": 120,
        "refundability": "Non-refundable after 24 hours",
        "seat_selection_included": False,
        "sports_equipment_fee_usd": 90,
        "extra_bag_fee_usd": 70,
    },
    "Saver": {
        "change_fee_usd": 90,
        "refundability": "Trip credit only after 24 hours",
        "seat_selection_included": False,
        "sports_equipment_fee_usd": 75,
        "extra_bag_fee_usd": 55,
    },
    "Value": {
        "change_fee_usd": 60,
        "refundability": "Refundable minus 20% fare penalty",
        "seat_selection_included": True,
        "sports_equipment_fee_usd": 60,
        "extra_bag_fee_usd": 45,
    },
    "Flex": {
        "change_fee_usd": 0,
        "refundability": "Fully refundable or free date change up to 6 hours before departure",
        "seat_selection_included": True,
        "sports_equipment_fee_usd": 35,
        "extra_bag_fee_usd": 30,
    },
}

BOOKINGS = {
    "BK-2401": {
        "booking_id": "BK-2401",
        "traveler_name": "Ayesha Khan",
        "origin": "Karachi",
        "destination": "Dubai",
        "flight_id": "VAC-DXB-101",
        "fare_class": "Saver",
        "status": "Confirmed",
        "hotel_check_in_local": "15:00",
        "current_delay_minutes": 155,
        "passport_months_validity": 5,
        "travelers": 2,
        "trip_type": "Vacation",
    },
    "BK-7730": {
        "booking_id": "BK-7730",
        "traveler_name": "Bilal Ahmed",
        "origin": "Karachi",
        "destination": "Istanbul",
        "flight_id": "VAC-IST-515",
        "fare_class": "Flex",
        "status": "Confirmed",
        "hotel_check_in_local": "16:00",
        "current_delay_minutes": 0,
        "passport_months_validity": 11,
        "travelers": 1,
        "trip_type": "Vacation",
    },
}

DESTINATION_ADVISORIES = {
    "Dubai": {
        "best_for": ["beach vacations", "short luxury breaks", "family-friendly resorts"],
        "passport_guidance": "Travelers should generally hold a passport valid for at least 6 months from arrival.",
        "weather_note": "Expect strong heat in June; morning arrivals are usually more comfortable for transfers.",
        "transfer_tip": "For resort transfers, arrivals before 15:00 local time are preferred.",
    },
    "Bangkok": {
        "best_for": ["city plus island vacations", "food-focused trips", "summer shopping"],
        "passport_guidance": "A passport with at least 6 months validity is typically recommended.",
        "weather_note": "July is humid with possible afternoon showers; nonstop or early arrival options reduce fatigue.",
        "transfer_tip": "Allow extra buffer time if connecting onward to island ferries.",
    },
    "Istanbul": {
        "best_for": ["history trips", "family sightseeing", "shoulder-season travel"],
        "passport_guidance": "A minimum of 6 months passport validity is the safer planning baseline.",
        "weather_note": "September is comfortable for walking itineraries and day tours.",
        "transfer_tip": "Landing before lunch helps with hotel check-in and same-day sightseeing.",
    },
}

SEASONAL_OFFERS = [
    {
        "offer_id": "SUMMER-DXB-01",
        "destination": "Dubai",
        "description": "Free airport-to-resort transfer on Flex fares for June beach itineraries.",
        "valid_for_fare_class": "Flex",
    },
    {
        "offer_id": "FAMILY-BKK-02",
        "destination": "Bangkok",
        "description": "25 kg baggage bonus for Value fare bookings with 2 or more travelers.",
        "valid_for_fare_class": "Value",
    },
]

POLICIES = {
    "refund_change": """
Vacation Flight Change and Refund Policy:
- Basic fares: Non-refundable after the 24-hour grace period. Date changes cost 120 USD plus any fare difference.
- Saver fares: Eligible for trip credit after the 24-hour grace period. Date changes cost 90 USD plus any fare difference.
- Value fares: Refundable minus a 20% fare penalty. Date changes cost 60 USD plus any fare difference.
- Flex fares: Fully refundable and date changes are free up to 6 hours before departure.
""".strip(),
    "baggage": """
Vacation Flight Baggage Policy:
- Basic includes 15 kg checked baggage.
- Saver includes 20 kg checked baggage.
- Value includes 25 kg checked baggage.
- Flex includes 30 kg checked baggage.
- Extra checked bag pricing is determined by fare rules.
- Sports equipment is charged separately unless a seasonal offer waives the fee.
""".strip(),
    "compensation": """
Irregular Operations Compensation Policy:
- Delays under 90 minutes: No compensation.
- Delays from 90 to 179 minutes: 35 USD meal credit.
- Delays of 180 minutes or more: Free same-cabin rebooking or 100 USD travel credit.
- If a delay causes a missed prepaid resort transfer, travelers may choose resort transfer reimbursement instead of the travel credit.
""".strip(),
    "travel_documents": """
Travel Document Guidance:
- For international vacation itineraries in this demo, planning should assume at least 6 months passport validity from arrival.
- If the traveler has less than 6 months validity, the agent should flag risk and recommend verifying official destination requirements before ticketing.
""".strip(),
    "offers": """
Seasonal Vacation Offers:
- Dubai Flex June itineraries include a complimentary airport-to-resort transfer.
- Bangkok Value bookings for 2 or more travelers include a 25 kg baggage bonus.
""".strip(),
}


def _find_flight(flight_id: str) -> dict[str, Any] | None:
    for flight in FLIGHTS:
        if flight["flight_id"] == flight_id:
            return flight
    return None


def _select_fare_rules(fare_class_or_flight_id: str) -> dict[str, Any] | None:
    if fare_class_or_flight_id in FARE_RULES:
        return FARE_RULES[fare_class_or_flight_id]
    flight = _find_flight(fare_class_or_flight_id)
    if not flight:
        return None
    return FARE_RULES.get(flight["fare_class"])


@mcp.tool()
def search_flights(
    origin: str,
    destination: str,
    dates: str,
    travelers: int = 1,
    preferences: str = "",
) -> dict[str, Any]:
    """Searches mocked vacation flight options and returns ranked matches."""
    prefs = preferences.lower()
    normalized_destination = destination.lower()
    matches = []

    for flight in FLIGHTS:
        if flight["origin"].lower() != origin.lower():
            continue
        if flight["destination"].lower() != normalized_destination:
            continue
        if dates and dates not in f"{flight['departure_date']} to {flight['return_date']}":
            continue

        score = 0
        if "minimal layover" in prefs or "nonstop" in prefs:
            score -= flight["layovers"] * 2
        if "kids" in prefs or "family" in prefs:
            score += 2 if not flight["overnight_connection"] else -5
        if "before 3 pm" in prefs or "before 15:00" in prefs:
            score += 3 if flight["arrival_time_local"] < "15:00" else -2
        if "25 kg" in prefs:
            score += 3 if flight["included_checked_baggage_kg"] >= 25 else -3
        if "budget" in prefs or "under" in prefs:
            score += max(0, 700 - flight["base_price_usd"])
        if travelers >= 2 and "family" in flight["tags"]:
            score += 2

        enriched = deepcopy(flight)
        enriched["estimated_total_base_usd"] = flight["base_price_usd"] * travelers
        enriched["match_score"] = score
        matches.append(enriched)

    matches.sort(key=lambda item: (-item["match_score"], item["base_price_usd"], item["layovers"]))
    return {
        "query": {
            "origin": origin,
            "destination": destination,
            "dates": dates,
            "travelers": travelers,
            "preferences": preferences,
        },
        "results": matches[:5],
    }


@mcp.tool()
def get_fare_rules(fare_class_or_flight_id: str) -> dict[str, Any]:
    """Returns baggage, refund, and change-fee rules for a fare class or flight ID."""
    rules = _select_fare_rules(fare_class_or_flight_id)
    if not rules:
        return {"error": "No fare rules found for that flight or fare class."}
    return rules


@mcp.tool()
def calculate_total_trip_cost(
    selection: str,
    baggage: int = 0,
    seats: int = 0,
    extras: str = "",
) -> dict[str, Any]:
    """Calculates the trip cost including baggage, seats, and optional sports equipment."""
    flight = _find_flight(selection)
    if not flight:
        return {"error": "Flight selection not found."}

    rules = FARE_RULES[flight["fare_class"]]
    extras_lower = extras.lower()
    extra_bag_cost = baggage * rules["extra_bag_fee_usd"]
    seat_cost = 0 if rules["seat_selection_included"] else seats * 18
    sports_fee = rules["sports_equipment_fee_usd"] if "sports" in extras_lower else 0

    total = flight["base_price_usd"] + extra_bag_cost + seat_cost + sports_fee
    return {
        "flight_id": selection,
        "fare_class": flight["fare_class"],
        "base_price_usd": flight["base_price_usd"],
        "extra_checked_bag_count": baggage,
        "extra_bag_cost_usd": extra_bag_cost,
        "seat_selection_count": seats,
        "seat_selection_cost_usd": seat_cost,
        "sports_equipment_cost_usd": sports_fee,
        "total_estimated_cost_usd": total,
    }


@mcp.tool()
def check_booking(booking_id: str) -> dict[str, Any]:
    """Returns a mocked booking record, including delay and passport-validity context."""
    booking = BOOKINGS.get(booking_id)
    if not booking:
        return {"error": "Booking not found."}

    flight = _find_flight(booking["flight_id"])
    result = deepcopy(booking)
    result["flight"] = flight
    return result


@mcp.tool()
def change_booking(booking_id: str, new_option: str) -> str:
    """Simulates changing an itinerary to a new flight option."""
    booking = BOOKINGS.get(booking_id)
    flight = _find_flight(new_option)
    if not booking:
        return "ERROR: Booking not found."
    if not flight:
        return "ERROR: New flight option not found."

    return (
        f"SUCCESS: Booking {booking_id} moved to {new_option} "
        f"({flight['airline']} {flight['departure_date']} -> {flight['return_date']})."
    )


@mcp.tool()
def get_disruption_options(booking_id: str) -> dict[str, Any]:
    """Returns recovery choices for a disrupted vacation itinerary."""
    booking = BOOKINGS.get(booking_id)
    if not booking:
        return {"error": "Booking not found."}

    if booking["current_delay_minutes"] < 90:
        return {
            "booking_id": booking_id,
            "delay_minutes": booking["current_delay_minutes"],
            "options": ["Keep current itinerary"],
        }

    return {
        "booking_id": booking_id,
        "delay_minutes": booking["current_delay_minutes"],
        "options": [
            "Rebook to VAC-DXB-204 with same-day earlier arrival",
            "Accept 100 USD travel credit",
            "Request resort transfer reimbursement if prepaid transfer is missed",
        ],
    }


@mcp.tool()
def process_refund_or_credit(booking_id: str, choice: str) -> str:
    """Processes a simulated refund, trip credit, or reimbursement decision."""
    if booking_id not in BOOKINGS:
        return "ERROR: Booking not found."
    return f"SUCCESS: {choice} has been processed for booking {booking_id}."


@mcp.tool()
def get_travel_policy(policy_type: str) -> str:
    """Returns a named policy document for baggage, refunds, compensation, or documents."""
    normalized = policy_type.strip().lower().replace(" ", "_")
    aliases = {
        "refund": "refund_change",
        "refunds": "refund_change",
        "change": "refund_change",
        "baggage_policy": "baggage",
        "documents": "travel_documents",
        "travel_docs": "travel_documents",
        "compensation_policy": "compensation",
        "seasonal_offers": "offers",
    }
    key = aliases.get(normalized, normalized)
    return POLICIES.get(key, "No policy found for that topic.")


@mcp.tool()
def get_destination_advisory(destination: str) -> dict[str, Any]:
    """Returns vacation-oriented destination guidance and document reminders."""
    advisory = DESTINATION_ADVISORIES.get(destination)
    if not advisory:
        return {"error": "No destination advisory found."}
    offers = [offer for offer in SEASONAL_OFFERS if offer["destination"].lower() == destination.lower()]
    return {"destination": destination, "advisory": advisory, "seasonal_offers": offers}


@mcp.resource("policy://refund-change")
def refund_change_policy() -> str:
    return POLICIES["refund_change"]


@mcp.resource("policy://baggage")
def baggage_policy() -> str:
    return POLICIES["baggage"]


@mcp.resource("policy://compensation")
def compensation_policy() -> str:
    return POLICIES["compensation"]


@mcp.resource("policy://travel-documents")
def travel_documents_policy() -> str:
    return POLICIES["travel_documents"]


@mcp.resource("offers://seasonal")
def seasonal_offers_resource() -> str:
    return json.dumps(SEASONAL_OFFERS, indent=2)
