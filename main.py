from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
from jose import JWTError, jwt

# Assuming you have a function `run_task` which takes task, report_type and agent as parameters
# and returns the result when the task is complete.
from agent.run import run_agent

# Your secret key for encoding and decoding JWT
secret = os.environ['JWT_SECRET_KEY']



class ResearchRequest(BaseModel):
    task: str
    report_type: str
    agent: str

app = FastAPI()

bearer_scheme = HTTPBearer()

def authenticate(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials:
        token = credentials.credentials
        try:
            payload = jwt.decode(token, secret, algorithms=["HS256"])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code"
        )

# Dynamic directory for outputs once first research is run
@app.on_event("startup")
def startup_event():
    if not os.path.isdir("outputs"):
        os.makedirs("outputs")

@app.get("/")
async def read_root(token: str = Depends(authenticate)):
    return {"message": "Server is running"}

@app.post("/start")
async def start_research(request: ResearchRequest, token: str = Depends(authenticate)):
    task = request.task
    report_type = request.report_type
    agent = request.agent
    if task and report_type and agent:
        result = await run_agent(task, report_type, agent)
        print("final",result)
        return {"status": "success", "result": result}
    else:
        return {"status": "error", "message": "Not enough parameters provided."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3200)
