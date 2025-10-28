"""
Future State Generator: Uses Chain-of-Thought prompting with LLMFallbackClient 
to generate comprehensive future state recommendations.
"""
from llm_fallback_client import LLMFallbackClient


def generate_future_state_with_llm(current_state: str, source_code: str, 
                                  business_constraints: str, architecture_preferences: str,
                                  search_query: str = ""):
    """
    Generate future state recommendations using Chain-of-Thought prompting.
    
    Args:
        current_state: The existing business requirement
        source_code: The current implementation code
        business_constraints: Business limitations and requirements
        architecture_preferences: Technology and architecture preferences
        search_query: Original search query for context
    
    Returns:
        Generated future state recommendations
    """
    try:
        client = LLMFallbackClient()
        
        # Chain-of-Thought prompting structure
        chain_of_thought_prompt = f"""
You are a senior business analyst and solution architect with expertise in digital transformation, business process optimization, and modern software architecture.

As a senior business analyst and solution architect, I need to analyze the current state and generate comprehensive future state recommendations using a systematic approach.

Let me work through this step by step:

**Step 1: Current State Analysis**
Current Business Requirement:
{current_state}

Current Source Code Implementation:
{source_code}

Analysis: Let me understand what this current implementation does, its strengths, and potential areas for improvement.

**Step 2: Context Understanding**
Original Search Query: {search_query}
This helps me understand what the user is trying to achieve or improve.

**Step 3: Constraint Evaluation**
Business Constraints to Consider:
{business_constraints}

Analysis: I need to ensure any recommendations respect these business limitations and requirements.

**Step 4: Architecture & Technology Planning**
Target Architecture Preferences:
{architecture_preferences}

Analysis: I should align recommendations with the preferred technology stack and architectural patterns.

**Step 5: Gap Analysis**
Let me identify the gaps between current state and desired future state:
- Functional gaps
- Performance gaps  
- Scalability gaps
- Security gaps
- Maintainability gaps

**Step 6: Future State Design**
Based on my analysis, here are my comprehensive recommendations:

## 🎯 Executive Summary
[Provide a clear, concise summary of the recommended future state]

## 📊 Current State Assessment
[Analyze the strengths and weaknesses of the current implementation]

## 🚀 Recommended Future State

### Business Process Improvements
[Detail how business processes should evolve]

### Technical Architecture Recommendations
[Describe the recommended technical architecture]

### Implementation Approach
[Provide step-by-step implementation guidance]

## 💰 Business Value & Benefits
[Quantify the expected benefits and ROI]

## 🛡️ Risk Assessment & Mitigation
[Identify potential risks and mitigation strategies]

## 📅 Implementation Roadmap
[Provide a phased implementation plan]

### Phase 1: Foundation (Months 1-2)
[Immediate steps to start the transformation]

### Phase 2: Core Implementation (Months 3-4)
[Main development and implementation work]

### Phase 3: Optimization & Rollout (Months 5-6)
[Testing, optimization, and deployment]

## 🔧 Technical Specifications
[Detailed technical requirements and specifications]

## 📈 Success Metrics & KPIs
[Define how success will be measured]

## 🔄 Migration Strategy
[How to transition from current to future state]

Please provide detailed, actionable recommendations that respect the business constraints while leveraging the preferred architecture and technologies.
"""

        response = client.ask(
            user_prompt=chain_of_thought_prompt,
            code=f"Current State: {current_state}\n\nSource Code: {source_code}",
            program="Future State Analysis"
        )
        
        if response.get("success"):
            # Extract text content properly from LLM response
            result_content = response.get("result")
            formatted_text = ""
            
            try:
                # Handle different response types from different providers
                if result_content and hasattr(result_content, 'text'):
                    # Gemini Content object with .text attribute
                    formatted_text = str(result_content.text)
                elif result_content and hasattr(result_content, 'parts') and getattr(result_content, 'parts', None):
                    # Gemini Content object with parts
                    parts = getattr(result_content, 'parts', [])
                    text_parts = []
                    for part in parts:
                        if hasattr(part, 'text'):
                            text_parts.append(str(getattr(part, 'text', '')))
                    formatted_text = ''.join(text_parts)
                elif isinstance(result_content, str):
                    # OpenAI returns string directly
                    formatted_text = result_content
                else:
                    # Fallback: convert to string
                    formatted_text = str(result_content) if result_content else ""
                
                # Use the LLMFallbackClient's extract_text method as backup
                if not formatted_text or len(formatted_text.strip()) == 0:
                    formatted_text = client.extract_text(response)
                
                # Ensure we return a plain string
                formatted_text = str(formatted_text) if formatted_text else "No content generated"
                
            except Exception as e:
                # If all else fails, use the extract_text method
                print(f"Error extracting text from LLM response: {e}")
                formatted_text = client.extract_text(response)
                if not isinstance(formatted_text, str):
                    formatted_text = str(formatted_text)
            
            return {"success": True, "future_state": formatted_text}
        else:
            return {"success": False, "error": response.get("error", "Future state generation failed.")}
            
    except Exception as e:
        return {"success": False, "error": f"Future state generation error: {str(e)}"}


