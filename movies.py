from bs4 import BeautifulSoup as bs
import requests
import csv
import os

headers = {
    "User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0"
}

# get image src
def get_images_src(page):
    container = bs(page.content, "lxml")
    lst_of_movies = container.find_all("li", class_ = "ipc-metadata-list-summary-item")
    images_src = []
    for lst in lst_of_movies:
        images_tag = lst.find("img")
        images_src.append(images_tag["src"])
    
    # return list of images src
    return images_src

# get images names to rename images
def get_image_name(page):
    source = bs(page.content, "lxml")
    container = source.find_all("div", class_ = "ipc-metadata-list-summary-item__c")
    images_names = []
    for item in container:
        name = item.find("h3", class_ = "ipc-title__text").text
        idx = name.index('.')
        name = name[idx + 1:]
        images_names.append(name)

    # return list of images names
    return images_names

# download images and put them in any dir we want
def download_images(images_scr, images_names, dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    for i in range(len(images_scr)):
        img_name = images_names[i].replace(" ", "_").replace("/", "_") + ".jpg"
        img_name = img_name[1:]
        try:
            response = requests.get(images_scr[i])
            response.raise_for_status()
            img = response.content
            with open(os.path.join(dir_path, img_name), 'wb') as img_file:
                img_file.write(img)
                print(f"Downloading.. {img_name}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {images_scr[i]}: {e}")

# create csv file to put the data in it
csv_file = open("movies.csv", 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["name", "year", "rating"])

# function to get name and year and rating of each film
def get_data(page):
    source = bs(page.content, "lxml")
    container = source.find_all("div", class_ = "ipc-metadata-list-summary-item__c")
    for item in container:
        name = item.find("h3", class_ = "ipc-title__text").text
        idx = name.index('.')
        name = name[idx + 1:]
        year = item.find("span", class_ = "cli-title-metadata-item").text
        rating = item.find("span", class_ = "ipc-rating-star").text[:3]
        csv_writer.writerow([name, year, rating])
    csv_file.close()


# main fucntion
def main():
    url = "https://m.imdb.com/chart/top/"
    page = requests.get(url, headers=headers)
    get_data(page)
    imgs_src = get_images_src(page)
    imgs_names = get_image_name(page)
    download_images(imgs_src, imgs_names, "best_movies_imgs")

if __name__ == "__main__":
    main()