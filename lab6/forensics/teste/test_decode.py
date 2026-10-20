# teste/test_decode.py
import re
def ghici_strat(s)->str:
    # TODO: daca are %xx -> "url"
    if re.search(r'%[0-9a-fA-F]{2}',s):
        return "url"
    # TODO: daca doar 0-9 a-f si lungime para -> "hex"
    if re.fullmatch(r'[0-9a-fA-F]+', s) and len(s) % 2 == 0:
        return "hex"
    # TODO: daca doar A-Za-z0-9+/= -> "base64"
    if re.fullmatch(r'[A-Za-z0-9+/=]+', s):
        return "base64"
    
    return "necunoscut"
import base64
from urllib.parse import unquote
def desfa(s):
    strat = ghici_strat(s)
    # TODO: pentru fiecare strat, decodeaza
    #   base64 -> base64.b64decode(s)
    #   hex    -> bytes.fromhex(s)
    #   url    -> unquote(s).encode()
    # intoarce (strat, rezultat_bytes)
    rezultat_bytes = b""
    if strat == "base64":
        rezultat_bytes = base64.b64decode(s)
    if strat == "hex":
        rezultat_bytes = bytes.fromhex(s)
    elif strat == "url":
        rezultat_bytes = unquote(s).encode()
    
    return strat, rezultat_bytes
def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"