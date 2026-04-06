from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Docker Compose!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/echo")
def echo(body: dict):
    return body