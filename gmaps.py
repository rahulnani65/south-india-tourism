from google.genai import types
from google import genai
from composio_gemini import Action, ComposioToolSet, App
import json
import time

client = genai.Client(api_key="AIzaSyD3WSnlZlux7vVPP2LQ7fZvg8O43J01mK8")

toolset = ComposioToolSet(api_key="nc2ixnab83qtj43zyjmgn")

# entity_id="3248c265-bcf3-4376-baa9-c187a1cc034d"

tools = toolset.get_tools(actions=[Action.GOOGLE_MAPS_GET_DIRECTION],skip_default=True)



response = toolset.execute_action(
    action=Action.GOOGLE_MAPS_GET_DIRECTION,
    params={
        "origin": "disneyland",
        "destination": "universal studios hollywood"
    },
)


print(response)