import asyncio
from fastapi import APIRouter, HTTPException
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.tools import DuckDuckGoSearchRun
from langchain.llms import VertexAI
from pymongo import MongoClient
from bson.objectid import ObjectId
import vertexai
from vertexai.language_models import TextGenerationModel
from typing import List, Dict
from pydantic import BaseModel

# Constants
MONGODB_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "JuryNova"
PROJECT_ID = "lofty-bolt-383703"
LOCATION = "us-central1"
MODEL_NAME = "text-bison@001"

# Model definitions
class MarketAnalysis(BaseModel):
    question: str
    answer: str

# Configuration
router = APIRouter()
client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]

# Vertex AI parameters
GENERATION_PARAMS = {
    "temperature": 0.2,
    "max_output_tokens": 1000,
    "top_p": 0.8,
    "top_k": 40
}

MARKET_QUESTIONS = [
    "Who is the target audience of this idea?",
    "What is the potential of this idea?",
    "What is the market size of this idea?",
    "What are the pitfalls of this idea?",
    "Are there any platforms like the idea, that already exist?"
]

@router.get("/market-agent")
async def marketagent_endpoint():
    await asyncio.sleep(5)
    return {"message": "Hello from Market Agent"}

async def get_hackathon_details() -> tuple:
    """Fetch hackathon details from database."""
    hackathon = db.hackathons.find_one()
    if not hackathon:
        raise HTTPException(status_code=404, message="No hackathon found")
    return hackathon.get("technologies", []), hackathon.get("theme", "")

async def get_market_analysis(llm: VertexAI, search_tool: DuckDuckGoSearchRun, idea: str) -> List[MarketAnalysis]:
    """Generate market analysis for the given idea."""
    tools = [Tool(
        name="Intermediate Answer",
        func=search_tool.run,
        description="useful for when you need to ask with search",
    )]
    
    agent = initialize_agent(tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True)
    
    async def analyze_question(question: str) -> str:
            prompt = """
            You are an experienced market research analyst with expertise in technology and innovation.
            
            IDEA TO ANALYZE: {idea}
            SPECIFIC QUESTION: {question}
            
            Analysis Guidelines:
            1. Provide data-driven insights and market statistics where applicable
            2. Consider market trends, competition, and growth potential
            3. Focus on actionable insights and concrete market opportunities
            4. Include relevant market size figures or growth rates if available
            5. Address potential risks and challenges objectively
            
            Response Requirements:
            - Keep response to one concise paragraph (maximum 70 words)
            - Be specific and quantitative where possible
            - Maintain a professional, analytical tone
            - Focus on factual market insights rather than opinions
            - Avoid any marketing language or hype
            
            Provide your market analysis:
            """.format(question=question, idea=idea)
            return agent.run(prompt)

    analyses = []
    for question in MARKET_QUESTIONS:
        answer = await analyze_question(question)
        analyses.append(MarketAnalysis(question=question, answer=answer))
    
    return analyses

async def get_theme_match(model: TextGenerationModel, idea: str, theme: str) -> str:
    """Determine the matching theme for the idea."""
    theme_prompt = """
    Themes : {theme}
    Idea: {idea}
    Task : To which of the above themes does the idea belong to?
    Rules: 
    1. The theme must be from the above list
    2. Just give the matched theme and nothing more.
    3. If the idea does not match any of the themes, just say "None"
    """.format(theme=theme, idea=idea)
    
    response = await model.predict(theme_prompt, **GENERATION_PARAMS)
    return response.text

async def invoke_market_agent(project_id: str, idea: str):
    """Main function to analyze market potential and theme matching."""
    try:
        # Initialize Vertex AI
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        
        # Get hackathon details
        technologies, theme = await get_hackathon_details()
        
        # Initialize tools
        llm = VertexAI()
        search_tool = DuckDuckGoSearchRun()
        
        # Get market analysis
        market_analysis = await get_market_analysis(llm, search_tool, idea)
        
        # Get theme matching
        model = TextGenerationModel.from_pretrained(MODEL_NAME)
        final_theme = await get_theme_match(model, idea, theme)
        
        # Update database
        query = {"_id": ObjectId(project_id)}
        newvalues = {
            "$set": {
                "marketAgentAnalysis": [analysis.dict() for analysis in market_analysis],
                "theme": final_theme
            }
        }
        
        result = db.projects.update_one(query, newvalues)
        if not result.modified_count:
            raise HTTPException(status_code=404, message=f"Project {project_id} not found")
        
        print("Market Agent: Task Complete")
        
    except Exception as e:
        print(f"Error in market agent: {str(e)}")
        raise HTTPException(status_code=500, message=str(e))