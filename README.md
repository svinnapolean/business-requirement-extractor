# Business Rule Extractor Agent AI

Enterprise-grade COBOL requirements extraction and modernization assistant powered by advanced AI agents and vector search technology.

## 🎯 System Overview

This comprehensive AI-powered system modernizes legacy COBOL applications through intelligent business rule extraction, semantic search, and AI-driven future state recommendations. It combines traditional parsing with cutting-edge LLM capabilities to transform legacy codebases into searchable knowledge bases and generate modernization roadmaps.

### 🌟 Core Capabilities

- **🤖 AI Agent Extraction**: Advanced LLM-powered analysis using OpenAI and Gemini models with intelligent fallback
- **📊 Vector Database Storage**: Qdrant-based semantic search with 384-dimensional embeddings
- **🔍 Knowledge Base Explorer**: Interactive search and discovery of extracted business requirements
- **🚀 Future State Generation**: Chain-of-Thought AI prompting for modernization recommendations
- **⚡ Multi-LLM Support**: OpenAI → Gemini automatic failover for uninterrupted service
- **🎨 Modern Web Interface**: ChatGPT-style UI with markdown rendering and responsive design
- **🔌 REST API Integration**: Complete programmatic access for enterprise workflows
- **📈 Business Intelligence**: Advanced analytics and insights from legacy codebase patterns

## 🏗️ System Architecture

```
COBOL Files → AI Agent Extractor → Vector Database → Knowledge Explorer → Future State Generator
     ↓              ↓                    ↓               ↓                    ↓
 (Legacy Code) → (LLM Analysis) → (Semantic Search) → (Discovery UI) → (Modernization AI)
```

### Technology Stack

- **Backend**: FastAPI with async support
- **AI Models**: OpenAI GPT-4, Google Gemini Pro (with fallback)
- **Vector DB**: Qdrant with SentenceTransformers (all-MiniLM-L6-v2)
- **Frontend**: Modern HTML5/CSS3/JavaScript with marked.js
- **Orchestration**: Agent-based architecture with Chain-of-Thought prompting

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ with pip
- Docker Desktop (for Qdrant vector database)
- API Keys: OpenAI API key and/or Google Gemini API key
- Modern web browser (Chrome, Firefox, Edge)

### Installation & Setup

1. **Clone and install dependencies:**

   ```bash
   git clone <repository-url>
   cd business-rule-extractor-agent
   pip install -r requirements.txt
   ```
2. **Configure LLM API keys:**
   Edit `llm_config.json`:

   ```json
   {
     "openai_api_key": "your-openai-api-key-here",
     "gemini_api_key": "your-gemini-api-key-here"
   }
   ```
3. **Start the vector database:**

   ```bash
   docker run -p 6333:6333 -d qdrant/qdrant
   ```
4. **Launch the AI system:**

   ```bash
   python cobol_requirements_api.py
   ```
5. **Access the web interfaces:**

   - **Agent Extractor**: http://localhost:8000/static/agent_extractor.html
   - **Knowledge Base Explorer**: http://localhost:8000/static/future_state.html
   - **API Documentation**: http://localhost:8000/docs

## 📁 System Components

```
├── 🤖 AI Extraction Engine
│   ├── agent_extractor.py              # LLM-powered business rule extraction
│   ├── cobol_requirements_extractor.py # Traditional COBOL parsing engine
│   └── llm_fallback_client.py          # Multi-provider LLM client with failover
│
├── 🌐 Web Services
│   ├── cobol_requirements_api.py       # FastAPI backend with all endpoints
│   └── future_state_generator.py       # Chain-of-Thought AI generation
│
├── 🎨 User Interfaces
│   ├── static/agent_extractor.html     # Main extraction and analysis UI
│   ├── static/future_state.html        # Knowledge Base Explorer & Future State
│   └── static/index.html               # Legacy simple interface
│
├── 📊 Analysis & Configuration
│   ├── cobol_requirements_analysis.ipynb # Jupyter analysis notebooks
│   ├── llm_config.json                 # LLM API configuration
│   ├── requirements.txt                # Python dependencies
│   └── sample_customer_validation.cbl  # Example COBOL program
│
└── 📚 Documentation
    ├── README.md                       # This comprehensive guide
    └── .github/copilot-instructions.md # GitHub Copilot integration rules
```

## 🎯 User Workflows

### 1. AI-Powered Code Analysis

**Agent Extractor Interface** (`/static/agent_extractor.html`):

1. Upload COBOL files or paste code directly
2. AI agents analyze and extract business requirements using LLM intelligence
3. View structured results with business rules, data definitions, and logic patterns
4. Results automatically stored in vector database for future search

