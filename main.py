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
from google.genai import errors
from google.genai._gaos.lib import compat_errors
from fastapi import HTTPException
from fastapi.responses import JSONResponse

config = dotenv_values(".env")

app = FastAPI()

client = genai.Client(api_key = config["GEMINI_API_KEY"])

class InputModel(BaseModel):
    input_str: str

@app.post(
    "/input",
    status_code = 200
)
def user_input(data: InputModel):
    try:
        stream = client.interactions.create(
                model="gemini-3.8-flash",
                input=data.input_str
                #stream=True,
            )
            # for event in stream: # type: ignore
            #     if event.event_type == "step.delta":
            #         if event.delta.type == "text":
            #             print(event.delta.text, end="", flush=True)
        result =  stream.output_text
    except (compat_errors.RateLimitError, compat_errors.APIError) as e:
        return JSONResponse(
            status_code =429,
            content = {"error": "Rate limit exceeded. Free Tier allows 20 requests/day." }
        )
    except errors.ServerError as e:
        if e.code == 500:
            print("Internal Server Error gemini is overwhelmed with so many requests")
        else: 
            print(f"Other server error {e.code}")
        return e.code
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "An unexpected server error occurred."}
        )
    except Exception as e:
        # General catch-all fallback for unexpected logic issues
        print(f"Unexpected application error: {str(e)}")
        raise HTTPException(status_code=500, detail="An internal processing error occurred.")
    else:
        print("everything went smoothly!")
        return result
    finally:
        print("final block is printed irrespective of above blocks")