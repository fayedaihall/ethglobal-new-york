# LoveFi Dating Matcher Agent

A decentralized AI agent that calculates compatibility scores between dating profiles using the uAgents framework. This agent can be deployed on Vercel and integrated with Agentverse for seamless operation.

## 🚀 Features

- **Smart Compatibility Scoring**: Analyzes age difference, common interests, and location compatibility
- **Blockchain Integration**: Built on the Fetch.ai ecosystem using uAgents
- **Serverless Deployment**: Optimized for Vercel deployment
- **TypeScript Client**: Easy integration with existing applications
- **Pure uAgent Intelligence**: Advanced compatibility analysis using Fetch.ai's native uAgent framework

## 📁 Project Structure

```
lovefi-agents/
├── api/
│   └── index.py              # Vercel API endpoint
├── dating_matcher.py         # Main agent code
├── app.ts                   # TypeScript client
├── package.json             # Node.js dependencies
├── requirements.txt         # Python dependencies
├── vercel.json             # Vercel configuration
├── tsconfig.json           # TypeScript configuration
└── README.md               # This file
```

## 🛠️ Setup and Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- Vercel CLI (optional, for deployment)

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd lovefi-agents

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install
```

### 2. Configure the Agent

Update the configuration in `dating_matcher.py`:

```python
agent = Agent(
    name="dating_matcher",
    seed="your_secure_seed_phrase_here",  # Generate a secure seed
    port=8000,
    endpoint=["https://your-deployment.vercel.app/api/submit"],
)
```

### 3. Configure the TypeScript Client

Update the configuration in `app.ts`:

```typescript
const SEED_PHRASE = 'your_client_seed_phrase_here';
const TARGET_AGENT_ADDRESS = 'agent1q...'; // From agent logs
const TARGET_ENDPOINT = 'https://your-deployment.vercel.app/api/submit';
```

## 🚀 Deployment to Vercel

### Method 1: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow the prompts and note your deployment URL
```

### Method 2: GitHub Integration

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your GitHub repository
4. Vercel will automatically detect the configuration
5. Deploy and note the URL

### Environment Variables (Optional)

For enhanced logging and debugging, add these environment variables in Vercel:

```bash
AGENT_DEBUG=true
AGENT_LOG_LEVEL=info
```

## 🔧 Local Testing

### Test the Agent Locally

```bash
# Run the agent
python dating_matcher.py

# The agent will log its address, copy it for client configuration
```

### Test the TypeScript Client

```bash
# In a new terminal
npm run dev

# Or compile and run
npm run build
npm start
```

## 🤖 Agentverse Integration

### 1. Register with Agentverse

1. Go to [agentverse.ai](https://agentverse.ai)
2. Sign up with your Google account
3. Navigate to the dashboard

### 2. Add Your Agent

1. In Agentverse dashboard, go to "My Agents"
2. Click "Add Agent"
3. Provide your Vercel deployment URL
4. The system will discover your agent automatically

### 3. Get Mailbox Credentials

1. In Agentverse, go to "Mailbox"
2. Copy the mailbox credentials
3. Add them as environment variables in Vercel:
   ```
   AGENT_MAILBOX_KEY=your_mailbox_key
   ```

## 📋 API Usage

### Profile Format

```typescript
interface DatingProfile {
  age: number;
  interests: string[];
  location: string;
  name?: string;
  bio?: string;
}
```

### Example Request

```typescript
const profile1 = {
  age: 28,
  interests: ['hiking', 'reading', 'cooking'],
  location: 'New York'
};

const profile2 = {
  age: 30,
  interests: ['hiking', 'music', 'photography'],
  location: 'New York'
};

// Send to agent
await sendMatchingRequest(profile1, profile2, senderAddress, keyPair);
```

### Example Response

```json
{
  "score": 75.5,
  "explanation": "Age difference: 2 years (score: 16). Common interests: 1/5 (score: 10.0). Location match: Yes (score: 30)."
}
```

## 🔍 Enhanced uAgent Scoring Algorithm

The agent uses Fetch.ai's native intelligence to evaluate compatibility across multiple dimensions:

### **1. Age Compatibility Analysis (25% weight)**
- **Optimal Range**: 0-2 years difference (100% compatibility)
- **Good Range**: 3-5 years difference (80% compatibility)
- **Moderate Range**: 6-10 years difference (60-40% compatibility)
- **Significant Gap**: 10+ years (20% compatibility)
- **Life Stage Matching**: Evaluates career and life milestone alignment

### **2. Interest Compatibility Analysis (50% weight)**
- **Direct Matching**: Exact interest overlaps (2x weight)
- **Semantic Matching**: Category-based interest grouping
  - Outdoor: hiking, camping, cycling, etc.
  - Creative: art, music, photography, etc.
  - Intellectual: reading, science, philosophy, etc.
  - Social: networking, volunteering, community, etc.
  - Tech: programming, AI, blockchain, etc.
- **Jaccard Similarity**: Advanced overlap calculation

### **3. Location Compatibility Analysis (25% weight)**
- **Exact Match**: Same location (100% compatibility)
- **Same Metropolitan Area**: Major city matching (80% compatibility)
- **Same State/Region**: Long-distance viable (40% compatibility)
- **Different Regions**: Challenging but possible (10% compatibility)

### **4. AI-Powered Recommendations**
The agent generates personalized recommendations based on:
- Common interests for date planning
- Life stage compatibility insights
- Location-specific suggestions
- Relationship potential assessment

**Total Score**: Weighted combination yielding 0-100 compatibility score

## 🔐 Security Considerations

1. **Seed Phrases**: Use cryptographically secure seed phrases
2. **Environment Variables**: Store sensitive data in environment variables
3. **Rate Limiting**: Consider implementing rate limiting for production
4. **Input Validation**: Validate all incoming profile data

## 🛠️ Development

### Running Tests

```bash
# Test the TypeScript client
npm test

# Test the Python agent
python -m pytest tests/
```

### Adding New Features

1. Extend the `MatchingRequest` model in `dating_matcher.py`
2. Update the scoring algorithm
3. Update the TypeScript interfaces in `app.ts`
4. Test locally before deployment

## 📈 Monitoring and Logging

- Check Vercel function logs in the Vercel dashboard
- Monitor agent activity in Agentverse
- Use console logs in TypeScript for client-side debugging

## 🐛 Troubleshooting

### Common Issues

1. **Agent not responding**
   - Check Vercel deployment status
   - Verify endpoint URLs
   - Check environment variables

2. **TypeScript compilation errors**
   - Run `npm install` to ensure all dependencies
   - Check TypeScript version compatibility

3. **uAgent communication failures**
   - Verify agent addresses are correct
   - Check envelope formatting
   - Ensure signatures are properly generated

### Debug Commands

```bash
# Check Python environment
python --version
pip list | grep uagents

# Check Node.js environment
node --version
npm list

# Test Vercel deployment
curl https://your-deployment.vercel.app/api
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- [uAgents Documentation](https://docs.fetch.ai/uAgents)
- [Agentverse Support](https://agentverse.ai/support)
- [Vercel Documentation](https://vercel.com/docs)

---

Built with ❤️ for ETH Global New York 2025
