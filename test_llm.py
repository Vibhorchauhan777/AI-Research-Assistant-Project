from app.llm import get_llm

print("1. Import successful")

llm = get_llm()

print("2. LLM object created")

print("3. Sending request...")

response = llm.invoke("Say only the word: Hello")

print("4. Response received")

print(response)

print(response.content)