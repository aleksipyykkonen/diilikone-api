

def get_message(deal, provision):
    message = """Arvon myyjä, %s!

Olet juuri sinetöinyt Wapustasi unohtumattoman kokemuksen tekemällä Äpy-diilin. Alta löydät yhteenvedon diilisi tiedoista sekä henkilökohtaisen myyjäpalvelijasi yhteystiedot.

Muistathan, että voit vielä nostaa diilisi provikkaa liittämällä henkilökohtaisen diilisi johonkin ryhmädiiliin tai perustamalla oman ryhmädiilin. Tämän voit tehdä ottamalla yhteyttä henkilökohtaiseen myyjäpalvelijaasi.

[diilin yhteenveto, jos on aikaa ja jaksaa, niin tähän voi pistää jonkun “tällä provikalla saat n pakettia kyniä pohjois-tiibetiläisille koululapsille tai z kpl hitsauslaseja laivapurkaamoilla rehkiville keskislapsille]

Lehtien määrä: %d
Provikka: %.2fe

Myyjäpalvelijasi:

[yhteystiedot, noreply@äpy.fi]

Terveisin,
Diilikoneesi, M. Asiina
Äpy - Neljä kirjainta joihin voit luottaa""" %(deal.salesperson.first_name, deal.size, provision)

    return message
