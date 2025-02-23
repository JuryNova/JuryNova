from typing import Dict, List, Optional
from fastapi import APIRouter, Request
from bson import ObjectId
from pymongo import MongoClient
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatVertexAI
from langchain.memory import VectorStoreRetrieverMemory
from elevenlabs import generate, set_api_key
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Constants
MONGODB_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "JuryNova"
# ...existing code...

DEFAULT_TEMPLATE = """You are an expert hackathon judge and technical analyst with deep experience in market research and code review.

Context for evaluation:
- Project Description: {project_desc}
- Hackathon Theme: {theme}
- Required Technologies: {technologies}

Previous conversation context:
{history}

Guidelines for your response:
1. Provide data-driven insights when discussing market potential
2. Evaluate technical implementation and code quality when relevant
3. Consider alignment with hackathon theme and required technologies
4. Keep responses clear, concise, and under 70 words
5. Format as a single, well-structured paragraph
6. Base technical feedback on the complete project codebase

Current question:
Human: {input}
AI: """



class ChatAgent:
    def __init__(self):
        self.client = MongoClient(MONGODB_URL)
        self.db = self.client[DATABASE_NAME]
        self.llm = ChatVertexAI()
        # Initialize ElevenLabs
        set_api_key(os.getenv("ELEVENLABS_API_KEY"))
        
    def get_hackathon_info(self) -> tuple[str, str, bool]:
        hackathon = next(self.db.hackathons.find(), {})
        return (
            hackathon.get("technologies", ""),
            hackathon.get("theme", ""),
            hackathon.get("isAllowed", False)
        )
    
    def get_project_info(self, project_id: str) -> Optional[Dict]:
        return self.db.projects.find_one({"_id": ObjectId(project_id)})
    
    def setup_memory(self, project_id: str, project_desc: str, theme: str, technologies: str):
        directory = f"projects_source_code/{project_id}"
        loader = DirectoryLoader(directory, silent_errors=True)
        index = VectorstoreIndexCreator().from_loaders([loader])
        retriever = index.vectorstore.as_retriever()
        memory = VectorStoreRetrieverMemory(retriever=retriever)
        
        # Save context
        memory.save_context({"input": f"Idea : {project_desc}"}, {"output": "..."})
        memory.save_context({"input": f"Theme for the Hackathon : {theme}"}, {"output": "..."})
        memory.save_context(
            {"input": f"Technologies that must be used for the hackathon project : {technologies}"}, 
            {"output": "..."}
        )
        
        return memory
    
    # ...existing code...

async def process_chat(self, request_data: Dict) -> Dict:
    technologies, theme, is_allowed = self.get_hackathon_info()
        
    if not is_allowed:
        return {"answer": "Sorry, We have reached our credit limit.", "chathistory": [], "audio": None}
        
    project = self.get_project_info(request_data["project_id"])
    if not project:
        return {"answer": "Project not found.", "chathistory": [], "audio": None}
        
        
    memory = self.setup_memory(
        request_data["project_id"],
        project["shortDescription"],
        theme,
        technologies
    )
    
    prompt = PromptTemplate(
        input_variables=["history", "input", "project_desc", "theme", "technologies"], 
        template=DEFAULT_TEMPLATE
    )
    
    conversation = ConversationChain(
        llm=self.llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )
    
    try:
        audio = generate(
            text=ai_response,
            voice="Rachel",  # You can change this to any available voice
            model="eleven_monolingual_v1"
        )
    except Exception as e:
        print(f"Error generating audio: {e}")
        audio = None
    
    chat_history = request_data["chathistory"]
    chat_history.append({
        "input": request_data["question"], 
        "output": ai_response
    })
    
    return {
        "answer": ai_response,
        "chathistory": chat_history,
        "audio": audio  # This will be binary audio data
    }