# JuryNova

JuryNova is a modern web application built with SvelteJS that streamlines hackathon project evaluation through AI-powered analysis and judging tools.

## Features

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

## Tech Stack

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

## Getting Started

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
