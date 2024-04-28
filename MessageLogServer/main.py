import uvicorn
import sys

if __name__ == "__main__":
    sys.argv.append("--reload-ignore=venv")
    uvicorn.run("MessageLogServer:app", host="0.0.0.0", port=22366, reload=True, log_level="info")
