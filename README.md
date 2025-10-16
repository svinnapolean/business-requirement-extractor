# Business Requirements Extraction System. Agentic AI
## Legacy COBOL Programme Requirements Extraction

An intelligent system that leverages Agentic AI to extract business requirements from legacy COBOL programs and store them in a vector database for intelligent search and analysis.

## 🎯 Project Overview

This system helps organizations modernize legacy COBOL applications by automatically extracting and cataloging business requirements from source code using advanced AI agents. It combines natural language processing, vector embeddings, and large language model capabilities to make legacy business logic searchable, analyzable, and understandable for modern development teams.

### Key Features

- **COBOL Parsing**: Extracts business rules from comments, logic patterns, and data definitions
- **Agentic AI Integration**: Uses LLM agents for intelligent requirement extraction and analysis
- **Vector Search**: Semantic similarity search using SentenceTransformers and Qdrant vector database
- **Multiple LLM Support**: Compatible with OpenAI, Anthropic, Azure OpenAI, and other providers
- **Fallback Mechanisms**: Robust error handling with multiple LLM provider fallbacks
- **Web Interface**: Modern UI for file uploads and requirement searches
- **REST API**: Programmatic access for integration with other tools
- **Jupyter Analysis**: Interactive notebooks for deep analysis and visualization

## 🚀 Quick Start

### Prerequisites

#### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher (3.9+ recommended)
- **Memory**: Minimum 8GB RAM (16GB recommended for large COBOL programs)
- **Storage**: At least 2GB free disk space
- **Internet**: Required for LLM API calls and package downloads

#### Required Software
- **Docker Desktop**: For running Qdrant vector database
  - Download from: https://www.docker.com/products/docker-desktop/
  - Ensure Docker is running before starting the application
- **Git**: For cloning the repository
- **Text Editor/IDE**: VS Code recommended for development

#### API Keys and Configuration
You'll need API keys from at least one of the following LLM providers:
- **OpenAI**: API key from https://platform.openai.com/
- **Anthropic**: API key from https://console.anthropic.com/
- **Azure OpenAI**: Endpoint and API key from Azure portal
- **Other providers**: As configured in `llm_config.json`

#### Python Dependencies
All Python packages are listed in `requirements.txt` and will be installed automatically:
- `fastapi`: Web framework for REST API
- `uvicorn`: ASGI server for FastAPI
- `qdrant-client`: Vector database client
- `sentence-transformers`: For text embeddings
- `openai`: OpenAI API client
- `anthropic`: Anthropic API client
- `jupyter`: For analysis notebooks
- `pandas`: Data manipulation
- `numpy`: Numerical computing
- `matplotlib`: Plotting and visualization

#### Network Requirements
- **Port 8000**: For the web interface and API server
- **Port 6333**: For Qdrant vector database
- **Port 8888**: For Jupyter notebook server (if used)
- **HTTPS Access**: For LLM API calls (OpenAI, Anthropic, etc.)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/svinnapolean/business-requirement-extractor.git
   cd business-requirement-extractor
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Use `pip3` on systems where Python 2 is also installed*

3. **Configure LLM providers:**
   - Copy `llm_config.json.template` to `llm_config.json` (if template exists)
   - Or edit `llm_config.json` directly with your API keys:
   ```json
   {
     "openai_api_key": "your_openai_api_key_here",
     "anthropic_api_key": "your_anthropic_api_key_here",
     "azure_openai_endpoint": "your_azure_endpoint_here",
     "azure_openai_key": "your_azure_key_here"
   }
   ```
   **⚠️ Security Note**: Never commit API keys to version control. Keep `llm_config.json` in your `.gitignore` file.

4. **Start the vector database:**
   ```bash
   # Start Qdrant using Docker
   docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
   ```
   *Verify Qdrant is running by visiting: http://localhost:6333/dashboard*

5. **Start the API server:**
   ```bash
   python cobol_requirements_api.py
   ```

6. **Access the web interface:**
   Open http://localhost:8000 in your browser

### Alternative Installation (Development Mode)

For development or if you want to run Jupyter notebooks:

```bash
# Install in development mode
pip install -e .

# Start Jupyter notebook server
jupyter notebook cobol_requirements_analysis.ipynb
```

## 📁 Project Structure

```
├── agent_extractor.py              # Agentic AI extraction engine
├── cobol_requirements_extractor.py # Core COBOL parsing and extraction engine
├── cobol_requirements_api.py       # FastAPI web service
├── cobol_requirements_analysis.ipynb # Jupyter notebook for analysis
├── llm_config.json                 # LLM provider configuration (keep secure!)
├── llm_fallback_client.py          # LLM client with fallback mechanisms
├── static/
│   ├── index.html                  # Main web interface
│   └── agent_extractor.html        # AI agent interface
├── sample_customer_validation.cbl  # Example COBOL program
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

## 🔧 Usage

### 1. Upload COBOL Files

Use the web interface to upload `.cbl`, `.cob`, `.cobol`, or `.txt` files containing COBOL programs. The system supports both individual files and batch uploads.

### 2. AI-Powered Analysis

The agentic AI system automatically extracts:
- **Business Rules**: From comments, documentation, and IF-THEN-ELSE logic
- **Data Definitions**: PIC clauses, data structures, and field relationships  
- **File Operations**: OPEN, READ, WRITE, CLOSE statements and file handling patterns
- **Procedures**: Paragraph and section names with their business context
- **Validation Logic**: Data validation patterns and business constraints
- **Cross-References**: Dependencies between different code sections
- **Requirements Traceability**: Links between code and business requirements

### 3. Intelligent Search

Use natural language queries powered by vector similarity search:
- "customer validation logic and credit checks"
- "file processing operations for daily batch jobs"  
- "data validation rules for account numbers"
- "business rules for loan approval process"
- "error handling patterns for transaction processing"

### 4. Agentic AI Interface

Access the specialized AI agent interface at `/agent` for:
- Interactive requirement extraction
- Contextual business rule analysis  
- Code modernization recommendations
- Legacy system documentation generation

### 5. API Integration

REST endpoints for programmatic access:

```bash
# Upload COBOL file
curl -X POST -F "file=@program.cbl" http://localhost:8000/upload-cobol

# Search requirements using vector similarity
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "customer validation", "limit": 5}' \
  http://localhost:8000/search-requirements

# AI agent extraction (requires LLM configuration)
curl -X POST -H "Content-Type: application/json" \
  -d '{"cobol_code": "your_cobol_code_here", "analysis_type": "business_rules"}' \
  http://localhost:8000/agent-extract

# Get all requirements
curl http://localhost:8000/list-all-requirements

# Health check and system status
curl http://localhost:8000/health
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