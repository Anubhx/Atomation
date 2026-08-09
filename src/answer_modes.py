from typing import Dict, Any, List, Optional
from src.router import IntentRouter, AnswerSource
from src.llm import GeminiClient
from src.citations import format_source_citations
from src import prompts

QUIZ_QUESTION_BANK = [
    {
        "topic": "ERP 3-Way Match",
        "question": "What three documents are compared during an ERP Accounts Payable 3-Way Match?",
        "options": [
            "A) Purchase Order, Goods Receipt, Vendor Invoice",
            "B) Requisition, Purchase Order, Packing Slip",
            "C) Sales Order, Delivery Note, Customer Invoice",
            "D) Purchase Order, Bill of Lading, Credit Memo"
        ],
        "answer": "A) Purchase Order, Goods Receipt, Vendor Invoice",
        "explanation": "3-Way Match compares PO (ordered), Goods Receipt (received), and Vendor Invoice (billed) to authorize AP payment."
    },
    {
        "topic": "Playwright Locators",
        "question": "Which Playwright locator is recommended as the highest priority accessibility-first choice?",
        "options": [
            "A) page.locator('css=button.primary')",
            "B) page.get_by_role('button', name='Submit')",
            "C) page.locator('xpath=//button[1]')",
            "D) page.get_by_id('submit-btn')"
        ],
        "answer": "B) page.get_by_role('button', name='Submit')",
        "explanation": "get_by_role reflects how screen readers and users perceive the UI, making locators resilient to CSS/DOM changes."
    },
    {
        "topic": "Pytest Fixtures",
        "question": "Which Pytest fixture scope executes setup once per entire test suite run?",
        "options": [
            "A) scope='function'",
            "B) scope='class'",
            "C) scope='module'",
            "D) scope='session'"
        ],
        "answer": "D) scope='session'",
        "explanation": "'session' scope fixtures run once at start of test execution and teardown after all tests finish."
    }
]

