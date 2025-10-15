# cobol_requirements_extractor.py

from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
import re
import os
from typing import List, Dict, Optional
import uuid
import datetime

class COBOLRequirementsExtractor:
    """
    Extract business requirements from COBOL programs and store in vector database.
    Designed to work with GitHub Copilot for intelligent analysis without third-party LLMs.
    """
    
    def __init__(self, api_key=None):
        self.collection_name = "cobol_requirements"
        self.qdrant_url = "http://localhost:6333"
        self.client = QdrantClient(url=self.qdrant_url, api_key=api_key)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Create collection if it doesn't exist"""
        try:
            self.client.get_collection(self.collection_name)
        except:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
            )
    
    def parse_cobol_file(self, file_path: str) -> Dict:
        """
        Parse COBOL file and extract structural information.
        Use this as a base for GitHub Copilot to suggest improvements.
        """
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().upper()
        
        # Basic COBOL structure extraction
        program_info = {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'program_id': self._extract_program_id(content),
            'divisions': self._extract_divisions(content),
            'data_items': self._extract_data_items(content),
            'procedures': self._extract_procedures(content),
            'business_logic': self._extract_business_logic(content),
            'file_operations': self._extract_file_operations(content),
            'comments': self._extract_comments(content)
        }
        
        return program_info
    
    def _extract_program_id(self, content: str) -> str:
        """Extract PROGRAM-ID from COBOL content"""
        match = re.search(r'PROGRAM-ID\.\s*([A-Z0-9\-]+)', content)
        return match.group(1) if match else "UNKNOWN"
    
    def _extract_divisions(self, content: str) -> Dict[str, str]:
        """Extract the four COBOL divisions"""
        divisions = {}
        
        # Extract each division section
        div_patterns = {
            'IDENTIFICATION': r'(IDENTIFICATION\s+DIVISION\..*?)(?=\n\s*[A-Z]+\s+DIVISION\.|$)',
            'ENVIRONMENT': r'(ENVIRONMENT\s+DIVISION\..*?)(?=\n\s*[A-Z]+\s+DIVISION\.|$)',
            'DATA': r'(DATA\s+DIVISION\..*?)(?=\n\s*[A-Z]+\s+DIVISION\.|$)',
            'PROCEDURE': r'(PROCEDURE\s+DIVISION\..*?)(?=$)'
        }
        
        for div_name, pattern in div_patterns.items():
            match = re.search(pattern, content, re.DOTALL)
            divisions[div_name] = match.group(1) if match else ""
        
        return divisions
    
    def _extract_data_items(self, content: str) -> List[Dict]:
        """Extract data items and their levels"""
        data_items = []
        
        # Pattern for data items (level number, name, PIC clause, etc.)
        pattern = r'^\s*(\d{2})\s+([A-Z0-9\-]+).*?PIC\s+([A-Z0-9\(\)]+)'
        
        for match in re.finditer(pattern, content, re.MULTILINE):
            data_items.append({
                'level': match.group(1),
                'name': match.group(2),
                'picture': match.group(3)
            })
        
        return data_items
    
    def _extract_procedures(self, content: str) -> List[str]:
        """Extract paragraph/section names from PROCEDURE DIVISION"""
        procedures = []
        
        # Pattern for paragraph names
        pattern = r'^\s*([A-Z0-9\-]+)\.\s*$'
        
        # Only look in PROCEDURE DIVISION
        proc_match = re.search(r'PROCEDURE\s+DIVISION\.(.*)', content, re.DOTALL)
        if proc_match:
            proc_content = proc_match.group(1)
            for match in re.finditer(pattern, proc_content, re.MULTILINE):
                procedures.append(match.group(1))
        
        return procedures
    
    def _extract_business_logic(self, content: str) -> List[str]:
        """Extract business rules and logic patterns"""
        business_rules = []
        
        # Common business logic patterns in COBOL
        patterns = [
            r'IF\s+.*?THEN.*?(?:END-IF|\.)',
            r'PERFORM\s+.*?UNTIL.*?',
            r'COMPUTE\s+.*?=.*?\.',
            r'MOVE\s+.*?TO.*?\.',
            r'ADD\s+.*?TO.*?\.',
            r'SUBTRACT\s+.*?FROM.*?\.'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            business_rules.extend(matches)
        
        return business_rules
    
    def _extract_file_operations(self, content: str) -> List[str]:
        """Extract file I/O operations"""
        file_ops = []
        
        patterns = [
            r'OPEN\s+(INPUT|OUTPUT|I-O|EXTEND)\s+([A-Z0-9\-]+)',
            r'READ\s+([A-Z0-9\-]+)',
            r'WRITE\s+([A-Z0-9\-]+)',
            r'CLOSE\s+([A-Z0-9\-]+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            file_ops.extend([f"{op[0]} {op[1]}" if len(op) > 1 else str(op) for op in matches])
        
        return file_ops
    
    def _extract_comments(self, content: str) -> List[str]:
        """Extract comments that might contain business requirements"""
        comments = []
        
        # COBOL comments start with * in column 7 or are between *> markers
        lines = content.split('\n')
        for line in lines:
            if len(line) > 6 and line[6] == '*':
                comment = line[7:].strip()
                if len(comment) > 10:  # Only meaningful comments
                    comments.append(comment)
            elif '*>' in line:
                comment = line.split('*>')[1].strip()
                if len(comment) > 10:
                    comments.append(comment)
        
        return comments
    
    def extract_requirements_from_program(self, file_path: str) -> Dict:
        """
        Main method to extract requirements from a COBOL program.
        GitHub Copilot can help enhance this with more sophisticated analysis.
        """
        program_info = self.parse_cobol_file(file_path)
        
        # Create requirement text for embedding
        requirement_text = self._create_requirement_text(program_info)
        
        # Generate embedding
        embedding = self.model.encode(requirement_text).tolist()
        
        # Store in vector database
        point_id = str(uuid.uuid4())
        
        payload = {
            'program_id': program_info['program_id'],
            'file_path': file_path,
            'file_name': program_info['file_name'],
            'requirement_text': requirement_text,
            'extracted_data': program_info,
            'extraction_timestamp': str(datetime.datetime.now())
        }
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[models.PointStruct(id=point_id, vector=embedding, payload=payload)]
        )
        
        return {
            'id': point_id,
            'program_id': program_info['program_id'],
            'requirements_extracted': len(program_info['business_logic']),
            'data_items_found': len(program_info['data_items']),
            'procedures_found': len(program_info['procedures'])
        }
    
    def _create_requirement_text(self, program_info: Dict) -> str:
        """
        Convert extracted program information into searchable text.
        This is where GitHub Copilot can help create better requirement descriptions.
        """
        parts = []
        
        # Program identification
        parts.append(f"Program: {program_info['program_id']}")
        
        # Business logic description
        if program_info['business_logic']:
            parts.append("Business Logic:")
            parts.extend(program_info['business_logic'][:5])  # Limit for embedding size
        
        # Data processing
        if program_info['data_items']:
            data_desc = f"Processes {len(program_info['data_items'])} data items"
            parts.append(data_desc)
        
        # File operations
        if program_info['file_operations']:
            file_desc = "File operations: " + " ".join(program_info['file_operations'][:3])
            parts.append(file_desc)
        
        # Comments (business requirements)
        if program_info['comments']:
            parts.append("Requirements from comments:")
            parts.extend(program_info['comments'][:3])
        
        return " | ".join(parts)
    
    def search_similar_requirements(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Search for similar requirements or programs.
        GitHub Copilot can help improve the query processing.
        """
        query_embedding = self.model.encode(query).tolist()
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit
        )
        
        return [
            {
                'program_id': result.payload.get('program_id') if result.payload else 'Unknown',
                'file_name': result.payload.get('file_name') if result.payload else 'Unknown',
                'similarity_score': result.score,
                'requirement_text': result.payload.get('requirement_text') if result.payload else ''
            }
            for result in results
        ]
    
    def get_all_requirements(self) -> List[Dict]:
        """Get all stored requirements"""
        points, _ = self.client.scroll(collection_name=self.collection_name, limit=1000)
        return [point.payload for point in points if point.payload is not None]


# Example usage for GitHub Copilot integration
def process_cobol_directory(directory_path: str, extractor: COBOLRequirementsExtractor):
    """
    Process all COBOL files in a directory.
    GitHub Copilot can suggest improvements and additional file patterns.
    """
    cobol_extensions = ['.cbl', '.cob', '.cobol', '.CBL', '.COB']
    results = []
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if any(file.endswith(ext) for ext in cobol_extensions):
                file_path = os.path.join(root, file)
                try:
                    result = extractor.extract_requirements_from_program(file_path)
                    results.append(result)
                    print(f"Processed: {file} - {result['requirements_extracted']} requirements extracted")
                except Exception as e:
                    print(f"Error processing {file}: {e}")
    
    return results


if __name__ == "__main__":
    # Example usage
    extractor = COBOLRequirementsExtractor()
    
    # Process a single file
    # result = extractor.extract_requirements_from_program("path/to/your/program.cbl")
    
    # Process entire directory
    # results = process_cobol_directory("path/to/cobol/programs", extractor)
    
    # Search for requirements
    # similar = extractor.search_similar_requirements("customer data validation")
    
    pass