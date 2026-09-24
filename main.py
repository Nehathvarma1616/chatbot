# from google import genai

# client = genai.Client(api_key = "")

# interaction = client.interactions.create(
#     model="gemini-3.8-flash",
#     input="Explain how AI works in a few words",
#     stream = True
# )
# for tokens in interaction:
#     print(tokens)
# print(interaction.output_text)
from dotenv import dotenv_values
from fastapi import FastAPI # type: ignore
from google import genai
from pydantic import BaseModel

config = dotenv_values(".env")
# print(config["GEMINI_API_KEY"])
# print(type(config["GEMINI_API_KEY"]))
app = FastAPI()
client = genai.Client(api_key = config["GEMINI_API_KEY"])

class InputModel(BaseModel):
    input_str: str

@app.post(
    "/input",
    status_code = 200
)
def user_input(data: InputModel):
    stream = client.interactions.create(
        model="gemini-3.8-flash",
        input=data.input_str
        #stream=True,
    )
    # for event in stream: # type: ignore
    #     if event.event_type == "step.delta":
    #         if event.delta.type == "text":
    #             print(event.delta.text, end="", flush=True)
    return stream.output_text