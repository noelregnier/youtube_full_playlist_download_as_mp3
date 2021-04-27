import time
import timeit
import glob
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


start_url = "https://www.youtube.com/watch?v=hgJdxtkChCo&list=PLtzZV0KlZ_lfisdOPulLWqi1b3HhhRLW5"
driver = webdriver.Chrome(executable_path='/home/noel/apps/Selenium_drivers/chromedriver')
urls_and_titles = {}


def get_urls(playlist_url):
    driver.get(playlist_url)

    #wait for panel videos to appear
    wait = WebDriverWait(driver, 7)
    wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//a[contains(@class,'ytd-playlist-panel-video-renderer')]")))
    playlist_title = driver.find_element_by_xpath("//div[@id='header-description']/h3").text
    print(playlist_title)
    panel_links = driver.find_elements_by_xpath(
        "//a[contains(@class,'ytd-playlist-panel-video-renderer')]")
    print("the number of links is ", len(panel_links))

    for i,element in enumerate(panel_links):
        url = element.get_attribute("href")
        name = element.find_element_by_xpath("div/div/h4/span").get_attribute("title")
        if name == "":
            name = "no_title_name"+str(i)
        urls_and_titles[url] = name

    for i, k in urls_and_titles.items():
        print(i, k)
    return playlist_title

def convertor(video_url, title: str):
    # title = title.replace(" ", "_")
    # title = title.replace(",", "_")
    driver.get("https://s8.converto.io")
    driver.find_element_by_css_selector("#youtube-url").send_keys(video_url)
    #wait for the convert button to become visible

    wait = WebDriverWait(driver, 10)
    wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".convert-btn")))
    driver.find_element_by_css_selector(".convert-btn").click()


    # time.sleep(3)
    #maybe wait until it is clicked

    #it redirects us to an ad page and we return back
    wait = WebDriverWait(driver, 5)
    wait.until(expected_conditions.new_window_is_opened)
    driver.switch_to.window(driver.window_handles[0])

    #getting the download link
    try:
        wait = WebDriverWait(driver, 300)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "a[id='download-url']")))
    except:
        driver.refresh()
        wait = WebDriverWait(driver, 3)
        wait.until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "a[id='download-url']")))

    driver.find_element_by_css_selector("a[id='download-url']").click()


    #checking that file is downloaded
    mp3_files = glob.glob('/home/noel/Downloads/*.mp3', recursive=True)
    mp3_files_start = len(mp3_files)

    starttime = timeit.default_timer()
    while True:
        mp3_files_check = glob.glob('/home/noel/Downloads/*.mp3', recursive=True)
        mp3_files_now = len(mp3_files_check)
        if mp3_files_now > mp3_files_start:
            break
        if int(timeit.default_timer() - starttime) > 600:
            print("!!!!! Extracting the file takes more than 10 min. Stop extracting")
            print("Not extracted", video_url, title)
            break
        time.sleep(2)


#running the script and writing down the urls which are not extracted
file_name = get_urls(start_url)

with open(file_name, "x") as fhand:
    for url, file_title in urls_and_titles.items():
        try:
            convertor(url, file_title)
            print("Successfully extracted", url, file_title)
        except:
            print("Extraction FAILED", url, file_title)
            fhand.write(file_title+"\n")
            fhand.write(url+"\n")
        #get rid of all tabs except the one
        driver.get("https://s8.converto.io")
        windows = driver.window_handles
        for child_window in windows[1:]:
            driver.switch_to.window(child_window)
            driver.close()
        driver.switch_to.window(driver.window_handles[0])
        # driver.get("https://s8.converto.io")
        # driver.refresh()
        # driver.switch_to.window(driver.window_handles[0])



# driver.close()
