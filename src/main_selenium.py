import img2pdf
import os
import queue
import random
import time
import yaml
from selenium import webdriver
from utils import get_url_to_dir_name, remove_alpha


config = None
with open("config.yml", 'r') as stream:
    config = yaml.safe_load(stream)

website = config["website"]
course_homepage = config["course_homepage"]
next_topic_url_pattern = config["next_topic_url_pattern"]

visited_urls = set()
urls_to_visit = queue.Queue()

course_dir = os.path.join("data", get_url_to_dir_name(course_homepage))
os.makedirs(course_dir, exist_ok=True)
urls_to_visit.put(course_homepage)

options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome('driver/chromedriver', options=options)
driver.set_window_size(1920, 1080)

driver.get(website)
time.sleep(5)

# click login
buttons = driver.find_elements_by_tag_name('button')
for b in buttons:
    if b.get_property('innerText') == "Log in":
        b.click()
        print("Clicked login button")

time.sleep(1)

# login
email_ele = driver.execute_script("return document.body.querySelector('input[name=\"email\"]');")
if email_ele is None:
    print("email_ele not found")
    exit

email_ele.send_keys(config["username"])

password_ele = driver.execute_script("return document.body.querySelector('input[name=\"password\"]');")
if password_ele is None:
    print("password_ele not found")
    exit

password_ele.send_keys(config["password"])

login_ele = driver.execute_script("return document.body.querySelector('button#modal-login');")
login_ele.click()
print("Submitted creds")
time.sleep(5)

while not urls_to_visit.empty():
    print ("URLs to visit %s" % urls_to_visit.qsize())

    url = urls_to_visit.get()
    print("Fetching ... %s" % url)
    driver.get(url)
    time.sleep(5)

    links_in_page = driver.execute_script("return document.body.querySelectorAll('a[href^=\"%s\"]');" % next_topic_url_pattern)
    for link in links_in_page:
        link_href = link.get_attribute("href")
        if (link_href not in visited_urls and
            link_href.startswith(course_homepage) and
            len(link_href) > len(course_homepage) + 1):
            urls_to_visit.put(link_href)
            visited_urls.add(link_href)

    base_filepath = os.path.join(course_dir, get_url_to_dir_name(url))
    image_filepath = base_filepath + ".png"
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(S('Width'),S('Height'))
    driver.find_element_by_tag_name('body').screenshot(image_filepath)
    print("Saved %s" % image_filepath)

    # image_filepath_without_alpha = base_filepath + "_without_alpha.png"
    # remove_alpha(image_filepath, image_filepath_without_alpha)
    # pdf_filepath = base_filepath + ".pdf"
    # a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
    # layout_fun = img2pdf.get_layout_fun(a4inpt)
    # with open(pdf_filepath,"wb") as f:
    #     f.write(img2pdf.convert(image_filepath_without_alpha, layout_fun=layout_fun))

    time.sleep(random.randint(1, 5))

driver.quit()