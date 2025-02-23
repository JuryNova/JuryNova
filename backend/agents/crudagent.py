from bson import ObjectId
from fastapi import APIRouter, Request, HTTPException
from pymongo import MongoClient
from typing import List, Dict, Any
from pydantic import BaseModel, HttpUrl
from agents.codeagent import invoke_code_agent
from agents.marketagent import invoke_market_agent
from annoy import AnnoyIndex
import cohere
import numpy as np
import pandas as pd
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Pydantic models for request validation
class ProjectCreate(BaseModel):
    shortDescription: str
    longDescription: str
    githubLink: HttpUrl
    theme: str

class HackathonCreate(BaseModel):
    name: str
    description: str
    startDate: str
    endDate: str

class ReviewUpdate(BaseModel):
    project_id: str
    isReviewed: bool

class SearchQuery(BaseModel):
    query: str

# Configuration
router = APIRouter()
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
client = MongoClient(MONGODB_URL)
db = client["JuryNova"]
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

@router.get("/crud-agent")
async def crud_agent_endpoint() -> Dict[str, str]:
    """Health check endpoint"""
    return {"message": "Crud Agent service is running"}

@router.post("/create-project")
async def create_project(project: ProjectCreate) -> Dict[str, str]:
    """Create a new project and trigger related agents"""
    try:
        project_dict = project.dict()
        project_dict["isReviewed"] = False
        
        new_project = db.projects.insert_one(project_dict)
        project_id = str(new_project.inserted_id)

        # Launch async tasks
        asyncio.create_task(invoke_market_agent(project_id, project.shortDescription))
        asyncio.create_task(invoke_code_agent(str(project.githubLink), project_id))
        
        return {"message": "Project created", "project_id": project_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-project/{project_id}")
async def get_project(project_id: str) -> Dict[str, Any]:
    """Retrieve a specific project by ID
    
    Args:
        project_id (str): The unique identifier of the project
        
    Returns:
        Dict[str, Any]: Dictionary containing project details and success message
        
    Raises:
        HTTPException: 404 if project not found, 400 if invalid ID format, 500 for server errors
    """
    try:
        if not ObjectId.is_valid(project_id):
            raise HTTPException(status_code=400, detail="Invalid project ID format")
            
        project = db.projects.find_one({"_id": ObjectId(project_id)})
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        project["_id"] = str(project["_id"])
        return {"message": "successful", "project": project}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.get("/get-all")
async def get_all_projects() -> Dict[str, Any]:
    """Retrieve all projects in reverse chronological order
    
    Returns:
        Dict[str, Any]: Dictionary containing list of projects and success message
        
    Raises:
        HTTPException: 500 for server errors
    """
    try:
        projects = list(db.projects.find({}).sort("_id", -1))  # Sort by _id desc
        for project in projects:
            project["_id"] = str(project["_id"])
        return {"message": "successful", "projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.post("/search")
async def search_projects(query: SearchQuery) -> Dict[str, Any]:
    """Search projects using semantic similarity"""
    try:
        # Fetch all projects
        projects = list(db.projects.find({}))
        for project in projects:
            project["_id"] = str(project["_id"])

        # Create document embeddings
        docs = [f"Project Description: {p['longDescription']} Hackathon Theme: {p['theme']}" 
               for p in projects]

        # Generate embeddings using Cohere
        embeds = cohere_client.embed(
            texts=docs,
            model="large",
            truncate="RIGHT"
        ).embeddings

        # Build search index
        search_index = AnnoyIndex(len(embeds[0]), 'angular')
        for i, embed in enumerate(embeds):
            search_index.add_item(i, embed)
        search_index.build(10)

        # Search for similar projects
        query_embed = cohere_client.embed(
            texts=[query.query],
            model="large",
            truncate="RIGHT"
        ).embeddings

        similar_indices, _ = search_index.get_nns_by_vector(
            query_embed[0], 
            10, 
            include_distances=True
        )
        
        similar_projects = [projects[i] for i in similar_indices]
        return {"message": "successful", "projects": similar_projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))