### 2. Knowledge Base Exploration

**Knowledge Explorer Interface** (`/static/future_state.html`):

1. Search existing requirements using semantic similarity
2. Browse and filter extracted business rules
3. Select requirements for modernization analysis
4. Access comprehensive knowledge base of all extracted rules

### 3. Future State Generation

**AI Modernization Assistant**:

1. Select extracted requirements from knowledge base
2. Specify business constraints and architecture preferences
3. Generate detailed modernization recommendations using Chain-of-Thought AI
4. Receive step-by-step transformation roadmaps and technology suggestions

## 🔧 Advanced Features

### Multi-LLM Intelligence

- **Primary**: OpenAI GPT-4 for high-quality analysis
- **Fallback**: Google Gemini Pro for quota resilience
- **Automatic**: Seamless switching based on API availability

### Vector Database Capabilities

- **Collection**: `cobol_requirements` with 384-dimensional embeddings
- **Search**: Semantic similarity with configurable thresholds (0.5-0.95)
- **Storage**: Persistent across sessions with full metadata

### Chain-of-Thought Prompting

## 🛠️ API Reference

### Core Endpoints

| Endpoint                   | Method | Description                             |
| -------------------------- | ------ | --------------------------------------- |
| `/extract-with-agent`    | POST   | AI-powered extraction with LLM analysis |
| `/search-requirements`   | GET    | Semantic search in vector database      |
| `/list-all-requirements` | GET    | Retrieve all stored requirements        |
| `/generate-future-state` | POST   | AI modernization recommendations        |
| `/upload-cobol`          | POST   | Traditional file upload and parsing     |
| `/stats`                 | GET    | System statistics and metrics           |

### AI Agent Extraction

**Endpoint**: `POST /extract-with-agent`

```json
{
  "cobol_code": "IDENTIFICATION DIVISION...",
  "additional_context": "Customer validation module"
}
```

**Response**: Comprehensive business rule analysis with metadata storage.

### Semantic Search

**Endpoint**: `GET /search-requirements?query=customer+validation&limit=10`

**Response**: Vector similarity results with relevance scores.

### Future State Generation

**Endpoint**: `POST /generate-future-state`

```json
{
  "selected_requirements": ["req_id_1", "req_id_2"],
  "business_constraints": "Cloud-first, microservices",
  "architecture_preferences": "Event-driven, containerized"
}
```

**Response**: Chain-of-Thought modernization roadmap.

## 🧠 AI Integration Details

### LLM Configuration

**File**: `llm_config.json`

```json
{
  "openai_api_key": "sk-...",
  "gemini_api_key": "AIza...",
  "default_model": "gpt-4",
  "fallback_model": "gemini-pro",
  "max_tokens": 4000,
  "temperature": 0.3
}
```

### Prompt Engineering

**Business Rule Extraction**:

```
Analyze this COBOL code and extract:
1. Business rules and validation logic
2. Data flow and transformations
3. Integration points and dependencies
4. Modernization opportunities
```

**Future State Generation**:

```
Given business requirements: {requirements}
Business constraints: {constraints}
Architecture preferences: {preferences}

Provide step-by-step modernization analysis...
```

## 📊 Analytics & Insights

### System Statistics

- Total requirements extracted
- Vector database size and performance
- LLM usage and fallback metrics
- Search query patterns and effectiveness

### Business Intelligence

- Common business rule patterns
- Legacy system complexity metrics
- Modernization readiness assessment
- Technology mapping recommendations

## 🚨 Troubleshooting

### Common Issues

**Qdrant Connection Errors**:

```bash
# Check Qdrant status
curl http://localhost:6333/dashboard
# Restart if needed
docker restart <qdrant-container-id>
```

**LLM API Failures**:

- Verify API keys in `llm_config.json`
- Check quota limits and billing status
- Monitor fallback mechanism in logs

**Vector Search Issues**:

- Adjust similarity thresholds (0.5-0.95)
- Verify embedding model compatibility
- Check collection status in Qdrant

### Performance Optimization

**Large Codebase Processing**:

- Use batch processing for directories
- Implement parallel file processing
- Configure memory-efficient embedding

**Search Performance**:

- Optimize vector dimensions
- Use appropriate similarity thresholds
- Implement result caching

## 🔒 Security Considerations

### API Key Management

- Store keys securely in `llm_config.json`
- Use environment variables in production
- Implement key rotation procedures

### Data Privacy

- Local vector storage (no external data sharing)
- Configurable data retention policies
- COBOL code processed locally first

### Access Control

- Implement authentication for production
- Add rate limiting for API endpoints
- Monitor usage patterns and anomalies

