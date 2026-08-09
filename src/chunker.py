import re
import hashlib
from typing import List, Dict, Any
from src.document_loader import LoadedDocument

class DocumentChunk:
    def __init__(
        self,
        chunk_id: str,
        doc_id: str,
        title: str,
        category: str,
        subcategory: str,
        keywords: List[str],
        rel_path: str,
        section_heading: str,
        start_line: int,
        end_line: int,
        text: str,
        content_hash: str,
        doc_type: str = "general"
    ):
        self.chunk_id = chunk_id
        self.doc_id = doc_id
        self.title = title
        self.category = category
        self.subcategory = subcategory
        self.keywords = keywords
        self.rel_path = rel_path
        self.section_heading = section_heading
        self.start_line = start_line
        self.end_line = end_line
        self.text = text
        self.content_hash = content_hash
        self.doc_type = doc_type

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "doc_id": self.doc_id,
            "title": self.title,
            "category": self.category,
            "subcategory": self.subcategory,
            "keywords": self.keywords,
            "rel_path": self.rel_path,
            "section_heading": self.section_heading,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "text": self.text,
            "content_hash": self.content_hash,
            "doc_type": self.doc_type
        }

def compute_sha256(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

def chunk_document(doc: LoadedDocument, min_chunk_chars: int = 150, max_chunk_chars: int = 1500) -> List[DocumentChunk]:
    """
    Intelligent semantic chunker for Markdown documents.
    Splits content along headings (H1, H2, H3) while keeping code blocks intact.
    """
    lines = doc.content.splitlines()
    if not lines:
        return []

    sections = []
    current_heading = doc.title
    current_lines = []
    current_start = 1
    in_code_block = False

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        
        # Toggle code block state
        if stripped.startswith("```"):
            in_code_block = not in_code_block
        
        # Heading match (only outside code blocks)
        is_heading = not in_code_block and re.match(r"^#{1,3}\s+(.+)$", line)

        if is_heading:
            if current_lines:
                chunk_text = "\n".join(current_lines).strip()
                if chunk_text:
                    sections.append((current_heading, current_start, idx - 1, chunk_text))
            heading_text = is_heading.group(1).strip()
            current_heading = heading_text
            current_lines = [line]
            current_start = idx
        else:
            current_lines.append(line)

    if current_lines:
        chunk_text = "\n".join(current_lines).strip()
        if chunk_text:
            sections.append((current_heading, current_start, len(lines), chunk_text))

    chunks: List[DocumentChunk] = []
    chunk_index = 0

    for heading, start, end, text in sections:
        # If section is very large, split into sub-chunks at paragraph boundaries
        if len(text) > max_chunk_chars:
            paragraphs = text.split("\n\n")
            accumulated = []
            acc_len = 0
            sub_start = start

            for para in paragraphs:
                if acc_len + len(para) > max_chunk_chars and accumulated:
                    sub_text = "\n\n".join(accumulated).strip()
                    if sub_text:
                        c_hash = compute_sha256(sub_text)
                        c_id = f"{doc.doc_id}__chunk_{chunk_index}"
                        chunks.append(DocumentChunk(
                            chunk_id=c_id,
                            doc_id=doc.doc_id,
                            title=doc.title,
                            category=doc.category,
                            subcategory=doc.subcategory,
                            keywords=doc.keywords,
                            rel_path=doc.rel_path,
                            section_heading=heading,
                            start_line=sub_start,
                            end_line=end,
                            text=sub_text,
                            content_hash=c_hash,
                            doc_type=doc.doc_type
                        ))
                        chunk_index += 1
                    accumulated = [para]
                    acc_len = len(para)
                else:
                    accumulated.append(para)
                    acc_len += len(para)

            if accumulated:
                sub_text = "\n\n".join(accumulated).strip()
                if sub_text:
                    c_hash = compute_sha256(sub_text)
                    c_id = f"{doc.doc_id}__chunk_{chunk_index}"
                    chunks.append(DocumentChunk(
                        chunk_id=c_id,
                        doc_id=doc.doc_id,
                        title=doc.title,
                        category=doc.category,
                        subcategory=doc.subcategory,
                        keywords=doc.keywords,
                        rel_path=doc.rel_path,
                        section_heading=heading,
                        start_line=sub_start,
                        end_line=end,
                        text=sub_text,
                        content_hash=c_hash,
                        doc_type=doc.doc_type
                    ))
                    chunk_index += 1
        else:
            if len(text) >= 20:  # Skip tiny whitespace fragments
                c_hash = compute_sha256(text)
                c_id = f"{doc.doc_id}__chunk_{chunk_index}"
                chunks.append(DocumentChunk(
                    chunk_id=c_id,
                    doc_id=doc.doc_id,
                    title=doc.title,
                    category=doc.category,
                    subcategory=doc.subcategory,
                    keywords=doc.keywords,
                    rel_path=doc.rel_path,
                    section_heading=heading,
                    start_line=start,
                    end_line=end,
                    text=text,
                    content_hash=c_hash,
                    doc_type=doc.doc_type
                ))
                chunk_index += 1

    return chunks
