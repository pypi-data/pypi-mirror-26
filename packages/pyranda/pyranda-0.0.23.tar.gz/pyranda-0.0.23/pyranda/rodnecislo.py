class RodneCislo:
    """ Třída zapouzdřující chování rodného čísla.. """
    def __init__(self, cislo):
        self.SetCislo(cislo)


    def SetCislo(self, cislo):
        """ Načtení atributů rodného číslo z předaného rodného čísla.. """
        if cislo == "":
            self.cislo = ""
            self.rok = 0
            self.mesic = 0
            self.den = 0
            self.pohlavi = 0
            return

        self.cislo = cislo
        self.den = int(cislo[4:6])
        self.pohlavi = 1

        mesic =  int(cislo[2:4])
        if mesic > 70:
            mesic -= 70
            self.pohlavi = 2
        if mesic > 50:
            mesic -= 50
            self.pohlavi = 2
        if mesic > 20:
            mesic -= 20
            self.pohlavi = 1
        self.mesic = mesic

        rok = int(cislo[:2])
        if len(cislo) == 10:
            rok += 1900
        if len(cislo) == 11 and rok >= 54:
            rok += 1900
        if len(cislo) == 11 and rok < 54:
            rok += 2000

        self.rok = rok

