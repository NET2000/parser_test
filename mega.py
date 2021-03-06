import os
from selenium import webdriver

from requests import get
from bs4 import BeautifulSoup

from fnmatch import fnmatch
from shutil import move

def make_download_dir(were):
    if not os.path.exists(were):
        os.makedirs(were)

def make_album_dir(default_download_path, album_title):
    try:
        album_folder=f'{default_download_path}\\{album_title}'
        make_download_dir(f'{default_download_path}./{album_title}/')
    except OSError:
        print('[не могу создать директорию с именем альбома, файлы будут загружены в папку "Backup folder"]')
        album_folder=f'{default_download_path}\\Backup folder'
        if not os.path.exists(album_folder):
            os.makedirs(f'{default_download_path}./Backup folder/')
    return album_folder

def something_wrong_msg(level):
	msg={
                0:'[нужно указать только 1 или 2]',
		1:'[введена не соответствующая ссылка]',
		2:'[обьект не доступен]'
            }
	print(msg[level])

def chrome_download_path(home_path):
    default_download_path=None
    print('1 - создать каталог \'Music store\' в папке \'Загрузки\'\n2 - указать другую папку для хранения музыки?')
    while not default_download_path:
        dir_choice=input('> ')
        if dir_choice=='1':
            make_download_dir(f'{home_path}./Music store/') 
            default_download_path=f'{home_path}\\Music store'
            with open('my_download_folder', 'w') as f:
                f.write(default_download_path)
        elif dir_choice=='2':
            while not default_download_path:
                some_user_path=input(r'скопируйте и вставьте путь: ')
                if os.path.exists(some_user_path):
                    default_download_path=some_user_path
                else: print('неверный формат записи, попробуйте ещё раз\n')
            with open('my_download_folder', 'w') as f:
                f.write(default_download_path)
        else: something_wrong_msg(0)
    return default_download_path

def checking_album_title(name):
    name=('%r'%name.split('-',1)[-1].strip()).strip("'")
    characters='\/:*?"<>|'
    for e in characters:
        if e in name:
            name=name.replace(e, '')
    return name

def get_tracklists(url, source, mirror, empty=None): 
    html_doc=get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    #title=soup.find('td', class_='txt').span.text
    album_title=checking_album_title(soup.title.string)
    source_track_list=empty or []
    mirror_track_list=empty or []
    for link in soup.find_all('div', class_='ui360'):
        preview_track=link.find('a').get('href')
        # СПЕЦИАЛЬНО УБРАНЫ ЗНАЧЕНИЯ ЗАМЕНЯЮЩИЕ ЧАСТЬ СТРОК, ИНФА НЕ ПРЕДУСМОТРЕНА ДЛЯ ПРОМОТРА ТРЕТЬЕГО ЛИЦА
        source_track_list.append(preview_track.replace(source+r'common/preview/track/', source+r''))
        mirror_track_list.append(preview_track.replace(source+r'common/preview/track/', mirror+r''))
    return source_track_list, mirror_track_list, album_title

# ***********************************************************************************************************************************

# lelel 0 - выбор сервера, выбор папки загрузки, параметры браузера
server_one='https://megaboon.com/'
server_two='https://melodysale.com/'
print(f'источники:\n1 - {server_one}\n2 - {server_two}\nс которого начнем?')
source=None
while not source:
    choice=input('\n> ')
    if choice=='1':
        source=server_one
        mirror=server_two
    elif choice=='2':
        source=server_two
        mirror=server_one
    else: something_wrong_msg(0)

# стандартная пака "Загрузки" windows 10
user_download_path=os.path.expanduser('~'+'\\Downloads') 


if not os.path.exists('my_download_folder'):
    default_download_path=chrome_download_path(user_download_path)
else:
    default_download_path=open('my_download_folder').readline()
    if not os.path.exists(default_download_path):
        default_download_path=chrome_download_path(user_download_path)
          

