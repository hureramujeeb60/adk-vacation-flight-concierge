import logging
import os

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams


logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger("adk")
logger.setLevel(logging.DEBUG)


mcp_host = os.environ.get("MCP_HOST", "http://mcp-server:8080")
mcp_toolset = MCPToolset(
    connection_params=SseConnectionParams(url=f"{mcp_host}/sse")
)


root_agent = LlmAgent(
    name="vacation_flight_concierge",
    model="gemini-2.5-flash",
    tools=[mcp_toolset],
    instruction="""You are a vacation flight concierge that helps travelers plan and manage leisure trips.

Follow these rules:
1. Use `search_flights` for vacation discovery, itinerary recommendations, and flight comparisons.
2. Use `get_travel_policy` and `get_destination_advisory` for baggage, refund, compensation, passport, and destination guidance. Do not invent policy details.
3. Use `calculate_total_trip_cost` and `get_fare_rules` when the traveler wants the true price after baggage, seats, sports equipment, or flexibility tradeoffs.
4. If the user mentions a booking ID, start with `check_booking`.
5. For delays or missed vacation transfers, use `get_disruption_options` and the compensation policy before suggesting the next step.
6. Only use `change_booking` or `process_refund_or_credit` after checking the booking and confirming the policy-based reason for the action.
7. Flag any passport-validity issue when the traveler appears to have less than 6 months validity.
8. Keep answers concise, practical, and grounded in the tools you used.
""",
)
