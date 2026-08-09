context Build me a private, personal RAG-powered Quality Engineering / ERP Testing assistant from my existing `notes/` knowledge base.

IMPORTANT CONTEXT

I already have an Enterprise QA Knowledge Base in:

notes/

It contains approximately 89 structured Markdown documents across modules covering:

- Software Testing
- Quality Engineering
- ERP Testing
- ERP workflows
- Test Design
- API Testing
- Database / SQL Testing
- Playwright
- Pytest
- Automation Architecture
- AI-assisted testing
- CI/CD
- Security
- Healthcare / MedTech QA
- Agile
- Defect Management
- Test Data
- Performance Testing
- Integration Testing
- Production Testing
- Cheat Sheets
- Troubleshooting
- Templates
- Interview scenarios

The repository is already RAG-friendly with YAML metadata.

I want you to build a PERSONAL QA ASSISTANT around this existing knowledge base.

==================================================
1. CORE GOAL
==================================================

Build a Streamlit application that allows me to ask questions such as:

"What should I test for a purchase order approval workflow?"

"How do I test a 3-way match?"

"Give me Playwright code for this form."

"What does this Playwright strict mode error mean?"

"Which SQL query can verify this transaction?"

"What should I test when a buyer cannot approve their own PO?"

"Explain this ERP requirement."

"Generate test cases from this requirement."

"How would a senior QA engineer approach this?"

"What should I ask the BA?"

"Give me a regression checklist for this feature."

The assistant should answer primarily from my local `notes/` knowledge base.

This is a PERSONAL TOOL.

It does NOT need:
- Multi-user accounts
- SaaS architecture
- Public registration
- Enterprise billing
- Analytics
- Social features

Keep it simple, private, fast, and maintainable.

==================================================
2. TECHNOLOGY STACK
==================================================

Use:

Python
Streamlit
Google Gemini API
Google GenAI Python SDK
Local vector index
Markdown documents
Pytest for tests

Prefer a lightweight local vector database/index.

Possible implementation:

- FAISS
OR
- ChromaDB
OR
- another lightweight local vector store

Choose the simplest reliable option.

The application should work locally first.

Then make it deployable to Streamlit Community Cloud.

Do NOT introduce unnecessary infrastructure such as:
- PostgreSQL
- Redis
- Kubernetes
- Docker
- separate backend services

unless genuinely necessary.

==================================================
3. GEMINI
==================================================

Use the current official Google GenAI Python SDK.

Do NOT hardcode API keys.

Use:

st.secrets

locally through:

.streamlit/secrets.toml

and Streamlit deployment secrets in production.

The official Streamlit documentation recommends keeping secrets outside source control. Make sure `.streamlit/secrets.toml` is included in `.gitignore`.

Use the current Gemini API documentation when choosing model names and SDK APIs.

Do not hardcode obsolete model names.

Make model names configurable in configuration.

Example conceptual configuration:

GEMINI_GENERATION_MODEL
GEMINI_EMBEDDING_MODEL

Do not assume a model name without verifying the current Gemini API documentation.

==================================================
4. PERSONAL KEY POOL
==================================================

I may have multiple Gemini API keys that I legitimately own.

Implement a configurable key pool.

Example:

[gemini]
keys = [
    "KEY_1",
    "KEY_2",
    "KEY_3"
]

IMPORTANT:

This is NOT intended to bypass Google's quotas, rate limits, safety restrictions, or billing controls.

The key manager must:

- Rotate keys only when appropriate
- Detect transient rate-limit errors
- Use exponential backoff
- Avoid infinite retries
- Log which logical key slot was used, but NEVER log the actual key
- Never expose keys in the UI
- Never expose keys to the client/browser
- Never print keys
- Never commit keys
- Allow disabling a key
- Allow health status tracking

Implement:

KeyPool

with:

get_available_key()
mark_rate_limited()
mark_failed()
mark_healthy()
cooldown handling

Use a configurable maximum retry count.

Example:

MAX_RETRIES = 3

Do NOT blindly cycle through every key for every failed request.

If all keys are unavailable:

Show a useful error.

==================================================
5. VERY IMPORTANT: REDUCE GEMINI USAGE
==================================================

