from together import Together
from dotenv import load_dotenv
import os

load_dotenv()

# api_key = os.getenv("api_key")

# client = Together(api_key=api_key)

# response = client.chat.completions.create(
#     model="meta-llama/Llama-Vision-Free",
#     messages=[
#         {
#             "role": "user",
#             "content": "What are some fun things to do in New York?"
#         }
#     ]
# )
# print(response.choices[0].message.content)


# import cohere
# api_key_cohere = os.getenv("api_key_cohere")
# co = cohere.ClientV2(api_key_cohere)
# response = co.chat(
#     model="command-a-03-2025", 
#     messages=[{"role": "user", "content": "hello world!"}]
# )
# print(response)

