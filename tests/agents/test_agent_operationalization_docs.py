from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


REQUIRED_DOCS = [
    "docs/agents/operationalization-plan.md",
    "docs/knowledge/enterprise-knowledge-architecture.md",
    "docs/knowledge/tap-lite-knowledge-base.md",
    "docs/knowledge/aap-knowledge-base.md",
    "docs/knowledge/satellite-knowledge-base.md",
    "docs/agents/agent-evaluation-framework.md",
    "docs/agents/agent-memory-architecture.md",
    "docs/agents/agent-orchestration.md",
    "docs/agents/executive-automation-workflows.md",
    "docs/knowledge/redhat-summit-assistant.md",
    "docs/agents/business-value-framework.md",
]


AGENTS = [
    "Enterprise Architecture Copilot",
    "AAP Platform Copilot",
    "Satellite Platform Copilot",
    "Server Engineering Copilot",
    "Executive Communications Copilot",
    "Automation Discovery Copilot",
    "Operational Review Copilot",
]


def read_doc(relative_path: str) -> str:
    return (ROOT / relative_path).read_text()


def test_required_operationalization_docs_exist():
    missing = [path for path in REQUIRED_DOCS if not (ROOT / path).is_file()]

    assert missing == []


def test_operationalization_plan_covers_every_documented_agent():
    text = read_doc("docs/agents/operationalization-plan.md")

    for agent in AGENTS:
        assert agent in text

    for required in [
        "runtime",
        "Prompt source",
        "Required tools",
        "Required knowledge",
        "Validation strategy",
        "http://127.0.0.1:18080/v1",
        "mlx-community--gemma-4-31b-it-4bit",
        "mlx-community--gemma-4-26b-a4b-it-4bit",
        "mlx-community--gemma-4-e4b-it-4bit",
        "mlx-community--gemma-4-e2b-it-4bit",
        "Boneman",
    ]:
        assert required in text


def test_enterprise_knowledge_architecture_defines_source_lifecycle():
    text = read_doc("docs/knowledge/enterprise-knowledge-architecture.md")

    for section in ["## Ingestion", "## Indexing", "## Retrieval", "## Maintenance"]:
        assert section in text

    for domain in ["Enterprise Architecture", "Automation Platform", "Satellite Platform", "Operations", "Governance"]:
        assert domain in text


def test_domain_knowledge_bases_include_expected_capabilities():
    expectations = {
        "docs/knowledge/tap-lite-knowledge-base.md": [
            "TAP Lite generation",
            "Architecture review",
            "Risk identification",
            "Decision records",
            "Executive summaries",
        ],
        "docs/knowledge/aap-knowledge-base.md": [
            "automation recommendations",
            "Playbook review",
            "Upgrade guidance",
            "ROI estimation",
            "Executive reporting",
        ],
        "docs/knowledge/satellite-knowledge-base.md": [
            "Lifecycle management",
            "Content views",
            "Compliance",
            "Upgrades",
            "Governance",
        ],
    }

    for path, expected_terms in expectations.items():
        text = read_doc(path)
        for term in expected_terms:
            assert term in text


def test_evaluation_framework_has_required_dimensions_and_harness():
    text = read_doc("docs/agents/agent-evaluation-framework.md")

    for dimension in [
        "Accuracy",
        "Completeness",
        "Consistency",
        "Usefulness",
        "Executive quality",
        "Governance compliance",
    ]:
        assert dimension in text

    assert "Reusable Evaluation Harness" in text
    assert "Final pass/fail" in text


def test_memory_architecture_defines_memory_types_and_rules():
    text = read_doc("docs/agents/agent-memory-architecture.md")

    for memory_type in ["Short-term memory", "Project memory", "Knowledge memory", "Evaluation memory", "Business value memory"]:
        assert memory_type in text

    assert "Current source evidence overrides memory" in text
    assert "Secrets" in text


def test_orchestration_documents_required_handoffs():
    text = read_doc("docs/agents/agent-orchestration.md")

    for workflow in [
        "Automation Discovery Copilot -> Enterprise Architecture Copilot -> Executive Communications Copilot",
        "Server Engineering Copilot -> Operational Review Copilot",
        "AAP Platform Copilot -> Executive Communications Copilot",
    ]:
        assert workflow in text

    assert "Standard Handoff Record" in text


def test_executive_and_summit_workflows_are_operational():
    executive_text = read_doc("docs/agents/executive-automation-workflows.md")
    summit_text = read_doc("docs/knowledge/redhat-summit-assistant.md")

    for workflow in ["Quarterly review", "Monthly update", "Red Hat Summit briefing", "Automation ROI report"]:
        assert workflow in executive_text

    for capability in ["Announcement triage", "Architecture implication review", "Executive briefing", "Follow-up backlog"]:
        assert capability in summit_text


def test_business_value_framework_defines_measurement_metrics():
    text = read_doc("docs/agents/business-value-framework.md")

    for metric in [
        "Time saved",
        "Automation opportunities found",
        "Architecture effort reduced",
        "Reporting effort reduced",
        "Operational efficiency",
    ]:
        assert metric in text

    assert "Value Record" in text


def test_catalog_runtime_and_skills_link_operational_artifacts():
    combined = "\n".join(
        [
            read_doc("docs/agents/agent-catalog.md"),
            read_doc("docs/agents/agent-runtime-architecture.md"),
            read_doc("docs/skills/codex-skills.md"),
        ]
    )

    for path in REQUIRED_DOCS:
        assert path in combined
