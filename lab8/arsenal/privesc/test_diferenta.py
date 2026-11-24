from arsenal.privesc.diferenta import noi_fata_de_baza, periculoase


def test_doar_ce_e_nou():
    acum = {"/bin/a", "/bin/b", "/bin/c"}
    baza = {"/bin/a", "/bin/b"}
    assert noi_fata_de_baza(acum, baza) == {"/bin/c"}


def test_nimic_nou():
    assert noi_fata_de_baza({"/bin/a"}, {"/bin/a"}) == set()


def test_periculoase_doar_din_gtfo():
    noi = {"/usr/bin/find", "/bin/mount", "/bin/cp"}
    assert periculoase(noi) == ["/bin/cp", "/usr/bin/find"]
