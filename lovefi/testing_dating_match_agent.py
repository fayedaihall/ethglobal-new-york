from uagents import Agent, Context, Model
from typing import List, Dict

# Define the MatchRequest data model
class MatchRequest(Model):
    name1: str
    age1: int
    interests1: List[str]
    location1: str
    preferences1: Dict
    name2: str
    age2: int
    interests2: List[str]
    location2: str
    preferences2: Dict

# Initialize the test agent
test_agent = Agent(
    name="TestAgent",
    seed="test_seed_5678",  # Static seed
    metadata={"type": "test"}
)

# Send a test request on startup
@test_agent.on_event("startup")
async def send_test_request(ctx: Context):
    request = MatchRequest(
        name1="Alice",
        age1=25,
        interests1=["reading", "hiking"],
        location1="New York",
        preferences1={"max_age_diff": 5},
        name2="Bob",
        age2=27,
        interests2=["hiking", "music"],
        location2="New York",
        preferences2={"max_age_diff": 7}
    )
    # Use the specific DatingMatchAgent address
    dating_agent_address = "agent1qgh8g2gfcrrcjqjuuav8v6de3tp3dtc7f5hz4aveccpyym0g6s06ge5yf9w"
    await ctx.send(dating_agent_address, request)
    ctx.logger.info("Sent test MatchRequest to DatingMatchAgent")

# Add this at the end to run the agent
if __name__ == "__main__":
    # Simple test - just create agents and show addresses
    print("Creating test agents...")
    
    # Create the test agent
    test_agent = Agent(name="TestAgent", seed="test_seed_5678", metadata={"type": "test"})
    print(f"TestAgent address: {test_agent.address}")
    
    # Create the dating match agent
    dating_agent = Agent(name="DatingMatchAgent", seed="dating_match_seed_1234", metadata={"type": "dating_match"})
    print(f"DatingMatchAgent address: {dating_agent.address}")
    
    print("\nAgents created successfully!")
    print("To test communication between agents, you would need to run them with proper endpoints.")