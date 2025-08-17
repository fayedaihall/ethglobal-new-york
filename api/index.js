export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Handle OPTIONS request for CORS preflight
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Handle different routes
  const { url, method } = req;
  
  try {
    if (url === '/' || url === '/api' || url === '/api/') {
      // Health check endpoint
      res.status(200).json({
        status: "Dating Matcher Agent is running",
        agent: "lovefi-matcher", 
        message: "Node.js endpoint working",
        method: method,
        timestamp: new Date().toISOString()
      });
    } else if (url === '/submit' || url === '/api/submit') {
      // Agent message handler
      if (method === 'POST') {
        // Parse JSON body
        let body = {};
        if (req.body) {
          body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
        }

        // Handle uAgent message envelope
        if (body.payload) {
          try {
            // Decode base64 payload
            const payloadStr = Buffer.from(body.payload, 'base64').toString('utf-8');
            const payloadData = JSON.parse(payloadStr);

            // Process matching request
            if (payloadData.profile1 && payloadData.profile2) {
              const matchResult = calculateCompatibility(payloadData.profile1, payloadData.profile2);
              
              // Create response envelope
              const responsePayload = {
                score: matchResult.score,
                explanation: matchResult.explanation,
                compatibility_factors: matchResult.compatibility_factors,
                recommendations: matchResult.recommendations
              };

              const responseEnvelope = {
                version: 1,
                sender: "agent1qlovefi...",
                target: body.sender || '',
                session: body.session || '',
                schema_digest: "matching_response_schema",
                protocol_digest: null,
                payload: Buffer.from(JSON.stringify(responsePayload)).toString('base64'),
                expires: body.expires || 0,
                nonce: body.nonce || 0,
                signature: null
              };

              res.status(200).json(responseEnvelope);
            } else {
              res.status(200).json({
                status: "received",
                message: "Payload processed but no profiles found"
              });
            }
          } catch (parseError) {
            res.status(200).json({
              status: "received",
              message: "Could not parse payload",
              error: parseError.message
            });
          }
        } else {
          res.status(200).json({
            status: "POST received",
            message: "Submit endpoint working",
            received_data: Object.keys(body).length > 0,
            method: "POST"
          });
        }
      } else {
        res.status(200).json({
          status: "GET received",
          message: "Submit endpoint working",
          method: "GET"
        });
      }
    } else {
      res.status(404).json({
        status: "error",
        message: "Endpoint not found",
        available_endpoints: ["/", "/api", "/submit", "/api/submit"]
      });
    }
  } catch (error) {
    res.status(500).json({
      status: "error",
      message: error.message,
      endpoint: url,
      method: method
    });
  }
}

// Compatibility calculation function
function calculateCompatibility(profile1, profile2) {
  // Interest analysis
  const interests1 = profile1.interests || [];
  const interests2 = profile2.interests || [];
  const commonInterests = interests1.filter(i => interests2.includes(i));
  const totalInterests = [...new Set([...interests1, ...interests2])];
  const interestScore = totalInterests.length > 0 ? (commonInterests.length / totalInterests.length) * 100 : 0;

  // Age analysis
  const age1 = profile1.age || 25;
  const age2 = profile2.age || 25;
  const ageDiff = Math.abs(age1 - age2);
  let ageScore;
  let ageReason;
  
  if (ageDiff <= 2) {
    ageScore = 100;
    ageReason = "Very close in age - excellent life stage alignment";
  } else if (ageDiff <= 5) {
    ageScore = 80;
    ageReason = "Good age compatibility - similar life experiences";
  } else if (ageDiff <= 10) {
    ageScore = Math.max(20, 60 - (ageDiff - 5) * 8);
    ageReason = "Moderate age gap - some life stage differences";
  } else {
    ageScore = Math.max(10, 40 - (ageDiff - 10) * 2);
    ageReason = "Significant age gap - may have different priorities";
  }

  // Location analysis
  const loc1 = (profile1.location || '').toLowerCase();
  const loc2 = (profile2.location || '').toLowerCase();
  let locationScore;
  let locationReason;
  
  if (loc1 === loc2) {
    locationScore = 100;
    locationReason = "Same location - easy to meet";
  } else if (loc1.includes('new york') && loc2.includes('new york')) {
    locationScore = 80;
    locationReason = "Same metropolitan area - manageable distance";
  } else {
    locationScore = 20;
    locationReason = "Different regions - long-distance challenges";
  }

  // Calculate final weighted score
  const finalScore = Math.round(
    (interestScore * 0.5) + (ageScore * 0.25) + (locationScore * 0.25)
  );

  // Generate recommendations
  const recommendations = [];
  if (commonInterests.length > 0) {
    recommendations.push(`Plan activities around shared interests: ${commonInterests.slice(0, 3).join(', ')}`);
  }
  if (ageDiff <= 5) {
    recommendations.push("Your similar life stages create great potential for shared goals");
  } else {
    recommendations.push("Embrace the different perspectives your age difference brings");
  }
  if (locationScore >= 80) {
    recommendations.push("Being in the same area makes meeting up easy - suggest local date spots");
  }

  return {
    score: finalScore,
    explanation: `Compatibility Analysis:
• Age: ${ageReason} (Score: ${ageScore}/100)
• Interests: ${commonInterests.length} direct matches (Score: ${Math.round(interestScore)}/100)
• Location: ${locationReason} (Score: ${locationScore}/100)`,
    compatibility_factors: {
      age: { score: ageScore, reason: ageReason, age_difference: ageDiff },
      interests: { score: Math.round(interestScore), direct_matches: commonInterests.length, common_interests: commonInterests },
      location: { score: locationScore, reason: locationReason },
      overall_score: finalScore
    },
    recommendations: recommendations
  };
}
