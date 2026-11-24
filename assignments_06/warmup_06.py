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
from llama_index.llms.openai import OpenAI
from llama_index.core import SimpleDirectoryReader
from llama_index.core import SimpleDirectoryReader,VectorStoreIndex

Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.llm = OpenAI(model="gpt-4o-mini")
docs = SimpleDirectoryReader("brightleaf_pdfs").load_data()
index = VectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine(similarity_top_k=3)
questions = [
    "What employee benefits does BrightLeaf offer?",
    "What are BrightLeaf's security policies?",
]
print("\n===== K=3 RESULTS =====")
for q in questions:
    print(f"\nQ:{q}")
    response = query_engine.query(q)
    print("A:", response)
    for node_with_score in response.source_nodes:
        print(f"Similarity Score:{node_with_score.score:.4f}")
        print(f"Text Snippet:{node_with_score.node.get_content()[:150]}")
        print("-"*30)
    #**1. Do the retrieved chunks look relevant to the question? Yes. For employee benefits, the retrieved chunks explained the health benefits, financial benefits, parental leave, and professional development, which are all benefits Brightleaf offers.

    #For security policies, yes and no. It explained things like layered security defenses and multi-factor authentication, which are relevant. But it also went into incident response plans and employee security training, which I felt was a little extra compared to what I was asking.

    #2. Does the model's response sound confident and specific?
    # Yes. The model's response sounds confident and specific because it's referencing information from the PDFs. I didn't notice it using phrases like "based on the context" or "I'm not sure."

    #3. Did anything unexpected get retrieved?
    # Yes. For the security policies question, it also retrieved information about employee training, ISO practices, and quarterly risk reviews. I wasn't necessarily expecting all that extra information because I was mainly asking about Brightleaf's security policies.
    #Q2#
query_engine = index.as_query_engine(similarity_top_k=1)
questions = [
    "What employee benefits does BrightLeaf offer?"
]
print("\n===== K=1 RESULTS =====")
for q in questions:
    print(f"\nQ:{q}")
    response = query_engine.query(q)
    print("A:", response)
    for node_with_score in response.source_nodes:
        print(f"Similarity Score:{node_with_score.score:.4f}")
        print(f"Text Snippet:{node_with_score.node.get_content()[:150]}")
        print("-"*30)

    query_engine = index.as_query_engine(similarity_top_k=5)
    questions = [
        "What employee benefits does BrightLeaf offer?"
    ]
    print("\n===== K=5 RESULTS =====")
    for q in questions:
        print(f"\nQ:{q}")
        response = query_engine.query(q)
        print("A:", response)
        for node_with_score in response.source_nodes:
            print(f"Similarity Score:{node_with_score.score:.4f}")
            print(f"Text Snippet:{node_with_score.node.get_content()[:150]}")
        print("-"*30)
        #The responses for K=1 and K=5 were pretty similar. Both explained Brightleaf's employee benefits, including health, financial benefits, parental leave, and career development. K=1 retrieved one relevant chunk, while K=5 retrieved five chunks, including some unrelated information about partnerships, finances, and security. I don't think more retrieved context is always better because it can bring in information that doesn't really relate to the question.#

print("\n===== Specific K3 RESULTS =====")
#Q3#
query_engine = index.as_query_engine(similarity_top_k=3)
question = "What is the company policy when it comes to establishing new partnerships?"
response1 = query_engine.query(question)
print("A:", response1)
for node_with_score in response1.source_nodes:
    print(f"Similarity Score:{node_with_score.score:.4f}")
    print(f"Text Snippet:{node_with_score.node.get_content()[:150]}")
    print("-"*30)   
  
# I predict that the model may struggle to find information related to the question and may result in no overlap.#
# The model surprisingly gave me information about Brightleaf's strategy for choosing partnerships, but it didn't necessarily explain what their actual policy is.#
# I guess I would change my prompt to tell the model to say when the documents don't have the exact answer instead of giving me info that's unrelated to my question.#

#Q4#
from llama_index.core.evaluation import FaithfulnessEvaluator,RelevancyEvaluator
llm = OpenAI(model="gpt-4o-mini", temperature=0.2)
faithfulness_evaluator = FaithfulnessEvaluator(llm=llm)
relevancy_evaluator = RelevancyEvaluator(llm=llm)
print("\n===== Q4 EVALUATION RESULTS =====")
q = "What employee benefits does BrightLeaf offer?"
response2 =query_engine.query(q)
faithfulness_result = faithfulness_evaluator.evaluate_response(query=q,response=response2)
print("Faithfulness Evaluation: "+ str(faithfulness_result.score))
relevancy_result = relevancy_evaluator.evaluate_response(query=q,response=response2)
print("Relevancy Result: " + str(relevancy_result.score))

print("\n===== QUESTION 4 PART 2 =====")
q2 = "What opportunities for upward development that Brightleaf possesses?"
response3 = query_engine.query(q2)
print("A:", response3)
faithfulness_result2 = faithfulness_evaluator.evaluate_response(query=q2,response=response3)
print("Faithfulness Evaluation: "+ str(faithfulness_result2.score))
relevancy_result2 = relevancy_evaluator.evaluate_response(query=q2,response=response3)
print("Relevancy Result: " + str(relevancy_result2.score))
#A faithfulness score of 1.0 means the model's response was supported by the information it retrieved and didn't hallucinate or make things up. A score of 0.0 means the response wasn't supported by the retrieved information and may have included hallucinations.Relevancy measures whether the model's response is on topic or if it's rambling and giving information that doesn't relate to the question. The difference is that relevancy checks if the answer stays on topic, while faithfulness checks if the model is making things up or giving information supported by the documents.
# No, both queries received a faithfulness and relevancy score of 1.0. I think this happened because the model was able to find relevant information for both questions. The questions were specific enough, and the model didn't have to go off topic or make anything up.LLM-as-a-judge is using another AI model to evaluate how well the original model answered a question. It's used for RAG evaluation because it can look at whether the response is relevant and supported by the retrieved information instead of just checking if the answer is right or wrong. It can also be faster and more efficient than having multiple people evaluate the responses.#