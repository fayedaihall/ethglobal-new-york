from uagents import Agent, Context, Model, Protocol, Bureau
from uagents.setup import fund_agent_if_low
from pydantic import Field
import hashlib
import json
import math
from typing import List, Dict, Optional

# Define the input model for matching request
class MatchingRequest(Model):
    profile1: dict = Field(description="First dating profile as JSON, e.g., {'age': 30, 'interests': ['hiking', 'reading'], 'location': 'New York'}")
    profile2: dict = Field(description="Second dating profile as JSON, e.g., {'age': 28, 'interests': ['hiking', 'music'], 'location': 'Brooklyn'}")

# Define the output model for matching response
class MatchingResponse(Model):
    score: float = Field(description="Matching score between 0 and 100")
    explanation: str = Field(description="Explanation of the score")
    compatibility_factors: dict = Field(description="Detailed breakdown of compatibility factors")
    recommendations: List[str] = Field(description="Personalized recommendations based on the match")

# Create the agent
agent = Agent(
    name="dating_matcher",
    seed="your_secret_seed_phrase",  # Replace with a secure seed for fixed address
    port=8000,
    endpoint=["https://your-app.vercel.app/api/submit"],  # Update with your Vercel deployment URL
)

# Protocol for the agent (optional, but good practice)
protocol = Protocol(name="dating_matcher_protocol", version="1.0")

class CompatibilityAnalyzer:
    """Advanced compatibility analysis using uAgent's native intelligence"""
    
    @staticmethod
    def analyze_interests(interests1: List[str], interests2: List[str]) -> Dict:
        """Analyze interest compatibility with semantic grouping"""
        # Interest categories for semantic matching
        interest_categories = {
            'outdoor': ['hiking', 'camping', 'climbing', 'running', 'cycling', 'surfing', 'skiing'],
            'creative': ['art', 'music', 'writing', 'photography', 'painting', 'drawing', 'crafts'],
            'intellectual': ['reading', 'chess', 'debate', 'learning', 'philosophy', 'science'],
            'social': ['dancing', 'parties', 'networking', 'volunteering', 'community'],
            'culinary': ['cooking', 'baking', 'wine', 'restaurants', 'food'],
            'fitness': ['gym', 'yoga', 'pilates', 'sports', 'martial arts', 'crossfit'],
            'tech': ['programming', 'gaming', 'gadgets', 'ai', 'blockchain', 'coding']
        }
        
        # Categorize interests
        def categorize_interests(interests):
            categories = {}
            for interest in interests:
                for category, keywords in interest_categories.items():
                    if any(keyword in interest.lower() for keyword in keywords):
                        categories.setdefault(category, []).append(interest)
            return categories
        
        cats1 = categorize_interests(interests1)
        cats2 = categorize_interests(interests2)
        
        # Calculate semantic overlap
        common_categories = set(cats1.keys()) & set(cats2.keys())
        total_categories = set(cats1.keys()) | set(cats2.keys())
        
        direct_overlap = len(set(interests1) & set(interests2))
        semantic_overlap = len(common_categories)
        
        return {
            'direct_matches': direct_overlap,
            'semantic_matches': semantic_overlap,
            'total_interests': len(set(interests1) | set(interests2)),
            'common_categories': list(common_categories),
            'compatibility_score': (direct_overlap * 2 + semantic_overlap) / len(total_categories) if total_categories else 0
        }
    
    @staticmethod
    def analyze_age_compatibility(age1: int, age2: int) -> Dict:
        """Advanced age compatibility analysis"""
        age_diff = abs(age1 - age2)
        
        # Optimal age ranges based on psychological research
        if age_diff <= 2:
            compatibility = 1.0
            reason = "Very close in age - excellent life stage alignment"
        elif age_diff <= 5:
            compatibility = 0.8
            reason = "Good age compatibility - similar life experiences"
        elif age_diff <= 10:
            compatibility = 0.6 - (age_diff - 5) * 0.08
            reason = "Moderate age gap - some life stage differences"
        else:
            compatibility = max(0.2, 0.4 - (age_diff - 10) * 0.02)
            reason = "Significant age gap - may have different priorities"
        
        return {
            'age_difference': age_diff,
            'compatibility_score': compatibility,
            'reason': reason,
            'life_stage_match': compatibility > 0.7
        }
    
    @staticmethod
    def analyze_location(location1: str, location2: str) -> Dict:
        """Enhanced location compatibility analysis"""
        loc1_clean = location1.lower().strip()
        loc2_clean = location2.lower().strip()
        
        if loc1_clean == loc2_clean:
            return {
                'match_type': 'exact',
                'compatibility_score': 1.0,
                'reason': 'Same location - easy to meet'
            }
        
        # Check for same city different areas (simplified)
        major_cities = ['new york', 'los angeles', 'chicago', 'houston', 'phoenix', 'philadelphia']
        for city in major_cities:
            if city in loc1_clean and city in loc2_clean:
                return {
                    'match_type': 'same_city',
                    'compatibility_score': 0.8,
                    'reason': f'Same metropolitan area ({city}) - manageable distance'
                }
        
        # Check for same state (simplified)
        states = ['california', 'texas', 'florida', 'new york', 'illinois']
        for state in states:
            if state in loc1_clean and state in loc2_clean:
                return {
                    'match_type': 'same_state',
                    'compatibility_score': 0.4,
                    'reason': f'Same state ({state}) - possible for long-distance'
                }
        
        return {
            'match_type': 'different',
            'compatibility_score': 0.1,
            'reason': 'Different regions - long-distance challenges'
        }

