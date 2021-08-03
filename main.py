from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from random import randint
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def get_posts(url, scroll_iterations_count, df_name, separator):
    profile = webdriver.ChromeOptions()
    profile.add_argument("--window-size=1920,950")
    profile.add_argument("user-data-dir=selenium")
    # mobile_emulation = {"deviceName": "iPad Pro"}
    # profile.add_experimental_option("mobileEmulation", mobile_emulation)
    driver = webdriver.Chrome(chrome_options=profile)
    driver.get(url)
    
    for scroll_iteration in range(scroll_iterations_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_sleep = randint(422, 633)
        time.sleep(random_sleep / 1000)
        print("Scroll iteration number: " + str(scroll_iteration) + " / " + str(scroll_iterations_count))

    soup = BeautifulSoup(driver.page_source, "html.parser")
    posts = soup.find("div", id="results").find_all("div", class_="_post_content")

    output_df = pd.read_csv(filepath_or_buffer = df_name, sep = separator)

    print("Posts count: " + str(len(posts)))

    for post in posts:
        # strip убирает пробелы по границам строки
        try:
            post_id = post.get("data-post-id")
        except Exception as e:
            post_id = "Без ID"
        # print(post_id)

        try:
            post_author_name = post.find("h5", class_="post_author").find("a").text.strip()
        except Exception as e:
            post_author_name = "Без автора"
        # print(post_author_name)

        try:
            post_author_href = post.find("h5", class_="post_author").find("a").get("href")
            post_author_href = "https://vk.com" + str(post_author_href)
        except Exception as e:
            post_author_href = "Без ссылки"
        # print(post_author_href)

        try:
            post_content = post.find("div", class_="post_content").find("div", class_="wall_post_text").text.replace(";", " ").replace("\n", ". ").strip()
            post_content = post_content.replace("1","0").replace("2","0").replace("3","0").replace("4","0").replace("5","0").replace("6","0").replace("7","0").replace("8","0").replace("9","0")
        except Exception as e:
            post_content = "Без контента"
        # print(post_content)

        try:
            post_commercial_type = post.find("div", class_="post_content").find("div", class_="wall_marked_as_ads").text.strip()
        except Exception as e:
            post_commercial_type = "Без пометки"
        # print(post_commercial_type)

        output_df = output_df.append({
            "id":post_id
            , "post_author_name":post_author_name
            , "post_author_href":post_author_href
            , "post_content":post_content
            , "post_commercial_type":post_commercial_type
            }, ignore_index=True)

    output_df.to_csv(df_name, index=False, sep=";")

    print("Output dataframe lenth is: " + str(len(output_df)))

    random_sleep = randint(666, 999)
    time.sleep(random_sleep / 1000)
    driver.close()


def open_file(file_name):
    file_df = pd.read_csv(file_name + ".csv", dtype="str", sep="~")
    return file_df


if __name__ == "__main__":
    random_sleep = randint(99999)
    time.sleep(random_sleep / 1000)
    queries = open_file("queries")
    
    for qurrent_query in queries["queries"]:
        print("Qurrent querie: " + str(qurrent_query))
        scroll_iterations_count = 5
        df_name = "main.csv"
        
        query = qurrent_query.split()
        url_query = "%20".join(query)
        url = "https://vk.com/search?c%5Bper_page%5D=40&c%5Bq%5D=" + str(url_query) + "&c%5Bsection%5D=statuses"

        get_posts(url, scroll_iterations_count, df_name, ";")

    print("Parsing has been completed successfully!")