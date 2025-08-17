from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
from typing import List, Dict, Optional, Any
import base64

try:
    from mangum import Mangum
except ImportError:
    # Fallback if mangum is not available
    Mangum = None

app = FastAPI(title="Dating Matcher API")

@app.post("/api/submit")
@app.post("/submit")
async def handle_agent_message(request: Request):
    """
    Handle incoming uAgent messages
    """
    try:
        body = await request.json()
        
        # Extract payload from uAgent envelope
        if 'payload' in body:
            import base64
            payload_str = base64.b64decode(body['payload']).decode('utf-8')
            payload_data = json.loads(payload_str)
            
            # Process the matching request
            if 'profile1' in payload_data and 'profile2' in payload_data:
                profile1 = payload_data['profile1']
                profile2 = payload_data['profile2']
                
                # Import the enhanced compatibility analyzer
                from typing import List, Dict
                
                class CompatibilityAnalyzer:
                    @staticmethod
                    def analyze_interests(interests1: List[str], interests2: List[str]) -> Dict:
                        interest_categories = {
                            'outdoor': ['hiking', 'camping', 'climbing', 'running', 'cycling', 'surfing', 'skiing'],
                            'creative': ['art', 'music', 'writing', 'photography', 'painting', 'drawing', 'crafts'],
                            'intellectual': ['reading', 'chess', 'debate', 'learning', 'philosophy', 'science'],
                            'social': ['dancing', 'parties', 'networking', 'volunteering', 'community'],
                            'culinary': ['cooking', 'baking', 'wine', 'restaurants', 'food'],
                            'fitness': ['gym', 'yoga', 'pilates', 'sports', 'martial arts', 'crossfit'],
                            'tech': ['programming', 'gaming', 'gadgets', 'ai', 'blockchain', 'coding']
                        }
                        
                        def categorize_interests(interests):
                            categories = {}
                            for interest in interests:
                                for category, keywords in interest_categories.items():
                                    if any(keyword in interest.lower() for keyword in keywords):
                                        categories.setdefault(category, []).append(interest)
                            return categories
                        
                        cats1 = categorize_interests(interests1)
                        cats2 = categorize_interests(interests2)
                        
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
                        age_diff = abs(age1 - age2)
                        
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
                        loc1_clean = location1.lower().strip()
                        loc2_clean = location2.lower().strip()
                        
                        if loc1_clean == loc2_clean:
                            return {
                                'match_type': 'exact',
                                'compatibility_score': 1.0,
                                'reason': 'Same location - easy to meet'
                            }
                        
                        major_cities = ['new york', 'los angeles', 'chicago', 'houston', 'phoenix', 'philadelphia']
                        for city in major_cities:
                            if city in loc1_clean and city in loc2_clean:
                                return {
                                    'match_type': 'same_city',
                                    'compatibility_score': 0.8,
                                    'reason': f'Same metropolitan area ({city}) - manageable distance'
                                }
                        
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
                    recommendations = []
                    
                    if compatibility_factors['interests']['direct_matches'] > 0:
                        common_interests = list(set(profile1.get('interests', [])) & set(profile2.get('interests', [])))
                        recommendations.append(f"Plan activities around shared interests: {', '.join(common_interests[:3])}")
                    
                    age_factor = compatibility_factors['age']
                    if age_factor['life_stage_match']:
                        recommendations.append("Your similar life stages create great potential for shared goals")
                    else:
                        recommendations.append("Embrace the different perspectives your age difference brings")
                    
                    location_factor = compatibility_factors['location']
                    if location_factor['match_type'] == 'exact':
                        recommendations.append("Being in the same area makes meeting up easy - suggest local date spots")
                    elif location_factor['match_type'] == 'same_city':
                        recommendations.append("Explore different neighborhoods together to bridge your local differences")
                    
                    return recommendations
                
                # Enhanced compatibility analysis using uAgent intelligence
                analyzer = CompatibilityAnalyzer()
                
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
                
                final_score = max(0, min(100, final_score))
                
                compatibility_factors = {
                    'age': age_analysis,
                    'interests': interest_analysis,
                    'location': location_analysis,
                    'overall_score': final_score
                }
                
                explanation = f"""Compatibility Analysis:
• Age: {age_analysis['reason']} (Score: {age_analysis['compatibility_score']*100:.0f}/100)
• Interests: {interest_analysis['direct_matches']} direct matches, {interest_analysis['semantic_matches']} category overlaps (Score: {interest_analysis['compatibility_score']*100:.0f}/100)
• Location: {location_analysis['reason']} (Score: {location_analysis['compatibility_score']*100:.0f}/100)"""
                
                recommendations = generate_recommendations(profile1, profile2, compatibility_factors)
                
                # Create enhanced response envelope
                response_payload = {
                    "score": final_score,
                    "explanation": explanation,
                    "compatibility_factors": compatibility_factors,
                    "recommendations": recommendations
                }
                
                response_envelope = {
                    "version": 1,
                    "sender": "agent1qlovefi...",  # Your agent address
                    "target": body.get('sender', ''),
                    "session": body.get('session', ''),
                    "schema_digest": "matching_response_schema",
                    "protocol_digest": None,
                    "payload": base64.b64encode(json.dumps(response_payload).encode()).decode(),
                    "expires": body.get('expires', 0),
                    "nonce": body.get('nonce', 0),
                    "signature": None
                }
                
                return JSONResponse(content=response_envelope, status_code=200)
        
        return JSONResponse(content={"status": "received"}, status_code=200)
        
    except Exception as e:
        print(f"Error processing request: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/")
@app.get("/api")
async def health_check():
    """Health check endpoint"""
    return {"status": "Dating Matcher Agent is running", "agent": "lovefi-matcher"}

# Create the Mangum handler for Vercel
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
