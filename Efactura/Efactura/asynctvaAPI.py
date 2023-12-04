import asyncio
from datetime import datetime
from time import sleep
import json, httpx
import asyncio


class Anafapi:
    ANAF_AURL = "https://webservicesp.anaf.ro/AsynchWebService/api/v8/ws/tva"
    ANAF_URL = "https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/ws/tva"
    headers: dict[str, str] = {
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.7,ro;q=0.3",
        "Connection": "keep-alive",
        "Referer": "https://mfinante.gov.ro",
        "Content-Type": "application/json",
    }
    today: str = datetime.today().strftime("%Y-%m-%d")

    def __init__(self, cui) -> None:
        self.classname: str = self.__class__.__name__
        self.payload: list[dict] = [{"cui": cui, "data": self.__class__.today}]
        print(self.payload)

    async def syncpost(self) -> httpx.Response | dict:
        try:
            async with httpx.AsyncClient() as asynclient:
                asyncresponse: httpx.Response = await asynclient.post(
                    "https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/ws/tva",
                    data=json.dumps(self.payload),
                    headers=self.__class__.headers,
                    timeout=5,
                )
                print(asyncresponse.status_code, asyncresponse.json())
                return asyncresponse
        except Exception as connerror:
            print("Eroare de conexiune la serverele ANAF!", connerror)
            return {
                "message": "Eroare de conexiune la serverele ANAF!",
                "error": connerror,
            }
        
    async def asyncpostid(self) -> httpx.Response | dict:
        try:
            async with httpx.AsyncClient() as asynclient:
                asyncresponse: httpx.Response = await asynclient.post(
                    "https://webservicesp.anaf.ro/AsynchWebService/api/v8/ws/tva",
                    data=json.dumps(self.payload),
                    headers=self.__class__.headers,
                    timeout=10)
            print(self.payload, asyncresponse.status_code, asyncresponse.json())
            return asyncresponse
        except Exception as connerror:
            print("Eroare de conexiune asincronă la serverele ANAF!", connerror)
            return {
                "message": "Eroare de conexiune la serverele ANAF!",
                "error": connerror,
            }

    async def parseresponse(self):
        try:
            data = await self.syncpost()
            if type(data) == dict and data.status_code == 200:
                categories: dict = data.json()["found"]
                date_generale: dict = categories["date_generale"]
                inregistrare_scop_Tva: dict = categories["inregistrare_scop_Tva"]
                perioade_TVA: list = inregistrare_scop_Tva["perioade_TVA"]
        except Exception as parsingerror:
            print("Eroare parsare json!", parsingerror)

    async def parsecorrelationId(self, idresponse):
        idresponse = await self.asyncpostid()
        if type(idresponse) == dict:
            return idresponse # error
        else:
            correlationId = idresponse.json().get('correlationId')
            print(correlationId)
            return correlationId

    async def asyncgetid(self, correlationId) -> httpx.Response | dict:
        try:
            async with httpx.AsyncClient() as asynclient:
                asyncresponse: httpx.Response = await asynclient.post(
                    f'https://webservicesp.anaf.ro/AsynchWebService/api/v8/ws/tva?id={correlationId}',
                    headers=self.__class__.headers,
                    timeout=10)
            print(self.data, asyncresponse.status_code, asyncresponse.json())
            return asyncresponse
        except Exception as connerror:
            print("Eroare de conexiune asincronă la serverele ANAF!", connerror)
            return {
                "message": "Eroare de conexiune la serverele ANAF!",
                "error": connerror,
            }

    async def main(self):
        try:
            response = await self.syncpost()
            if type(response) != dict:
                return await self.parseresponse()
            else:
                print("Eroare serviciu sincron, încerc serviciul asincron!")
                asyncidresponse = await self.asyncpostid()
                correlationId = await self.parsecorrelationId(asyncidresponse)
                await asyncio.sleep(2)
                asyncresponse = await self.asyncgetid(correlationId)
                if type(asyncresponse) != dict:
                    return await self.parseresponse()
                return asyncresponse
        except Exception as mainerror:
            print("Eroare funcție principală, încerc serviciul asincron!", mainerror)


