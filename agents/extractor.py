import os
import csv


def extract_inputs(config: dict) -> dict:
    """
    Parse all files in inputs/models/ and inputs/data/ into structured text.

    Args:
        config: Project config dict.

    Returns:
        dict with keys:
            - model_text: str — combined structured text from all model files
            - csv_summaries: list[dict] — schema + stats per CSV file
    """
    model_text = _parse_models(config["inputs"]["models"])
    csv_summaries = _parse_csvs(config["inputs"]["data"])

    return {"model_text": model_text, "csv_summaries": csv_summaries}


def _parse_models(models_dir: str) -> str:
    """
    Read all TMDL and JSON files in models_dir and return combined text.

    Args:
        models_dir: Path to the models input directory.

    Returns:
        Combined text content of all model files.

    Raises:
        FileNotFoundError: If models_dir does not exist.
    """
    if not os.path.exists(models_dir):
        raise FileNotFoundError(f"Models directory not found: {models_dir}")

    parts = []
    for filename in os.listdir(models_dir):
        if filename.startswith("."):
            continue
        if not filename.endswith((".tmdl", ".json")):
            continue
        file_path = os.path.join(models_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        parts.append(f"--- FILE: {filename} ---\n{content}")

    if not parts:
        raise ValueError(f"No TMDL or JSON files found in: {models_dir}")

    return "\n\n".join(parts)


def _parse_csvs(data_dir: str) -> list[dict]:
    """
    Read all CSV files in data_dir and return schema + basic stats per file.

    Args:
        data_dir: Path to the data input directory.

    Returns:
        List of dicts, each with:
            - filename: str
            - columns: list[str]
            - row_count: int
            - sample_rows: list[dict] (first 3 rows)

    Raises:
        FileNotFoundError: If data_dir does not exist.
    """
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    summaries = []
    for filename in os.listdir(data_dir):
        if filename.startswith("."):
            continue
        if not filename.endswith(".csv"):
            continue
        file_path = os.path.join(data_dir, filename)
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        summaries.append(
            {
                "filename": filename,
                "columns": reader.fieldnames or [],
                "row_count": len(rows),
                "sample_rows": rows[:3],
            }
        )

    return summaries
