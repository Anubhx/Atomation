from typing import List, Dict, Any

SYSTEM_PERSONA = """You are QE Copilot, an elite Senior Quality Engineer, ERP Testing SME, Playwright/Python Test Architect, and Enterprise QA Leader.

CORE OPERATING RULES:
1. Ground your answers primarily in the provided local Knowledge Base context.
2. Never invent client-specific business rules, architecture, or database schemas that are not documented.
3. Clearly distinguish between facts retrieved from the local Knowledge Base and general software engineering principles.
4. If the retrieved knowledge base context does not contain enough information to answer fully, explicitly state what is present in the KB and what is general best practice.
5. Provide actionable, high-quality Playwright Python / Pytest code using accessibility-first locators (`get_by_role`, `get_by_label`) where appropriate.
6. Provide concrete risk assessments, edge cases, and list items to verify with Business Analysts (BA) or development team.
7. Maintain a clean, structured, enterprise-grade response format.
"""

ANSWER_TEMPLATE = """
### 🎯 Direct Answer
{direct_answer}

### 💡 Why It Matters
{why_it_matters}

### 🛠️ Recommended Approach & Step-by-Step Strategy
{recommended_approach}

### 💻 Automation / Code Example (if applicable)
{code_example}

### ⚠️ Risks & Edge Cases
{risks}

### 📋 Things to Verify with Project Team / BA
{things_to_verify}
"""

def build_rag_prompt(query: str, retrieved_chunks: List[Dict[str, Any]], conversation_summary: str = "") -> str:
    context_str = ""
    for idx, chunk in enumerate(retrieved_chunks, start=1):
        context_str += f"\n--- DOCUMENT SOURCE {idx}: [{chunk['rel_path']}] Heading: {chunk['section_heading']} ---\n"
        context_str += f"Title: {chunk['title']} | Category: {chunk['category']} | Subcategory: {chunk['subcategory']}\n"
        context_str += f"Content:\n{chunk['text']}\n"

    prompt = f"""
{SYSTEM_PERSONA}

CONVERSATION SUMMARY / CONTEXT:
{conversation_summary if conversation_summary else "No prior history."}

LOCAL KNOWLEDGE BASE RETRIEVED CONTEXT:
{context_str if context_str else "No relevant documents retrieved from local knowledge base."}

USER QUERY:
{query}

INSTRUCTIONS:
Synthesize a comprehensive, senior-level response following the structured format:
1. Direct Answer
2. Why It Matters
3. Recommended Approach & Strategy
4. Code / Example (if applicable)
5. Risks & Edge Cases
6. Things to Verify
"""
    return prompt

def build_test_case_generator_prompt(requirement: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    context_str = "\n".join([f"[{c['rel_path']}] {c['text']}" for c in retrieved_chunks])
    return f"""
{SYSTEM_PERSONA}

Generate enterprise-grade test scenarios for the following requirement:

REQUIREMENT:
{requirement}

LOCAL KB CONTEXT:
{context_str}

Format the response with a markdown table containing:
- Test ID
- Scenario Description
- Preconditions
- Test Data
- Test Steps
- Expected Result
- Priority (P1/P2/P3)
- Risk Level
- Automation Candidate (Yes/No & Reason)
"""

def build_automation_generator_prompt(requirement: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    context_str = "\n".join([f"[{c['rel_path']}] {c['text']}" for c in retrieved_chunks])
    return f"""
{SYSTEM_PERSONA}

Generate production-ready Playwright Python + Pytest automation for the requirement below.

REQUIREMENT:
{requirement}

LOCAL KB CONTEXT:
{context_str}

INCLUDE:
1. Recommended Automation Level (UI vs API vs DB)
2. Production-grade Playwright Python Code (Page Object Model or fixture-based)
3. Accessibility-first Locator Strategy explanation
4. Strong assertions & wait strategy
5. Required test data
6. Potential flakiness risks & prevention
"""

def build_debug_failure_prompt(error_message: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    context_str = "\n".join([f"[{c['rel_path']}] {c['text']}" for c in retrieved_chunks])
    return f"""
{SYSTEM_PERSONA}

Analyze this test failure / traceback and provide diagnosis and fix:

ERROR TRACEBACK / MESSAGE:
{error_message}

LOCAL KB TROUBLESHOOTING CONTEXT:
{context_str}

PROVIDE:
1. What Failed (Root cause analysis)
2. Likely Cause
3. Step-by-Step Diagnostic Guide
4. Concrete Code Fix / Patch
5. Prevention Best Practices
"""

def build_sql_helper_prompt(requirement: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    context_str = "\n".join([f"[{c['rel_path']}] {c['text']}" for c in retrieved_chunks])
    return f"""
{SYSTEM_PERSONA}

Generate SQL validation queries for testing this business requirement:

REQUIREMENT:
{requirement}

LOCAL KB CONTEXT:
{context_str}

PROVIDE:
1. Suggested SQL Queries for data verification
2. Explanation of query logic
3. Conceptual tables involved
4. Data integrity & boundary caveats
(Explicitly note that table and column names should be matched to the actual target project schema).
"""

def build_api_helper_prompt(requirement: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    context_str = "\n".join([f"[{c['rel_path']}] {c['text']}" for c in retrieved_chunks])
    return f"""
{SYSTEM_PERSONA}

Design an API testing strategy and automation suite:

REQUIREMENT:
{requirement}

LOCAL KB CONTEXT:
{context_str}

PROVIDE:
1. Target Endpoint, Method, Headers, Request Body
2. Expected Response & Status Codes
3. Positive Test Scenarios
4. Negative & Security Test Scenarios
5. Playwright Python API Request Automation Code
"""

def build_erp_workflow_prompt(workflow_name: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    context_str = "\n".join([f"[{c['rel_path']}] {c['text']}" for c in retrieved_chunks])
    return f"""
{SYSTEM_PERSONA}

Provide an end-to-end ERP Workflow Testing Guide for:

WORKFLOW:
{workflow_name}

LOCAL KB CONTEXT:
{context_str}

PROVIDE:
1. Actors & Roles involved (SOD matrix)
2. End-to-End Business Flow Steps
3. Key Test Scenarios
4. Test Data Requirements
5. Integrations & Interfaces
6. 3-Way Validation Strategy (UI, API, DB)
7. High-Risk Compliance & Financial Areas
"""

def build_codegen_cleaner_prompt(codegen_output: str) -> str:
    return f"""
{SYSTEM_PERSONA}

Transform the following messy Playwright Codegen output into clean, robust, production-style Playwright Python + Pytest code.

CODEGEN OUTPUT:
{codegen_output}

REFACTOR RULES:
- Replace fragile CSS/XPath selectors with accessibility-first locators (`get_by_role`, `get_by_label`, `get_by_test_id`).
- Use `exact=True` where text collision is possible.
- Remove hardcoded `page.wait_for_timeout()`.
- Add explicit assertions (`expect(locator)...`).
- Explain locator decisions and potential POM structure.
"""

def build_code_review_prompt(code_content: str, file_path: str) -> str:
    return f"""
{SYSTEM_PERSONA}

Perform a rigorous QA Code Review on this test automation file:

FILE PATH: {file_path}

CODE CONTENT:
{code_content}

EVALUATE:
- Locator quality
- Assertions strength
- Wait strategy & dynamic waits
- Test isolation & fixture usage
- Page Object Model & maintainability
- Flakiness risks & security / hardcoded secrets

OUTPUT FORMAT:
- Overall Verdict: GOOD | ⚠️ IMPROVE | ❌ PROBLEM
- Summary Findings
- Specific Issues & Lines
- Improved Refactored Code
"""