def generate_recommendations(profile1: Dict, profile2: Dict, compatibility_factors: Dict) -> List[str]:
    """Generate personalized recommendations using uAgent intelligence"""
    recommendations = []
    
    # Interest-based recommendations
    if compatibility_factors['interests']['direct_matches'] > 0:
        common_interests = list(set(profile1.get('interests', [])) & set(profile2.get('interests', [])))
        recommendations.append(f"Plan activities around shared interests: {', '.join(common_interests[:3])}")
    
    # Age-based recommendations
    age_factor = compatibility_factors['age']
    if age_factor['life_stage_match']:
        recommendations.append("Your similar life stages create great potential for shared goals")
    else:
        recommendations.append("Embrace the different perspectives your age difference brings")
    
    # Location-based recommendations
    location_factor = compatibility_factors['location']
    if location_factor['match_type'] == 'exact':
        recommendations.append("Being in the same area makes meeting up easy - suggest local date spots")
    elif location_factor['match_type'] == 'same_city':
        recommendations.append("Explore different neighborhoods together to bridge your local differences")
    
    return recommendations

# Handler for incoming matching requests
@protocol.on_message(model=MatchingRequest, replies=MatchingResponse)
async def handle_matching_request(ctx: Context, sender: str, msg: MatchingRequest):
    profile1 = msg.profile1
    profile2 = msg.profile2
    
    analyzer = CompatibilityAnalyzer()
    
    # Comprehensive analysis using uAgent's native intelligence
    age_analysis = analyzer.analyze_age_compatibility(
        profile1.get('age', 25), 
        profile2.get('age', 25)
    )
    
    interest_analysis = analyzer.analyze_interests(
        profile1.get('interests', []), 
        profile2.get('interests', [])
    )
    
    location_analysis = analyzer.analyze_location(
        profile1.get('location', ''), 
        profile2.get('location', '')
    )
    
    # Calculate weighted final score
    age_weight = 0.25
    interest_weight = 0.50
    location_weight = 0.25
    
    final_score = (
        age_analysis['compatibility_score'] * age_weight * 100 +
        interest_analysis['compatibility_score'] * interest_weight * 100 +
        location_analysis['compatibility_score'] * location_weight * 100
    )
    
    # Ensure score is within bounds
    final_score = max(0, min(100, final_score))
    
    # Create detailed compatibility factors
    compatibility_factors = {
        'age': age_analysis,
        'interests': interest_analysis,
        'location': location_analysis,
        'overall_score': final_score
    }
    
    # Generate AI-powered explanation
    explanation = f"""Compatibility Analysis:
• Age: {age_analysis['reason']} (Score: {age_analysis['compatibility_score']*100:.0f}/100)
• Interests: {interest_analysis['direct_matches']} direct matches, {interest_analysis['semantic_matches']} category overlaps (Score: {interest_analysis['compatibility_score']*100:.0f}/100)
• Location: {location_analysis['reason']} (Score: {location_analysis['compatibility_score']*100:.0f}/100)"""
    
    # Generate personalized recommendations
    recommendations = generate_recommendations(profile1, profile2, compatibility_factors)
    
    ctx.logger.info(f"Computed advanced match score: {final_score:.1f} for sender {sender}")
    
    await ctx.send(sender, MatchingResponse(
        score=final_score,
        explanation=explanation,
        compatibility_factors=compatibility_factors,
        recommendations=recommendations
    ))

# Include the protocol in the agent
agent.include(protocol)

if __name__ == "__main__":
    agent.run()
