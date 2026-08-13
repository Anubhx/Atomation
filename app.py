import sys
import time
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import streamlit as st
from src.config import (
    DEFAULT_GENERATION_MODEL,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_TOP_K,
    DEFAULT_TEMPERATURE,
    NOTES_DIR,
    PERSONAL_DIR,
    PROJECT_NOTES_DIR
)
from src.key_pool import KeyPool
from src.embeddings import EmbeddingManager
from src.vector_store import VectorStore
from src.retrieval import Retriever
from src.cache import AnswerCache
from src.router import IntentRouter, AnswerSource
from src.llm import GeminiClient
from src.answer_modes import ModeHandler
from src.file_browser import get_directory_tree, read_markdown_document, save_personal_note
from src.code_browser import list_code_files, get_related_documents_for_code
from src.global_search import perform_global_search
from src.workspace import WorkspaceManager
from src.usage import UsageTracker
from src.document_loader import load_all_knowledge_documents

# Streamlit Page Config
st.set_page_config(
    page_title="QE Copilot — Enterprise QA & ERP Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Resources (Cached once per session)
@st.cache_resource
def get_shared_resources():
    key_pool = KeyPool()
    emb_mgr = EmbeddingManager(key_pool=key_pool)
    vector_store = VectorStore()
    if not vector_store.is_built():
        vector_store.load()
    retriever = Retriever(vector_store=vector_store, embedding_manager=emb_mgr)
    cache = AnswerCache()
    router = IntentRouter(retriever=retriever)
    usage = UsageTracker()
    workspace = WorkspaceManager()
    return key_pool, emb_mgr, vector_store, retriever, cache, router, usage, workspace

key_pool, emb_mgr, vector_store, retriever, cache, router, usage, workspace = get_shared_resources()

# Initialize LLM Client and Mode Handler in Session State
if "local_only" not in st.session_state:
    st.session_state.local_only = False
if "gen_model" not in st.session_state:
    st.session_state.gen_model = DEFAULT_GENERATION_MODEL
if "top_k" not in st.session_state:
    st.session_state.top_k = DEFAULT_TOP_K
if "temperature" not in st.session_state:
    st.session_state.temperature = DEFAULT_TEMPERATURE
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_doc_path" not in st.session_state:
    st.session_state.selected_doc_path = None
if "selected_code_path" not in st.session_state:
    st.session_state.selected_code_path = None

llm_client = GeminiClient(
    key_pool=key_pool,
    model_name=st.session_state.gen_model,
    local_only=st.session_state.local_only
)
mode_handler = ModeHandler(router=router, llm_client=llm_client)

if "nav_selection" not in st.session_state:
    st.session_state.nav_selection = "🏠 Home"

llm_client = GeminiClient(
    key_pool=key_pool,
    model_name=st.session_state.gen_model,
    local_only=st.session_state.local_only
)
mode_handler = ModeHandler(router=router, llm_client=llm_client)

# Helper function to process queries
def process_query(query_text: str):
    st.session_state.chat_history.append({"role": "user", "content": query_text})
    cached_res = cache.get(query_text)
    if cached_res:
        usage.log_request("cache_hit")
        answer_text = f"⚡ *(Cached Local Answer)*\n\n{cached_res['answer']}"
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer_text,
            "badge": "Normalized Query Cache"
        })
    else:
        res = mode_handler.execute_ask_mode(
            query=query_text,
            top_k=st.session_state.top_k,
            target_doc_id=st.session_state.selected_doc_path
        )
        answer_text = res["answer"]
        badge = res["source_type"]

        if res.get("used_gemini"):
            usage.log_request("gemini")
        else:
            usage.log_request("local_answer")

        cache.set(query_text, answer_text, res.get("sources", []), source_type=badge)
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer_text,
            "badge": badge
        })

# ==============================================================================
# SIDEBAR NAVIGATION & SETTINGS
# ==============================================================================
st.sidebar.title("🤖 QE Copilot")
st.sidebar.caption("Personal RAG QA & ERP Testing Assistant")

