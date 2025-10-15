# cobol_requirements_api.py
from fastapi import FastAPI, Request, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from agent_extractor import agent_extract
from cobol_requirements_extractor import COBOLRequirementsExtractor
import tempfile
import os
from typing import List, Dict

app = FastAPI(title="COBOL Requirements Extraction API", version="1.0")

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