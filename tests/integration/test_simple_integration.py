# This file is part of youtube-links.
#
# Copyright 2025 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License version 3, as published by the Free
# Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranties of MERCHANTABILITY, SATISFACTORY
# QUALITY, or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

"""Simple integration tests for youtube-links extension."""

import sys
from pathlib import Path

# Add the extension to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "youtube_links"))


def test_extension_can_be_imported():
    """Test that the extension can be imported without errors."""
    try:
        import youtube_links
        assert hasattr(youtube_links, 'setup')
        assert callable(youtube_links.setup)
        assert hasattr(youtube_links, 'YouTubeLink')
    except ImportError as e:
        pytest.fail(f"Failed to import youtube_links: {e}")


def test_extension_setup_function():
    """Test that the setup function returns correct metadata."""
    from unittest.mock import Mock
    import youtube_links
    
    app_mock = Mock()
    app_mock.add_directive = Mock()
    
    with patch('youtube_links.common.add_css') as mock_add_css:
        result = youtube_links.setup(app_mock)
    
    assert "version" in result
    assert "parallel_read_safe" in result
    assert "parallel_write_safe" in result
    assert result["parallel_read_safe"] is True
    assert result["parallel_write_safe"] is True
    
    # Check that directive was registered
    app_mock.add_directive.assert_called_once_with("youtube", youtube_links.YouTubeLink)


def test_youtube_directive_instantiation():
    """Test that YouTube directive can be instantiated."""
    from unittest.mock import Mock
    import youtube_links
    
    # Test directive can be created
    directive = youtube_links.YouTubeLink(
        name="youtube",
        arguments=["https://www.youtube.com/watch?v=test"],
        options={"title": "Test Title"},
        content=[],
        lineno=1,
        content_offset=0,
        block_text="",
        state=Mock(),
        state_machine=Mock()
    )
    
    assert directive.required_arguments == 1
    assert directive.optional_arguments == 0
    assert directive.has_content is False
    assert "title" in directive.option_spec


def test_youtube_directive_execution():
    """Test that YouTube directive can be executed."""
    from unittest.mock import Mock
    import youtube_links
    
    directive = youtube_links.YouTubeLink(
        name="youtube",
        arguments=["https://www.youtube.com/watch?v=test"],
        options={"title": "Test Title"},
        content=[],
        lineno=1,
        content_offset=0,
        block_text="",
        state=Mock(),
        state_machine=Mock()
    )
    
    result = directive.run()
    
    assert len(result) == 1
    raw_node = result[0]
    assert raw_node.tagname == "raw"
    assert raw_node.children
    
    html_content = str(raw_node.children[0])
    assert "Test Title" in html_content
    assert "https://www.youtube.com/watch?v=test" in html_content
    assert "youtube_link" in html_content


# Import necessary modules
import pytest
from unittest.mock import patch