I specifically want the application designed to minimize unnecessary Gemini API calls.

Implement a TWO-LAYER ANSWER SYSTEM.

Layer 1:
LOCAL / DETERMINISTIC ANSWERS

Layer 2:
RAG + GEMINI

The router should first determine whether the question can be answered from local deterministic knowledge.

Examples:

"Playwright get_by_role syntax"

"HTTP 404 meaning"

"pytest fixture syntax"

"SQL INNER JOIN syntax"

"Git status command"

"Playwright codegen command"

"Common Playwright strict mode fix"

These should preferably be answered directly from local cheat sheets / structured knowledge without calling Gemini.

Only use Gemini when:
- The question requires synthesis
- Multiple documents must be combined
- The user asks for explanation
- The user asks for custom code
- The question requires reasoning
- The retrieved information needs summarization
- The user asks for scenario-specific guidance

==================================================
6. LOCAL ANSWER CACHE
==================================================

Implement semantic or normalized query caching.

If I ask:

"What is Playwright get_by_role?"

and later ask:

"Explain get_by_role"

do not automatically call Gemini again.

Use a local cache.

Cache:

- normalized question
- retrieved document IDs
- generated answer
- timestamp
- knowledge-base version

When the knowledge base changes, invalidate the affected cache.

Use a reasonable TTL or KB versioning mechanism.

==================================================
7. CHEAT SHEET FAST PATH
==================================================

Create a local intent router.

Examples:

If query contains:

playwright + locator

retrieve:

21_CHEAT_SHEETS / Playwright cheat sheet

If query contains:

HTTP + 401

retrieve:

API / HTTP status code cheat sheet

If query contains:

SQL + JOIN

retrieve:

SQL cheat sheet

If query contains:

ERP + 3-way match

retrieve:

ERP three-way match document

If query contains:

pytest + fixture

retrieve:

Pytest cheat sheet

This does NOT need to be a dumb keyword-only system.

Use a small hybrid strategy:

1. Exact/keyword rules
2. Metadata matching
3. Vector search
4. Gemini only if needed

==================================================
8. RAG PIPELINE
==================================================

Build:

Markdown files
↓
Parser
↓
Metadata extraction
↓
Chunking
↓
Embedding
↓
Vector index
↓
Retriever
↓
Reranker if useful
↓
Context builder
↓
Gemini
↓
Answer

Chunk documents intelligently.

Do NOT split blindly every N characters.

Prefer semantic chunks based on:

- H1
- H2
- H3
- code blocks
- lists
- tables

Preserve document metadata:

title
category
subcategory
keywords
difficulty
file path
section heading

Each retrieved chunk should know where it came from.

==================================================
9. INDEX BUILDING
==================================================

Create:

scripts/build_index.py

It should:

1. Scan `notes/`
2. Find Markdown files
3. Parse YAML metadata
4. Split content into chunks
5. Generate embeddings
6. Store vectors
7. Store metadata
8. Generate index manifest

Do NOT regenerate embeddings unnecessarily.

Compute a content hash.

Example:

SHA256(document content)

If content has not changed:

SKIP EMBEDDING

This is extremely important for reducing API usage.

Only embed:
- New files
- Changed files
- Deleted files require index cleanup

==================================================
10. EMBEDDING CACHE
==================================================

Store:

content_hash
embedding_model
embedding_vector
metadata

If the same chunk already exists:

DO NOT call Gemini embedding API again.

This makes rebuilding the index cheap.

==================================================
11. RETRIEVAL STRATEGY
==================================================

Default:

Top K = 5

But make configurable.

Use:

top_k = 3–5

Avoid dumping 20 documents into Gemini.

Prefer high-quality retrieval.

Use metadata filtering when possible.

For example:

Question:
"How do I test ERP approval roles?"

Prefer:

category = ERP
subcategory = RBAC

before searching the entire KB.

==================================================
12. RAG ANSWER PROMPT
==================================================

Create a strong system prompt.

The model should behave as:

Senior Quality Engineer
ERP Testing SME
Playwright/Python Automation Engineer
Enterprise QA Architect

Rules:

