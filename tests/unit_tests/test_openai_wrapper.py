import os
import openai
from prompt_optimizer.poptim import StopWordOptim
from prompt_optimizer.wrapper.sql_db import SQLDBManager
from prompt_optimizer.wrapper.openai import OpenAIWrapper
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
def test_openai_wrapper():
    response = True
    assert response is not None, "Failed!"
test_openai_wrapper()