class ModeHandler:
    def __init__(self, router: IntentRouter, llm_client: GeminiClient):
        self.router = router
        self.llm_client = llm_client

    def execute_ask_mode(self, query: str, top_k: int = 5, target_doc_id: Optional[str] = None) -> Dict[str, Any]:
        """Mode 1: Normal RAG Ask question."""
        decision = self.router.route(query, top_k=top_k, target_doc_id=target_doc_id)
        
        if decision.source == AnswerSource.LOCAL:
            citations_text = format_source_citations(decision.source_docs, [])
            return {
                "answer": f"{decision.answer}\n{citations_text}",
                "source_type": "LOCAL (Deterministic Fast-Path)",
                "sources": decision.source_docs,
                "used_gemini": False
            }

        # RAG + Gemini synthesis
        retrieved_raw = [c[0] for c in decision.retrieved_chunks]
        prompt = prompts.build_rag_prompt(query, retrieved_raw)
        response = self.llm_client.generate(prompt)

        citations_text = format_source_citations(decision.source_docs, retrieved_raw)
        full_answer = f"{response['text']}\n{citations_text}"

        return {
            "answer": full_answer,
            "source_type": f"RAG + Gemini ({response['slot_name']})" if response['success'] else "RAG (Local Only)",
            "sources": decision.source_docs,
            "used_gemini": response['success']
        }

    def execute_test_case_generator(self, requirement: str, top_k: int = 5) -> Dict[str, Any]:
        """Mode 2: Test Case Generator."""
        decision = self.router.route(requirement, top_k=top_k, force_rag=True)
        retrieved_raw = [c[0] for c in decision.retrieved_chunks]
        prompt = prompts.build_test_case_generator_prompt(requirement, retrieved_raw)
        response = self.llm_client.generate(prompt)
        citations_text = format_source_citations(decision.source_docs, retrieved_raw)
        return {
            "answer": f"{response['text']}\n{citations_text}",
            "sources": decision.source_docs
        }

    def execute_automation_generator(self, requirement: str, top_k: int = 5) -> Dict[str, Any]:
        """Mode 3: Automation Generator."""
        decision = self.router.route(requirement, top_k=top_k, force_rag=True)
        retrieved_raw = [c[0] for c in decision.retrieved_chunks]
        prompt = prompts.build_automation_generator_prompt(requirement, retrieved_raw)
        response = self.llm_client.generate(prompt)
        citations_text = format_source_citations(decision.source_docs, retrieved_raw)
        return {
            "answer": f"{response['text']}\n{citations_text}",
            "sources": decision.source_docs
        }

    def execute_debug_failure(self, traceback: str, top_k: int = 5) -> Dict[str, Any]:
        """Mode 4: Debug Failure."""
        decision = self.router.route(traceback, top_k=top_k, force_rag=True)
        retrieved_raw = [c[0] for c in decision.retrieved_chunks]
        prompt = prompts.build_debug_failure_prompt(traceback, retrieved_raw)
        response = self.llm_client.generate(prompt)
        citations_text = format_source_citations(decision.source_docs, retrieved_raw)
        return {
            "answer": f"{response['text']}\n{citations_text}",
            "sources": decision.source_docs
        }

    def execute_sql_helper(self, requirement: str, top_k: int = 5) -> Dict[str, Any]:
        """Mode 5: SQL Helper."""
        decision = self.router.route(requirement, top_k=top_k, force_rag=True)
        retrieved_raw = [c[0] for c in decision.retrieved_chunks]
        prompt = prompts.build_sql_helper_prompt(requirement, retrieved_raw)
        response = self.llm_client.generate(prompt)
        citations_text = format_source_citations(decision.source_docs, retrieved_raw)
        return {
            "answer": f"{response['text']}\n{citations_text}",
            "sources": decision.source_docs
        }

    def execute_api_helper(self, requirement: str, top_k: int = 5) -> Dict[str, Any]:
        """Mode 6: API Helper."""
        decision = self.router.route(requirement, top_k=top_k, force_rag=True)
        retrieved_raw = [c[0] for c in decision.retrieved_chunks]
        prompt = prompts.build_api_helper_prompt(requirement, retrieved_raw)
        response = self.llm_client.generate(prompt)
        citations_text = format_source_citations(decision.source_docs, retrieved_raw)
        return {
            "answer": f"{response['text']}\n{citations_text}",
            "sources": decision.source_docs
        }

    def execute_erp_workflow(self, workflow_name: str, top_k: int = 5) -> Dict[str, Any]:
        """Mode 7: ERP Workflow."""
        decision = self.router.route(workflow_name, top_k=top_k, force_rag=True)
        retrieved_raw = [c[0] for c in decision.retrieved_chunks]
        prompt = prompts.build_erp_workflow_prompt(workflow_name, retrieved_raw)
        response = self.llm_client.generate(prompt)
        citations_text = format_source_citations(decision.source_docs, retrieved_raw)
        return {
            "answer": f"{response['text']}\n{citations_text}",
            "sources": decision.source_docs
        }

    def execute_study_quiz(self, topic: str = "") -> Dict[str, Any]:
        """Mode 8: Study / Quiz (Uses local question bank without calling Gemini if available!)."""
        matched = [q for q in QUIZ_QUESTION_BANK if topic.lower() in q["topic"].lower() or topic.lower() in q["question"].lower()]
        if matched:
            q = matched[0]
            answer_text = f"### 🧠 Quiz Question: {q['topic']}\n\n**{q['question']}**\n\n"
            for opt in q["options"]:
                answer_text += f"- {opt}\n"
            answer_text += f"\n<details><summary>Click to reveal answer</summary>\n\n**Correct Answer:** {q['answer']}\n\n*{q['explanation']}*\n</details>"
            return {"answer": answer_text, "used_gemini": False, "sources": []}

        # Fallback to local default quiz list
        q = QUIZ_QUESTION_BANK[0]
        answer_text = f"### 🧠 Quiz Question: {q['topic']}\n\n**{q['question']}**\n\n"
        for opt in q["options"]:
            answer_text += f"- {opt}\n"
        answer_text += f"\n<details><summary>Click to reveal answer</summary>\n\n**Correct Answer:** {q['answer']}\n\n*{q['explanation']}*\n</details>"
        return {"answer": answer_text, "used_gemini": False, "sources": []}

    def execute_codegen_cleaner(self, codegen_output: str) -> Dict[str, Any]:
        """Playwright Codegen Helper."""
        prompt = prompts.build_codegen_cleaner_prompt(codegen_output)
        response = self.llm_client.generate(prompt)
        return {"answer": response["text"], "sources": ["Playwright Best Practices"]}

    def execute_code_review(self, code_content: str, file_path: str) -> Dict[str, Any]:
        """Code Review Mode."""
        prompt = prompts.build_code_review_prompt(code_content, file_path)
        response = self.llm_client.generate(prompt)
        return {"answer": response["text"], "sources": [file_path]}
