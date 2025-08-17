import express from "express";
import fetch from "node-fetch";
import * as nacl from "tweetnacl";
import * as naclUtil from "tweetnacl-util";
import * as bip39 from "bip39";
import { bech32 } from "bech32";
import { sha256 } from "@cosmjs/crypto";
import { toBech32 } from "@cosmjs/encoding";
import { v4 as uuidv4 } from "uuid";

const app = express();
app.use(express.json());

const PORT = 8001; // Your local port for receiving responses
const ENDPOINT = `http://localhost:${PORT}/submit`; // Your endpoint

// Configuration - Update these with your actual values
const SEED_PHRASE = "your_client_seed_phrase_replace_with_secure_seed"; // Replace with secure seed
const TARGET_AGENT_ADDRESS = "agent1qlovefi..."; // Replace with deployed agent's address
const TARGET_ENDPOINT = "https://ethglobal-new-york.vercel.app/api/submit"; // Replace with Vercel deployment URL

// Interface definitions
interface DatingProfile {
  age: number;
  interests: string[];
  location: string;
  name?: string;
  bio?: string;
}

interface MatchingRequest {
  profile1: DatingProfile;
  profile2: DatingProfile;
}

interface MatchingResponse {
  score: number;
  explanation: string;
  compatibility_factors: {
    age: {
      age_difference: number;
      compatibility_score: number;
      reason: string;
      life_stage_match: boolean;
    };
    interests: {
      direct_matches: number;
      semantic_matches: number;
      total_interests: number;
      common_categories: string[];
      compatibility_score: number;
    };
    location: {
      match_type: string;
      compatibility_score: number;
      reason: string;
    };
    overall_score: number;
  };
  recommendations: string[];
}

interface AgentEnvelope {
  version: number;
  sender: string;
  target: string;
  session: string;
  schema_digest: string;
  protocol_digest?: string;
  payload: string;
  expires: number;
  nonce: number;
  signature?: string;
}

// Generate sender identity from seed
async function generateSenderIdentity() {
  const seed = await bip39.mnemonicToSeed(SEED_PHRASE);
  const keyPair = nacl.sign.keyPair.fromSeed(seed.slice(0, 32));
  const publicKey = keyPair.publicKey;

  // Generate Bech32 address with 'agent1' prefix
  const addressPrefix = "agent1";
  const pubKeyHash = sha256(publicKey).slice(0, 20);
  const senderAddress = toBech32(addressPrefix, pubKeyHash);

  return { keyPair, senderAddress };
}

// Create and sign envelope for uAgent communication
function createEnvelope(
  senderAddress: string,
  keyPair: nacl.SignKeyPair,
  target: string,
  payload: object,
  schemaDigest: string
): AgentEnvelope {
  const envelope: AgentEnvelope = {
    version: 1,
    sender: senderAddress,
    target: target,
    session: uuidv4(),
    schema_digest: schemaDigest,
    protocol_digest: undefined,
    payload: naclUtil.encodeBase64(
      new TextEncoder().encode(JSON.stringify(payload))
    ),
    expires: Math.floor(Date.now() / 1000) + 3600, // 1 hour
    nonce: Math.floor(Math.random() * 1000000),
  };

  // Sign the envelope (optional but recommended)
  const messageToSign = JSON.stringify({ ...envelope, signature: null });
  const digest = sha256(new TextEncoder().encode(messageToSign));
  const signatureBytes = nacl.sign.detached(digest, keyPair.secretKey);

  // Convert signature to bech32 format
  const words = bech32.toWords(signatureBytes);
  envelope.signature = bech32.encode("agent1", words);

  return envelope;
}

// Send matching request to agent
async function sendMatchingRequest(
  profile1: DatingProfile,
  profile2: DatingProfile,
  senderAddress: string,
  keyPair: nacl.SignKeyPair
): Promise<void> {
  const payload: MatchingRequest = { profile1, profile2 };
  const schemaDigest = "matching_request_schema"; // Custom schema identifier
  const envelope = createEnvelope(
    senderAddress,
    keyPair,
    TARGET_AGENT_ADDRESS,
    payload,
    schemaDigest
  );

  try {
    console.log("Sending matching request...");
    console.log("Profile 1:", profile1);
    console.log("Profile 2:", profile2);

    const response = await fetch(TARGET_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(envelope),
    });

    if (response.ok) {
      console.log("✅ Request sent successfully");
      console.log("Response status:", response.status);
    } else {
      console.error("❌ Error sending request:", response.status);
      const errorText = await response.text();
      console.error("Error details:", errorText);
    }
  } catch (error) {
    console.error("❌ Fetch error:", error);
  }
}

