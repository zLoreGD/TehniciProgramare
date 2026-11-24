from pathlib import Path

from arsenal.windows.inventar import Eveniment, Inventar, Proces

START = Path(__file__).resolve().parents[2] / "start"


def test_proces_din_temp_e_suspect():
    p = Proces(1, "x.exe", "ana", "C:\\Users\\ana\\AppData\\Local\\Temp\\x.exe")
    assert p.e_suspect() is True


def test_proces_din_windows_nu_e_suspect():
    p = Proces(2, "svchost.exe", "SYSTEM", "C:\\Windows\\System32\\svchost.exe")
    assert p.e_suspect() is False


def test_eveniment_dupa_id_si_dupa_nivel():
    assert Eveniment(4625, "warning", "Security", "x", "m").e_suspect() is True
    assert Eveniment(1, "critical", "Security", "x", "m").e_suspect() is True
    assert Eveniment(4624, "info", "Security", "x", "m").e_suspect() is False


def test_inventar_foloseste_propriile_procese():
    inv = Inventar([Proces(1, "a.exe", "ana", "C:\\Temp\\a.exe"),
                    Proces(2, "b.exe", "bob", "C:\\Windows\\b.exe")])
    assert [p.nume for p in inv.suspecte()] == ["a.exe"]
    assert inv.pe_user() == {"ana": ["a.exe"], "bob": ["b.exe"]}


def test_inventar_din_json():
    inv = Inventar.din_json(START / "procese.json")
    assert len(inv) == 7
    assert len(inv.suspecte()) == 2
