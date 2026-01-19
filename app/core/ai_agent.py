from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from app.config.settings import Settings
from app.common.custom_exception import CustomException
from app.common.logger import get_logger
import traceback
import groq

logger = get_logger(__name__)


def get_response_from_ai_agents(llm_id,query,allow_search,system_prompt):
    try:
        logger.info(f"Creating LLM with model: {llm_id}")
    llm= ChatGroq(model=llm_id)  #this llm id is basically the type of model we are using to generate the response

        logger.info(f"Setting up tools, allow_search: {allow_search}")
        tools=[TavilySearch(max_results=2)] if allow_search else []   #allow_search is a boolean value that tells us whether we want to use the search tool or not

        logger.info("Creating react agent...")
    agent=create_react_agent(
        model=llm,
        tools=tools,
            prompt=system_prompt if system_prompt else None,
        )

        # Convert string messages to HumanMessage objects
        logger.info(f"Converting {len(query)} messages to HumanMessage objects")
        messages = [HumanMessage(content=msg) for msg in query]
        state={"messages": messages}
        
        logger.info("Invoking agent...")
    response=agent.invoke(state)
        logger.info("Agent invocation completed")
        
    messages=response.get("messages")
        logger.info(f"Got {len(messages)} messages from response")

    ai_messages=[message.content for message in messages if isinstance(message,AIMessage) ]
        logger.info(f"Found {len(ai_messages)} AI messages")

        if not ai_messages:
            raise CustomException("No AI response generated from agent", error_detail=None)

    return ai_messages[-1]
    
    except groq.BadRequestError as e:
        # Handle Groq API errors (like model decommissioned)
        error_msg = str(e)
        if "decommissioned" in error_msg.lower() or "model_decommissioned" in error_msg:
            logger.error(f"Model {llm_id} has been decommissioned by Groq")
            raise CustomException(
                f"The model '{llm_id}' has been decommissioned and is no longer available. "
                f"Please select a different model from the available options. "
                f"See https://console.groq.com/docs/deprecations for more information.",
                error_detail=e
            )
        else:
            logger.error(f"Groq API error: {error_msg}")
            raise CustomException(f"Groq API error: {error_msg}", error_detail=e)
    except Exception as e:
        error_traceback = traceback.format_exc()
        logger.error(f"Error in get_response_from_ai_agents: {str(e)}")
        logger.error(f"Full traceback:\n{error_traceback}")
        raise