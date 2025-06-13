from langchain_openai import ChatOpenAI

from src.llms import get_llm_by_type


def test_get_llm_by_type() -> None:
    assert isinstance(get_llm_by_type(), ChatOpenAI)
