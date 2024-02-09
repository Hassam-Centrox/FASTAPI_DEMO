import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import warnings
warnings.filterwarnings("ignore")
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_together import Together
import os
app = FastAPI()

path_project = os.path.dirname(os.path.abspath(__file__))
public = os.path.join(path_project, "templates")
app.mount("/templates", StaticFiles(directory=public), name="templates")

templates = Jinja2Templates(directory=os.path.join(path_project, "templates"))
print(templates)
def together_Ai(model_name="mistralai/Mixtral-8x7B-Instruct-v0.1",
                temperature=0.0, tokens=192):
    """
    Create and initialize a Together AI language model.

    Parameters:
    - model_name (str, optional): The name of the Together AI language model.
    - temperature (float, optional): The parameter for randomness in text generation.
    - tokens (int, optional): The maximum number of tokens to generate.

    Returns:
    - llm (Together): The initialized Together AI language model.
    """


    model_name = "togethercomputer/llama-2-7b-chat"

    llm = Together(
        model=model_name,
        temperature=temperature,
        max_tokens=tokens,
        together_api_key=api_key
    )

    return llm
llm=together_Ai()
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

def generate_chatbot_response(message):
    res = conversation.predict(input=message)
    return res
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    ps = "Welcome"
    return templates.TemplateResponse("index.html", {"request": request, "message1": ps})


@app.post("/")  # Handle POST requests to the root URL
async def submit_form(request: Request):
    form_data = await request.form()  # Retrieve form data
    # Get the value of the input field named "user_input"
    user_input = form_data.get("user_input")
    result=generate_chatbot_response(user_input)
    return templates.TemplateResponse("index.html", {"request": request, "message1": user_input, "message2": result})  # Return the user input