def generate_future_state_summary(current_state: str, business_constraints: str):
    """
    Generate a quick summary of future state recommendations.
    
    Args:
        current_state: The existing business requirement
        business_constraints: Business limitations and requirements
    
    Returns:
        Brief future state summary
    """
    try:
        client = LLMFallbackClient()
        
        summary_prompt = f"""
You are a business analyst providing concise future state recommendations.

Analyze this current business requirement and provide a brief future state summary:

Current State: {current_state}
Business Constraints: {business_constraints}

Please provide:
1. Key improvement opportunities (3-5 points)
2. Recommended technology modernization
3. Expected business benefits
4. Implementation complexity (Low/Medium/High)

Keep the response concise and actionable.
"""

        response = client.ask(
            user_prompt=summary_prompt,
            code=current_state,
            program="Future State Summary"
        )
        
        if response.get("success"):
            # Extract text content properly from LLM response
            result_content = response.get("result")
            formatted_text = ""
            
            try:
                # Handle different response types from different providers
                if result_content and hasattr(result_content, 'text'):
                    # Gemini Content object with .text attribute
                    formatted_text = str(result_content.text)
                elif result_content and hasattr(result_content, 'parts') and getattr(result_content, 'parts', None):
                    # Gemini Content object with parts
                    parts = getattr(result_content, 'parts', [])
                    text_parts = []
                    for part in parts:
                        if hasattr(part, 'text'):
                            text_parts.append(str(getattr(part, 'text', '')))
                    formatted_text = ''.join(text_parts)
                elif isinstance(result_content, str):
                    # OpenAI returns string directly
                    formatted_text = result_content
                else:
                    # Fallback: convert to string
                    formatted_text = str(result_content) if result_content else ""
                
                # Use the LLMFallbackClient's extract_text method as backup
                if not formatted_text or len(formatted_text.strip()) == 0:
                    formatted_text = client.extract_text(response)
                
                # Ensure we return a plain string
                formatted_text = str(formatted_text) if formatted_text else "No summary generated"
                
            except Exception as e:
                # If all else fails, use the extract_text method
                print(f"Error extracting text from LLM response: {e}")
                formatted_text = client.extract_text(response)
                if not isinstance(formatted_text, str):
                    formatted_text = str(formatted_text)
            
            return {"success": True, "summary": formatted_text}
        else:
            return {"success": False, "error": response.get("error", "Summary generation failed.")}
            
    except Exception as e:
        return {"success": False, "error": f"Summary generation error: {str(e)}"}


# For testing
if __name__ == "__main__":
    test_current_state = """
    Customer validation process requires manual data entry and verification.
    Current system processes 100 customers per day with 2-hour average processing time.
    """
    
    test_source_code = """
    IF CUSTOMER-ID IS NOT NUMERIC
        DISPLAY 'Invalid customer ID'
        GO TO VALIDATION-ERROR
    END-IF
    
    PERFORM MANUAL-VERIFICATION
    PERFORM UPDATE-CUSTOMER-RECORD
    """
    
    test_constraints = "Budget: $100K, Timeline: 6 months, Must maintain data integrity"
    test_preferences = "Cloud-native, Microservices, API-first architecture"
    
    result = generate_future_state_with_llm(
        test_current_state, 
        test_source_code, 
        test_constraints, 
        test_preferences,
        "customer validation automation"
    )
    
    print("Future State Generation Result:")
    print(result)