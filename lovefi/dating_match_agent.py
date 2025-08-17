from datetime import datetime, timedelta
from uuid import uuid4
from typing import Any, List, Dict
from uagents import Agent, Context, Model, Protocol
import requests
from math import radians, sin, cos, sqrt, asin
import difflib

# Import the necessary components of the chat protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

# Helper functions
def calculate_age(birthday_str: str) -> int | None:
    if not birthday_str:
        return None
    try:
        birth_date = datetime.fromisoformat(birthday_str)
        today = datetime.utcnow()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except:
        return None

def get_coordinates(address: str) -> tuple[float, float]:
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(address)}&format=json&limit=1"
        response = requests.get(url, headers={'User-Agent': 'DatingMatchAgent/1.0'})
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
    except:
        pass
    return None, None

def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

# Define sub models
class Location(Model):
    address: str
    search_radius: int = 10

class Preference(Model):
    category: str
    question: str
    options: List[str]
    selected_index: int
    selected_option: str

class PersonalInfo(Model):
    first_name: str
    last_name: str
    birthday: str = ""

# Define the MatchRequest and MatchResponse data models
class MatchRequest(Model):
    personal_info1: PersonalInfo
    gender1: str
    location1: Location
    personal_interests1: List[str]
    partner_preferences1: List[Preference]
    personal_info2: PersonalInfo
    gender2: str
    location2: Location
    personal_interests2: List[str]
    partner_preferences2: List[Preference]

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

# Function to calculate match score (wrapper for simple parameters)
def calculate_match_score(
    name1: str = None, age1: int = None, interests1: List[str] = None, location1: str = None, preferences1: dict = None,
    name2: str = None, age2: int = None, interests2: List[str] = None, location2: str = None, preferences2: dict = None,
    # Original parameters for backward compatibility
    personal_info1: PersonalInfo = None, gender1: str = None, location1_obj: Location = None, personal_interests1: List[str] = None, partner_preferences1: List[Preference] = None,
    personal_info2: PersonalInfo = None, gender2: str = None, location2_obj: Location = None, personal_interests2: List[str] = None, partner_preferences2: List[Preference] = None
) -> tuple[float, str]:
    # Handle simple parameter format (for testing)
    if name1 is not None and personal_info1 is None:
        # Create PersonalInfo objects from simple parameters
        personal_info1 = PersonalInfo(first_name=name1.split()[0] if name1 else "Unknown", last_name=name1.split()[-1] if name1 and len(name1.split()) > 1 else "", birthday="")
        personal_info2 = PersonalInfo(first_name=name2.split()[0] if name2 else "Unknown", last_name=name2.split()[-1] if name2 and len(name2.split()) > 1 else "", birthday="")
        
        # Create Location objects from simple parameters
        max_age_diff1 = preferences1.get("max_age_diff", 10) if preferences1 else 10
        max_age_diff2 = preferences2.get("max_age_diff", 10) if preferences2 else 10
        location1_obj = Location(address=location1 if location1 else "", search_radius=max_age_diff1)  # Reuse for search radius
        location2_obj = Location(address=location2 if location2 else "", search_radius=max_age_diff2)
        
        # Use provided interests or empty list
        personal_interests1 = interests1 if interests1 else []
        personal_interests2 = interests2 if interests2 else []
        
        # Create empty preferences list for now
        partner_preferences1 = []
        partner_preferences2 = []
        
        # Set default genders
        gender1 = "not_specified"
        gender2 = "not_specified"
        
        # Call special version for simple parameters that handles ages directly
        return calculate_match_score_simple(
            age1, age2, personal_interests1, personal_interests2, location1_obj, location2_obj, 
            partner_preferences1, partner_preferences2, max_age_diff1, max_age_diff2
        )
    
    return calculate_match_score_internal(
        personal_info1, gender1, location1_obj, personal_interests1, partner_preferences1,
        personal_info2, gender2, location2_obj, personal_interests2, partner_preferences2
    )