if __name__ == "__main__":
    anafapi_instance = Anafapi(19479100)
    asyncio.run(anafapi_instance.main())

"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.7,ro;q=0.3',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json',
    'Origin': 'https://www.totalfirme.ro',
    'DNT': '1',
    'Alt-Used': 'www.totalfirme.ro',
    'Connection': 'keep-alive',
    'Referer': 'https://www.totalfirme.ro/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}
    json_data = {
        'query': '19467555',
    }

    response = client.post('https://www.totalfirme.ro/firmelike', headers=headers, json=json_data)

    print(response.json())

    
# from requests.adapters import HTTPAdapter

# DEFAULT_TIMEOUT = 5 # seconds

# class TimeoutHTTPAdapter(HTTPAdapter):
#     def __init__(self, *args, **kwargs):
#         self.timeout = DEFAULT_TIMEOUT
#         if "timeout" in kwargs:
#             self.timeout = kwargs["timeout"]
#             del kwargs["timeout"]
#         super().__init__(*args, **kwargs)

#     def send(self, request, **kwargs):
#         timeout = kwargs.get("timeout")
#         if timeout is None:
#             kwargs["timeout"] = self.timeout
#         return super().send(request, **kwargs)

# session = requests.Session()
# # Mount it for both http and https usage
# adapter = TimeoutHTTPAdapter(timeout=10)
# session.mount("https://", adapter)
# session.mount("http://", adapter)


data = [{'cui': '19467555', 'data': today}]



In caz de inregistrare cu success a cererii:
            {"cod": 200,
               "message": "Successful",
               "correlationId": "ef050120-067e-4ba9-bc34-b8976081d289"}
2) Pentru descarcarea raspunsului se apeleaza urmatorul serviciu web prin GET:
            https://webservicesp.anaf.ro/AsynchWebService/api/v8/ws/tva?id=ef050120-067e-4ba9-bc34-b8976081d289
a) Raspunsul poate fi descarcat o singura data
b) Clientul trebuie sa astepte minim 2 secunde inainte sa inceapa descarcarea raspunsului (primul GET). 
La fiecare GET efectuat pe serviciul de descarcare raspuns exista posibilitatea ca raspunsul sa nu fie inca disponibil. 
In acest scenariu, clientul trebuie sa reincerce descarcarea prin efectuarea unui nou request GET. 
Se recomanda configurarea clientului astfel incat sa suporte un timeout de minim 10 secunde pentru un request.
"""

"""
def get_Anaf(cod, data=False):
    if not data:
        # data = datetime.now()
        data = '2023-17-10'
    if type(cod) in [list, tuple]:
        json_data = [{"cui": x, "data": data} for x in cod]
    else:
        json_data = [{"cui": cod, "data": data}]
    try:
        res = requests.post(ANAF_URL, json=json_data, headers=headers, timeout=30)
    except Exception as ex:
        return ("ANAF Webservice not working. Exeption=%s.") % ex, {}
    
    result = {}
    anaf_error = ""
    if (
        res.status_code == 200
        and res.headers.get("content-type") == "application/json"
    ):
        resjson = res.json()
        if type(cod) in [list, tuple]:
            result = resjson
        else:
            if resjson.get("found") and resjson["found"][0]:
                result = resjson["found"][0]
            if not result or not result.get("date_generale"):
                anaf_error = _("Anaf didn't find any company with VAT=%s !") % cod
    else:
        anaf_error = _(
            "Anaf request error: \nresponse=%(response)s "
            "\nreason=%(reason)s \ntext=%(text)s",
            response=res,
            reason=res.reason,
            text=res.text,
        )
    return anaf_error, result

print(get_Anaf(19467555, data=False))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.7,ro;q=0.3',
    'Referer': 'https://mfinante.gov.ro/apps/agenticod.html',
    'Origin': 'https://mfinante.gov.ro',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

data = {
    'pagina': 'domenii',
    'cod': '19467555',
    'B1': 'VIZUALIZARE',
}

