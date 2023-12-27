from fastapi import FastAPI, APIRouter
from routers.users import router_users
from routers.tasks import router_tasks

import uvicorn

app = FastAPI(debug=True)

app.include_router(router=router_users, tags=["users"])
app.include_router(router=router_tasks, tags=["tasks"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)