from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import Settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException


app=FastAPI(title="Multi AI Agent")

logger=get_logger(__name__)

@app.get("/health")
def health_check():
    """Health check endpoint for ECS"""
    return {"status": "healthy", "service": "Multi AI Agent"}

class RequestState(BaseModel):
    model_name:str
    system_prompt:str
    messages:List[str]
    allow_search:bool

@app.post("/chat")
def chat_endpoint(request:RequestState):
    logger.info(f"Received request for model:{request.model_name}")
    
    if request.model_name not in Settings.ALLOWED_MODEL_NAMES:
        logger.warning(f"Model {request.model_name} is not allowed")
        raise HTTPException(status_code=400,detail="Invalid Model Name")

    try:
        response=get_response_from_ai_agents(
            request.model_name,
            request.messages,
            request.allow_search,
            request.system_prompt
        )

        logger.info(f"Successfully got response from AI Agents {request.model_name}")

        return {"response": response}

    except CustomException as e:
        logger.error(f"CustomException occurred: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        logger.error(f"Error occurred during response generation: {str(e)}")
        logger.error(f"Full traceback:\n{error_traceback}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get AI response: {str(e)}\n\nTraceback:\n{error_traceback}"

        )
