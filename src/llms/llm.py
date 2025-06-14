import logging

from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

def get_llm_by_type() -> ChatOpenAI:
    """Get llm instance."""
    return ChatOpenAI(
        model="deepseek-chat",
        # model="gemini/gemini-2.0-flash",
        base_url="https://api.deepseek.com",
    )


if __name__ == "__main__":
    # Initialize LLMs for different purposes - now these will be cached
    basic_llm = get_llm_by_type()
    logger.info(basic_llm.invoke("Hello"))