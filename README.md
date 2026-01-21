# Multi-AI Agent System

A production-ready, full-stack AI agent platform that integrates multiple Large Language Models with real-time web search capabilities. Built with modern Python frameworks, this system enables dynamic AI agent creation with customizable system prompts, model selection, and optional web search integration.

## Overview

The Multi-AI Agent System is an enterprise-grade application that provides a unified interface for interacting with multiple AI models through a sophisticated agent architecture. The system leverages LangGraph's ReAct agent pattern to create intelligent agents capable of reasoning, tool usage, and dynamic response generation. Users can define custom AI agents with specific roles and behaviors, select from multiple LLM providers, and enable real-time web search to enhance response accuracy and relevance.

The platform follows a microservices architecture with clear separation between frontend presentation, b`ackend API services, and core AI agent logic. It implements comprehensive error handling, logging, and process management to ensure reliability and observability in production environments.

## Architecture

The system is organized into three primary layers:

**Frontend Layer**: Streamlit-based web interface providing an intuitive user experience for agent configuration and interaction. The frontend handles user input, model selection, system prompt definition, and displays formatted agent responses.

**Backend Layer**: FastAPI REST API serving as the communication bridge between frontend and AI services. Implements request validation, model authorization, error handling, and response formatting. The API follows RESTful principles with proper HTTP status codes and detailed error messages.

**Core Layer**: LangGraph-powered AI agent engine that orchestrates LLM interactions, tool execution, and state management. Implements the ReAct (Reasoning and Acting) pattern, allowing agents to reason about queries, decide when to use tools, and generate contextual responses. The core layer supports multiple LLM providers through LangChain abstractions and integrates Tavily search for real-time information retrieval.

**Infrastructure**: The system includes comprehensive logging infrastructure, custom exception handling with detailed error tracking, environment-based configuration management, and graceful process lifecycle management for concurrent service execution.

## Technical Depth

**Agent Architecture**: The system implements LangGraph's prebuilt ReAct agent executor, which provides a sophisticated state machine for agent reasoning cycles. Agents maintain conversation state, execute tool calls conditionally, and generate responses based on accumulated context. The architecture supports dynamic tool registration, allowing agents to seamlessly integrate web search capabilities when enabled.

**Model Integration**: Multi-provider LLM support through LangChain's unified interface. Currently integrated with Groq's high-performance inference API, supporting models including Llama 3.3 70B, Llama 3.1 variants, Mixtral, and Gemma. The system includes model validation, deprecation detection, and automatic error handling for API-level issues.

**Tool System**: Conditional tool integration using Tavily Search API for real-time web information retrieval. Tools are dynamically registered based on user preferences, allowing agents to access current information when needed. The tool system follows LangChain's tool interface standards, ensuring compatibility with the broader ecosystem.

**Error Handling**: Multi-tier error handling strategy including API-level error detection, custom exception types with detailed context, comprehensive logging at all layers, and user-friendly error messages. The system distinguishes between client errors (400) and server errors (500), providing appropriate feedback for debugging and user experience.

**Process Management**: Sophisticated process orchestration using Python's subprocess and threading modules. Implements daemon threads for background services, signal handlers for graceful shutdown, process health monitoring, and coordinated service lifecycle management.

**Configuration Management**: Environment-based configuration using python-dotenv for secure credential management. Centralized settings class for model whitelisting, API key management, and runtime configuration. Supports development and production environment variations.

## Technology Stack

**Core Framework**: Python 3.13

**AI/ML Stack**:
- LangChain: Agent orchestration and LLM abstraction layer
- LangGraph: State machine and agent execution engine
- LangChain Groq: Groq API integration for high-performance inference
- LangChain Tavily: Web search tool integration

**Backend Stack**:
- FastAPI: Modern, high-performance web framework for building APIs
- Uvicorn: ASGI server for async request handling
- Pydantic: Data validation and settings management
- Python-dotenv: Environment variable management

**Frontend Stack**:
- Streamlit: Rapid web application development framework
- Requests: HTTP client for API communication

**Infrastructure**:
- Threading: Concurrent service execution
- Subprocess: Process lifecycle management
- Logging: Comprehensive application logging
- Pathlib: Modern path handling

**Development Tools**:
- Virtual Environment: Isolated dependency management
- Setup.py: Package configuration and distribution

## Key Features

- Dynamic AI agent creation with customizable system prompts
- Multi-model support with automatic model validation
- Optional real-time web search integration
- RESTful API with comprehensive error handling
- Production-ready logging and monitoring
- Graceful service lifecycle management
- Environment-based configuration
- Type-safe request/response validation

## Project Structure

```
Multi-AI Agent/
├── app/
│   ├── backend/          # FastAPI REST API
│   ├── frontend/         # Streamlit web interface
│   ├── core/             # AI agent engine
│   ├── common/           # Shared utilities (logging, exceptions)
│   ├── config/           # Configuration management
│   └── main.py           # Application entry point
├── logs/                 # Application logs
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Getting Started

1. Clone the repository and navigate to the project directory
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with required API keys:
   ```
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```
6. Run the application: `python -m app.main`

The system will start the backend API on `http://127.0.0.1:9999` and the frontend interface will be accessible through Streamlit's default port.

## API Endpoints

**POST /chat**: Main chat endpoint accepting JSON payload with:
- `model_name`: Selected LLM model identifier
- `system_prompt`: Custom agent behavior definition
- `messages`: Array of user messages
- `allow_search`: Boolean flag for web search enablement

Returns JSON response with agent-generated content.

## Error Handling

The system implements comprehensive error handling:
- Model validation and deprecation detection
- API error translation to user-friendly messages
- Detailed logging for debugging
- Proper HTTP status codes (400 for client errors, 500 for server errors)

## License

This project is available for demonstration and portfolio purposes.

