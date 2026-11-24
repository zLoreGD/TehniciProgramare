import base64
import hashlib

from arsenal.forensics.decode import (PROBE, desfa, desface_complet, ghici_strat,
                                      sparge_hash, sparge_xor)


def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"


def test_hex_si_url():
    assert desfa("48656c6c6f") == ("hex", b"Hello")
    assert desfa("%2Fetc") == ("url", b"/etc")


def test_text_simplu_e_necunoscut():
    assert ghici_strat("Salut!") == "necunoscut"


def test_straturi_multiple_pana_la_flag():
    straturi, clar = desface_complet((PROBE / "mesaj.txt").read_text().strip())
    assert straturi == ["base64", "base64", "hex"]
    assert clar == b"FLAG{straturi_de_encoding}"


def test_xor_gaseste_cheia():
    k, text = sparge_xor((PROBE / "xor.bin").read_bytes())[0]
    assert k == 0x80
    assert "FLAG{xor_un_octet}" in text


def test_hash_prin_dictionar():
    tinta = hashlib.md5(b"password").hexdigest()
    cuvinte = (PROBE / "wordlist.txt").read_text(encoding="latin1").splitlines()
    assert sparge_hash(tinta, cuvinte) == "password"
    assert sparge_hash("0" * 32, cuvinte) is None
