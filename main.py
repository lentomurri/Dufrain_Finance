from config import config, validate_config
from agents.extractor import extract_inputs
from agents.assessor import assess
from agents.scorer import score_and_report


def main() -> None:
    """
    Orchestrate the full assessment pipeline:
    extract → assess → score → report.
    """
    validate_config(config)

    extracted = extract_inputs(config)
    findings = assess(extracted, config)
    score_and_report(findings, config)


if __name__ == "__main__":
    main()
