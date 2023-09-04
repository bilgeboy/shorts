from config import open_api_key
import openai

# example of how to use open ai in prompt
openai.api_key = open_api_key
prompt = "Once upon a time"
response = openai.Completion.create(
    engine="ada",  # Choose the engine you want to use
    prompt=prompt,
    max_tokens=50  # Set the maximum number of tokens in the response
)

generated_text = response.choices[0].text.strip()
print("Generated Response:", generated_text)
