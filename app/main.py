import subprocess
import threading
import time
import os
import signal
import sys
from pathlib import Path
from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger=get_logger(__name__)

load_dotenv()

backend_process = None
frontend_process = None

def run_backend():
    global backend_process
    try:
        logger.info("Starting backend service")
        # Get project root directory (parent of 'app' directory)
        project_root = Path(__file__).parent.parent
        # Set PYTHONPATH to include project root
        env = os.environ.copy()
        env['PYTHONPATH'] = str(project_root) + (os.pathsep + env.get('PYTHONPATH', ''))
        backend_process = subprocess.Popen(
            ["uvicorn","app.backend.api:app","--host","127.0.0.1","--port","9999"],
            env=env,
            cwd=str(project_root)
        )
        backend_process.wait()
    except Exception as e:
        logger.error(f"Problem with Backend Service: {str(e)}")
        logger.exception(e)

def run_frontend():
    global frontend_process
    try:
        logger.info("Starting Frontend Service")
        project_root = Path(__file__).parent.parent
        env = os.environ.copy()
        env['PYTHONPATH'] = str(project_root) + (os.pathsep + env.get('PYTHONPATH', ''))
        frontend_process = subprocess.Popen(
            ["streamlit","run","app/frontend/ui.py"],
            env=env,
            cwd=str(project_root)
        )
        frontend_process.wait()
    except Exception as e:
        logger.error(f"Problem with frontend service: {str(e)}")
        logger.exception(e)

def signal_handler(sig, frame):
    logger.info("Shutting down services...")
    if backend_process:
        logger.info("Stopping backend...")
        backend_process.terminate()
        backend_process.wait()
    if frontend_process:
        logger.info("Stopping frontend...")
        frontend_process.terminate()
        frontend_process.wait()
    logger.info("Shutdown complete")
    sys.exit(0)

if __name__=="__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start backend in a daemon thread
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Wait a bit for backend to start
        logger.info("Waiting for backend to start...")
        time.sleep(3)
        
        # Check if backend is still running
        if backend_process and backend_process.poll() is not None:
            logger.error("Backend process exited unexpectedly")
            sys.exit(1)
        
        logger.info("Backend started successfully, starting frontend...")
        # Run frontend in main thread (blocking)
        run_frontend()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
        signal_handler(None, None)
    except Exception as e:
        logger.exception(f"Error occurred: {str(e)}")
        signal_handler(None, None)






