nav_choice = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "💬 Ask QE",
        "📚 Knowledge Base",
        "💻 Code Browser",
        "🔍 Global Search",
        "🧪 Test Case Generator",
        "🤖 Automation Generator",
        "🐛 Debugger",
        "🗄️ SQL Helper",
        "🔌 API Helper",
        "🏭 ERP Workflows",
        "⭐ My Workspace",
        "📊 Usage & Metrics",
        "⚙️ Settings"
    ],
    key="nav_selection"
)

st.sidebar.markdown("---")

# Quick Privacy Warning
st.sidebar.caption("🔒 **Privacy Notice**: Confidential project credentials or patient data should never be pasted into external API models.")

# ==============================================================================
# VIEW 1: HOME / DASHBOARD
# ==============================================================================
if nav_choice == "🏠 Home":
    st.title("🏠 QE Copilot Dashboard")
    st.subheader("Personal Enterprise Quality Engineering & ERP Testing Knowledge Assistant")

    col1, col2, col3, col4 = st.columns(4)

    # Document & Vector Metrics
    manifest = vector_store.manifest
    total_docs = manifest.get("total_docs", 89)
    total_chunks = manifest.get("total_chunks", 552)

    with col1:
        st.metric("KB Documents", f"{total_docs} files")
    with col2:
        st.metric("Vector Chunks", f"{total_chunks} chunks")
    with col3:
        usage_sum = usage.get_summary()
        st.metric("Cache Hits", usage_sum.get("cache_hits", 0))
    with col4:
        st.metric("Local Fast Answers", usage_sum.get("local_answers", 0))

    st.markdown("---")
    st.markdown("### 🚀 Quick Access Modes & Features")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.info("💬 **Ask QE**\n\nAsk questions about P2P workflows, 3-way matching, Playwright locators, pytest fixtures, and SQL verification.")
        if st.button("Go to Ask QE 💬", key="dash_btn_ask"):
            st.session_state.nav_selection = "💬 Ask QE"
            st.rerun()
    with col_b:
        st.success("📚 **Knowledge Base Browser**\n\nExplore 89+ structured QA Markdown guides across 26 modules with frontmatter metadata & search.")
        if st.button("Browse Knowledge Base 📚", key="dash_btn_kb"):
            st.session_state.nav_selection = "📚 Knowledge Base"
            st.rerun()
    with col_c:
        st.warning("💻 **Code Browser**\n\nBrowse test code files and automatically see linked QA documentation and perform AI code reviews.")
        if st.button("Open Code Browser 💻", key="dash_btn_code"):
            st.session_state.nav_selection = "💻 Code Browser"
            st.rerun()

    st.markdown("---")
    st.markdown("### 📌 Pinned Workspace Shortcuts")
    pins = workspace.get_pins()
    p_cols = st.columns(min(len(pins), 5))
    for idx, pin in enumerate(pins[:5]):
        with p_cols[idx]:
            if st.button(pin["title"], key=f"home_pin_{idx}"):
                st.session_state.selected_doc_path = pin["path"]
                st.session_state.nav_selection = "📚 Knowledge Base"
                st.rerun()

