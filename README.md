# Build a Vacation Flight Concierge with Google ADK and MCP

## Executive Summary
This project demonstrates how to build a deterministic, tool-using Google ADK agent for a vacation air-travel use case. Instead of a generic support bot, the agent acts like a vacation flight concierge that can compare flight options, explain baggage and refund rules, review existing bookings, react to delays, and complete follow-up actions in a mocked environment.

The demo is designed to showcase:
- multi-step reasoning
- grounded policy lookup
- cost and tradeoff analysis
- autonomous tool chaining

## Tech Stack
- Google ADK for the agent orchestration layer
- FastMCP for exposing tools and resources to the model
- Gemini 2.5 Flash as the reasoning model
- Docker Compose for the local two-service setup

## What Makes This Demo Different
This example is not just "search a flight" or "book a ticket."

The concierge helps with scenarios like:
- finding the best vacation itinerary under budget
- comparing fares after baggage and sports-equipment fees
- recommending safer refundable fares for families
- checking whether a booking disruption affects a hotel or resort transfer
- applying compensation or changing an itinerary after policy checks
- flagging passport-validity risk for international travel

## Repository Structure
```text
transit-agent/
|-- .env.example
|-- Dockerfile
|-- docker-compose.yml
|-- README.md
|-- vacation_flight_server.py
`-- agents/
    `-- __init__.py
```

## Quick Start
### 1. Clone the project
```bash
git clone <your-github-repo-url> vacation-flight-concierge
cd vacation-flight-concierge
```

### 2. Add your API key
Copy the example environment file:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
GOOGLE_API_KEY="YOUR_API_KEY"
```

### 3. Start the demo
```bash
docker compose up --build
```

This starts:
- the FastMCP server on port `8080`
- the ADK web app on port `8000`

### 4. Open the ADK Web UI
Visit:

```text
http://localhost:8000
```

Select this agent in the dropdown:

```text
vacation_flight_concierge
```

## Architecture Overview
### 1. MCP Server
`vacation_flight_server.py` exposes deterministic travel tools and resources, including:
- flight search
- fare rules
- full trip cost calculation
- booking lookup
- rebooking and refund simulation
- destination advisories
- baggage, compensation, refund, and travel-document policies

### 2. ADK Agent
`agents/__init__.py` connects to the MCP server over SSE and instructs Gemini to:
- gather evidence before acting
- consult policies instead of guessing
- compare options using tool outputs
- autonomously complete changes or credits when the user explicitly authorizes them

## MCP Surface
### Tools
- `search_flights(origin, destination, dates, travelers, preferences)`
- `get_fare_rules(fare_class_or_flight_id)`
- `calculate_total_trip_cost(selection, baggage, seats, extras)`
- `check_booking(booking_id)`
- `change_booking(booking_id, new_option)`
- `get_disruption_options(booking_id)`
- `process_refund_or_credit(booking_id, choice)`
- `get_travel_policy(policy_type)`
- `get_destination_advisory(destination)`

### Resources
- `policy://refund-change`
- `policy://baggage`
- `policy://compensation`
- `policy://travel-documents`
- `offers://seasonal`

## Suggested Demo Prompts
Use these in the ADK Web UI to test progressively more agentic behavior.

### Level 1: Simple Search
The agent should primarily use `search_flights`.

**"I want a 5-day beach vacation from Karachi to Dubai in June for 2 travelers under 700 USD each. Find the best option with minimal layovers."**

### Level 2: Policy and Fare Understanding
The agent should use `get_fare_rules`, `get_travel_policy`, or both.

**"Compare the refundability and baggage rules for VAC-DXB-101 and VAC-DXB-204, and tell me which one is safer for a family trip."**

### Level 3: True Cost Comparison
The agent should combine `calculate_total_trip_cost` with fare rules.

**"I'm choosing between VAC-DXB-101 and VAC-DXB-204. I need 2 extra checked bags and sports equipment. Which fare is actually cheaper after all fees?"**

### Level 4: Destination and Travel-Risk Reasoning
The agent should use `get_destination_advisory` and `get_travel_policy`.

**"I'm planning a Dubai vacation and my passport expires in 5 months. Is this risky, and which itinerary in your system lands early enough for a resort transfer?"**

### Level 5: Booking Recovery
The agent should start with `check_booking`, then use disruption and policy tools.

**"Use booking BK-2401. Check whether my vacation is affected, tell me what compensation or rebooking options I have, and explain which option is best if I do not want to miss hotel check-in."**

### Level 6: Autonomous Action
The agent should inspect the booking, evaluate the disruption, and then act.

**"Use booking BK-2401. If I qualify for a same-cabin rebooking that gets me into Dubai earlier, change my booking to the best option. Otherwise process the most valuable compensation available."**

## Notes for Publishing
- The project uses mocked travel data so it is reproducible and easy to demo.
- No real booking or payment is performed.
- The strongest GitHub demo value comes from the README scenarios and the agent's reasoning trace, not from backend complexity.
- Keep `.env` out of version control. A `.gitignore` is included for that purpose.
