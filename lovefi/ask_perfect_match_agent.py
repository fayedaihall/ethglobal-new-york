from pydantic import BaseModel, Field
from uagents import Agent, Context, Model

# Initialize the client agent without server to avoid pydantic validation error
agent = Agent(
    name="user_client_agent",
    seed="user_client_seed"
    # No port or endpoint specified to avoid REST server and pydantic validation bug
)

# Define request and response models (must match the AI Agent's)
class MatchRequest(BaseModel):
    description: str = Field(
        description="The user's personal description to find a perfect match for."
    )

class MatchResponse(BaseModel):
    match_profile: str = Field(
        description="The generated profile of the perfect match."
    )
    image_url: str = Field(
        description="The URL of the AI-generated image of the perfect match."
    )

# Replace this with your actual description
USER_DESCRIPTION = "Enter your personal description here, e.g., age, interests, personality, what you're looking for."


# AI Agent's address (copy this from the AI Agent's startup log, e.g., agent1q...')
AI_AGENT_ADDRESS = "agent1qwzw2gu2ql5q4f0whugwgenqt9dpn742ckevrn7272nsl6ecvlme26smv57"  # Paste the actual address here after running ai_agent.py

# Startup event to send the request
@agent.on_event("startup")
async def send_request(ctx: Context):
    ctx.logger.info(f"Sending description: {USER_DESCRIPTION}")
    await ctx.send(AI_AGENT_ADDRESS, MatchRequest(description=USER_DESCRIPTION))

# Handler for the response
@agent.on_message(model=MatchResponse)
async def handle_response(ctx: Context, sender: str, msg: MatchResponse):
    ctx.logger.info(f"Received from {sender}:")
    ctx.logger.info(f"Perfect Match Profile: {msg.match_profile}")
    ctx.logger.info(f"AI-Generated Image URL: {msg.image_url}")
    # You can open the image URL in a browser to view it

if __name__ == "__main__":
    agent.run()