# Simple function for test cases with direct age parameters
def calculate_match_score_simple(
    age1: int, age2: int, personal_interests1: List[str], personal_interests2: List[str], 
    location1: Location, location2: Location, partner_preferences1: List[Preference], 
    partner_preferences2: List[Preference], max_age_diff1: int, max_age_diff2: int
) -> tuple[float, str]:
    score = 0.0
    details = []

    # Interest compatibility (40%)
    common_interests = set(personal_interests1).intersection(set(personal_interests2))
    max_interests = max(len(personal_interests1), len(personal_interests2), 1)
    interest_score = (len(common_interests) / max_interests) * 40
    score += interest_score
    details.append(f"Interest compatibility: {interest_score:.1f}/40 (Common interests: {', '.join(common_interests) or 'None'})")

    # Age compatibility (20%) - Use direct ages
    if age1 is not None and age2 is not None:
        age_diff = abs(age1 - age2)
        max_age_diff = max(max_age_diff1, max_age_diff2)
        age_score = max(0, (1 - age_diff / max_age_diff)) * 20 if max_age_diff > 0 else 20
        age_detail = f"{age_diff} years"
    else:
        age_score = 10  # Neutral if unknown
        age_detail = "Unknown"
    score += age_score
    details.append(f"Age compatibility: {age_score:.1f}/20 (Age difference: {age_detail})")

    # Location compatibility (20%)
    loc_score = 0.0
    dist = None
    try:
        lat1, lon1 = get_coordinates(location1.address)
        lat2, lon2 = get_coordinates(location2.address)
        if lat1 is not None and lon1 is not None and lat2 is not None and lon2 is not None:
            dist = haversine(lon1, lat1, lon2, lat2)
            max_radius = max(location1.search_radius, location2.search_radius)
            if dist <= max_radius:
                loc_score = 20 * (1 - dist / max_radius)
            else:
                loc_score = 0
        else:
            # Fallback to string similarity
            similarity = difflib.SequenceMatcher(None, location1.address.lower(), location2.address.lower()).ratio()
            loc_score = similarity * 20
    except Exception:
        # Fallback
        similarity = difflib.SequenceMatcher(None, location1.address.lower(), location2.address.lower()).ratio()
        loc_score = similarity * 20
    score += loc_score
    dist_str = f"{dist:.1f} km" if dist is not None else "Unknown"
    details.append(f"Location compatibility: {loc_score:.1f}/20 (Distance: {dist_str})")

    # Preference compatibility (20%)
    num_matching = 0
    total = min(len(partner_preferences1), len(partner_preferences2))
    if total > 0:
        for p1, p2 in zip(partner_preferences1, partner_preferences2):
            if p1.selected_option == p2.selected_option:
                num_matching += 1
        pref_score = (num_matching / total) * 20
    else:
        pref_score = 0
    score += pref_score
    details.append(f"Preference compatibility: {pref_score:.1f}/20 (Matching preferences: {num_matching}/{total})")

    # Ensure score is between 0 and 100
    score = min(max(score, 0), 100)
    return score, "; ".join(details)

