"""Tests for XDG Base Directory Specification utilities."""

import os
from pathlib import Path
from unittest.mock import patch

from mcp_jenkins.xdg import get_cache_dir, get_config_dir, get_data_dir


class TestXDGDirectories:
    """Test XDG directory functions with and without environment variables."""

    def test_get_config_dir_default(self):
        """Test get_config_dir returns default path when XDG_CONFIG_HOME is not set."""
        with patch.dict(os.environ, {}, clear=True):
            result = get_config_dir()
            expected = Path.home() / '.config' / 'mcp-jenkins'
            assert result == expected

    def test_get_config_dir_with_env_var(self):
        """Test get_config_dir uses XDG_CONFIG_HOME when set."""
        with patch.dict(os.environ, {'XDG_CONFIG_HOME': '/custom/config'}):
            result = get_config_dir()
            expected = Path('/custom/config') / 'mcp-jenkins'
            assert result == expected

    def test_get_data_dir_default(self):
        """Test get_data_dir returns default path when XDG_DATA_HOME is not set."""
        with patch.dict(os.environ, {}, clear=True):
            result = get_data_dir()
            expected = Path.home() / '.local' / 'share' / 'mcp-jenkins'
            assert result == expected

    def test_get_data_dir_with_env_var(self):
        """Test get_data_dir uses XDG_DATA_HOME when set."""
        with patch.dict(os.environ, {'XDG_DATA_HOME': '/custom/data'}):
            result = get_data_dir()
            expected = Path('/custom/data') / 'mcp-jenkins'
            assert result == expected

    def test_get_cache_dir_default(self):
        """Test get_cache_dir returns default path when XDG_CACHE_HOME is not set."""
        with patch.dict(os.environ, {}, clear=True):
            result = get_cache_dir()
            expected = Path.home() / '.cache' / 'mcp-jenkins'
            assert result == expected

    def test_get_cache_dir_with_env_var(self):
        """Test get_cache_dir uses XDG_CACHE_HOME when set."""
        with patch.dict(os.environ, {'XDG_CACHE_HOME': '/custom/cache'}):
            result = get_cache_dir()
            expected = Path('/custom/cache') / 'mcp-jenkins'
            assert result == expected
