from arsenal.forensics.fisiere import (PROBE, ascunde, carving, dezvaluie, gps,
                                       tip_real)


def test_tip_real():
    assert tip_real(PROBE / "foto.jpg") == "jpeg"
    assert tip_real(PROBE / "ascuns.png") == "png"


def test_gps_chisinau():
    lat, lon = gps(PROBE / "foto.jpg")
    assert abs(lat - 47.0167) < 1e-3 and abs(lon - 28.8575) < 1e-3


def test_carving_scoate_flag(tmp_path):
    continut = carving(PROBE / "ascuns.png", tmp_path / "gasit.zip")
    assert "FLAG{ascuns_prin_carving}" in continut["secret.txt"]


def test_lsb_dus_intors(tmp_path):
    iesire = tmp_path / "stego.png"
    ascunde(PROBE / "foto.jpg", b"FLAG{ascuns_in_pixeli}", iesire)
    assert dezvaluie(iesire) == b"FLAG{ascuns_in_pixeli}"
