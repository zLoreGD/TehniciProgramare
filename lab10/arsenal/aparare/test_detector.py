from collections import Counter

import pytest

from arsenal.aparare.detector import suspecti
from arsenal.aparare.parse_auth import esec, pe_ip


def test_pragul_taie():
    c = Counter({"a": 13, "b": 2})
    assert suspecti(c, 10) == [("a", 13)]


def test_prag_invalid():
    with pytest.raises(ValueError):
        suspecti({}, 0)


def test_esec_valid_si_stricat():
    linie = "Jan 10 sshd[1]: Failed password for root from 203.0.113.9 port 51230 ssh2"
    assert esec(linie) == ("root", "203.0.113.9")
    assert esec("<linie stricata fara structura>") is None


def test_pe_ip():
    esecuri = [{"user": "a", "ip": "1.1.1.1"}, {"user": "b", "ip": "1.1.1.1"}]
    assert pe_ip(esecuri) == Counter({"1.1.1.1": 2})
