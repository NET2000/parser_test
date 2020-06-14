from bs4 import BeautifulSoup
import os,requests,wget,zipfile
from win32com.client import Dispatch # модуль pywin32

def get_driver(l):
    all_links=list()
    for e in l.find_all('a'):
        wpath=e.get('href')
        if not wpath in all_links: all_links.append(wpath)
    clear_links=['/'.join(x.split('/')[:-1]) for x in all_links if x and x.endswith('notes.txt')]
    clear_links={e.split('/')[-1]:e for e in clear_links}
    return clear_links

def get_version(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version

# удаляем старый файл
driver='chromedriver.exe'
if driver in os.listdir():
    os.remove(driver)

# узнаем версию google chrome 
x86,x64=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe', r'C:\Program Files\Google\Chrome\Application\chrome.exe'
my_version=get_version(x86) or get_version(x64)
if not my_version:
    upath=input('папка браузера не найдена по стандартному пути\nвведите своё расположение по примеру: My_path\Google\Chrome\Application\chrome.exe\n')
    my_version=get_version(upath)
    if not my_version: input('файл по этому пути не обнаружен, перезапустите программу и введите корректный путь, или загрузите драйвер самостоятельно\nнажмите Enter для выхода'), quit() 


mvp=lambda x:'.'.join(x.split('.')[:-1])
#print(mvp(my_version))

# парсер составляет словарь ссылок на драйвер, key - версия браузера, value - ссылка на загрузку
try: html=requests.get('https://chromedriver.chromium.org/downloads').text
except: print('ресурс не доступен, проверьте подключение к интернету\n'),input('Enter для выхода '),quit()
page=BeautifulSoup(html, 'html.parser')
fragment=page.find('td', class_="sites-layout-tile sites-tile-name-content-1")
dlinks=get_driver(fragment)

# определяем необходимую ссылку по версии браузера
file='chromedriver_win32.zip'
for e in dlinks:
    if my_version==e or mvp(my_version)==mvp(e):
        my_driver_link=f'{dlinks[e]}/{file}'
        break
#print(my_driver_link)

# загружаем и распаковываем архив
wget.download(my_driver_link)
with zipfile.ZipFile(file) as zfile:
    zfile.extractall()

# удаляем архив
os.remove(file)
input('\nchrome драйвер установлен!\n\nнажмите Enter для выхода, и запустите программу ещё раз'),quit()


