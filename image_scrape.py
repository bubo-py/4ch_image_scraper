import os
from shutil import move
import requests
from urllib.request import urlretrieve
from bs4 import BeautifulSoup


# pattern for putting url here is /board/thread/9999, ex: https://boards.4channel.org/c/thread/3752784
# set url to get
url = input('Pattern for putting url is /board/thread/9999\nPut your url here: ')
source_code = requests.get(url).text # get url by requests and HTML code by .text

soup = BeautifulSoup(source_code, 'lxml') # parse HTML code by lxml parser and bs

c = 1 # set default count value

# find all <div> with class 'postContainer' in parsed HTML
for post in soup.find_all('div', class_='postContainer'):

    try:
        # look for <div> with class 'file' in every found post
        post_file_section = post.find('div', class_='file')

        # get <a> from extracted above section
        post_image = post_file_section.a

        # get only text without HTML code(here it happens to be exactly image name)
        image_name = post_image.text

        image_link = post_image.get('href') # get 'href' link from <a> tag
        image_link = image_link.split('//')[1] # split and get the proper link

    # if there's not image, continue scraping next posts(instead of crashing program)
    except AttributeError:
        continue
    
    # download image from extracted link with the name that it had
    urlretrieve(f"http://{image_link}", f"{image_name}")

    print(f'#{c} Succesfully downloaded {image_name}') # feedback to user
    c += 1 # increase counting images every download image
    
print('All possible images have been downloaded!')

# ask if user want to rename images
rename_answer = input('Do you want to rename your images? Type "n" or "y": ')


if rename_answer == 'y':
    new_name = input('\nWhat do you want new filename to be?\n') # ask for new filename
    n = 0
    for filename in os.listdir(): # look for files in current directory
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.gif'): # take all jpg/png/gif
            # change to given filename and count them
            os.rename(filename, f'{new_name}_{n}{filename[-4:]}')
            n += 1 # every file increase the number

print('All filenames have been changed!') # additional user feedback

# location of the destination folder
new_location = "ADD_FOLDER_PATH_HERE"
move_answer = input('Do you want to move your images? Type "n" or "y": ')

if move_answer == 'y':
    for filename in os.listdir(): # look for files in current directory
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.gif'): # take all jpg/png/gif
            # shutil method that moves file to different location with the same name
            move(f"{filename}", f"{new_location}/{filename}")