// Handler for incoming responses from agent
app.post("/submit", async (req, res) => {
  try {
    const envelope: AgentEnvelope = req.body;
    console.log("📨 Received envelope from:", envelope.sender);

    if (envelope.sender === TARGET_AGENT_ADDRESS && envelope.payload) {
      // Decode the payload
      const decodedBytes = naclUtil.decodeBase64(envelope.payload);
      const payloadStr = new TextDecoder().decode(decodedBytes);
      const response: MatchingResponse = JSON.parse(payloadStr);

      console.log("\n🎯 DETAILED MATCHING RESULTS:");
      console.log("=".repeat(50));
      console.log(
        `📊 Overall Compatibility Score: ${response.score.toFixed(1)}/100\n`
      );

      // Display compatibility factors breakdown
      const factors = response.compatibility_factors;
      console.log("🔍 DETAILED ANALYSIS:");
      console.log(
        `👥 Age Compatibility: ${(
          factors.age.compatibility_score * 100
        ).toFixed(0)}/100`
      );
      console.log(`   └─ ${factors.age.reason}`);
      console.log(
        `   └─ Age difference: ${factors.age.age_difference} years\n`
      );

      console.log(
        `❤️  Interest Compatibility: ${(
          factors.interests.compatibility_score * 100
        ).toFixed(0)}/100`
      );
      console.log(`   └─ Direct matches: ${factors.interests.direct_matches}`);
      console.log(
        `   └─ Semantic matches: ${factors.interests.semantic_matches}`
      );
      console.log(
        `   └─ Common categories: ${
          factors.interests.common_categories.join(", ") || "None"
        }\n`
      );

      console.log(
        `📍 Location Compatibility: ${(
          factors.location.compatibility_score * 100
        ).toFixed(0)}/100`
      );
      console.log(`   └─ ${factors.location.reason}`);
      console.log(`   └─ Match type: ${factors.location.match_type}\n`);

      // Display personalized recommendations
      if (response.recommendations && response.recommendations.length > 0) {
        console.log("💡 PERSONALIZED RECOMMENDATIONS:");
        response.recommendations.forEach((rec, index) => {
          console.log(`${index + 1}. ${rec}`);
        });
        console.log("");
      }

      console.log("=".repeat(50));

      // Here you can integrate with your app logic
      // For example, save to database, notify users, etc.
      const detailedResult = {
        status: "processed",
        score: response.score,
        compatibility_breakdown: {
          age_score: factors.age.compatibility_score * 100,
          interests_score: factors.interests.compatibility_score * 100,
          location_score: factors.location.compatibility_score * 100,
        },
        recommendations: response.recommendations,
        match_quality:
          response.score >= 75
            ? "Excellent"
            : response.score >= 60
            ? "Good"
            : response.score >= 40
            ? "Moderate"
            : "Low",
      };

      res.status(200).json(detailedResult);
    } else {
      console.log("📋 General message received");
      res.status(200).json({ status: "received" });
    }
  } catch (error) {
    console.error("❌ Error processing response:", error);
    res.status(500).json({ error: "Processing failed" });
  }
});

// Health check endpoint
app.get("/", (req, res) => {
  res.json({
    status: "LoveFi Client Running",
    port: PORT,
    endpoint: ENDPOINT,
  });
});

// Example usage function
async function runExample() {
  try {
    const { keyPair, senderAddress } = await generateSenderIdentity();
    console.log(`🚀 Client address: ${senderAddress}`);

    // Example dating profiles
    const profile1: DatingProfile = {
      age: 28,
      interests: ["hiking", "reading", "cooking", "travel"],
      location: "New York",
      name: "Alice",
      bio: "Love exploring new places and trying new cuisines!",
    };

    const profile2: DatingProfile = {
      age: 30,
      interests: ["hiking", "music", "cooking", "photography"],
      location: "New York",
      name: "Bob",
      bio: "Outdoor enthusiast and music lover",
    };

    // Send matching request
    await sendMatchingRequest(profile1, profile2, senderAddress, keyPair);
  } catch (error) {
    console.error("❌ Example execution failed:", error);
  }
}

// Start server
app.listen(PORT, () => {
  console.log(`🔥 LoveFi Client server listening on port ${PORT}`);
  console.log(`📡 Endpoint: ${ENDPOINT}`);
  console.log("📋 Update the following values in the code:");
  console.log(`   - SEED_PHRASE: Generate a secure seed phrase`);
  console.log(`   - TARGET_AGENT_ADDRESS: Your deployed agent's address`);
  console.log(`   - TARGET_ENDPOINT: Your Vercel deployment URL + /api/submit`);
  console.log("");

  // Run example after a short delay to ensure server is ready
  setTimeout(() => {
    console.log("🎯 Running example matching request...");
    runExample();
  }, 2000);
});

// Export for use in other modules
export {
  sendMatchingRequest,
  generateSenderIdentity,
  DatingProfile,
  MatchingRequest,
  MatchingResponse,
};
