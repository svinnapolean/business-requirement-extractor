# Copilot instructions for COBOL Requirements Extraction Project

Purpose: Extract business requirements from legacy COBOL programs and store them in a vector database for intelligent analysis and search.

## Project Overview

This repository contains a **COBOL requirements extraction and analysis system** with the following components:

- **COBOL Parser**: `cobol_requirements_extractor.py` — Parses COBOL programs to extract business rules, data definitions, and functional requirements
- **Vector Database**: Qdrant-based storage using SentenceTransformers (`all-MiniLM-L6-v2`) for semantic similarity search
- **REST API**: `cobol_requirements_api.py` — FastAPI service for file uploads, analysis, and requirement searches
- **Analysis Notebook**: `cobol_requirements_analysis.ipynb` — Interactive workflow for batch processing and visualization
- **Web Interface**: `static/index.html` — Simple UI for testing COBOL file uploads and searches

**Data Flow**: COBOL Files → Parser → Requirements Extraction → Vector Embeddings → Searchable Database

## Key Dependencies & Environment

- **Vector Store**: Qdrant server (`localhost:6333`) — start with `docker run -p 6333:6333 qdrant/qdrant`
- **ML Models**: SentenceTransformers (`all-MiniLM-L6-v2`) for text embeddings
- **Python Stack**: FastAPI, pandas, numpy, qdrant-client, sentence-transformers, nltk
- **Visualization**: matplotlib, seaborn, wordcloud for analysis dashboards
- **File Processing**: Support for `.cbl`, `.cob`, `.cobol`, `.CBL`, `.COB`, `.txt` files
- **No External LLMs**: Uses only local models and GitHub Copilot for enhancement

## Critical Workflows

**Start Development Environment:**
```bash
# 1. Start Qdrant vector database
docker run -p 6333:6333 qdrant/qdrant
# 2. Start COBOL API server
python cobol_requirements_api.py  
# 3. Open web UI at http://localhost:8000
```

**COBOL Analysis Workflow:**
1. Place COBOL files in accessible directory or use file upload API
2. Run `cobol_requirements_analysis.ipynb` for interactive analysis
3. Use API endpoints for programmatic access and integration

## Code Patterns & COBOL-Specific Conventions

**COBOL Parser (`cobol_requirements_extractor.py`):**
- **Divisions**: Extracts IDENTIFICATION, ENVIRONMENT, DATA, PROCEDURE divisions
- **Business Logic**: Identifies IF-THEN-ELSE, PERFORM-UNTIL, validation patterns
- **Data Items**: Parses PIC clauses, level numbers, field definitions
- **Comments**: Extracts requirement comments (lines starting with `*` in column 7)
- **File Operations**: Identifies OPEN, READ, WRITE, CLOSE statements

**Vector Database Integration:**
- Collection: `cobol_requirements` for storing extracted requirements
- Embeddings: Combines program structure, business logic, and comments into searchable text
- Search: Semantic similarity for finding related requirements across programs

**API Endpoints (`cobol_requirements_api.py`):**
- `/upload-cobol`: Upload COBOL files for analysis
- `/analyze-text`: Analyze COBOL code from text input
- `/search-requirements`: Vector similarity search for requirements
- `/list-all-requirements`: Get all extracted requirements
- `/stats`: Analysis statistics and metrics

## GitHub Copilot Enhancement Strategies

**COBOL-Specific Prompting:**
- `// Extract COBOL business rules from comments and logic`
- `# Parse COBOL DATA DIVISION for field definitions`
- `// Improve regex patterns for COBOL paragraph identification`
- `# Enhance validation rule extraction from IF statements`

**Pattern Recognition Improvements:**
- Ask Copilot to suggest better regex for COBOL syntax
- Request domain-specific business rule patterns
- Get suggestions for handling different COBOL dialects
- Improve error handling for malformed COBOL syntax

**Fine-tuning Approaches:**
- Similarity threshold adjustment (0.5-0.95)
- Pattern enhancement for specific COBOL constructs
- Feedback collection for iterative improvement
- Custom extraction rules for domain-specific requirements

## Integration Points

- **File I/O**: Supports multiple COBOL file extensions and encodings
- **Vector Database**: Single collection `cobol_requirements` for all extracted data
- **Web Interface**: Static HTML for manual testing and demonstrations
- **API Integration**: RESTful endpoints for external system integration

## Debugging & Troubleshooting

**Common Issues:**
- **Qdrant Connection**: Check server status at `http://localhost:6333/dashboard`
- **File Encoding**: Supports UTF-8, CP1252, ASCII, ISO-8859-1
- **COBOL Parsing**: Handles variations in COBOL syntax and formatting
- **Vector Search**: Adjustable similarity thresholds for different use cases

**Performance Optimization:**
- Batch processing for large COBOL codebases
- Parallel file processing for directories
- Configurable embedding chunk sizes
- Memory-efficient processing for large legacy systems

## Sample COBOL Program Structure

The extractor handles standard COBOL programs with:
```cobol
IDENTIFICATION DIVISION.
PROGRAM-ID. program-name.
* Business requirements in comments
ENVIRONMENT DIVISION.
DATA DIVISION.
   01 data-items PIC clauses
PROCEDURE DIVISION.
   paragraph-names.
   IF-THEN-ELSE logic
   PERFORM statements
```

## Next Steps for Enhancement

1. **GitHub Copilot Integration**: Use Copilot chat for pattern improvements
2. **Domain Customization**: Adapt patterns for specific COBOL environments
3. **Batch Processing**: Scale for enterprise COBOL codebases
4. **Integration**: Connect with legacy system documentation tools
5. **Reporting**: Generate requirement traceability reports
