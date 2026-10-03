def format_context_chunk(chunk):
    """Format one retrieved chunk for the prompt context block."""
    return (
        f"[Source ID: {chunk.get('source_id', 'unknown')}]\n"
        f"Title: {chunk.get('title', '')}\n"
        f"Category: {chunk.get('category', '')}\n"
        f"Section: {chunk.get('section', '')}\n"
        f"{chunk.get('text', '').strip()}"
    )


def build_rag_prompt(question, context_chunks):
    """Build a structured RAG prompt from a question and retrieved context."""
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question cannot be blank.")

    if not context_chunks:
        raise ValueError("Context cannot be empty.")

    usable_chunks = [
        chunk
        for chunk in context_chunks
        if isinstance(chunk.get("text"), str)
        and chunk.get("text").strip()
    ]

    if not usable_chunks:
        raise ValueError("Context cannot be empty.")

    context = "\n\n".join(
        format_context_chunk(chunk)
        for chunk in usable_chunks
    )

    return f"""Instructions:
Answer the user's question using only the approved context.
Do not invent or assume information that is not supported by the context.
If the context does not contain enough information, identify what is missing.

Context:
{context}

Question:
{question.strip()}

Response Requirements:
- Answer concisely.
- Use only information supported by the context.
- Identify missing information when needed.
- Refer to source IDs when helpful.
"""
