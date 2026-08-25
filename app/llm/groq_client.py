from groq import Groq

from app.config import settings

_client = Groq(api_key=settings.groq_api_key)


def generate_answer(
    question: str,
    context_chunks: list[str],
    stock_data: dict | None = None,
) -> str:
    """
    Generate an answer to the question, grounded strictly in the
    provided context chunks and, if available, live stock data.
    Refuses to guess if the available context is insufficient.
    """
    context_text = "\n\n---\n\n".join(
        f"[Chunk {i+1}]: {chunk}" for i, chunk in enumerate(context_chunks)
    )

    stock_text = ""
    if stock_data:
        stock_text = (
            f"\n\nLIVE MARKET DATA (as of {stock_data.get('latest_trading_day', 'unknown date')}, "
            f"this is real-time/current data, NOT from any uploaded document):\n"
            f"Ticker: {stock_data.get('ticker')}\n"
            f"Current Price: {stock_data.get('price')}\n"
            f"Change: {stock_data.get('change')} ({stock_data.get('change_percent')})\n"
            f"Volume: {stock_data.get('volume')}"
        )

    system_prompt = (
        "You are a financial document analysis assistant. "
        "Answer the user's question using ONLY the information in the "
        "provided document context chunks and, if given, the live market data below. "
        "Clearly distinguish between information from the uploaded documents "
        "(which may be historical or as of a filing date) and live market data "
        "(which is current as of right now). Do not confuse the two or imply "
        "a document 'predicted' or 'contains' a live price it does not mention. "
        "If the context does not contain enough information to answer, "
        "say clearly: 'I don't have enough information in the provided "
        "documents to answer that.' "
        "Do not use outside knowledge. Do not make up numbers or facts. "
        "When you use information from a chunk, mention which chunk number it came from."
    )

    user_prompt = f"Document Context:\n{context_text}{stock_text}\n\nQuestion: {question}"

    response = _client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content
