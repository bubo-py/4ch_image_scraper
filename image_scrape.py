import requests
from urllib.request import urlretrieve
from bs4 import BeautifulSoup


# pattern for putting url here is /board/thread/9999, ex: https://boards.4channel.org/c/thread/3752784
# set url to get
url = input('Pattern for putting url is /board/thread/9999\nPut your url here: ')
source_code = requests.get(url).text # get url by requests and HTML code by .text

soup = BeautifulSoup(source_code, 'lxml') # parse HTML code by lxml parser and bs

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

    print(f'Succesfully downloaded {image_name}') # feedback to user

print('All possible images have been downloaded!')