## 🎓 Advanced Usage

### Jupyter Analysis Workflow

**File**: `cobol_requirements_analysis.ipynb`

1. **Batch Processing**: Analyze entire COBOL directories
2. **Pattern Analysis**: Identify common business rule structures
3. **Visualization**: Generate insights and trend reports
4. **Export**: Create modernization documentation

### Custom Pattern Recognition

**Enhance extraction patterns**:

```python
# Add domain-specific COBOL patterns
custom_patterns = {
    'validation_rules': r'IF\s+.*\s+NOT\s+VALID',
    'calculation_logic': r'COMPUTE\s+.*\s+ROUNDED',
    'file_handling': r'(OPEN|READ|WRITE|CLOSE)\s+.*'
}
```

### Integration Examples

**Enterprise Workflow**:

```python
# Automated modernization pipeline
from cobol_requirements_api import extract_requirements
from future_state_generator import generate_roadmap

# Extract from legacy system
requirements = extract_requirements(cobol_directory)
# Generate modernization plan  
roadmap = generate_roadmap(requirements, constraints)
```

## 🚀 Deployment

### Production Setup

**Docker Deployment**:

```bash
# Build application container
docker build -t cobol-extractor .

# Deploy with docker-compose
docker-compose up -d
```

**Cloud Deployment**:

- Azure Container Instances
- AWS ECS with Fargate
- Google Cloud Run

### Monitoring & Observability

**Health Checks**:

- API endpoint availability
- Vector database connectivity
- LLM service responsiveness

**Metrics Collection**:

- Extraction processing times
- Search query performance
- AI generation success rates

## 🤝 Contributing

### Development Guidelines

1. **Code Style**: Follow PEP 8 for Python code
2. **Testing**: Add unit tests for new features
3. **Documentation**: Update README for major changes
4. **AI Integration**: Test with both OpenAI and Gemini models

### GitHub Copilot Enhancement

**Optimization Prompts**:

- `# Improve COBOL parsing accuracy for business rules`
- `// Enhance vector search relevance scoring`
- `# Add Chain-of-Thought prompt optimization`

### Feature Requests

**Roadmap Items**:

- Multi-language legacy code support
- Advanced visualization dashboards
- Enterprise SSO integration
- Real-time collaborative analysis

## 📞 Support

### Resources

- **Documentation**: Complete API docs at `/docs`
- **Examples**: Sample COBOL files and analysis notebooks
- **Community**: GitHub Discussions for Q&A