try:
    download_path={'download.default_directory' : default_download_path, 'directory_upgrade' : True}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('prefs', download_path)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])   # "DevTools listening on ws://127.0.0.1"
    chrome_options.add_argument("user-data-dir=chrome_settings") 
    chrome_driver=webdriver.Chrome(options=chrome_options)
    chrome_driver.get(source)
except:
    print('\nЧто то не так, возможно:\n1 - "браузер открыт повторно" - закройте отдельные окна браузера, и перезапустите программу\n2 - "устарела библиотека webdriver" по причине обновления вашего браузера - необходимо загрузить файл "chromedriver" соответствующей версии ващего браузера в директорию с программой, ресурс: https://chromedriver.chromium.org/download\n')
    print('команда \'auto\' - позволит программе попытатся самой скачать и установить chromedriver')
    action=None
    while not action:
        action=input('auto(a) | quit(q)\n> ')
        if action=='auto' or action=='a': import add_on_
        elif action=='quit' or action=='q':quit()
        else: action=None; print('не известная команда')
    
# ***********************************************************************************************************************************

def download_files_selectively(string_numbers):
    '''загрузка файлов по номерам в строке'''
    for user_number in string_numbers.split(','):
        if user_number.isdigit():
            user_number=int(user_number)
            if user_number<1:
                print(f'трэка c номером {user_number} в списке нет, первый трэк имеет номер 1')
                continue
            elif user_number>len(temp[0]):
                print(f'число {user_number} превышает количество трэков в списке')
                continue
            try:
                chrome_driver.get(temp[0][user_number-1])
            except:
                try:
                    chrome_driver.get(temp[1][user_number-1])
                except:
                    something_wrong_msg(2)    
        else:
            print(f'\'{user_number}\' - неизвестное выражение')
            continue

def download_all_files():
    try:
        for link in temp[0]:
            chrome_driver.get(link)
    except:
        try:
            for rlink in temp[1]:
                chrome_driver.get(rlink)
        except:
            something_wrong_msg(2)
       
def bundle_folder():
    for music_file in [file for file in os.listdir(default_download_path) if fnmatch(file, '*.mp3')]:
        current_file=f'{default_download_path}//{music_file}'
        if music_file in os.listdir(album_folder): os.remove(current_file)
        else: move(current_file, album_folder)
        
def help_msg():
    print(f'\n[music parser v2.0]\n\nquit\t\tбезопасное завершение программы\nurl\t\tввести ссылку альбома\nall\t\tскачать альбом полностью\n1,3,9..\t\tформа записи для выборочной загрузки трэков\n')
    print('примечание: для смены "папки загрузок" можна вручную изменить путь в файле my_download_folder.txt в папке с программой, или удалить этот файл, и переопределить папку при следующем старте программы')

def check_link(l):
        lp=[e for e in l.split('/') if e]
        if (lp[0]=='https:' or lp[0]=='http:') and (lp[1] in source) and len(lp)==4 and lp[-1].endswith('.html'):
                return True
        something_wrong_msg(1)
        global user_link
        user_link=None
        
# ***********************************************************************************************************************************        

#level 1 - меню, порядок переключения
print(f'\nДо работы с приложением войдите в учётную запись {source}')
 
while True:
    user_link=input('\nurl > ')
    if user_link=='quit': chrome_driver.quit(),quit()
    elif check_link(user_link):
        temp=get_tracklists(user_link, source, mirror)
        if not temp[0]: 
            temp=None
            something_wrong_msg(1)
        else: album_folder=make_album_dir(default_download_path, temp[2])
        while temp:
            user_command=input('\n[1,2,3..] | all | url | help | quit\n> ')
            if user_command=='all':download_all_files()
            elif user_command=='url':
                bundle_folder()
                temp=None
            elif user_command=='help':help_msg()
            elif user_command=='quit':bundle_folder(),chrome_driver.quit(),quit()
            else: download_files_selectively(user_command)

            
# Ukraine, 08.2019
