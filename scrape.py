import requests
from lxml import html
from BeautifulSoup import BeautifulSoup, Comment
import httplib  # or http.client if you're on Python 3

httplib._MAXHEADERS = 1000

class Scraper():
    my_headers = ''
    startpagina_url = ''
    personalia_url = ''
    authenticate_url = ''
    resultaten_url = ''
    resultaten = []
    form = ''
    session = ''

    def __init__(self, username, password):
        # Aanvraagheaders
        self.my_headers = {
            "Host": "studievolg.hsleiden.nl",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "nl,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Referer": "https://studievolg.hsleiden.nl/student/StartPagina.do",
            "Connection": "keep-alive"
        }

        self.startpagina_url = 'https://studievolg.hsleiden.nl/student/StartPagina.do'
        self.personalia_url = 'https://studievolg.hsleiden.nl/student/Personalia.do'  # add headers here..
        self.authenticate_url = 'https://studievolg.hsleiden.nl/student/AuthenticateUser.do'  # add form shit here
        self.resultaten_url = 'https://studievolg.hsleiden.nl/student/ToonResultaten.do'

        # aanvraag form voor authentication
        self.form = {
            "startUrl": "Personalia.do",
            "inPortal": "",
            "callDirect": "",
            "VB_gebruikersNaam": username,
            "VB_wachtWoord": password,
            "event": "login",
            "requestToken": ""
        }

        self.session = requests.Session()

    def get_startpagina(self):
        self.my_headers['startUrl'] = "Personalia.do"
        request = self.session.get(self.startpagina_url, params=self.my_headers)
        response_html = html.fromstring(request.content)
        self.form['requestToken'] = response_html.xpath('//input[@id="requestToken"]/@value')[0]

    def get_personalia(self):
        self.my_headers['Referer'] = self.startpagina_url
        self.session.get(self.personalia_url, params=self.my_headers)

    def get_authorisation(self):
        self.my_headers['Referer'] = self.personalia_url
        self.session.post(self.authenticate_url, params=self.my_headers, data=self.form)

    def get_resultaten(self):
        request = self.session.get(self.resultaten_url, params=self.my_headers)
        resultaten_html = BeautifulSoup(request.content)
        return resultaten_html

    def get_cijfers(self, resultaten_html):
        table_rows = resultaten_html.find('table', {"class": "OraTableContent"})
        results = []
        td = table_rows.findAll("tr")
        # [1:] is alles behalve eerste resultaat, bevat namelijk de headers
        for row in td[1:]:
            test = row.findAll("span")
            for index, element in enumerate(test):
                test[index] = test[index].text

            print('Result obtained:', test)

            results.append(test)
        self.resultaten = results
        return results

    def get_cijferlijst(self):
        return self.resultaten

    def scrape(self):
        self.get_startpagina()
        self.get_personalia()
        self.get_authorisation()
        resultaten_html = self.get_resultaten()
        results = self.get_cijfers(resultaten_html)
        return results