response = requests.post('https://mfinante.gov.ro/apps/infocodfiscal.html', headers=headers, data=data)
print(response.text)

Function to retrieve data from ANAF for one vat number
at certain date

:param str cod:  vat number without country code or a list of codes
:param date data: date of the interogation
:return dict result: cost of the body's operation

{
"cui": "-- codul fiscal --",
"data": "-- data pentru care se efectueaza cautarea --",
"denumire": "-- denumire --",
"adresa": "-- adresa --",
"nrRegCom": "-- numar de inmatriculare la Registrul Comertului --",
"telefon": "-- Telefon --",
"fax": "-- Fax --",
"codPostal": "-- Codul Postal --",
"act": "-- Act autorizare --",
"stare_inregistrare": "-- Stare Societate --",
"scpTVA": " -- true -pentru platitor in scopuri de tva / false in cazul in
               care nu e platitor  in scopuri de TVA la data cautata  --",
"data_inceput_ScpTVA": " -- Data înregistrării în scopuri de TVA anterioară --",
"data_sfarsit_ScpTVA": " -- Data anulării înregistrării în scopuri de TVA --",
"data_anul_imp_ScpTVA": "-- Data operarii anularii înregistrării în scopuri de TVA --",
"mesaj_ScpTVA": "-- MESAJ:(ne)platitor de TVA la data cautata --",
"dataInceputTvaInc": " -- Data de la care aplică sistemul TVA la încasare -- ",
"dataSfarsitTvaInc": " -- Data până la care aplică sistemul TVA la încasare --",
"dataActualizareTvaInc": "-- Data actualizarii --",
"dataPublicareTvaInc": "-- Data publicarii --""
"tipActTvaInc": " --Tip actualizare --",
"statusTvaIncasare": " -- true -pentru platitor TVA la incasare/ false in
                       cazul in care nu e platitor de TVA la incasare la
                       data cautata --",
"dataInactivare": " --     -- ",
"dataReactivare": " --     -- ",
"dataPublicare": " --     -- ",
"dataRadiere": " -- Data radiere -- ",
"statusInactivi": " -- true -pentru inactiv / false in cazul in care nu este
                       inactiv la data cautata -- ",
"dataInceputSplitTVA": "--     --",
"dataAnulareSplitTVA": "--     --",
"statusSplitTVA": "-- true -aplica plata defalcata a Tva / false - nu aplica
                     plata defalcata a Tva la data cautata  --",
"iban": "-- contul IBAN --",
"statusRO_e_Factura": "-- true - figureaza in Registrul RO e-Factura / false
                     - nu figureaza in Registrul RO e-Factura la data cautata  --",
"sdenumire_Strada": "-- Denumire strada sediu --",
"snumar_Strada": "-- Numar strada sediu --",
"sdenumire_Localitate": "-- Denumire localitate sediu --",
"scod_Localitate": "-- Cod localitate sediu --",
"sdenumire_Judet": "-- Denumire judet sediu --",
"scod_Judet": "-- Cod judet sediu --",
"stara": "-- Denumire tara sediu -- ",
"sdetalii_Adresa": "-- Detalii adresa sediu --",
"scod_Postal": "-- Cod postal sediu --",
"ddenumire_Strada":  -- Denumire strada domiciliu fiscal --",
"dnumar_Strada": "-- Numar strada domiciliu fiscal --",
"ddenumire_Localitate": "-- Denumire localitate domiciliu fiscal --",
"dcod_Localitate": "-- Cod localitate domiciliu fiscal --",
"ddenumire_Judet": "-- Denumire judet domiciliu fiscal --",
"dcod_Judet": "-- Cod judet domiciliu fiscal --",
"dtara": "-- Denumire tara domiciliu fiscal --",
"ddetalii_Adresa": "-- Detalii adresa domiciliu fiscal --",
"dcod_Postal": "-- Cod postal domiciliu fiscal --",
"data_inregistrare": "-- Data inregistrare -- ",
"cod_CAEN": "-- Cod CAEN --",             }
"""
