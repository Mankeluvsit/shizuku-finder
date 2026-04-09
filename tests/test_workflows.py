from pathlib import Path


def test_ci_workflow_runs_ruff_mypy_and_pytest() -> None:
    workflow = Path('.github/workflows/ci.yml').read_text(encoding='utf-8')
    assert 'ruff check .' in workflow
    assert 'mypy src' in workflow
    assert 'pytest' in workflow


def test_scheduled_workflow_publishes_diff_and_supports_target_repo() -> None:
    workflow = Path('.github/workflows/scheduled-scan.yml').read_text(encoding='utf-8')
    assert 'TARGET_LIST_REPO' in workflow
    assert 'DIFF.md' in workflow
    assert '--diff-file DIFF.md' in workflow
