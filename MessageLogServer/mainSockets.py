import uvicorn
import sys

if __name__ == "__main__":
    sys.argv.append("--reload-ignore=venv")
    uvicorn.run("MessageLogServerSockets:app", host="0.0.0.0", port=22367, reload=True, log_level="info")
