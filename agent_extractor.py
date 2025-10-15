"""
Agent Extractor: Uses LLMFallbackClient to extract requirements from COBOL or other code and stores results in Qdrant vector DB.
"""
import os
from llm_fallback_client import LLMFallbackClient
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION = "agent_requirements"

model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient(QDRANT_URL)


def ensure_collection_exists():
    """
    Ensure the agent_requirements collection exists in Qdrant.
    """
    from qdrant_client.http.models import Distance, VectorParams
    
    try:
        # Check if collection exists
        collections = qdrant.get_collections()
        collection_names = [c.name for c in collections.collections]
        
        if COLLECTION not in collection_names:
            # Create collection with proper vector configuration
            qdrant.create_collection(
                collection_name=COLLECTION,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print(f"Created collection: {COLLECTION}")
        else:
            print(f"Collection {COLLECTION} already exists")
    except Exception as e:
        print(f"Error ensuring collection exists: {e}")
        raise


def extract_requirements_with_llm(code: str, language: str = "COBOL"):
    """
    Extract requirements using LLMFallbackClient (OpenAI, Gemini, etc).
    """
    try:
        client = LLMFallbackClient()
        user_prompt = (
            "As a business analyst, I want to extract the business rules and business requirements from the program and the code provided. "
            "The results should be well-formatted text suitable for creating documents, such as markdown documents. I wanted only business rules and requirements and relevant information. "
            "Do not include any other statements. which are not relevant to the requirements and business rules or context."
        )
        response = client.ask(user_prompt, code, language)
        if response.get("success"):
            # Return only formatted_text as plain string if present
            formatted = response.get("formatted_text")
            if formatted:
                return formatted
            # Fallback to raw result
            result_text = response.get("result", "")
            return result_text
        else:
            return response.get("error", "LLM extraction failed.")
    except Exception as e:
        return [{"error": f"LLMFallbackClient error: {str(e)}"}]


def store_requirements_in_vector_db(requirements, code):
    """
    Store requirements in Qdrant vector DB.
    """
    from qdrant_client.http.models import PointStruct
    
    # Ensure collection exists before storing
    ensure_collection_exists()
    # If requirements is a string, wrap in list
    if isinstance(requirements, str):
        texts = [requirements]
    else:
        texts = [r.get("text", str(r)) for r in requirements]
    embeddings = model.encode(texts)
    points = [
        PointStruct(
            id=i,
            vector=embeddings[i].tolist(),
            payload={
                "requirement": texts[i],
                "source_code": code
            }
        )
        for i in range(len(texts))
    ]
    qdrant.upsert(collection_name=COLLECTION, points=points)
    return points


def agent_extract(code: str, language: str = "COBOL"):
    """
    Main entry: extract requirements using LLM and store in vector DB.
    """
    # Ensure collection exists before processing
    ensure_collection_exists()
    
    requirements = extract_requirements_with_llm(code, language)
    # Ensure requirements is plain text for embedding
    from llm_fallback_client import LLMFallbackClient
    if isinstance(requirements, dict):
        requirements_text = LLMFallbackClient().extract_text(requirements)
    else:
        requirements_text = str(requirements)
    store_requirements_in_vector_db(requirements_text, code)
    return requirements

# For API usage
if __name__ == "__main__":
    sample_code = "IDENTIFICATION DIVISION. PROGRAM-ID. DEMO. * Business rule: Validate input."
    print(agent_extract(sample_code, "COBOL"))
