import uvicorn

if __name__ == "__main__":
    uvicorn.run("APIServer:app", host="0.0.0.0", port=9001, reload=True)