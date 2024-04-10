import uvicorn
import sys

if __name__ == "__main__":
    sys.argv.append("--reload-ignore=venv")
    uvicorn.run("APIServer:app", host="0.0.0.0", port=9001, reload=True, log_level="error")
