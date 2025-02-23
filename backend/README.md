# JuryNova - Backend

#### REVOLUTIONIZING HACKATHON JUDGING WITH AI-AGENTS

<div align="center">
  
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![ElevenLabs](https://img.shields.io/badge/Built_with-ElevenLabs-7C3AED)](https://elevenlabs.io)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-green.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

## 🎯 What is JuryNova?

JuryNova is an innovative AI-powered platform that transforms the hackathon judging experience. By combining advanced language models with specialized agents, it provides comprehensive project analysis, market insights, and interactive evaluation capabilities - making the judging process more efficient, objective, and scalable.

## 🤖 How does it work?

JuryNova leverages LangChain, Google Vertex AI, and Mistral to power its intelligent agents:

### 1. 🔍 Market Research Agent
- Conducts thorough market analysis
- Evaluates target market size and potential
- Identifies competitive advantages
- Assesses business viability

### 2. 💻 Code Analysis Agent
- Performs deep code review
- Validates technology stack
- Ensures hackathon compliance
- Evaluates code quality metrics

### 3. 💬 Chat Agent
- Enables interactive Q&A
- Provides contextual responses
- Combines insights from all agents
- Offers voice-enabled interactions

### 4. 🎯 Search Agent
- Enables semantic search
- Processes natural language queries
- Ranks submissions by relevance
- Facilitates quick navigation

## 🛠️ Technologies Used

- **Framework:** FlaskAPI
- **Database:** MongoDB
- **AI Models:**
  - Google Vertex AI
  - Mistral LLM
  - LangChain
- **Voice:** ElevenLabs

## ⚡ Quick Setup

```bash
# Clone repository
git clone https://github.com/JuryNova/JuryNova.git

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
echo GOOGLE_APPLICATION_CREDENTIALS=path/to/service-worker.json > .env
echo ELEVENLABS_API_KEY=your_key_here >> .env
echo MISTRAL_API_KEY=your_key_here >> .env

# Start server
python server.py
```

Server runs at `http://localhost:8000` 🚀

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Google Vertex AI
Mistral AI
ElevenLabs
MongoDB
