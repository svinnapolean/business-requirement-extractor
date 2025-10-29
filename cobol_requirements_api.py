# cobol_requirements_api.py
from fastapi import FastAPI, Request, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from agent_extractor import agent_extract
from cobol_requirements_extractor import COBOLRequirementsExtractor
from future_state_generator import generate_future_state_with_llm, generate_future_state_summary
import tempfile
import os
from typing import List, Dict

app = FastAPI(title="Requirements Extraction API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register /agent-extract endpoint
@app.post("/agent-extract")
async def agent_extract_api(request: Request):
    data = await request.json()
    code = data.get("code", "")
    language = data.get("language", "COBOL")
    results = agent_extract(code, language)
    # Ensure all results are serializable
    def make_serializable(item):
        if isinstance(item, dict):
            # Recursively convert any non-serializable values
            return {k: str(v) if not isinstance(v, (str, int, float, bool, type(None), dict, list)) else v for k, v in item.items()}
        elif isinstance(item, (str, int, float, bool, type(None))):
            return item
        else:
            return str(item)
    if isinstance(results, list):
        results = [make_serializable(r) for r in results]
    else:
        results = make_serializable(results)
    return {"requirements": results}

@app.post("/store-in-vector-db")
async def store_in_vector_db_api(request: Request):
    """Store extracted business requirements in Qdrant vector database"""
    from agent_extractor import store_requirements_in_vector_db
    
    data = await request.json()
    requirements_text = data.get("requirements", "")
    source_code = data.get("source_code", "")
    language = data.get("language", "COBOL")
    program_name = data.get("program_name", "UnknownProgram")
    
    if not requirements_text:
        raise HTTPException(status_code=400, detail="Requirements text cannot be empty")
    
    try:
        # Store in vector DB with language parameter
        points = store_requirements_in_vector_db(requirements_text, source_code, language)
        
        return {
            "status": "success",
            "message": f"Successfully stored {len(points)} requirement(s) in vector database",
            "program_name": program_name,
            "language": language,
            "points_stored": len(points)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing in vector DB: {str(e)}")

@app.post("/search-vector-db")
async def search_vector_db_api(request: Request):
    """Search for similar requirements in Qdrant vector database"""
    from agent_extractor import qdrant, model, COLLECTION
    from qdrant_client.http.models import SearchRequest
    
    data = await request.json()
    query_text = data.get("query", "")
    limit = data.get("limit", 5)
    
    if not query_text:
        raise HTTPException(status_code=400, detail="Query text cannot be empty")
    
    try:
        # Create embedding for the query
        query_embedding = model.encode([query_text])
        
        # Search in Qdrant
        search_results = qdrant.search(
            collection_name=COLLECTION,
            query_vector=query_embedding[0].tolist(),
            limit=limit
        )
        
        # Format results
        results = []
        for result in search_results:
            payload = result.payload or {}
            source_code = payload.get("source_code", "")
            # Return full source code instead of truncating
            
            results.append({
                "score": result.score,
                "requirement": payload.get("requirement", ""),
                "source_code": source_code  # Full source code without truncation
            })
        
        return {
            "status": "success",
            "query": query_text,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching vector DB: {str(e)}")

# Initialize the COBOL extractor
extractor = COBOLRequirementsExtractor()

# Serve static test UI
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return RedirectResponse(url='/static/index.html')

@app.post("/upload-cobol", summary="Upload and analyze COBOL file")
async def upload_cobol_file(file: UploadFile = File(...)):
    """
    Upload a COBOL file and extract requirements.
    GitHub Copilot can help enhance the analysis logic.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    # Check file extension
    valid_extensions = ['.cbl', '.cob', '.cobol', '.CBL', '.COB', '.txt']
    if not any(file.filename.lower().endswith(ext) for ext in valid_extensions):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Supported: {valid_extensions}"
        )
    
    tmp_file_path = None
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Extract requirements
        result = extractor.extract_requirements_from_program(tmp_file_path)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        return {
            "status": "success",
            "file_name": file.filename,
            "extraction_result": result
        }
    
    except Exception as e:
        # Clean up on error
        try:
            if tmp_file_path and os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
        except:
            pass
        
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/search-requirements", summary="Search for similar requirements")
def search_requirements(query: dict = Body(...)):
    """
    Search for similar requirements in the vector database.
    Example body: {"query": "customer validation logic", "limit": 5}
    """
    search_query = query.get("query", "")
    limit = query.get("limit", 5)
    
    if not search_query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        results = extractor.search_similar_requirements(search_query, limit)
        return {
            "status": "success",
            "query": search_query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/list-all-requirements", summary="Get all extracted requirements")
def list_all_requirements():
    """
    Get all requirements stored in the vector database.
    """
    try:
        requirements = extractor.get_all_requirements()
        return {
            "status": "success",
            "total_programs": len(requirements),
            "requirements": requirements
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving requirements: {str(e)}")

@app.post("/analyze-text", summary="Analyze COBOL code from text input")
def analyze_cobol_text(data: dict = Body(...)):
    """
    Analyze COBOL code provided as text input.
    Example body: {"cobol_code": "PROGRAM-ID. HELLO...", "program_name": "HELLO"}
    """
    cobol_code = data.get("cobol_code", "")
    program_name = data.get("program_name", "UNNAMED")
    
    if not cobol_code:
        raise HTTPException(status_code=400, detail="COBOL code cannot be empty")
    
    tmp_file_path = None
    try:
        # Save to temporary file for processing
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.cbl') as tmp_file:
            tmp_file.write(cobol_code)
            tmp_file_path = tmp_file.name
        
        # Extract requirements
        result = extractor.extract_requirements_from_program(tmp_file_path)
        
        # Clean up
        os.unlink(tmp_file_path)
        
        return {
            "status": "success",
            "program_name": program_name,
            "analysis_result": result
        }
    
    except Exception as e:
        if tmp_file_path and os.path.exists(tmp_file_path):
            try:
                os.unlink(tmp_file_path)
            except:
                pass
        
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.get("/health", summary="Health check")
def health_check():
    """Check if the service and vector database are running"""
    try:
        # Test Qdrant connection
        collections = extractor.client.get_collections()
        return {
            "status": "healthy",
            "qdrant_connection": "ok",
            "collections": [c.name for c in collections.collections] if collections else []
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "message": "Check if Qdrant server is running on localhost:6333"
            }
        )

@app.get("/debug-vector-data")
async def debug_vector_data():
    """Debug endpoint to check what's stored in vector database"""
    from agent_extractor import qdrant, COLLECTION
    
    try:
        # Get some sample points from the collection
        results = qdrant.scroll(
            collection_name=COLLECTION,
            limit=5  # Get first 5 records
        )
        
        points = results[0] if results else []
        debug_data = []
        
        for point in points:
            payload = point.payload or {}
            debug_data.append({
                "id": point.id,
                "requirement_length": len(payload.get("requirement", "")),
                "source_code_length": len(payload.get("source_code", "")),
                "language": payload.get("language", ""),
                "requirement_preview": payload.get("requirement", "")[:100] + "..." if len(payload.get("requirement", "")) > 100 else payload.get("requirement", ""),
                "source_code_preview": payload.get("source_code", "")[:200] + "..." if len(payload.get("source_code", "")) > 200 else payload.get("source_code", "")
            })
        
        return {
            "status": "success",
            "total_points_checked": len(debug_data),
            "data": debug_data
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/generate-future-state")
async def generate_future_state_api(request: Request):
    """Generate future state recommendations using Chain-of-Thought LLM prompting"""
    try:
        data = await request.json()
        current_state = data.get("current_state", "")
        source_code = data.get("source_code", "")
        business_constraints = data.get("business_constraints", "")
        architecture_preferences = data.get("architecture_preferences", "")
        search_query = data.get("search_query", "")
        
        # Validate required inputs
        if not current_state:
            return JSONResponse(
                status_code=400,
                content={"error": "Current state is required"}
            )
        
        if not source_code:
            return JSONResponse(
                status_code=400,
                content={"error": "Source code is required"}
            )
        
        # Import here to catch any import errors
        try:
            from future_state_generator import generate_future_state_with_llm
        except ImportError as ie:
            return JSONResponse(
                status_code=500,
                content={"error": f"Import error: {str(ie)}"}
            )
        
        # Generate future state using Chain-of-Thought prompting
        result = generate_future_state_with_llm(
            current_state=current_state,
            source_code=source_code,
            business_constraints=business_constraints,
            architecture_preferences=architecture_preferences,
            search_query=search_query
        )
        
        if result.get("success"):
            future_state_content = result.get("future_state")
            
            # Extra safety: ensure the content is JSON serializable
            if not isinstance(future_state_content, str):
                print(f"Warning: future_state is not a string, converting from {type(future_state_content)}")
                future_state_content = str(future_state_content)
            
            return JSONResponse(
                content={
                    "status": "success",
                    "future_state": future_state_content,
                    "metadata": {
                        "current_state_length": len(current_state),
                        "source_code_length": len(source_code),
                        "has_constraints": bool(business_constraints.strip()),
                        "has_preferences": bool(architecture_preferences.strip())
                    }
                }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"error": f"Future state generation failed: {result.get('error', 'Unknown error')}"}
            )
            
    except Exception as e:
        # Return JSON error response instead of letting FastAPI handle it
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in generate-future-state: {error_details}")  # Log to server console
        
        return JSONResponse(
            status_code=500,
            content={"error": f"Server error: {str(e)}"}
        )

@app.post("/generate-future-state-summary")
async def generate_future_state_summary_api(request: Request):
    """Generate a quick summary of future state recommendations"""
    try:
        data = await request.json()
        current_state = data.get("current_state", "")
        business_constraints = data.get("business_constraints", "")
        
        if not current_state:
            return JSONResponse(
                status_code=400,
                content={"error": "Current state is required"}
            )
        
        # Import here to catch any import errors
        try:
            from future_state_generator import generate_future_state_summary
        except ImportError as ie:
            return JSONResponse(
                status_code=500,
                content={"error": f"Import error: {str(ie)}"}
            )
        
        # Generate quick summary
        result = generate_future_state_summary(
            current_state=current_state,
            business_constraints=business_constraints
        )
        
        if result.get("success"):
            summary_content = result.get("summary")
            
            # Extra safety: ensure the content is JSON serializable
            if not isinstance(summary_content, str):
                print(f"Warning: summary is not a string, converting from {type(summary_content)}")
                summary_content = str(summary_content)
            
            return JSONResponse(
                content={
                    "status": "success",
                    "summary": summary_content
                }
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"error": f"Summary generation failed: {result.get('error', 'Unknown error')}"}
            )
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in generate-future-state-summary: {error_details}")
        
        return JSONResponse(
            status_code=500,
            content={"error": f"Server error: {str(e)}"}
        )

@app.get("/stats", summary="Get extraction statistics")
def get_statistics():
    """Get statistics about extracted requirements"""
    try:
        requirements = extractor.get_all_requirements()
        
        # Basic statistics
        total_programs = len(requirements)
        
        # Count by file type if available
        file_types = {}
        for req in requirements:
            file_name = req.get('file_name', '')
            ext = os.path.splitext(file_name)[1].lower()
            file_types[ext] = file_types.get(ext, 0) + 1
        
        return {
            "status": "success",
            "total_programs": total_programs,
            "file_types": file_types,
            "last_extraction": max([req.get('extraction_timestamp', '') for req in requirements]) if requirements else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("Starting COBOL Requirements Extraction API...")
    print("Make sure Qdrant is running: docker run -p 6333:6333 qdrant/qdrant")
    print("API will be available at: http://localhost:8000")
    print("Web UI will be available at: http://localhost:8000/static/index.html")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)