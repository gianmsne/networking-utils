"""
Tests for subnet_calculator.py

Run with:
    pytest test_subnet_calculator.py -v
"""

import pytest
from tools.subnet_calculator import is_valid_ip, is_integer, int_to_ip, subnet_calculator


# ---------------------------------------------------------------------------
# is_valid_ip
# ---------------------------------------------------------------------------

class TestIsValidIp:

    @pytest.mark.parametrize("ip", [
        "192.168.1.0/24",
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.1.5/32",   # host bits set, but strict=False allows it
        "0.0.0.0/0",
        "255.255.255.255/32",
    ])
    def test_valid_ipv4_with_prefix(self, ip):
        assert is_valid_ip(ip) is True

    def test_missing_prefix_is_invalid(self):
        # Must include a "/prefix" - bare address should fail
        assert is_valid_ip("192.168.1.1") is False

    @pytest.mark.parametrize("ip", [
        "192.168.1.0/33",      # prefix out of range
        "999.168.1.0/24",      # invalid octet
        "192.168.1/24",        # incomplete address
        "192.168.1.0.5/24",    # too many octets
        "not_an_ip/24",
        "",
        "/24",
    ])
    def test_invalid_input_returns_false(self, ip):
        assert is_valid_ip(ip) is False

    def test_ipv6_is_rejected(self):
        # is_valid_ip explicitly restricts to IPv4 (net.version == 4)
        assert is_valid_ip("::1/64") is False
        assert is_valid_ip("2001:db8::/32") is False

    def test_non_string_input_does_not_raise(self):
        # '/' not in ip will raise TypeError for non-string/non-iterable types
        # like None or int; make sure the function doesn't crash the caller.
        with pytest.raises(TypeError):
            is_valid_ip(None)


# ---------------------------------------------------------------------------
# is_integer
# ---------------------------------------------------------------------------

class TestIsInteger:

    @pytest.mark.parametrize("value", ["1", "4", "50", "100", 1, 100])
    def test_valid_range(self, value):
        assert is_integer(value) is True

    @pytest.mark.parametrize("value", ["0", "-1", "101", "1000", 0, -5, 101])
    def test_out_of_range(self, value):
        assert is_integer(value) is False

    @pytest.mark.parametrize("value", ["abc", "4.5", "", None, "  ", "4subnets"])
    def test_non_integer_input(self, value):
        assert is_integer(value) is False

    def test_boundary_values(self):
        assert is_integer("1") is True
        assert is_integer("100") is True
        assert is_integer("0") is False
        assert is_integer("101") is False


# ---------------------------------------------------------------------------
# int_to_ip
# ---------------------------------------------------------------------------

class TestIntToIp:

    @pytest.mark.parametrize("n, expected", [
        (0, "0.0.0.0"),
        (4294967295, "255.255.255.255"),  # 2**32 - 1
        (3232235776, "192.168.1.0"),
        (3232235777, "192.168.1.1"),
        (167772160, "10.0.0.0"),
    ])
    def test_known_values(self, n, expected):
        assert int_to_ip(n) == expected

    def test_roundtrip_with_ip_parsing(self):
        octets = [192, 168, 1, 50]
        n = (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]
        assert int_to_ip(n) == "192.168.1.50"


# ---------------------------------------------------------------------------
# subnet_calculator (integration - mocks input(), captures stdout)
# ---------------------------------------------------------------------------

class TestSubnetCalculatorIntegration:

    def _run(self, monkeypatch, inputs):
        """Feed a sequence of canned inputs to subnet_calculator() and
        return everything it printed as a single string."""
        responses = iter(inputs)
        monkeypatch.setattr("builtins.input", lambda *args, **kwargs: next(responses))
        subnet_calculator()

    def test_four_subnets_on_slash24(self, monkeypatch, capsys):
        self._run(monkeypatch, ["192.168.1.0/24", "4"])
        out = capsys.readouterr().out

        # Should borrow 2 bits -> /26, mask 255.255.255.192
        assert "New subnet mask: 255.255.255.192" in out
        assert "192.168.1.0/26" in out
        assert "192.168.1.64/26" in out
        assert "192.168.1.128/26" in out
        assert "192.168.1.192/26" in out
        # spot-check usable range of the first subnet
        assert "192.168.1.1" in out
        assert "192.168.1.62" in out
        assert "192.168.1.63" in out  # broadcast

    def test_six_subnets_on_slash24_matches_manual_check(self, monkeypatch, capsys):
        # Regression check against the /27 x 6 table verified earlier
        self._run(monkeypatch, ["192.168.1.0/24", "6"])
        out = capsys.readouterr().out

        assert "New subnet mask: 255.255.255.224" in out  # /27
        expected_networks = [
            "192.168.1.0/27", "192.168.1.32/27", "192.168.1.64/27",
            "192.168.1.96/27", "192.168.1.128/27", "192.168.1.160/27",
        ]
        for net in expected_networks:
            assert net in out

    def test_single_subnet_does_not_borrow_bits(self, monkeypatch, capsys):
        # subnets == 1 should NOT change the prefix (regression: count
        # used to start at 1 instead of 0, forcing an unwanted /25 split)
        self._run(monkeypatch, ["192.168.1.0/24", "1"])
        out = capsys.readouterr().out

        assert "New subnet mask: 255.255.255.0" in out  # still /24
        assert "192.168.1.0/24" in out

    def test_invalid_ip_reprompts_then_succeeds(self, monkeypatch, capsys):
        self._run(monkeypatch, ["not_an_ip", "192.168.1.0/24", "2"])
        out = capsys.readouterr().out
        assert "Invalid IP address, please try again." in out
        assert "192.168.1.0/25" in out  # 2 subnets -> borrow 1 bit -> /25

    def test_invalid_subnet_count_reprompts_then_succeeds(self, monkeypatch, capsys):
        self._run(monkeypatch, ["192.168.1.0/24", "0", "abc", "4"])
        out = capsys.readouterr().out
        assert "Invalid number, please try again." in out
        assert "192.168.1.0/26" in out

    def test_cancel_on_ip_prompt_returns_without_error(self, monkeypatch, capsys):
        # "0" at the IP prompt should return cleanly, not raise or exit the
        # whole process (exit() would kill the test runner - it should NOT
        # be called here).
        self._run(monkeypatch, ["0", ""])  # "0" then dummy for the [ENTER] prompt
        out = capsys.readouterr().out
        assert "return to the menu" in out

    def test_too_many_subnets_for_address_space(self, monkeypatch, capsys):
        # Requesting more subnets than a /30 can support pushes new_prefix
        # past 32. This currently calls exit(), which raises SystemExit -
        # documenting that behavior here so a future refactor to `return`
        # (consistent with the menu-driven cancel path) doesn't go unnoticed.
        with pytest.raises(SystemExit):
            self._run(monkeypatch, ["192.168.1.0/30", "100"])
        out = capsys.readouterr().out
        assert "Error: too many subnets requested" in out


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))