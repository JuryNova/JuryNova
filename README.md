
# JuryNova

Revolutionizing Hackathon Judging with AI-Powered Insights

<div align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python"></a>
  <a href="https://elevenlabs.io"><img src="https://img.shields.io/badge/Built_with-ElevenLabs-7C3AED" alt="ElevenLabs"></a>
  <a href="https://www.mongodb.com/"><img src="https://img.shields.io/badge/MongoDB-4.4+-green.svg" alt="MongoDB"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
</div>

---

## ElevenLabs x A16z Worldwide Hackathon

This project was developed as part of the ElevenLabs x A16z worldwide hackathon, aiming to push the boundaries of AI and technology in hackathon judging.

---

## 🎯 What is JuryNova?

JuryNova is an innovative AI-powered platform that transforms the hackathon judging experience. By combining advanced language models with specialized agents, it provides comprehensive project analysis and fair evaluations.

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
.\\venv\\Scripts\\activate

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

## 🙌 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Vertex AI
- Mistral AI
- ElevenLabs
- MongoDB

---

## ElevenLabs x A16z Worldwide Hackathon

This project was developed as part of the ElevenLabs x A16z worldwide hackathon, aiming to push the boundaries of AI and technology in hackathon judging. Join us in revolutionizing the way hackathons are judged!

---

## Frontend

JuryNova is a modern web application built with SvelteJS that streamlines hackathon project evaluation through AI-powered analysis and judging tools.

### Features

- **AI-Powered Project Analysis**
  - Market research analysis
  - Code quality assessment
  - Interactive AI chat assistant
  - Natural language search capabilities

- **Project Management**
  - Add individual projects manually
  - Bulk import projects via CSV
  - Track reviewed/unreviewed status
  - Detailed project insights

- **Configurable Platform**
  - Set hackathon themes
  - Define required technologies
  - Customize evaluation criteria

### Tech Stack

- **Frontend**
  - SvelteJS
  - TailwindCSS + DaisyUI
  - Svelte SPA Router
  - Axios for API calls
  - PapaParse for CSV handling

- **Key Dependencies**
  - `svelte-french-toast` - Toast notifications
  - `svelte-typewriter` - Text animation effects
  - `svelte-spa-router` - Client-side routing
  - `ordinal` - Number formatting

### Getting Started

1. Clone the repository
```sh
git clone https://github.com/JuryNova/JuryNova.git

Install dependencies
npm install

Configure environment variables Create a .env file:
VITE_BASEURL=http://localhost:8000/api

Start development server
npm run dev

Project Structure
src/
├── components/           # Reusable UI components
├── pages/               # Route pages
├── store/              # State management
└── routes.js           # Route definitions

Building for Production
npm run build

Contributing
Fork the repository
Create a feature branch
Make your changes
Submit a pull request

License
MIT License

Acknowledgments
SvelteJS
TailwindCSS
DaisyUI
```

