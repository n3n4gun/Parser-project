import requests
import pandas
import datetime
from bs4 import BeautifulSoup

# Создание класса парсера, в котором будут созданы метода для получения информации с сайта
# Метод получения URL адреса сайта https://finance.rambler.ru/currencies/
class WebReader:                                     
    def URLAcceptance(self, URLaddress):           
        self.URLaddress = URLaddress

# Метод отправки первоначального запроса на сайт
    def WEBrequest(self):                                   
        self.request = requests.get(self.URLaddress)   

# Метод получения информации с сайта
    def WEBparser(self):                              
        soup = BeautifulSoup(self.request.text, 'lxml')

        currencyInformation = []

        self.exchange_rate = [information.text.replace('\n', ' ') for information in soup.find('div', class_ = 'finance-currency-table__body')]
        self.dataFrame_exchange_rate = pandas.DataFrame(self.exchange_rate)
        for info in self.dataFrame_exchange_rate.iterrows():
            currencyInformation.append(info[1][0])

        for space in currencyInformation:
            if space == ' ':
                currencyInformation.remove(space)

        for strings in range(len(currencyInformation)):
            currencyInformation[strings] = currencyInformation[strings].strip()

        for elements in range(len(currencyInformation)):
            currencyInformation[elements] = currencyInformation[elements].split()

        self.dataFrame_exchange_rate = pandas.DataFrame(currencyInformation, columns = ['Код', 'Номинал', 'Валюта', '', 'Курс ЦБ', 'Изменения', '%', 'Доп. %', 'Доп. %']).to_markdown()

    # Метод вывода информации
    def showCurrencyInformation(self):                 

        now_time = datetime.datetime.now()
        print('Курс международных валют на: {}.{}.{} {}:{}'.format(now_time.day, now_time.month, now_time.year, now_time.hour, now_time.minute))
        
        with pandas.option_context('display.max_rows', None):
            print(self.dataFrame_exchange_rate)

if __name__ == '__main__':
    webSite = WebReader()
    webSite.URLAcceptance('https://finance.rambler.ru/currencies/')
    webSite.WEBrequest()
    webSite.WEBparser()
    webSite.showCurrencyInformation()