- Prefer retrieved knowledge
- Do not invent project-specific facts
- Clearly separate source-derived information from general knowledge
- If the knowledge base does not contain the answer, say so
- Provide practical steps
- Provide code when appropriate
- Explain why
- Mention relevant risks
- Mention what should be verified with the project team
- Never claim to know the client's actual architecture unless documented
- Never invent business rules

For answers, use:

1. Direct answer
2. Why it matters
3. Recommended approach
4. Example
5. Automation example if useful
6. Things to verify
7. Sources

==================================================
13. SOURCE CITATIONS
==================================================

Every RAG answer must show which local documents were used.

Example:

Sources:

- `03_ERP_TESTING/erp-three-way-match.md`
- `03_ERP_TESTING/erp-role-based-testing.md`

Make source names clickable in Streamlit if practical.

Also show the section heading used.

Do NOT cite documents that were not actually retrieved.

==================================================
14. UI
==================================================

Build a clean personal Streamlit UI.

Sidebar:

QA Assistant
----------------

Mode:
[Ask]
[Generate Test Cases]
[Generate Automation]
[Debug Failure]
[Explain Requirement]
[SQL Helper]
[API Helper]
[ERP Workflow]
[Study / Quiz]

Settings:
- Gemini model
- Top K
- Temperature
- Enable RAG
- Use Gemini
- Show sources
- Debug retrieval

Main screen:

Title:
"QE Copilot"

Subtitle:
"Personal Enterprise QA & ERP Testing Assistant"

Chat interface.

Use:

st.chat_input()

Use:

st.chat_message()

==================================================
15. MODES
==================================================

Implement special modes.

MODE 1 — ASK

Normal RAG question.

MODE 2 — TEST CASE GENERATOR

Input:

Requirement

Output:

Test ID
Scenario
Preconditions
Test Data
Steps
Expected Result
Priority
Risk
Automation Candidate

MODE 3 — AUTOMATION GENERATOR

Input:

Requirement/manual test.

Output:

Recommended automation level
Playwright/Pytest code
Locator strategy
Assertions
Test data requirements
Potential flaky points

MODE 4 — DEBUG FAILURE

Input:

Error message / traceback.

Output:

What failed
Likely cause
How to diagnose
Fix
Prevention

MODE 5 — SQL HELPER

Input:

Business requirement.

Output:

Suggested SQL validation
Explanation
Tables involved
Caveats

Clearly state that table/column names must match the actual project schema.

MODE 6 — API HELPER

Input:

API requirement.

Output:

Endpoint
Method
Headers
Request
Expected response
Positive tests
Negative tests
Security tests
Automation example

MODE 7 — ERP WORKFLOW

Input:

P2P/O2C/etc.

Output:

Actors
Business flow
Test scenarios
Roles
Data
Integrations
UI/API/DB validation
Risks

MODE 8 — STUDY / QUIZ

Generate questions from the local KB.

Do NOT use Gemini if an existing question bank can answer the request.

==================================================
16. AI AUTOMATION MODE
==================================================

Create an AI-assisted automation workflow.

Example:

Paste requirement:

"Buyer can create a PO but cannot approve their own PO."

System:

1. Retrieves ERP RBAC documentation
2. Retrieves approval workflow documentation
3. Retrieves Playwright patterns
4. Generates test scenarios
5. Generates Playwright code
6. Identifies test data
7. Identifies API/DB validation opportunities

Output:

Manual tests
+
Automation candidate
+
Playwright code
+
SQL validation
+
Risk notes

==================================================
17. PLAYWRIGHT CODEGEN HELPER
==================================================

Create a dedicated section for Playwright.

Allow me to paste Codegen output.

The assistant should transform:

messy Codegen output

into:

clean production-style Playwright + Pytest code.

It should:

- Replace fragile selectors
- Prefer get_by_role
- Prefer get_by_label
- Use exact=True where appropriate
- Remove unnecessary waits
- Add assertions
- Convert to Page Object Model when requested
- Explain locator decisions

==================================================
18. ERP KNOWLEDGE GRAPH-LIKE LINKS
==================================================

Use metadata and relationships.

Example:

Purchase Order
→ Procurement
→ P2P
→ Approval
→ RBAC
→ Inventory
→ Invoice
→ 3-Way Match