# ==============================================================================
# VIEW 2: ASK QE (CHAT INTERFACE)
# ==============================================================================
elif nav_choice == "💬 Ask QE":
    st.title("💬 QE Copilot — Interactive Assistant")
    st.caption("Ask questions about Software Testing, ERP Workflows, Playwright, Pytest, SQL, and Test Design.")

    # Pre-written Clickable Quick Questions (Local Fast-Path Answers)
    st.markdown("##### 💡 Quick Sample Questions (Local Fast-Path Answers):")
    sample_q_cols = st.columns(3)
    
    with sample_q_cols[0]:
        if st.button("⚡ ERP 3-Way Match", key="sample_q_3way", use_container_width=True):
            process_query("Explain 3-way match")
            st.rerun()
        if st.button("⚡ Playwright locators", key="sample_q_locators", use_container_width=True):
            process_query("What is Playwright get_by_role syntax?")
            st.rerun()

    with sample_q_cols[1]:
        if st.button("⚡ Playwright Strict Mode Fix", key="sample_q_strict", use_container_width=True):
            process_query("How to fix Playwright strict mode error?")
            st.rerun()
        if st.button("⚡ HTTP 401 / 403 / 404 Codes", key="sample_q_http", use_container_width=True):
            process_query("What is HTTP 401 403 404?")
            st.rerun()

    with sample_q_cols[2]:
        if st.button("⚡ Pytest Fixtures", key="sample_q_pytest", use_container_width=True):
            process_query("What is pytest fixture syntax?")
            st.rerun()
        if st.button("⚡ SQL JOIN Syntax", key="sample_q_sql", use_container_width=True):
            process_query("What is SQL INNER JOIN syntax?")
            st.rerun()

    st.markdown("---")

    # Show active target doc constraint if set
    if st.session_state.selected_doc_path:
        st.info(f"🎯 **Constrained Retrieval Active**: Answering focused on `{st.session_state.selected_doc_path}`")
        if st.button("Clear Doc Constraint"):
            st.session_state.selected_doc_path = None
            st.rerun()

    # Display Chat History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "badge" in msg:
                st.caption(f"Source: {msg['badge']}")

    # Chat Input
    if user_query := st.chat_input("Ask a QE question (e.g. 'How do I test a 3-way match?' or 'Playwright get_by_role syntax')"):
        process_query(user_query)
        st.rerun()

# ==============================================================================
# VIEW 3: KNOWLEDGE BASE BROWSER
# ==============================================================================
elif nav_choice == "📚 Knowledge Base":
    st.title("📚 Knowledge Base Browser")
    
    docs = load_all_knowledge_documents()
    doc_options = {d.rel_path: d for d in docs}

    selected_rel = st.selectbox(
        "Select Document to View",
        options=sorted(list(doc_options.keys())),
        index=0 if not st.session_state.selected_doc_path else (
            sorted(list(doc_options.keys())).index(st.session_state.selected_doc_path) 
            if st.session_state.selected_doc_path in doc_options else 0
        )
    )

    if selected_rel:
        doc = doc_options[selected_rel]
        st.session_state.selected_doc_path = selected_rel

        col_action1, col_action2, col_action3 = st.columns(3)
        with col_action1:
            if st.button("🤖 Explain This Document"):
                with st.spinner("Generating document explanation..."):
                    res = mode_handler.execute_ask_mode(f"Explain the document {doc.title} and summarize key concepts and QA risks.", target_doc_id=selected_rel)
                    st.markdown("### 🤖 Document Explanation")
                    st.markdown(res["answer"])
        with col_action2:
            if st.button("💬 Ask Questions About This Document"):
                st.info(f"Target document set to `{selected_rel}`. Go to 'Ask QE' tab to ask focused questions.")
        with col_action3:
            if st.button("⭐ Pin to My Workspace"):
                workspace.add_pin(f"⭐ {doc.title}", selected_rel)
                st.success("Pinned to Workspace!")

        tab_render, tab_raw, tab_meta, tab_edit = st.tabs(["📄 Rendered Markdown", "📝 Raw Markdown", "🏷 Metadata", "✏️ Edit Personal Note"])

        with tab_render:
            st.markdown(doc.content)

        with tab_raw:
            st.code(doc.content, language="markdown")

        with tab_meta:
            st.json({
                "title": doc.title,
                "category": doc.category,
                "subcategory": doc.subcategory,
                "keywords": doc.keywords,
                "audience": doc.audience,
                "difficulty": doc.difficulty,
                "doc_type": doc.doc_type,
                "rel_path": doc.rel_path
            })

        with tab_edit:
            if doc.doc_type == "personal":
                new_text = st.text_area("Edit Personal Note Content", value=doc.content, height=400)
                if st.button("💾 Save Personal Note"):
                    ok, msg = save_personal_note(doc.file_path, new_text)
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            else:
                st.warning("Read-Only: Only notes inside the `personal/` directory can be edited.")