# Internal function with original logic
def calculate_match_score_internal(
    personal_info1: PersonalInfo, gender1: str, location1: Location, personal_interests1: List[str], partner_preferences1: List[Preference],
    personal_info2: PersonalInfo, gender2: str, location2: Location, personal_interests2: List[str], partner_preferences2: List[Preference]
) -> tuple[float, str]:
    score = 0.0
    details = []

    # Calculate ages
    age1 = calculate_age(personal_info1.birthday)
    age2 = calculate_age(personal_info2.birthday)

    # Interest compatibility (40%)
    common_interests = set(personal_interests1).intersection(set(personal_interests2))
    max_interests = max(len(personal_interests1), len(personal_interests2), 1)
    interest_score = (len(common_interests) / max_interests) * 40
    score += interest_score
    details.append(f"Interest compatibility: {interest_score:.1f}/40 (Common interests: {', '.join(common_interests) or 'None'})")

    # Age compatibility (20%)
    if age1 is not None and age2 is not None:
        age_diff = abs(age1 - age2)
        max_age_diff = 10  # Default, can be extended if added to preferences
        age_score = max(0, (1 - age_diff / max_age_diff)) * 20 if max_age_diff > 0 else 20
        age_detail = f"{age_diff} years"
    else:
        age_score = 10  # Neutral if unknown
        age_detail = "Unknown"
    score += age_score
    details.append(f"Age compatibility: {age_score:.1f}/20 (Age difference: {age_detail})")

    # Location compatibility (20%)
    loc_score = 0.0
    dist = None
    try:
        lat1, lon1 = get_coordinates(location1.address)
        lat2, lon2 = get_coordinates(location2.address)
        if lat1 is not None and lon1 is not None and lat2 is not None and lon2 is not None:
            dist = haversine(lon1, lat1, lon2, lat2)
            max_radius = max(location1.search_radius, location2.search_radius)
            if dist <= max_radius:
                loc_score = 20 * (1 - dist / max_radius)
            else:
                loc_score = 0
        else:
            # Fallback to string similarity
            similarity = difflib.SequenceMatcher(None, location1.address.lower(), location2.address.lower()).ratio()
            loc_score = similarity * 20
    except Exception:
        # Fallback
        similarity = difflib.SequenceMatcher(None, location1.address.lower(), location2.address.lower()).ratio()
        loc_score = similarity * 20
    score += loc_score
    dist_str = f"{dist:.1f} km" if dist is not None else "Unknown"
    details.append(f"Location compatibility: {loc_score:.1f}/20 (Distance: {dist_str})")

    # Preference compatibility (20%)
    num_matching = 0
    total = min(len(partner_preferences1), len(partner_preferences2))
    if total > 0:
        for p1, p2 in zip(partner_preferences1, partner_preferences2):
            if p1.selected_option == p2.selected_option:
                num_matching += 1
        pref_score = (num_matching / total) * 20
    else:
        pref_score = 0
    score += pref_score
    details.append(f"Preference compatibility: {pref_score:.1f}/20 (Matching preferences: {num_matching}/{total})")

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
                    output_schema=MatchRequest.model_json_schema()
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
        score, details = calculate_match_score_internal(
            prompt.personal_info1, prompt.gender1, prompt.location1, prompt.personal_interests1, prompt.partner_preferences1,
            prompt.personal_info2, prompt.gender2, prompt.location2, prompt.personal_interests2, prompt.partner_preferences2
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

    name1 = f"{prompt.personal_info1.first_name} {prompt.personal_info1.last_name}"
    name2 = f"{prompt.personal_info2.first_name} {prompt.personal_info2.last_name}"
    response_text = f"Match Score for {name1} and {name2}: {score:.1f}/100\nDetails: {details}"
    chat_message = create_text_chat(response_text)
    await ctx.send(session_sender, chat_message)

# Protocol handler for direct match calculation requests
@agent.on_message(MatchRequest, replies=MatchResponse)
async def handle_match_calculation(ctx: Context, sender: str, msg: MatchRequest):
    ctx.logger.info(f"Received match calculation request from {sender}")
    try:
        score, details = calculate_match_score_internal(
            msg.personal_info1, msg.gender1, msg.location1, msg.personal_interests1, msg.partner_preferences1,
            msg.personal_info2, msg.gender2, msg.location2, msg.personal_interests2, msg.partner_preferences2
        )
        response = MatchResponse(score=score, details=details)
        await ctx.send(sender, response)
    except Exception as err:
        ctx.logger.error(f"Error processing match request: {err}")
        error_response = MatchResponse(
            score=0.0,
            details=f"Error processing match request: {str(err)}"
        )
        await ctx.send(sender, error_response)

# Include protocols in the agent
agent.include(chat_proto)
agent.include(struct_output_client_proto)

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"DatingMatchAgent started. Address: {ctx.agent.address}")
    ctx.logger.info("Agent accepts MatchRequest messages via protocol communication")

if __name__ == "__main__":
    print(f"DatingMatchAgent address: {agent.address}")
    print("Agent created successfully. Use this address in your tests.")
    print("Starting agent on http://localhost:8000...")
    print("Agent handles protocol-based messages: MatchRequest")
    agent.run()