If answering a Purchase Order question, suggest related documents.

Display:

Related topics:
- Procurement
- Approval workflows
- RBAC
- Goods Receipt
- Invoice
- 3-Way Match

==================================================
19. CONVERSATION MEMORY
==================================================

Because this is a personal assistant, implement LOCAL session memory.

Remember within a session:

- Current topic
- Current ERP workflow
- Current requirement
- Current error
- Current code
- Current selected mode

Do NOT send unnecessary previous conversation to Gemini.

Summarize conversation context when needed.

Avoid massive prompts.

==================================================
20. PERSONAL NOTES
==================================================

Create a:

personal/

directory.

Allow me to store personal notes such as:

- Project terminology
- Questions for BA
- Meeting notes
- My understanding of a workflow
- Lessons learned
- Mistakes
- Useful commands
- Project-specific test cases

But clearly separate:

GENERAL KNOWLEDGE

from:

PERSONAL PROJECT NOTES

Never assume personal notes are universally correct.

==================================================
21. PROJECT-SPECIFIC KNOWLEDGE
==================================================

Allow a separate:

project_notes/

directory.

Example:

project_notes/
├── glossary.md
├── architecture.md
├── workflows.md
├── roles.md
├── environments.md
├── integrations.md
├── test-data.md
└── open-questions.md

These should be higher-priority retrieval sources when I explicitly ask project-specific questions.

But never invent their contents.

==================================================
22. PRIVACY / SAFETY
==================================================

This is a PERSONAL QA tool.

Implement privacy safeguards.

Never log:

- API keys
- passwords
- access tokens
- cookies
- patient data
- production secrets

Add a warning before sending project notes to Gemini:

"Do not paste confidential client information unless approved by your organization's policy."

Add optional local-only mode:

LOCAL_ONLY = true

When enabled:

- No Gemini calls
- Search local KB only
- Use deterministic answers where available

==================================================
23. STREAMLIT DEPLOYMENT
==================================================

Make the application deployable to Streamlit Community Cloud.

Include:

requirements.txt

.streamlit/config.toml if needed

.streamlit/secrets.toml.example

.gitignore

README deployment instructions.

Never commit:

.streamlit/secrets.toml

or API keys.

Use:

st.secrets

for deployment secrets.

==================================================
24. CACHE DESIGN
==================================================

Use Streamlit caching appropriately.

Cache:

- Parsed documents
- Vector index
- Embeddings
- Static metadata

Do not repeatedly rebuild the vector index on every Streamlit rerun.

Initialize resources once per process/session where appropriate.

Be careful with Streamlit caching and untrusted serialized data.

Only load trusted local index files.

==================================================
25. PERFORMANCE
==================================================

The application should feel fast.

Target:

Simple cheat-sheet query:
< 1 second if possible

Local retrieval:
very fast

Gemini query:
only when necessary

Do not call Gemini unnecessarily.

Show:

"Local answer"

or:

"RAG + Gemini"

in debug information.

==================================================
26. COST / USAGE DASHBOARD
==================================================

Create a small optional sidebar panel:

Today's requests
Gemini requests
Embedding requests
Cache hits
RAG searches
Local answers
Failed requests
Rate-limited requests

Do NOT display API keys.

Store lightweight local usage metrics.

==================================================
27. ERROR HANDLING
==================================================

Handle:

- Gemini API timeout
- 429
- 401
- invalid key
- model unavailable
- embedding failure
- vector index missing
- malformed Markdown
- empty query
- network unavailable

Never crash the entire Streamlit app.

Provide useful error messages.

==================================================
28. TEST SUITE
==================================================

Create pytest tests for:

- Markdown parsing
- Metadata extraction
- Chunking
- Content hashing
- Embedding cache
- Retrieval
- Keyword router
- Local answer router
- Gemini key pool
- Retry logic
- Prompt construction
- Source citations
- Mode routing

Mock Gemini API calls in unit tests.

Do not use real API keys in tests.

==================================================
29. PROJECT STRUCTURE
==================================================

Use something similar to:

