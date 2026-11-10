#Part 1:Warmup Exercises#
from dotenv import load_dotenv
import os

if load_dotenv():
    print("API key loaded successfully.")
else:
    print("Warning: could not load API key. Check your .env file.")
                            #RAG Concepts#
#Q1#
#For Scenario A: I would say RAG would work best becasue the company has hundres of policy documents that get updated regularly. AI can look up the information it needs without it needing to be retrained.#
#For Scenario B: I would say Fine-tuning would be the best because they already have 3,000 examples of the specific writing styles they want the AI to use.#
#For Scenario C: I would say Prompt-Engineering would work because it's only one two page report. She could easily gave AI the report to directly and ask questions without needing to train a model.#
#Q2#
#A confidently wrong answer can be harmful because the person may be lead to believe that the information is correct even when it's not. An example of this could be the AI say that it's safe to take certain medications togther even if it's not, that could cause that person to have adverse side effects and go through unnecessary harm. The tone of the response can make the information seem trustworthy and accurate even when the AI is hallucinating and giving incorrect information.#
#Q3#
#steps = ["Generate a response from the LLM","Extract text from source documents","Receive the user's query","Retrieve the most relevant chunks","Convert text chunks into embeddings","Inject retrieved chunks into the prompt","Split text into chunks","Embed the user's query",]#
# Step 1. Extract text from source documents
# Get information from files or documents.

# Step 2. Split text into chunks
# Break the information into smaller pieces.

# Step 3. Convert text chunks into embeddings
# Turn each piece into numbers that represent its meaning.

# Step 4. Receive the user's query
# The user asks AI a question.

# Step 5. Embed the user's query
# Turn the user's question into numbers too.

# Step 6. Retrieve the most relevant chunks
# Find the pieces of information that best match the question.

# Step 7. Inject retrieved chunks into the prompt
# Give AI the matching information along with the question.

# Step 8. Generate a response from the LLM
# AI uses the information to answer the question.
import string

def simple_keyword_retrieval(query, documents, verbose=True):
    """Keyword retrieval using token overlap scoring."""
    stopwords = {
        "a", "an", "the", "and", "or", "in", "on", "of", "for", "to", "is",
        "are", "was", "were", "by", "with", "at", "from", "that", "this",
        "as", "be", "it", "its", "their", "they", "we", "you", "our"
    }
    translator = str.maketrans("", "", string.punctuation)

    query_words = {
        w.translate(translator)
        for w in query.lower().split()
        if w not in stopwords
    }
    if verbose:
        print(f"\nQuery tokens (filtered): {sorted(query_words)}")

    scores = []
    for name, content in documents.items():
        content_words = {
            w.translate(translator)
            for w in content.lower().split()
            if w not in stopwords
        }
        overlap = query_words & content_words
        score = len(overlap)
        scores.append((score, name, content))
        if verbose:
            print(f"[{name}] overlap={score} -> {sorted(overlap)}")

    scores.sort(reverse=True)
    best = next(((name, content) for score, name, content in scores if score > 0), None)
    if best:
        if verbose:
            print(f"\nSelected best match: {best[0]}")
        return [best]
    else:
        if verbose:
            print("\nNo overlapping keywords found.")
        return [("None found", "No relevant content.")]
        #Keyword#
#Q1#
simple_keyword_retrieval(query = "What are your hours on weekends?",

documents = {
    "menu.txt": "We serve espresso, lattes, cappuccinos, and cold brew. Pastries include croissants and muffins baked fresh daily. Oat milk and almond milk are available.",
    "hours.txt": "We are open Monday through Friday from 7am to 7pm. On weekends we open at 8am and close at 5pm. We are closed on Thanksgiving and Christmas Day.",
    "hiring.txt": "We are currently hiring baristas and shift supervisors. Send your resume to jobs@groundworkcoffee.com.",
    "loyalty.txt": "Join our loyalty program to earn one point per dollar spent. Redeem 100 points for a free drink of your choice.",
}, verbose=True)
# The loyalty.txt was selected, it was selected because of this part of the code scores.sort(reverse=True) had Python look at the code in reverse alphabetcial order.#
#Q2#
simple_keyword_retrieval(query = "Do you have anything without caffeine?",

documents = {
    "menu.txt": "We serve espresso, lattes, cappuccinos, and cold brew. Pastries include croissants and muffins baked fresh daily. Oat milk and almond milk are available.",
    "hours.txt": "We are open Monday through Friday from 7am to 7pm. On weekends we open at 8am and close at 5pm. We are closed on Thanksgiving and Christmas Day.",
    "hiring.txt": "We are currently hiring baristas and shift supervisors. Send your resume to jobs@groundworkcoffee.com.",
    "loyalty.txt": "Join our loyalty program to earn one point per dollar spent. Redeem 100 points for a free drink of your choice."
}, verbose=True)
# No document was selected because none of the words in the query matched the documents. Keyword RAG worked how it was supposed to, but it didn't really understand what I was asking. Semantic RAG would probably work better because it looks at meaning instead of just matching exact words.#
#Q3#
# My prediciton: I predict that it will return no overlapping key words found becasue none of the words within the query match the documents.
simple_keyword_retrieval(query = "How do I sign up for rewards?",documents = {
    "menu.txt": "We serve espresso, lattes, cappuccinos, and cold brew. Pastries include croissants and muffins baked fresh daily. Oat milk and almond milk are available.",
    "hours.txt": "We are open Monday through Friday from 7am to 7pm. On weekends we open at 8am and close at 5pm. We are closed on Thanksgiving and Christmas Day.",
    "hiring.txt": "We are currently hiring baristas and shift supervisors. Send your resume to jobs@groundworkcoffee.com.",
    "loyalty.txt": "Join our loyalty program to earn one point per dollar spent. Redeem 100 points for a free drink of your choice."
}, verbose=True)
#My prediciton was correct because Keyword Rag looked for the exact words in the query and didn't see it, and the result did not surpise me.#
                                #Semantic RAG Concepts#
#Q1#
#Vector Embedding is converting text into a list of numbers that represent what it means.#
#Cosine Similarity measures how close to vector points are to each other in the same direction.If the score is closer to 1 it means they are more closely related.#
#Semantic Search can find relationships through embeddings, basically looking to see the meaning of each word and how they are potentially connected.#
#Q2#
#| Feature                    | Keyword RAG                       | Semantic RAG |
# |----------------------------|-----------------------------------|--------------|
# | What is compared?          | Exact word overlap                |embeddings and word relation|
# | What is retrieved?         | Full document                     |partial document            |
# | Can it handle synonyms?    | No                                | Yes                        |
# | Storage format             | Plain text dictionary             | vector embeddings          |
# | Relevance score            | Number of overlapping keywords    | cosine simailarity         |#
                    #LlamaIndex#
#Q1#
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import SimpleDirectoryReader
from llama_index.core import SimpleDirectoryReader,VectorStoreIndex

Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
docs = SimpleDirectoryReader("brightleaf_pdfs").load_data()
index = VectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine(similarity_top_k=3)
questions = [
    "What employee benefits does BrightLeaf offer?",
    "What are BrightLeaf's security policies?",
]
for q in questions:
    print(f"\nQ:{q}")
    response = query_engine.query(q)
    print("A:", response)
for node_with_score in response.source_nodes:
    print()
    print()
    print()
    print()