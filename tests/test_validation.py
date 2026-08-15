from unittest.mock import patch

from tools.ports import parse_ports
from utils.validation import get_int_input, get_yes_no


class TestParsePorts:
    """Test port parsing functionality"""

    def test_parse_single_ports(self):
        """Test parsing individual port numbers"""
        result = parse_ports("22,80,443")
        assert result == [22, 80, 443]

    def test_parse_port_range(self):
        """Test parsing port ranges"""
        result = parse_ports("20-25")
        assert result == [20, 21, 22, 23, 24, 25]

    def test_parse_mixed_ports_and_ranges(self):
        """Test parsing combination of individual ports and ranges"""
        result = parse_ports("22,80-82,443")
        assert result == [22, 80, 81, 82, 443]


class TestGetYesNo:
    """Test yes/no input validation"""

    @patch("builtins.input", return_value="y")
    def test_yes_input(self, mock_input):
        """Test that 'y' returns True"""
        result = get_yes_no()
        assert result is True

    @patch("builtins.input", return_value="n")
    def test_no_input(self, mock_input):
        """Test that 'n' returns False"""
        result = get_yes_no()
        assert result is False

    @patch("builtins.input", return_value="")
    def test_empty_input_defaults_to_yes(self, mock_input):
        """Test that empty input defaults to True (yes)"""
        result = get_yes_no()
        assert result is True


class TestGetIntInput:
    """Test integer input validation"""

    @patch("builtins.input", return_value="2")
    def test_valid_input_within_bounds(self, mock_input):
        """Test that valid input within bounds is accepted"""
        result = get_int_input(0, 4)
        assert result == 2

    @patch("builtins.input", return_value="0")
    def test_lower_bound_inclusive(self, mock_input):
        """Test that lower bound is inclusive"""
        result = get_int_input(0, 4)
        assert result == 0

    @patch("builtins.input", return_value="4")
    def test_upper_bound_inclusive(self, mock_input):
        """Test that upper bound is inclusive"""
        result = get_int_input(0, 4)
        assert result == 4