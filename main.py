from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import json
import os
from dotenv import load_dotenv

import asyncio
from langflow.load import load_flow_from_json

load_dotenv()
print(os.getenv("OPENAI_API_KEY"))

from langflow.load import run_flow_from_json

TWEAKS = {
    "ChatInput-8BYvA": {},
    "Prompt-97C8j": {},
    "ChatOutput-auHvP": {},
    "OpenAIModel-1RVR7": {},
}


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print("Request for index page received")
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/favicon.ico")
async def favicon():
    file_name = "favicon.ico"
    file_path = "./static/" + file_name
    return FileResponse(
        path=file_path, headers={"mimetype": "image/vnd.microsoft.icon"}
    )


@app.post("/hello", response_class=HTMLResponse)
async def hello(request: Request, name: str = Form(...)):
    if name:
        print("Request for hello page received with name=%s" % name)
        return templates.TemplateResponse(
            "hello.html", {"request": request, "name": name}
        )
    else:
        print(
            "Request for hello page received with no name or blank name -- redirecting"
        )
        return RedirectResponse(
            request.url_for("index"), status_code=status.HTTP_302_FOUND
        )


@app.post("/hindi")
async def hindi(request: Request):
    with open("hello_world.json", "r") as file:
        json_data = json.load(file)

    # Extract the flow data (assuming it's the first item in the array)
    flow_data = json_data["flows"][0]

    TWEAKS = {
        "ChatInput-T2fB6": {},
        "Prompt-VKbE3": {},
        "ChatOutput-KMUev": {},
        "OpenAIModel-9Y4gs": {
            "api_key": "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"
        },
    }

    # Load the flow
    graph = load_flow_from_json(
        flow=flow_data,
        tweaks=TWEAKS,
    )

    # Run the graph
    result = await graph.arun(
        inputs=[{"input_value": "message"}],
        inputs_components=[],
        types=["chat"],
        outputs=[],
        session_id="",
        stream=False,
        fallback_to_env_vars=True,
    )

    print(result)
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
