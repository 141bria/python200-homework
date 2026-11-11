# Step 1 #
import os
from dotenv import load_dotenv
load_dotenv(".env")
api_key = os.getenv("OPENAI_API_KEY")
print("API key loaded succesfully!" if api_key else"API Key not found")
from pathlib import Path
docs_dir = Path("groundwork_docs")
assert docs_dir.exists(), f"Document directory not found: {docs_dir}"

# Step 2 #
from llama_index.core import SimpleDirectoryReader
reader = SimpleDirectoryReader(input_dir="groundwork_docs")
documents = reader.load_data()
print(len(documents))
for document in documents:
    print(document.metadata["file_name"])

#Step 3#
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import SimpleDirectoryReader
from llama_index.core import SimpleDirectoryReader,VectorStoreIndex

Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.llm = OpenAI(model="gpt-4o-mini")
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(similarity_top_k=3)
print("Index built successfully. Ready to answer questions.")


#Step 4#
questions = [
   "What are Groundwork's hours on weekends?",
    "Do you offer any dairy-free milk options?",
    "How does the loyalty program work?",
    "How did Groundwork Coffee get started?",
    "Do you offer catering or wholesale orders?",
]
for q in questions:
    print(f"\nQ:{q}")
    response = query_engine.query(q)
    print("A:", response)
for node_with_score in response.source_nodes:
        print(f"Similarity Score:{node_with_score.score:.4f}")
        print(f"Text Snippet:{node_with_score.node.get_content()[:200]}")
        print("-"*30)
#The assistant sounded confident and accurate in its responses. Since I had already reviewed the documents, I could tell that it was pulling information from the material provided. I even double-checked the wholesale information to make sure it was correct. None of the answers surprised me.#

# Step 5#
question1 = "What would I need to do to have an a private event after hours at the downtown location?"

response1= query_engine.query(question1)
print("Q:",question1)
print("A:",response1)
for node_with_score in response1.source_nodes:
    print("Document:", node_with_score.node.metadata["file_name"])
    print(f"Similarity Score: {node_with_score.score:.4f}")
    print(f"Text Snippet: {node_with_score.node.get_content()[:200]}")

# I asked the following question , "What would I need to do to have an a private event after hours at the downtown location?". I expected this to be hard becasue none of the files mention anything about having a private event at the shop, I inlcuded "after hours" because I wanted to see if the model would mention something about the hours of operation, and I included downtown because I knew they had a downtown location.#
# Something that went wrong was the model guessed anyway because none of the documents mentioned anything about hosting private events at the coffee shop.#
# The model's tone was kind of mixed. The model started by saying I would need to contact the establishment, but then gave additional information as if private events were an option. It still sounded confident, which shows why AI-generated responses should be trusted cautiously because you don't always know what information the AI is missing.#
#Something I would do to improve the system is,have the assistant clearly say when the documents don't provide enough information instead of making assumptions. That way, it doesn't give someone information that hasn't been confirmed.#

#Step 6#
#Q1:# My LlamaIndex implementation took about 4 lines of code. Using LlamaIndex helps reduce the amount of code needed, which leaves less room for errors. It also makes the process easier by streamlining everything instead of having to write all the steps myself.#
#Q2: # This could help businesses and organizations when HR isn't available. Employees could use the system to find information that's already been uploaded, like company history, benefits, or hours. This would allow employees to do some of the groundwork themselves instead of always having to reach out to HR.#
#Q3: One failure RAG can't fully prevent is hallcuination. Even when it gets the right info, AI can still make aassumptions that aren't supported by documents#

#AI Usage: I used ChatGPT to help me remember some Python syntax, understand how certain functions worked, and troubleshoot errors when I got stuck. I also used it to help organize my reflection comments. I worked through the assignment myself, researched syntax, tested my code, and corrected several errors on my own.#