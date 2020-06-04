import os
import pdfkit
import queue
import time
from selenium import webdriver
from utils import get_url_to_dir_name


course_homepage = "https://www.educative.io/courses/cpp-fundamentals-for-professionals"
command_format = "google-chrome --headless --disable-gpu --print-to-pdf=\"%s\" --virtual-time-budget=10000 %s"

visited_urls = set()
urls_to_visit = queue.Queue()

course_dir = os.path.join("data", get_url_to_dir_name(course_homepage))
os.makedirs(course_dir, exist_ok=True)
urls_to_visit.put(course_homepage)

while not urls_to_visit.empty():
    url = urls_to_visit.get()
    if url not in visited_urls:
        visited_urls.add(url)
        filepath = os.path.join(course_dir, get_url_to_dir_name(url) + ".pdf")

        command = command_format % (filepath, url)
        print(command)
        os.system(command)