# ==============================================================================
# VIEW 4: CODE BROWSER
# ==============================================================================
elif nav_choice == "💻 Code Browser":
    st.title("💻 Project Code Browser")
    
    code_files = list_code_files(BASE_DIR)
    code_options = {c["rel_path"]: c for c in code_files}

    if not code_options:
        st.info("No code files found in allowed project roots.")
    else:
        selected_code_rel = st.selectbox("Select Code File", options=sorted(list(code_options.keys())))
        if selected_code_rel:
            code_item = code_options[selected_code_rel]
            code_path = Path(code_item["path"])
            code_content = code_path.read_text(encoding="utf-8")

            col_c1, col_c2 = st.columns([3, 1])

            with col_c1:
                st.code(code_content, language="python" if code_path.suffix == ".py" else "text")

            with col_c2:
                st.markdown("### 🔗 Related Documentation")
                related_docs = get_related_documents_for_code(code_item["filename"], code_content)
                for r_doc in related_docs:
                    st.markdown(f"- 📄 `{r_doc}`")

                st.markdown("---")
                if st.button("🔍 Review This Code"):
                    with st.spinner("Performing QA Code Review..."):
                        res = mode_handler.execute_code_review(code_content, selected_code_rel)
                        st.markdown(res["answer"])

# ==============================================================================
# VIEW 5: GLOBAL SEARCH
# ==============================================================================
elif nav_choice == "🔍 Global Search":
    st.title("🔍 Global Search")
    st.caption("Search across Documentation, Code, Tests, SQL, and Templates")

    search_query = st.text_input("Enter search keywords (e.g. '3-way match', 'playwright', 'inner join'):")
    if search_query:
        results = perform_global_search(search_query)
        for cat, items in results.items():
            if items:
                st.markdown(f"### {cat} ({len(items)} matches)")
                for item in items:
                    with st.expander(f"{item.title} — `{item.path}`"):
                        st.markdown(f"**Match Type:** {item.match_type}")
                        st.markdown(f"> *{item.snippet}*")
                        if st.button(f"Open {item.title}", key=f"search_open_{item.path}"):
                            st.session_state.selected_doc_path = item.path

# ==============================================================================
# VIEW 6: TEST CASE GENERATOR
# ==============================================================================
elif nav_choice == "🧪 Test Case Generator":
    st.title("🧪 Test Case Generator Mode")
    req_input = st.text_area("Paste Business Requirement / User Story:", height=150, value="Buyer can create a Purchase Order up to $50,000 but cannot approve their own PO.")
    if st.button("Generate Test Cases"):
        with st.spinner("Generating test scenarios..."):
            res = mode_handler.execute_test_case_generator(req_input, top_k=st.session_state.top_k)
            st.markdown(res["answer"])

# ==============================================================================
# VIEW 7: AUTOMATION GENERATOR
# ==============================================================================
elif nav_choice == "🤖 Automation Generator":
    st.title("🤖 Playwright Automation Generator Mode")
    req_input = st.text_area("Paste Requirement or Manual Test Steps:", height=150, value="Navigate to ERP PO creation page, select vendor 'Acme Corp', enter line item 'Laptop', price 1200, submit PO, and verify PO status changes to 'PENDING_APPROVAL'.")
    if st.button("Generate Playwright Code"):
        with st.spinner("Generating production Playwright automation..."):
            res = mode_handler.execute_automation_generator(req_input, top_k=st.session_state.top_k)
            st.markdown(res["answer"])

# ==============================================================================
# VIEW 8: DEBUGGER
# ==============================================================================
elif nav_choice == "🐛 Debugger":
    st.title("🐛 Failure & Traceback Debugger")
    error_input = st.text_area("Paste Error Message / Playwright Traceback:", height=150, value="playwright._impl._errors.Error: locator.click: Error: strict mode violation: get_by_role('button', name='Save') resolved to 2 elements")
    if st.button("Analyze & Diagnose Failure"):
        with st.spinner("Analyzing traceback against troubleshooting KB..."):
            res = mode_handler.execute_debug_failure(error_input, top_k=st.session_state.top_k)
            st.markdown(res["answer"])

