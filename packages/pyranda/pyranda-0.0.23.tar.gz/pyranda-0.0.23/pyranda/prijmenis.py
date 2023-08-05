import random

from pyranda.prijmeni import Prijmeni

class Prijmenis:
    """ Třída zapouzdřující chování obyčejného příjmení.. """
    def __init__(self):
        self.prijmenis = []
        self.dataInit()

    def GetRandomPrijmeni(self, pohlavi):
        index = random.randint(0, len(self.prijmenis) - 1)
        prijmeni= self.prijmenis[index]
        if pohlavi == 2:
            return prijmeni.nazev2 
        return prijmeni.nazev 

    def dataInit(self):
        self.prijmenis.append(Prijmeni('Adamčík', 'Adamčíková'))
        self.prijmenis.append(Prijmeni('Adámek', 'Adámková'))
        self.prijmenis.append(Prijmeni('Adrián', 'Adriánová'))
        self.prijmenis.append(Prijmeni('Aizner', 'Aiznerová'))
        self.prijmenis.append(Prijmeni('Antalík', 'Antalíková'))
        self.prijmenis.append(Prijmeni('Antl', 'Antlová'))
        self.prijmenis.append(Prijmeni('Antončík', 'Antončíková'))
        self.prijmenis.append(Prijmeni('Antošík', 'Antošíková'))
        self.prijmenis.append(Prijmeni('Apolenář', 'Apolenářová'))
        self.prijmenis.append(Prijmeni('Astaloš', 'Astalošová'))
        self.prijmenis.append(Prijmeni('Ašenbryl', 'Ašenbrylová'))
        self.prijmenis.append(Prijmeni('Augustýn', 'Augustýnková'))
        self.prijmenis.append(Prijmeni('Bednář', 'Bednářová'))
        self.prijmenis.append(Prijmeni('Bubák', 'Bubáková'))
        self.prijmenis.append(Prijmeni('Babčák', 'Babčáková'))
        self.prijmenis.append(Prijmeni('Babin', 'Babincová'))
        self.prijmenis.append(Prijmeni('Bábor', 'Báborová'))
        self.prijmenis.append(Prijmeni('Babuka', 'Babuková'))
        self.prijmenis.append(Prijmeni('Badura', 'Badurová'))
        self.prijmenis.append(Prijmeni('Bachel', 'Bachelová'))
        self.prijmenis.append(Prijmeni('Bachman', 'Bachmannová'))
        self.prijmenis.append(Prijmeni('Bednařík', 'Bednaříková'))
        self.prijmenis.append(Prijmeni('Balada', 'Baladová'))
        self.prijmenis.append(Prijmeni('Balarin', 'Balarinová'))
        self.prijmenis.append(Prijmeni('Balatka', 'Balatková'))
        self.prijmenis.append(Prijmeni('Balcar', 'Balcarová'))
        self.prijmenis.append(Prijmeni('Balcarek', 'Balcarková'))
        self.prijmenis.append(Prijmeni('Bleša', 'Blešová'))
        self.prijmenis.append(Prijmeni('Baltair', 'Baltairová'))
        self.prijmenis.append(Prijmeni('Balvín', 'Balvínová'))
        self.prijmenis.append(Prijmeni('Caban', 'Cabanová'))
        self.prijmenis.append(Prijmeni('Cabuk', 'Cabuková'))
        self.prijmenis.append(Prijmeni('Cahlík', 'Cahlíková'))
        self.prijmenis.append(Prijmeni('Cakl', 'Caklová'))
        self.prijmenis.append(Prijmeni('Calta', 'Caltová'))
        self.prijmenis.append(Prijmeni('Cápík', 'Cápíková'))
        self.prijmenis.append(Prijmeni('Cardal', 'Cardalová'))
        self.prijmenis.append(Prijmeni('Cejhon', 'Cejhonová'))
        self.prijmenis.append(Prijmeni('Cekl', 'Ceklová'))
        self.prijmenis.append(Prijmeni('Celerin', 'Celerinová'))
        self.prijmenis.append(Prijmeni('Černý', 'Černá'))
        self.prijmenis.append(Prijmeni('Cibulka', 'Cibulková'))
        self.prijmenis.append(Prijmeni('Cidlík', 'Cidlíková'))
        self.prijmenis.append(Prijmeni('Císař', 'Císařová'))
        self.prijmenis.append(Prijmeni('Cigler', 'Ciglerová'))
        self.prijmenis.append(Prijmeni('Cichra', 'Cichrová'))
        self.prijmenis.append(Prijmeni('Cikl', 'Ciková'))
        self.prijmenis.append(Prijmeni('Ciprys', 'Ciprysová'))
        self.prijmenis.append(Prijmeni('Čagánek', 'Čagánková'))
        self.prijmenis.append(Prijmeni('Čapek', 'Čapková'))
        self.prijmenis.append(Prijmeni('Čapla', 'Čaplová'))
        self.prijmenis.append(Prijmeni('Černý', 'Černocká'))
        self.prijmenis.append(Prijmeni('Částka', 'Částková'))
        self.prijmenis.append(Prijmeni('Čavajda', 'Čavajdová'))
        self.prijmenis.append(Prijmeni('Čechal', 'Čechalová'))
        self.prijmenis.append(Prijmeni('Čepelík', 'Čepelíková'))
        self.prijmenis.append(Prijmeni('Červenka', 'Červenková'))
        self.prijmenis.append(Prijmeni('Černošek', 'Černošková'))
        self.prijmenis.append(Prijmeni('Červík', 'Červíková'))
        self.prijmenis.append(Prijmeni('Česák', 'Česáková'))
        self.prijmenis.append(Prijmeni('Češek', 'Češková'))
        self.prijmenis.append(Prijmeni('Češka', 'Češková'))
        self.prijmenis.append(Prijmeni('Čičela', 'Čičelová'))
        self.prijmenis.append(Prijmeni('Čokina', 'Čokinová'))
        self.prijmenis.append(Prijmeni('Čtvrtníček', 'Čtvrtníčková'))
        self.prijmenis.append(Prijmeni('Čubák', 'Čubáková'))
        self.prijmenis.append(Prijmeni('Čunek', 'Čunková'))
        self.prijmenis.append(Prijmeni('Cuřín', 'Cuřínová'))
        self.prijmenis.append(Prijmeni('Dratva', 'Dratvová'))
        self.prijmenis.append(Prijmeni('Dajka', 'Dajkvá'))
        self.prijmenis.append(Prijmeni('Dalibor', 'Daliborová'))
        self.prijmenis.append(Prijmeni('Damaška', 'Damašková'))
        self.prijmenis.append(Prijmeni('Dančák', 'Dančáková'))
        self.prijmenis.append(Prijmeni('Dandel', 'Dandelová'))
        self.prijmenis.append(Prijmeni('Danihel', 'Danihelková'))
        self.prijmenis.append(Prijmeni('Danko', 'Danková'))
        self.prijmenis.append(Prijmeni('Daráš', 'Darášová'))
        self.prijmenis.append(Prijmeni('Drábek', 'Drábková'))
        self.prijmenis.append(Prijmeni('Darebník', 'Derebníková'))
        self.prijmenis.append(Prijmeni('Darebníček', 'Darebníčková'))
        self.prijmenis.append(Prijmeni('Drtikol', 'Drtikolová'))
        self.prijmenis.append(Prijmeni('Drásal', 'Drásalová'))
        self.prijmenis.append(Prijmeni('David', 'Davidová'))
        self.prijmenis.append(Prijmeni('Dědek', 'Dětková'))
        self.prijmenis.append(Prijmeni('Dedek', 'Dedková'))
        self.prijmenis.append(Prijmeni('Didov', 'Didová'))
        self.prijmenis.append(Prijmeni('Dikoras', 'Dikorasová'))
        self.prijmenis.append(Prijmeni('Ditrich', 'Ditrichová'))
        self.prijmenis.append(Prijmeni('Djakov', 'Djakovová'))
        self.prijmenis.append(Prijmeni('Dlouhý', 'Dlouhá'))
        self.prijmenis.append(Prijmeni('Dobenčák', 'Dobenčáková'))
        self.prijmenis.append(Prijmeni('Dobrovský', 'Dobrovská'))
        self.prijmenis.append(Prijmeni('Dobřický', 'Dobřická'))
        self.prijmenis.append(Prijmeni('Dočekal', 'Dočekalová'))
        self.prijmenis.append(Prijmeni('Dohnalík', 'Dohnalíková'))
        self.prijmenis.append(Prijmeni('Donutil', 'Donutilová'))
        self.prijmenis.append(Prijmeni('Dokoupil', 'Dokoupilová'))
        self.prijmenis.append(Prijmeni('Domanín', 'Domanínová'))
        self.prijmenis.append(Prijmeni('Donáth', 'Donáthová'))
        self.prijmenis.append(Prijmeni('Donda', 'Dondová'))
        self.prijmenis.append(Prijmeni('Donner', 'Donnerová'))
        self.prijmenis.append(Prijmeni('Dopita', 'Dopitová'))
        self.prijmenis.append(Prijmeni('Dorazil', 'Dorazilová'))
        self.prijmenis.append(Prijmeni('Dorica', 'Doricová'))
        self.prijmenis.append(Prijmeni('Dorňák', 'Dorňáková'))
        self.prijmenis.append(Prijmeni('Dorotík', 'Dorotíková'))
        self.prijmenis.append(Prijmeni('Dort', 'Dortová'))
        self.prijmenis.append(Prijmeni('Dořman', 'Dořmanová'))
        self.prijmenis.append(Prijmeni('Dospíšil', 'Dospíšilová'))
        self.prijmenis.append(Prijmeni('Dostalík', 'Dostalíková'))
        self.prijmenis.append(Prijmeni('Dostál', 'Dostálová'))
        self.prijmenis.append(Prijmeni('Doupal', 'Doupalová'))
        self.prijmenis.append(Prijmeni('Dovrtil', 'Dovrtilová'))
        self.prijmenis.append(Prijmeni('Drabálek', 'Drabálková'))
        self.prijmenis.append(Prijmeni('Drábek', 'Drábková'))
        self.prijmenis.append(Prijmeni('Dratva', 'Dratvová'))
        self.prijmenis.append(Prijmeni('Darebníček', 'Darebníčková'))
        self.prijmenis.append(Prijmeni('Drahoš', 'Drahošová'))
        self.prijmenis.append(Prijmeni('Drásal', 'Drásalová'))
        self.prijmenis.append(Prijmeni('Drazdík', 'Drazdíková'))
        self.prijmenis.append(Prijmeni('Dráždil', 'Dráždilová'))
        self.prijmenis.append(Prijmeni('Drbálek', 'Drbálková'))
        self.prijmenis.append(Prijmeni('Drdák', 'Drdáková'))
        self.prijmenis.append(Prijmeni('Dřevojánek', 'Dřevojánková'))
        self.prijmenis.append(Prijmeni('Drhlík', 'Drhlíková'))
        self.prijmenis.append(Prijmeni('Driml', 'Drimlová'))
        self.prijmenis.append(Prijmeni('Drkoš', 'Drkošová'))
        self.prijmenis.append(Prijmeni('Drlík', 'Drlíková'))
        self.prijmenis.append(Prijmeni('Drobek', 'Drobečková'))
        self.prijmenis.append(Prijmeni('Drobný', 'Drobná'))
        self.prijmenis.append(Prijmeni('Drozdík', 'Drozdíková'))
        self.prijmenis.append(Prijmeni('Drozen', 'Drozenová'))
        self.prijmenis.append(Prijmeni('Drtílek', 'Drtílková'))
        self.prijmenis.append(Prijmeni('Držka', 'Držková'))
        self.prijmenis.append(Prijmeni('Dřevický', 'Dřevická'))
        self.prijmenis.append(Prijmeni('Dřevojan', 'Dřevojanová'))
        self.prijmenis.append(Prijmeni('Dřímal', 'Dřímalka'))
        self.prijmenis.append(Prijmeni('Dřímal', 'Dřímalková'))
        self.prijmenis.append(Prijmeni('Dřízal', 'Dřízalová'))
        self.prijmenis.append(Prijmeni('Duba', 'Dubová'))
        self.prijmenis.append(Prijmeni('Ducar', 'Ducarová'))
        self.prijmenis.append(Prijmeni('Dudáček', 'Dudáčková'))
        self.prijmenis.append(Prijmeni('Dudek', 'Dudeková'))
        self.prijmenis.append(Prijmeni('Dudlíček', 'Dudlíčková'))
        self.prijmenis.append(Prijmeni('Dujka', 'Dujková'))
        self.prijmenis.append(Prijmeni('Dukátník', 'Dukátníková'))
        self.prijmenis.append(Prijmeni('Dulo', 'Dulová'))
        self.prijmenis.append(Prijmeni('Dumka', 'Dumková'))
        self.prijmenis.append(Prijmeni('Dundr', 'Dundrová'))
        self.prijmenis.append(Prijmeni('Dungl', 'Dunglová'))
        self.prijmenis.append(Prijmeni('Dopita', 'Dopitová'))
        self.prijmenis.append(Prijmeni('Dusil', 'Dusilová'))
        self.prijmenis.append(Prijmeni('Dutko', 'Dutková'))
        self.prijmenis.append(Prijmeni('Dužík', 'Dužíková'))
        self.prijmenis.append(Prijmeni('Dvorčák', 'Dvorčáková'))
        self.prijmenis.append(Prijmeni('Dvorník', 'Dvorníková'))
        self.prijmenis.append(Prijmeni('Dvořák', 'Dvořáková'))
        self.prijmenis.append(Prijmeni('Dýčka', 'Dýčková'))
        self.prijmenis.append(Prijmeni('Dychtl', 'Dychtlová'))
        self.prijmenis.append(Prijmeni('Dykas', 'Dykasová'))
        self.prijmenis.append(Prijmeni('Dyml', 'Dymlová'))
        self.prijmenis.append(Prijmeni('Dyškant', 'Dyškantová'))
        self.prijmenis.append(Prijmeni('Dziak', 'Dziaková'))
        self.prijmenis.append(Prijmeni('Dzurenka', 'Dzurenková'))
        self.prijmenis.append(Prijmeni('Dzurko', 'Dzurková'))
        self.prijmenis.append(Prijmeni('Džurný', 'Džurná'))
        self.prijmenis.append(Prijmeni('Džurban', 'Džurbová'))
        self.prijmenis.append(Prijmeni('Ebel', 'Ebelová'))
        self.prijmenis.append(Prijmeni('Eben', 'Ebenová'))
        self.prijmenis.append(Prijmeni('Eberle', 'Eberlová'))
        self.prijmenis.append(Prijmeni('Eckart', 'Eckartová'))
        self.prijmenis.append(Prijmeni('Ecler', 'Eclerová'))
        self.prijmenis.append(Prijmeni('Edefer', 'Edeferová'))
        self.prijmenis.append(Prijmeni('Edr', 'Edrová'))
        self.prijmenis.append(Prijmeni('Efler', 'Eflerová'))
        self.prijmenis.append(Prijmeni('Egert', 'Egertová'))
        self.prijmenis.append(Prijmeni('Ehmig', 'Ehmigová'))
        self.prijmenis.append(Prijmeni('Eibel', 'Eibelová'))
        self.prijmenis.append(Prijmeni('Eichenmann', 'Eichnmannová'))
        self.prijmenis.append(Prijmeni('Eicher', 'Eicherová'))
        self.prijmenis.append(Prijmeni('Eisert', 'Eisertová'))
        self.prijmenis.append(Prijmeni('Eitler', 'Eitlerová'))
        self.prijmenis.append(Prijmeni('Ejem', 'Ejemová'))
        self.prijmenis.append(Prijmeni('Ekert', 'Ekertová'))
        self.prijmenis.append(Prijmeni('Ekrt', 'Ekrtová'))
        self.prijmenis.append(Prijmeni('Elek', 'Eleková'))
        self.prijmenis.append(Prijmeni('Eliáš', 'Eliášová'))
        self.prijmenis.append(Prijmeni('Elichar', 'Elicharová'))
        self.prijmenis.append(Prijmeni('Eller', 'Ellerová'))
        self.prijmenis.append(Prijmeni('Elman', 'Elmanová'))
        self.prijmenis.append(Prijmeni('Elšík', 'Elšíková'))
        self.prijmenis.append(Prijmeni('Emrich', 'Emrichová'))
        self.prijmenis.append(Prijmeni('Endel', 'Endelová'))
        self.prijmenis.append(Prijmeni('Endris', 'Endrisová'))
        self.prijmenis.append(Prijmeni('Engliš', 'Englišová'))
        self.prijmenis.append(Prijmeni('Eret', 'Eretová'))
        self.prijmenis.append(Prijmeni('Erhart', 'Erhartová'))
        self.prijmenis.append(Prijmeni('Erps', 'Erpsová'))
        self.prijmenis.append(Prijmeni('Ešler', 'Ešlerová'))
        self.prijmenis.append(Prijmeni('Eštok', 'Eštoková'))
        self.prijmenis.append(Prijmeni('Evják', 'Evjáková'))
        self.prijmenis.append(Prijmeni('Ezr', 'Ezrová'))
        self.prijmenis.append(Prijmeni('Eysselt', 'Eysseltová'))
        self.prijmenis.append(Prijmeni('Exner', 'Exnerová'))
        self.prijmenis.append(Prijmeni('Exel', 'Exelová'))
        self.prijmenis.append(Prijmeni('Exnar', 'Exnarová'))
        self.prijmenis.append(Prijmeni('Fábel', 'Fábelová'))
        self.prijmenis.append(Prijmeni('Fáber', 'Fáberová'))
        self.prijmenis.append(Prijmeni('Fábera', 'Fáberová'))
        self.prijmenis.append(Prijmeni('Fabián', 'Fabiánová'))
        self.prijmenis.append(Prijmeni('Fabich', 'Fabichová'))
        self.prijmenis.append(Prijmeni('Fabrika', 'Fabriková'))
        self.prijmenis.append(Prijmeni('Facon', 'Faconová'))
        self.prijmenis.append(Prijmeni('Fadler', 'Fadlerová'))
        self.prijmenis.append(Prijmeni('Faflák', 'Fafláková'))
        self.prijmenis.append(Prijmeni('Fahoun', 'Fahounová'))
        self.prijmenis.append(Prijmeni('Fail', 'Failová'))
        self.prijmenis.append(Prijmeni('Fajčík', 'Fajčíková'))
        self.prijmenis.append(Prijmeni('Fajkoš', 'Fajkošová'))
        self.prijmenis.append(Prijmeni('Fajnor', 'Fajnorová'))
        self.prijmenis.append(Prijmeni('Fajx', 'Fajxová'))
        self.prijmenis.append(Prijmeni('Fakan', 'Fakanová'))
        self.prijmenis.append(Prijmeni('Fakla', 'Faklová'))
        self.prijmenis.append(Prijmeni('Faktor', 'Faktorová'))
        self.prijmenis.append(Prijmeni('Falsman', 'Falcmanová'))
        self.prijmenis.append(Prijmeni('Faldus', 'Faldusová'))
        self.prijmenis.append(Prijmeni('Foltýn', 'Foltýnová'))
        self.prijmenis.append(Prijmeni('Falhar', 'Falharová'))
        self.prijmenis.append(Prijmeni('Falis', 'Falisová'))
        self.prijmenis.append(Prijmeni('Faltín', 'Faltínová'))
        self.prijmenis.append(Prijmeni('Fanfrla', 'Fanfrlová'))
        self.prijmenis.append(Prijmeni('Fantl', 'Fantlová'))
        self.prijmenis.append(Prijmeni('Farář', 'Farářová'))
        self.prijmenis.append(Prijmeni('Farda', 'Fardová'))
        self.prijmenis.append(Prijmeni('Farek', 'Farková'))
        self.prijmenis.append(Prijmeni('Farhat', 'Farhat'))
        self.prijmenis.append(Prijmeni('Fariz', 'Farizová'))
        self.prijmenis.append(Prijmeni('Farkas', 'Farkasová'))
        self.prijmenis.append(Prijmeni('Farkaš', 'Farkašová'))
        self.prijmenis.append(Prijmeni('Farlík', 'Farlíková'))
        self.prijmenis.append(Prijmeni('Faron', 'Faronová'))
        self.prijmenis.append(Prijmeni('Farský', 'Farská'))
        self.prijmenis.append(Prijmeni('Fastner', 'Fastnerová'))
        self.prijmenis.append(Prijmeni('Faško', 'Fašková'))
        self.prijmenis.append(Prijmeni('Fatrla', 'Fatrlová'))
        self.prijmenis.append(Prijmeni('Faustus', 'Faustusová'))
        self.prijmenis.append(Prijmeni('Fazor', 'Fazorová'))
        self.prijmenis.append(Prijmeni('Fecko', 'Fecková'))
        self.prijmenis.append(Prijmeni('Federer', 'Federerová'))
        self.prijmenis.append(Prijmeni('Fedorko', 'Fedorková'))
        self.prijmenis.append(Prijmeni('Fedotov', 'Fedotova'))
        self.prijmenis.append(Prijmeni('Feglar', 'Feglarová'))
        self.prijmenis.append(Prijmeni('Fenhl', 'Fenhlová'))
        self.prijmenis.append(Prijmeni('Feiferlik', 'Feiferlíková'))
        self.prijmenis.append(Prijmeni('Feikl', 'Feiklová'))
        self.prijmenis.append(Prijmeni('Feith', 'Feithová'))
        self.prijmenis.append(Prijmeni('Fejco', 'Fejcová'))
        self.prijmenis.append(Prijmeni('Fejfer', 'Fejferová'))
        self.prijmenis.append(Prijmeni('Fekl', 'Feklová'))
        self.prijmenis.append(Prijmeni('Felbr', 'Felbrová'))
        self.prijmenis.append(Prijmeni('Felix', 'Felixová'))
        self.prijmenis.append(Prijmeni('Fellmann', 'Fellmannová'))
        self.prijmenis.append(Prijmeni('Fencl', 'Fenclová'))
        self.prijmenis.append(Prijmeni('Fenčák', 'Fenčáková'))
        self.prijmenis.append(Prijmeni('Feňo', 'Feňová'))
        self.prijmenis.append(Prijmeni('Fenkl', 'Fenklová'))
        self.prijmenis.append(Prijmeni('Fenyk', 'Fenyková'))
        self.prijmenis.append(Prijmeni('Fenzel', 'Fenzelová'))
        self.prijmenis.append(Prijmeni('Ferák', 'Feráková'))
        self.prijmenis.append(Prijmeni('Ferbar', 'Ferbarová'))
        self.prijmenis.append(Prijmeni('Ferčák', 'Ferčáková'))
        self.prijmenis.append(Prijmeni('Ferdan', 'Ferdanová'))
        self.prijmenis.append(Prijmeni('Ferdus', 'Ferdusová'))
        self.prijmenis.append(Prijmeni('Ferenčák', 'Ferenčáková'))
        self.prijmenis.append(Prijmeni('Fereš', 'Ferešová'))
        self.prijmenis.append(Prijmeni('Ferkl', 'Ferklová'))
        self.prijmenis.append(Prijmeni('Ferstl', 'Ferstlová'))
        self.prijmenis.append(Prijmeni('Ferzik', 'Ferziková'))
        self.prijmenis.append(Prijmeni('Fialík', 'Fialíková'))
        self.prijmenis.append(Prijmeni('Fiala', 'Fialová'))
        self.prijmenis.append(Prijmeni('Fionta', 'Fiontová'))
        self.prijmenis.append(Prijmeni('Fiantok', 'Fiantoková'))
        self.prijmenis.append(Prijmeni('Fibrich', 'Fibrichová'))
        self.prijmenis.append(Prijmeni('Ficko', 'Ficková'))
        self.prijmenis.append(Prijmeni('Fiebich', 'Fiebichová'))
        self.prijmenis.append(Prijmeni('Fiedler', 'Fiedlerová'))
        self.prijmenis.append(Prijmeni('Fiedor', 'Fiedorová'))
        self.prijmenis.append(Prijmeni('Fieger', 'Fiegerová'))


    def PrintAll():
        for prijmeni in self.prijmenis:
            print(prijmeni.nazev)
