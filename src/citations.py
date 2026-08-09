from typing import List, Dict, Any

def format_source_citations(sources: List[str], retrieved_chunks: List[Dict[str, Any]]) -> str:
    """Formats source document references into clean Markdown citations."""
    if not sources and not retrieved_chunks:
        return ""

    citations = ["\n---\n#### 📚 Sources & Cited Knowledge Base Documents:"]
    seen = set()

    for chunk in retrieved_chunks:
        rel_path = chunk.get("rel_path", "")
        heading = chunk.get("section_heading", "General")
        title = chunk.get("title", rel_path)
        doc_type = chunk.get("doc_type", "general")

        key = (rel_path, heading)
        if key not in seen:
            seen.add(key)
            type_badge = "📌 [Project Note]" if doc_type == "project" else ("⭐ [Personal Note]" if doc_type == "personal" else "📄 [KB Doc]")
            citations.append(f"- {type_badge} `{rel_path}` (Section: **{heading}**)")

    return "\n".join(citations)
