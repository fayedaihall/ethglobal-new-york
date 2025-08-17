from datetime import datetime
from uuid import uuid4
from typing import Any, List, Dict
from uagents import Agent, Context, Model, Protocol

# Import the necessary components of the chat protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

# Define the MatchRequest and MatchResponse data models
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

class MatchResponse(Model):
    score: float
    details: str

# Initialize the agent
agent = Agent(
    name="DatingMatchAgent",
    seed="dating_match_seed_1234",
    metadata={"type": "dating_match"},
    port=8000,
    endpoint=["http://localhost:8000/submit"]
)

# Define the chat protocol and structured output protocol
chat_proto = Protocol(spec=chat_protocol_spec)
struct_output_client_proto = Protocol(
    name="StructuredOutputClientProtocol", version="0.1.0"
)

# Replace with one of the provided LLM addresses
AI_AGENT_ADDRESS = 'agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y'

if not AI_AGENT_ADDRESS:
    raise ValueError("AI_AGENT_ADDRESS not set")

# Function to create a chat message
def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )

# Function to calculate match score
def calculate_match_score(
    name1: str, age1: int, interests1: List[str], location1: str, preferences1: Dict,
    name2: str, age2: int, interests2: List[str], location2: str, preferences2: Dict
) -> tuple[float, str]:
    score = 0.0
    details = []

    # Interest compatibility (50% weight)
    common_interests = set(interests1).intersection(set(interests2))
    interest_score = (len(common_interests) / max(len(interests1), len(interests2))) * 50
    score += interest_score
    details.append(f"Interest compatibility: {interest_score:.1f}/50 (Common interests: {', '.join(common_interests) or 'None'})")

    # Age compatibility (30% weight)
    age_diff = abs(age1 - age2)
    max_age_diff = max(preferences1.get("max_age_diff", 10), preferences2.get("max_age_diff", 10))
    age_score = max(0, (1 - age_diff / max_age_diff)) * 30 if max_age_diff > 0 else 30
    score += age_score
    details.append(f"Age compatibility: {age_score:.1f}/30 (Age difference: {age_diff} years)")

    # Location compatibility (20% weight)
    location_score = 20 if location1.lower() == location2.lower() else 10
    score += location_score
    details.append(f"Location compatibility: {location_score}/20 (Same location: {location1 == location2})")

    # Ensure score is between 0 and 100
    score = min(max(score, 0), 100)
    return score, "; ".join(details)

class StructuredOutputPrompt(Model):
    prompt: str
    output_schema: dict[str, Any]

class StructuredOutputResponse(Model):
    output: dict[str, Any]

@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Got a message from {sender}: {msg.content}")
    ctx.storage.set(str(ctx.session), sender)
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id),
    )

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Got a start session message from {sender}")
            continue
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Got a text message from {sender}: {item.text}")
            ctx.storage.set(str(ctx.session), sender)
            await ctx.send(
                AI_AGENT_ADDRESS,
                StructuredOutputPrompt(
                    prompt=item.text,
                    output_schema=MatchRequest.schema()
                ),
            )
        else:
            ctx.logger.info(f"Got unexpected content from {sender}")

@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(
        f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}"
    )

@struct_output_client_proto.on_message(StructuredOutputResponse)
async def handle_structured_output_response(
    ctx: Context, sender: str, msg: StructuredOutputResponse
):
    session_sender = ctx.storage.get(str(ctx.session))
    if session_sender is None:
        ctx.logger.error(
            "Discarding message because no session sender found in storage"
        )
        return

    if "<UNKNOWN>" in str(msg.output):
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't process your match request. Please provide details for two people to compare."
            ),
        )
        return

    try:
        prompt = MatchRequest.parse_obj(msg.output)
    except Exception as err:
        ctx.logger.error(f"Error parsing structured output: {err}")
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't process your match request. Please try again with valid details."
            ),
        )
        return

    try:
        score, details = calculate_match_score(
            prompt.name1, prompt.age1, prompt.interests1, prompt.location1, prompt.preferences1,
            prompt.name2, prompt.age2, prompt.interests2, prompt.location2, prompt.preferences2
        )
    except Exception as err:
        ctx.logger.error(f"Error calculating match score: {err}")
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't process your match request. Please try again later."
            ),
        )
        return

    response_text = f"Match Score for {prompt.name1} and {prompt.name2}: {score:.1f}/100\nDetails: {details}"
    chat_message = create_text_chat(response_text)
    await ctx.send(session_sender, chat_message)

# REST POST endpoint for match requests
@agent.on_rest_post("/match/calculate", MatchRequest, MatchResponse)
async def handle_match_post(ctx: Context, req: MatchRequest) -> MatchResponse:
    ctx.logger.info(f"Received POST request for match calculation")
    try:
        score, details = calculate_match_score(
            req.name1, req.age1, req.interests1, req.location1, req.preferences1,
            req.name2, req.age2, req.interests2, req.location2, req.preferences2
        )
        return MatchResponse(score=score, details=details)
    except Exception as err:
        ctx.logger.error(f"Error processing match request: {err}")
        return MatchResponse(
            score=0.0,
            details=f"Error processing match request: {str(err)}"
        )

# Include protocols in the agent
agent.include(chat_proto)
agent.include(struct_output_client_proto)

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"DatingMatchAgent started. Address: {ctx.agent.address}")
    ctx.logger.info("REST endpoint available at http://localhost:8000/match/calculate")

if __name__ == "__main__":
    print(f"DatingMatchAgent address: {agent.address}")
    print("Agent created successfully. Use this address in your tests.")
    print("Starting agent on http://localhost:8000...")
    print("REST POST endpoint: http://localhost:8000/match/calculate")
    agent.run()