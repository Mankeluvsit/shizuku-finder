from pathlib import Path


def test_ci_workflow_runs_ruff_mypy_and_pytest() -> None:
    workflow = Path('.github/workflows/ci.yml').read_text(encoding='utf-8')
    assert 'ruff check .' in workflow
    assert 'mypy src' in workflow
    assert 'pytest' in workflow


def test_scheduled_workflow_publishes_diff_and_run_summary_and_supports_target_repo() -> None:
    workflow = Path('.github/workflows/scheduled-scan.yml').read_text(encoding='utf-8')
    assert 'TARGET_LIST_REPO' in workflow
    assert 'DIFF.md' in workflow
    assert 'RUN_SUMMARY.json' in workflow
    assert '--diff-file DIFF.md' in workflow
    assert '--run-summary-file RUN_SUMMARY.json' in workflow
    assert 'Publish run summary' in workflow
    assert 'Enforce minimum successful output' in workflow
    assert 'actions/upload-artifact@v4' in workflow
    assert 'git push origin HEAD:${{ github.ref_name }}' in workflow
    assert 'fetch-depth: 0' in workflow
    assert 'persist-credentials: true' in workflow
