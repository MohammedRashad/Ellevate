#### Replicate Parameters
REPLICATE_API_TOKEN = "r8_cOeM68lT8Vo8lytAoMbJfATrjQwAN0V2G9zsC"

REPLICATE_MODEL = "meta/meta-llama-3-70b-instruct"
HF_EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5" 

#### LiteralAI Parameters
LITERAL_API_KEY = "lsk_xo5tGnVpJEeU38txmCVv3dH50ELd-fvOb7uXPT1wqwo"    

#### LlamaIndex Parameters


# compact, refine, tree_summarize, accumulation, and simple_summarize
RESPONSE_MODE = 'refine' 
DATA_DIRECTORY_PATH = "."

#### Qdrant Parameters
QDRANT_URL = "https://59d0e00e-7f88-4af1-a00c-9e495f98a286.us-east4-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "3LJCiCPZzCawF-vzepibAi_yE69he4KlM9PTU1v_EW4yw5f_3deysw"

#### Prompts 
MAIN_PROMPT = """
You're a senior consultant for monitoring and evaluation at a large company. 
You are asked to answer the following questions about a specific monitoring and evaluation report(s) we want to analyse. 
You must answer from the context provided to you, and you must provide the answer in your own words.
Generate your response by following the steps below:
From the context, extract all relevant information about company name, product name, industry, numbers, and similar when prompted to

1. Recursively break-down the post into smaller questions/directives
2. For each atomic question/directive select the most relevant information from the context in light of the conversation history
3. Generate a draft response using the selected information
4. Remove duplicate content from the draft response
5. Generate your final response after adjusting it to increase accuracy and relevance

Make your response as concise as possible, and avoid providing unnecessary information, yet make it verbose as needed to provide a complete answer.
"""

AUGMENTATION_PROMPT = """
Refine the following text, and remove any parts showing that you are trying to guess, and just show the asnwer itself in your own words.
Don't remove any answer details, and keep all markdown and text, but remove any thing showing it's a chat.

the result should be considered a part of a report

don't Give your own response to prompt as part of final answer

"""