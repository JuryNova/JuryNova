import logging
from typing import List, Dict, Any
from pathlib import Path
from fastapi import APIRouter, HTTPException
from langchain.chat_models import ChatVertexAI
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import GitLoader
from git import Repo
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from pydantic import BaseSettings

# Configuration class
class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "JuryNova"
    PROJECT_DIR: str = "./projects_source_code"

    class Config:
        env_file = ".env"

settings = Settings()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# MongoDB client
client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]

class CodeAnalyzer:
    def __init__(self, repo_link: str, project_id: str):
        self.repo_link = repo_link
        self.project_id = project_id
        self.project_dir = Path(settings.PROJECT_DIR) / project_id
        self.llm = ChatVertexAI()

    async def get_technologies(self) -> str:
        """Fetch technologies from hackathon collection."""
        try:
            hackathon = await db.hackathons.find_one({})
            return hackathon.get("technologies", "") if hackathon else ""
        except Exception as e:
            logger.error(f"Error fetching technologies: {e}")
            return ""

    def clone_repository(self) -> GitLoader:
        """Clone repository and return GitLoader instance."""
        try:
            repo = Repo.clone_from(self.repo_link, self.project_dir)
            return GitLoader(repo_path=str(self.project_dir), branch=repo.head.reference)
        except Exception as e:
            logger.error(f"Error cloning repository: {e}")
            raise HTTPException(status_code=500, detail="Failed to clone repository")

    def get_questions(self, technologies: str) -> List[str]:
            """Return list of structured questions for comprehensive code analysis.
            
            Args:
                technologies: str - Comma-separated list of technologies to check for
                
            Returns:
                List[str] - List of analysis questions
            """
            return [
                """Analyze the technologies and programming languages used in this project:
                1. What is the primary programming language?
                2. What frameworks or major libraries are being used?
                3. What build tools or package managers are present?""",

                """Provide a concise project analysis:
                1. What is the main purpose of this project?
                2. What are the key features or functionalities?
                3. How is the project structured (main components/modules)?""",

                """Evaluate the code quality based on these criteria:
                1. Code organization and architecture
                2. Documentation and comments
                3. Error handling and edge cases
                4. Coding standards and best practices
                5. Test coverage (if present)""",

                f"""Analyze the project's technology stack:
                1. Which of these specific technologies are used: {technologies}?
                2. How are they implemented in the project?
                3. Are there any missing dependencies or incomplete implementations?""",

                """Identify potential improvements:
                1. What are the main areas that need enhancement?
                2. Are there any security concerns?
                3. What scalability considerations should be addressed?"""
            ]

    async def analyze_code(self) -> List[Dict[str, str]]:
        """Perform code analysis and return results."""
        try:
            loader = self.clone_repository()
            index = VectorstoreIndexCreator().from_loaders([loader])
            technologies = await self.get_technologies()
            questions = self.get_questions(technologies)
            
            results = []
            for question in questions:
                response = index.query(question, self.llm)
                results.append({"question": question, "answer": response})

            await self.save_results(results)
            return results

        except Exception as e:
            logger.error(f"Error in code analysis: {e}")
            raise HTTPException(status_code=500, detail="Code analysis failed")
        finally:
            # Cleanup: Remove cloned repository
            if self.project_dir.exists():
                import shutil
                shutil.rmtree(self.project_dir)

    async def save_results(self, results: List[Dict[str, str]]) -> None:
        """Save analysis results to database."""
        try:
            query = {"_id": ObjectId(self.project_id)}
            update = {"$set": {"codeAgentAnalysis": results}}
            await db.projects.update_one(query, update)
            logger.info(f"Analysis results saved for project {self.project_id}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            raise HTTPException(status_code=500, detail="Failed to save analysis results")

@router.get("/code-agent")
async def code_agent_endpoint():
    """Health check endpoint."""
    return {"status": "operational", "service": "Code Agent"}

async def invoke_code_agent(repo_link: str, project_id: str) -> None:
    """Main function to invoke code analysis."""
    analyzer = CodeAnalyzer(repo_link, project_id)
    await analyzer.analyze_code()