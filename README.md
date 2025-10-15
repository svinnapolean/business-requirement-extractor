# COBOL Requirements Extraction System

Extract business requirements from legacy COBOL programs and store them in a vector database for intelligent search and analysis.

## 🎯 Project Overview

This system helps organizations modernize legacy COBOL applications by automatically extracting and cataloging business requirements from source code. It uses natural language processing and vector embeddings to make legacy business logic searchable and analyzable.

### Key Features

- **COBOL Parsing**: Extracts business rules from comments, logic patterns, and data definitions
- **Vector Search**: Semantic similarity search using SentenceTransformers
- **GitHub Copilot Integration**: Enhanced pattern recognition with AI assistance
- **No External LLMs**: Works entirely with local models and GitHub Copilot
- **Web Interface**: Simple UI for file uploads and requirement searches
- **REST API**: Programmatic access for integration with other tools

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Docker (for Qdrant vector database)
- GitHub Copilot extension (optional, for enhanced analysis)

### Installation

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd cobol-requirements-extraction
   pip install -r requirements.txt
   ```

2. **Start the vector database:**
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

3. **Start the API server:**
   ```bash
   python cobol_requirements_api.py
   ```

4. **Access the web interface:**
   Open http://localhost:8000 in your browser

## 📁 Project Structure

```
├── cobol_requirements_extractor.py  # Core COBOL parsing and extraction engine
├── cobol_requirements_api.py        # FastAPI web service
├── cobol_requirements_analysis.ipynb # Jupyter notebook for analysis
├── static/index.html                # Web interface
├── sample_customer_validation.cbl   # Example COBOL program
├── requirements.txt                 # Python dependencies
└── .github/copilot-instructions.md  # GitHub Copilot guidance
```

## 🔧 Usage

### 1. Upload COBOL Files

Use the web interface to upload `.cbl`, `.cob`, `.cobol`, or `.txt` files containing COBOL programs.

### 2. Analyze Code

The system extracts:
- **Business Rules**: From comments and IF-THEN-ELSE logic
- **Data Definitions**: PIC clauses and data structures
- **File Operations**: OPEN, READ, WRITE, CLOSE statements
- **Procedures**: Paragraph and section names
- **Validation Logic**: Data validation patterns

### 3. Search Requirements

Use natural language queries to find similar requirements:
- "customer validation logic"
- "credit limit checking"
- "file processing operations"
- "data validation rules"

### 4. API Integration

REST endpoints for programmatic access:

```bash
# Upload COBOL file
curl -X POST -F "file=@program.cbl" http://localhost:8000/upload-cobol

# Search requirements
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "customer validation", "limit": 5}' \
  http://localhost:8000/search-requirements

# Get all requirements
curl http://localhost:8000/list-all-requirements
```

## 🤖 GitHub Copilot Integration

This project is designed to work with GitHub Copilot for enhanced analysis:

### Effective Prompting Strategies

1. **COBOL-Specific Context:**
   ```
   // Extract COBOL business rules from comments and logic
   # Parse COBOL DATA DIVISION for field definitions
   // Improve regex patterns for COBOL paragraph identification
   ```

2. **Pattern Enhancement:**
   ```
   // Create regex to match COBOL paragraph names
   # Extract validation rules from COBOL PERFORM statements
   // Parse COBOL SELECT statements for file operations
   ```

3. **Domain Knowledge:**
   ```
   // Using COBOL standards, suggest better parsing for PICTURE clauses
   # Based on mainframe conventions, improve file name detection
   ```

### Fine-tuning with Copilot

Ask GitHub Copilot to help improve:
- Regex patterns for COBOL syntax recognition
- Business rule extraction from comments
- Data validation pattern detection
- Error handling for malformed COBOL

## 📊 Analysis and Visualization

The Jupyter notebook (`cobol_requirements_analysis.ipynb`) provides:

- Interactive analysis workflow
- Visualization dashboards
- Batch processing capabilities
- Fine-tuning tools and feedback collection
- GitHub Copilot integration examples

## 🔍 Supported COBOL Patterns

### Business Logic
- IF-THEN-ELSE statements
- PERFORM-UNTIL loops
- COMPUTE operations
- Data validation rules

### Data Structures
- PIC clauses and data types
- Level numbers and hierarchies
- Working storage definitions
- File record layouts

### Comments and Requirements
- Business rule comments (starting with *)
- Requirement specifications
- Functional descriptions
- Validation constraints

## ⚙️ Configuration

### Similarity Thresholds
Adjust search sensitivity in the extractor:
```python
# Higher threshold = stricter matching
results = extractor.search_similar_requirements(query, threshold=0.8)
```

### File Encoding Support
The system handles multiple encodings commonly used in legacy systems:
- UTF-8
- CP1252 (Windows-1252)
- ASCII
- ISO-8859-1

## 🔧 Troubleshooting

### Common Issues

1. **Qdrant Connection Error**
   - Ensure Docker is running: `docker ps`
   - Check Qdrant status: http://localhost:6333/dashboard

2. **File Encoding Issues**
   - The system tries multiple encodings automatically
   - Convert files to UTF-8 if problems persist

3. **Low Search Results**
   - Lower the similarity threshold
   - Try different query phrasings
   - Check if requirements were extracted from uploaded files

### Performance Tips

- Process large COBOL codebases in batches
- Use parallel processing for directory analysis
- Adjust embedding chunk sizes for memory efficiency

## 🚀 Next Steps

1. **Scale for Enterprise**: Batch process entire COBOL codebases
2. **Custom Patterns**: Adapt extraction patterns for specific COBOL dialects
3. **Integration**: Connect with documentation and modernization tools
4. **Reporting**: Generate requirement traceability reports
5. **Enhancement**: Use GitHub Copilot to continuously improve extraction patterns

## 📄 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📞 Support

[Add support contact information here]