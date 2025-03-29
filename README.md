# Tietokannat-ja-web-ohjelmointi-projekti

Moi testi

projekti aihe:
Joku sovellus, jossa olisi kartta hanakaljan hinnoista. Käyttäjät pääsisi lisäämään baareja/klubeja/ravintoloita ja niissä olevien hanakaljojen hinnan. Niissä voi myös kategoroida minkä merkkistä kaljaa on, esim koffin/hartwallin tuotteet tai jotai sellasta.
Voisi sinäänsä olla jopa indeksinä sijainnin tuotteiden hinnalle.....?



Bisse sovellus
- Sovelluksessa on kartta, johon käyttäjät voi lisätä baareja. Tähän pitäisi sitten vielä olla joku systeemi vahinko inputeille, sulkeutuneille baareille, etc..
- Kartassa kun painelee sijainteja, niin voi nähdä baarin hanatuotteiden hintoja.
- Käyttäjät voivat luoda tunnuksen ja kirjautumaan sisään, vain rekisteröidyt käyttäjät voivat lisätä baareja ja muutella tuotteiden hintoja.
- Sovelluksessa voi etsiä baarin nimiä.
- Sovelluksessa voi katsoa käyttäjäsivua, josta näkee paljon käyttäjä on "kontribuoinut". määrä lisätyistä baareista, hintojen muutoksista, hintojen tarkkuudesta... Käyttäjä sivuissa voi olla myös esim. käyttäjä rating.
- Sovelluksissa voisi olla "opiskelija ystävälliset" baarit eri merkkauksilla. Esim. hyväksyvät haalarit sisään, opiskelija alennukset, haalarimerkkien myynti
- Sijaintien hanajuomissa, myös minkä panimon tuotteita, tai useammankin, juoman tilavuus (koko). (Hartwall, koff.....)
- Sijainteihin voi jättää kommentteja ja arvosteluita...? Ja niiden keskiarvosana.


Edit: 29.3

Kartan implementointi vaikuttaa nyt tosi vaikeelta. Ehkä vaihdan projektia niin, että se toimii ilman karttaa. Sovelluksessa voi nyt kirjautua sisään, rekisteröityä, kirjautua ulos. Sivustoissa lisätty sidebar/navigointi hommeli josta voi päästä sivulta toiseen. Sovelluksessa on sivu, jossa voi luoda uuden tietokohteen, mutta tietokohdetta ei lisätä tietokantaan, eikä sitä voi muokata/poistaa/lähettää (on vain sivusto). Luonti sivu on vaikea, paljon vaihoehtoja hanajuomista. Mietityttää, että olisiko jotenkin järkevämmin voinut laittaa noi ja vielä niin, että olisi helppo implementoida tuo tietokantaan...
