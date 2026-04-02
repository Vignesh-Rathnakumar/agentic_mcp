"""Unit tests for the Agentic MCP AI project."""

import pytest
from unittest.mock import Mock, MagicMock
from app.agent import ReactAgent, create_agent


class TestReactAgent:
    """Test suite for ReactAgent class."""

    def test_agent_initialization(self):
        """Test agent initialization with mock LLM."""
        mock_llm = Mock()
        mock_tool = Mock()
        mock_tool.name = "test_tool"
        mock_tool.description = "Test tool"

        agent = ReactAgent(llm=mock_llm, tools=[mock_tool])

        assert agent.llm == mock_llm
        assert "test_tool" in agent.tools
        assert agent.max_iterations == 8

    def test_agent_initialization_custom_iterations(self):
        """Test agent initialization with custom max iterations."""
        mock_llm = Mock()
        agent = ReactAgent(llm=mock_llm, tools=[], max_iterations=5)

        assert agent.max_iterations == 5

    def test_parse_action_valid(self):
        """Test parsing valid action format."""
        mock_llm = Mock()
        agent = ReactAgent(llm=mock_llm, tools=[])

        text = "Thought: I need to read a file\nAction: FileReader\nAction Input: {\"path\": \"/tmp/test.txt\"}"
        action, action_input = agent._parse_action(text)

        assert action == "FileReader"
        assert action_input == {"path": "/tmp/test.txt"}

    def test_parse_action_invalid(self):
        """Test parsing invalid action format."""
        mock_llm = Mock()
        agent = ReactAgent(llm=mock_llm, tools=[])

        # Missing action input
        text = "Thought: Something\nAction: FileReader"
        action, action_input = agent._parse_action(text)

        assert action is None
        assert action_input is None

        # Invalid JSON
        text = "Thought: Something\nAction: FileReader\nAction Input: {invalid}"
        action, action_input = agent._parse_action(text)

        assert action is None
        assert action_input is None

    def test_parse_action_no_action(self):
        """Test parsing when no action is present."""
        mock_llm = Mock()
        agent = ReactAgent(llm=mock_llm, tools=[])

        text = "Thought: I'm done here"
        action, action_input = agent._parse_action(text)

        assert action is None
        assert action_input is None


class TestCreateAgent:
    """Test suite for create_agent factory function."""

    def test_create_agent_returns_react_agent(self):
        """Test that create_agent returns a ReactAgent instance."""
        # This test would need proper environment setup
        # For now, test with mocked LLM
        from unittest.mock import patch

        with patch('app.agent.get_llm') as mock_get_llm:
            mock_llm = Mock()
            mock_get_llm.return_value = mock_llm

            agent = create_agent()

            assert isinstance(agent, ReactAgent)
            assert len(agent.tools) == 2
            assert "file_reader" in agent.tools
            assert "terminal" in agent.tools


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