qe_copilot/
│
├── app.py
│
├── notes/
│
├── project_notes/
│
├── personal/
│
├── src/
│   ├── config.py
│   ├── router.py
│   ├── rag.py
│   ├── retrieval.py
│   ├── embeddings.py
│   ├── llm.py
│   ├── key_pool.py
│   ├── cache.py
│   ├── prompts.py
│   ├── answer_modes.py
│   ├── document_loader.py
│   ├── chunker.py
│   └── citations.py
│
├── scripts/
│   ├── build_index.py
│   └── rebuild_index.py
│
├── data/
│   ├── vector_index/
│   └── cache/
│
├── tests/
│
├── .streamlit/
│   └── secrets.toml.example
│
├── requirements.txt
├── .gitignore
└── README.md

Keep the implementation modular.

==================================================
30. IMPORTANT: DO NOT OVERENGINEER
==================================================

This is a personal project.

Prefer:

simple
fast
reliable
understandable

over:

enterprise microservices
complex infrastructure
unnecessary databases
over-engineered abstractions

I should be able to open the project six months later and understand it.

==================================================
31. FINAL UX
==================================================

When I ask:

"What is 3-way matching?"

The app should preferably answer locally.

When I ask:

"Create 15 test cases for this specific P2P workflow and explain which ones should be automated with Playwright."

The app should retrieve relevant documents and use Gemini.

When I paste:

Playwright traceback

the app should retrieve troubleshooting + Playwright docs and explain the failure.

When I paste:

a requirement

the app should retrieve relevant ERP/test-design docs and generate a QA approach.

==================================================
32. FINAL DELIVERABLE
==================================================

Implement the application.

Do NOT merely describe it.

Create the actual files.

Run the test suite.

Fix errors.

Verify:

1. App starts
2. Index loads
3. Local retrieval works
4. Cheat-sheet fast path works
5. Gemini integration works when configured
6. Key pool works
7. Retry logic works
8. Cache works
9. Sources are displayed
10. Test suite passes

Finally provide:

- Folder tree
- Setup commands
- Required packages
- Environment/secrets setup
- Index build command
- Local run command
- Streamlit deployment instructions
- Example questions
- Architecture explanation
- Known limitations

Do not expose or print any API keys during setup or testing.==================================================
33. BUILT-IN KNOWLEDGE BASE / CODE BROWSER
==================================================

The Streamlit application must also act as a browser for my local
QA knowledge repository.

I want to be able to explore the actual files from inside Streamlit.

Create a "📚 Knowledge Base" section.

Show the folder hierarchy:

notes/
├── 00_START_HERE/
├── 01_SOFTWARE_TESTING/
├── 02_QUALITY_ENGINEERING/
├── 03_ERP_TESTING/
├── ...
├── 21_CHEAT_SHEETS/
├── 22_TROUBLESHOOTING/
├── 23_INTERVIEW_PREPARATION/
├── 24_REAL_WORLD_SCENARIOS/
└── 25_TEMPLATES/

Allow me to:

- Browse folders
- Search filenames
- Search document content
- Open Markdown files
- Render Markdown
- View raw Markdown
- Copy Markdown content
- See document metadata
- See related documents
- See which documents were retrieved by RAG

==================================================
34. CODE BROWSER
==================================================

Create a separate "💻 Code" section.

Allow browsing of code files from the project.

Support at minimum:

.py
.sql
.yaml
.yml
.json
.js
.ts
.tsx
.sh
.toml
ini

Show:

- File tree
- File content
- Syntax highlighting
- Copy button
- Search within file
- File path
- Related documentation

For example:

automation/
├── tests/
├── pages/
├── api/
├── utils/
└── conftest.py

I should be able to click:

tests/test_purchase_order.py

and see the actual code.

==================================================
35. CODE + DOCUMENT LINKING
==================================================

When viewing a code file, show related documentation where possible.

Example:

test_purchase_order.py

Related:
- ERP Purchase Order Testing
- P2P Workflow
- Playwright Cheat Sheet
- Pytest Fixtures
- ERP Negative Scenarios

When viewing:

erp-three-way-match.md

show related:

- SQL examples
- API testing
- Invoice testing
- Purchase order testing
- Data integrity testing

==================================================
36. DOCUMENT SEARCH
==================================================