### Contact
- **GitHub**: [@svinnapolean](https://github.com/svinnapolean)
- **Repository**: [business-requirement-extractor](https://github.com/svinnapolean/business-requirement-extractor)
- **Issues**: [GitHub issue tracker](https://github.com/svinnapolean/business-requirement-extractor/issues)
- **Enhancements**: [Feature request templates](https://github.com/svinnapolean/business-requirement-extractor/issues/new)
- **Enterprise**: Contact [@svinnapolean](https://github.com/svinnapolean) for commercial licensing

---

## 🎯 Success Stories

Transform your legacy COBOL applications into modern, maintainable systems with AI-powered analysis and intelligent modernization recommendations. This system bridges the gap between legacy expertise and modern architecture, enabling organizations to:

- **Accelerate Legacy Modernization** with AI-driven business rule extraction
- **Preserve Business Knowledge** through comprehensive requirement documentation
- **Enable Informed Architecture Decisions** with Chain-of-Thought AI analysis
- **Reduce Modernization Risk** through systematic requirement traceability

**Start your modernization journey today** with the Business Rule Extractor Agent AI system.

## 📄 License

**Proprietary Software License**

Copyright (c) 2025 Vincent Susai ([@svinnapolean](https://github.com/svinnapolean)). All rights reserved.

This software is private and proprietary. It is NOT open source software. 

**Key License Terms:**
- ✅ **Internal Business Use**: Permitted for your organization's internal purposes
- ❌ **No Distribution**: Cannot be shared, sold, or transferred to third parties  
- ❌ **No Modification**: Source code cannot be altered or derivative works created
- ❌ **No Reverse Engineering**: Disassembly or decompilation prohibited
- ❌ **No Commercial Redistribution**: Commercial use requires explicit written permission

**Proprietary Technology:**
- COBOL parsing algorithms and business rule extraction methods
- AI agent orchestration and Chain-of-Thought prompting techniques  
- Vector database implementation and semantic search optimization
- Multi-LLM fallback architecture and modernization recommendation engine

**Third-Party Components:** FastAPI, Qdrant, SentenceTransformers, and LLM APIs retain their respective licenses.

**Full License**: See `LICENSE` file for complete terms and conditions.

**Contact**: For licensing inquiries, permissions, or commercial use, contact [@svinnapolean](https://github.com/svinnapolean).

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

**Proprietary Software License**

Copyright (c) 2025 Vincent Susai ([@svinnapolean](https://github.com/svinnapolean)). All rights reserved.

This software is **private and proprietary**. It is NOT open source software.

**Key Terms:**
- ✅ **Internal Business Use**: Permitted for your organization's internal purposes
- ❌ **No Distribution**: Cannot be shared, sold, or transferred to third parties
- ❌ **No Modification**: Source code cannot be altered or derivative works created
- ❌ **No Reverse Engineering**: Disassembly or decompilation prohibited
- ❌ **No Commercial Redistribution**: Commercial use requires explicit written permission

**Contact**: For licensing inquiries, contact [@svinnapolean](https://github.com/svinnapolean)

Full license terms available in the `LICENSE` file.

## 🤝 Contributing

**Contribution Policy**: This is proprietary software with restricted contribution guidelines.

### For Authorized Contributors

**Development Guidelines:**
1. **Code Style**: Follow PEP 8 for Python code consistency
2. **Documentation**: Update README and docstrings for any changes
3. **Testing**: Add unit tests for new features and bug fixes
4. **AI Integration**: Test compatibility with both OpenAI and Gemini models

**Before Contributing:**
- ✅ **Authorization Required**: Contact [@svinnapolean](https://github.com/svinnapolean) for contribution permissions
- ✅ **Sign CLA**: Contributor License Agreement required for code submissions
- ✅ **Feature Discussion**: Discuss major features in GitHub Issues before implementation
- ✅ **Quality Standards**: Ensure code passes all tests and follows project patterns

**Contribution Process:**
1. **Fork & Branch**: Create feature branch from main
2. **Develop**: Implement changes following coding standards
3. **Test**: Verify functionality with sample COBOL files
4. **Document**: Update relevant documentation
5. **Pull Request**: Submit with detailed description of changes

**Enhancement Areas:**
- 🔧 **COBOL Parsing**: Improve regex patterns for legacy syntax variations
- 🤖 **AI Prompting**: Enhance Chain-of-Thought prompt optimization
- 🔍 **Vector Search**: Optimize semantic similarity algorithms
- 🎨 **UI/UX**: Improve web interface design and responsiveness
- 📊 **Analytics**: Add business intelligence and reporting features

**GitHub Copilot Integration:**
Use these prompts for AI-assisted development:
- `# Improve COBOL business rule extraction accuracy`
- `// Enhance vector search relevance scoring`
- `# Optimize Chain-of-Thought prompt structure`
- `// Add error handling for edge cases`

## 📞 Support

**Professional Support Available**

### **Community Support**
- **Documentation**: Complete guides available in this README
- **GitHub Issues**: [Report bugs and request features](https://github.com/svinnapolean/business-requirement-extractor/issues)
- **Sample Files**: Use `sample_customer_validation.cbl` for testing
- **API Documentation**: Available at `http://localhost:8000/docs` when running

### **Direct Support**
- **GitHub**: [@svinnapolean](https://github.com/svinnapolean)
- **Repository**: [business-requirement-extractor](https://github.com/svinnapolean/business-requirement-extractor)
- **Issues**: [Bug reports and feature requests](https://github.com/svinnapolean/business-requirement-extractor/issues)

### **Enterprise Support**
- **Commercial Licensing**: Contact [@svinnapolean](https://github.com/svinnapolean)
- **Custom Development**: Tailored solutions for enterprise environments
- **Training & Consultation**: COBOL modernization strategy and implementation
- **Priority Support**: Dedicated support channels for enterprise customers

### **Self-Service Resources**

**Quick Troubleshooting:**
```bash
# Check Qdrant vector database
curl http://localhost:6333/dashboard

# Verify API server
curl http://localhost:8000/stats

# Test LLM connectivity
python -c "from llm_fallback_client import LLMFallbackClient; print('✅ LLM client loaded')"
```

**Common Solutions:**
- **Vector DB Issues**: Restart Qdrant container: `docker restart <container-id>`
- **API Key Problems**: Verify `llm_config.json` configuration
- **Performance**: Adjust similarity thresholds and batch sizes
- **File Encoding**: System supports UTF-8, CP1252, ASCII, ISO-8859-1

**Support Response Times:**
- 🔴 **Critical Issues**: 24-48 hours
- 🟡 **Bug Reports**: 3-5 business days  
- 🟢 **Feature Requests**: 1-2 weeks
- 🔵 **Questions**: 1-3 business days

**Enterprise customers receive priority support with guaranteed response times.**
