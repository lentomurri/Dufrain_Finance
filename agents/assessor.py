import autogen
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex


def assess(extracted: dict, config: dict) -> dict:
    """
    RAG-based assessment: retrieve relevant knowledge chunks and compare
    against the extracted model using an AutoGen agent.

    Args:
        extracted: Output from extractor.extract_inputs().
        config: Project config dict.

    Returns:
        dict with key 'findings': list of structured finding strings per dimension.
    """
    query_engine = _build_query_engine(config["inputs"]["knowledge"])
    context = _retrieve_context(query_engine, extracted["model_text"])
    findings = _run_assessor_agent(extracted, context, config)

    return {"findings": findings}


def _build_query_engine(knowledge_dir: str):
    """
    Load MD knowledge base from knowledge_dir and build an in-memory vector index.

    Args:
        knowledge_dir: Path to the directory containing MD reference files.

    Returns:
        LlamaIndex query engine.
    """
    documents = SimpleDirectoryReader(knowledge_dir).load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()


def _retrieve_context(query_engine, model_text: str) -> str:
    """
    Run a set of standard assessment queries against the knowledge base.

    Args:
        query_engine: LlamaIndex query engine.
        model_text: Extracted model text.

    Returns:
        Combined retrieved context string.
    """
    queries = [
        "What measures are required for a complete P&L financial model?",
        "What are the best practices for naming conventions in a financial semantic model?",
        "What time intelligence measures should be present in a financial model?",
        "What dimensions and hierarchies are required for a financial model?",
        "What security and row-level security patterns are expected?",
    ]
    parts = []
    for q in queries:
        response = query_engine.query(q)
        parts.append(f"Q: {q}\nA: {response}")
    return "\n\n".join(parts)


def _run_assessor_agent(extracted: dict, context: str, config: dict) -> list[str]:
    """
    Use an AutoGen AssistantAgent to compare the model against retrieved context.

    Args:
        extracted: Output from extract_inputs().
        context: Retrieved knowledge base context.
        config: Project config dict.

    Returns:
        List of finding strings, one per assessment dimension.
    """
    llm_config = {
        "config_list": [
            {"model": config["model"], "api_key": config["openai_api_key"]}
        ]
    }

    assessor = autogen.AssistantAgent(
        name="Assessor",
        llm_config=llm_config,
        system_message=(
            "You are a senior financial BI consultant. "
            "You will receive a Power BI semantic model and reference best practices. "
            "Assess the model across these dimensions: "
            "Schema & Structure, Measure Completeness, Naming Conventions, "
            "Time Intelligence, Budget & Variance, Security, Data Quality. "
            "For each dimension, report: what is present, what is missing, and severity (High/Medium/Low). "
            "Be specific and reference measure/table/column names where possible. "
            "Output each dimension as a separate section."
        ),
    )

    proxy = autogen.UserProxyAgent(
        name="Pipeline",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        code_execution_config=False,
    )

    message = (
        f"## Semantic Model\n\n{extracted['model_text']}\n\n"
        f"## CSV Data Summary\n\n{extracted['csv_summaries']}\n\n"
        f"## Reference Best Practices (retrieved)\n\n{context}\n\n"
        "Please assess the model against the reference and return structured findings per dimension."
    )

    proxy.initiate_chat(assessor, message=message)

    last_message = assessor.last_message()
    findings_text = last_message.get("content", "") if last_message else ""

    return [findings_text]
