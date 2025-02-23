# tests/test_cli.py
"""Test main CLI interface."""

import pytest
from click.testing import CliRunner
from avrc.cli import main

def test_cli_version():
    """Test CLI version command."""
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0

def test_cli_help():
    """Test CLI help command."""
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert "Usage:" in result.output