# ==============================================================================
# VIEW 9: SQL HELPER
# ==============================================================================
elif nav_choice == "🗄️ SQL Helper":
    st.title("🗄️ Database & SQL Validation Helper")
    sql_req = st.text_input("Enter Business Requirement for SQL Verification:", value="Verify purchase order line items match the total amount on the parent PO table.")
    if st.button("Generate SQL Queries"):
        with st.spinner("Generating database validation queries..."):
            res = mode_handler.execute_sql_helper(sql_req, top_k=st.session_state.top_k)
            st.markdown(res["answer"])

# ==============================================================================
# VIEW 10: API HELPER
# ==============================================================================
elif nav_choice == "🔌 API Helper":
    st.title("🔌 API Testing Helper")
    api_req = st.text_input("Enter API Endpoint / Feature Requirement:", value="POST /api/v1/purchase-orders to create new PO with line items")
    if st.button("Generate API Test Suite"):
        with st.spinner("Designing API test cases and Playwright API automation..."):
            res = mode_handler.execute_api_helper(api_req, top_k=st.session_state.top_k)
            st.markdown(res["answer"])

# ==============================================================================
# VIEW 11: ERP WORKFLOWS
# ==============================================================================
elif nav_choice == "🏭 ERP Workflows":
    st.title("🏭 Enterprise ERP Workflow Testing Guide")
    wf_choice = st.selectbox("Select ERP Workflow Module:", ["Procure-to-Pay (P2P)", "Order-to-Cash (O2C)", "3-Way Matching Engine", "RBAC & SOD Testing", "Hire-to-Retire (H2R)", "Record-to-Report (R2R)"])
    if st.button("Generate E2E ERP Test Plan"):
        with st.spinner("Generating enterprise ERP workflow strategy..."):
            res = mode_handler.execute_erp_workflow(wf_choice, top_k=st.session_state.top_k)
            st.markdown(res["answer"])

# ==============================================================================
# VIEW 12: MY WORKSPACE
# ==============================================================================
elif nav_choice == "⭐ My Workspace":
    st.title("⭐ My Workspace")
    st.caption("Pinned shortcuts to your most important cheat sheets, notes, and guides.")

    pins = workspace.get_pins()
    for idx, pin in enumerate(pins):
        col_p1, col_p2 = st.columns([4, 1])
        with col_p1:
            st.markdown(f"**{pin['title']}** (`{pin['path']}`)")
        with col_p2:
            if st.button("Unpin", key=f"unpin_{idx}"):
                workspace.remove_pin(pin['path'])
                st.rerun()

# ==============================================================================
# VIEW 13: USAGE & METRICS
# ==============================================================================
elif nav_choice == "📊 Usage & Metrics":
    st.title("📊 Usage & Cost Dashboard")
    st.caption("Lightweight local metrics tracking to help minimize API usage.")

    u_sum = usage.get_summary()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Requests", u_sum.get("total_requests", 0))
    with c2:
        st.metric("Gemini API Calls", u_sum.get("gemini_requests", 0))
    with c3:
        st.metric("Embedding API Calls", u_sum.get("embedding_requests", 0))
    with c4:
        st.metric("Cache Hits", u_sum.get("cache_hits", 0))

    st.markdown("---")
    st.markdown("### 🔑 KeyPool Health & Status")
    status_summary = key_pool.get_status_summary()
    if not status_summary:
        st.warning("No API keys loaded in key pool.")
    else:
        st.table(status_summary)

# ==============================================================================
# VIEW 14: SETTINGS
# ==============================================================================
elif nav_choice == "⚙️ Settings":
    st.title("⚙️ Assistant Settings")

    st.session_state.gen_model = st.text_input("Gemini Generation Model", value=st.session_state.gen_model)
    st.session_state.top_k = st.slider("Top K Retrieval Chunks", min_value=1, max_value=10, value=st.session_state.top_k)
    st.session_state.temperature = st.slider("Model Temperature", min_value=0.0, max_value=1.0, value=st.session_state.temperature, step=0.05)
    st.session_state.local_only = st.checkbox("Enable Local-Only Mode (Disable All Gemini API Calls)", value=st.session_state.local_only)

    st.success("Settings updated for current session!")
