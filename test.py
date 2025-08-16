from together import Together
from dotenv import load_dotenv
import os

load_dotenv()

# TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# client = Together(api_key=TOGETHER_API_KEY)

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
# COHERE_API_KEY = os.getenv("COHERE_API_KEY")
# co = cohere.ClientV2(COHERE_API_KEY)
# response = co.chat(
#     model="command-a-03-2025", 
#     messages=[{"role": "user", "content": "hello world!"}]
# )
# print(response)