Create a global search box.

Search should search:

1. Markdown filenames
2. Markdown content
3. Code filenames
4. Code content
5. Metadata
6. Keywords

Return results grouped by:

📚 Documentation
💻 Code
🧪 Tests
🗄 SQL
📋 Templates

Each result should show:

filename
path
matching section
short snippet

Clicking a result should open the file.

==================================================
37. RAG + FILE BROWSER INTEGRATION
==================================================

When RAG retrieves a document, the answer should show:

Sources:

📄 erp-three-way-match.md
📄 erp-data-integrity.md
📄 api-testing.md

Each source should be clickable.

Clicking the source opens that exact Markdown document
inside the Streamlit application.

If possible, automatically scroll to the relevant heading.

==================================================
38. "EXPLAIN THIS FILE" FEATURE
==================================================

When I open a Markdown or code file, provide an optional:

"🤖 Explain this"

button.

If clicked:

- Analyze the selected file
- Explain it
- Identify important concepts
- Show related documents
- Highlight important QA implications

Do not call Gemini if a local deterministic explanation is already
available.

==================================================
39. "ASK ABOUT THIS FILE"
==================================================

When viewing a document, provide:

"Ask about this document"

This should constrain retrieval to:

- The selected document
- Related documents

Example:

I open:

erp-procure-to-pay.md

Then ask:

"What are the highest-risk areas?"

The assistant should prioritize that document.

==================================================
40. CODE REVIEW MODE
==================================================

When viewing a Python/Playwright test file, provide:

"🔍 Review this code"

The assistant should analyze:

- Locator quality
- Assertions
- Wait strategy
- Test isolation
- Fixture usage
- Page Object Model
- Maintainability
- Flakiness risks
- Security issues
- Hardcoded secrets
- Duplicate code
- Missing negative tests
- Missing cleanup
- Missing API/DB validation

Return:

GOOD
⚠️ IMPROVE
❌ PROBLEM

Then provide improved code.

==================================================
41. MARKDOWN EDITOR
==================================================

Allow optional editing of personal Markdown files.

Do NOT allow editing of the main knowledge base by default.

Make two modes:

READ ONLY
EDIT PERSONAL NOTES

Personal notes can be edited from Streamlit and saved locally.

For safety:

- Never overwrite files silently
- Provide Save button
- Show changed file path
- Confirm before overwriting
- Keep a backup/version if practical

==================================================
42. PROJECT DASHBOARD
==================================================

Create a dashboard showing:

Knowledge Base:
- Markdown files
- Categories
- Last indexed
- Index status

Automation:
- Python files
- Test files
- Number of tests if detectable

RAG:
- Total indexed chunks
- Last index build
- Cache hits
- Gemini calls
- Local answers
- Retrieval count

==================================================
43. FILE SECURITY
==================================================

The file browser must only allow access to explicitly configured
directories.

Do NOT allow arbitrary filesystem traversal.

Create an allowed roots configuration:

ALLOWED_ROOTS:
- notes/
- personal/
- project_notes/
- tests/
- pages/
- api/
- utils/

Reject attempts to access:

../
absolute paths
system directories
.env
secret files
credential files

Never display:

.env
secrets.toml
private keys
credentials
tokens

==================================================
44. RESPONSIVE STREAMLIT LAYOUT
==================================================

Use a clean layout.

Sidebar:

🏠 Home
💬 Ask QE
📚 Knowledge Base
💻 Code Browser
🔍 Global Search
🧪 Test Case Generator
🤖 Automation Generator
🐛 Debugger
🗄 SQL Helper
🔌 API Helper
🏭 ERP Workflows
📊 Usage
⚙️ Settings

Main content changes based on selection.

==================================================
45. PERSONAL WORKSPACE
==================================================

Create:

"⭐ My Workspace"

Allow me to pin:

- Important documents
- Frequently used cheat sheets
- Current project notes
- Frequently used code files
- Troubleshooting guides

Example:

⭐ Playwright Cheat Sheet
⭐ ERP P2P
⭐ RBAC Testing
⭐ SQL Cheat Sheet
⭐ API Status Codes
⭐ Playwright Debugging
⭐ Bug Report Template

Store pins locally.