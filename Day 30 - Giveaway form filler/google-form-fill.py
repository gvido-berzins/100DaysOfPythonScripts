import sys
import threading
import time

from selenium import webdriver

url = sys.argv[1]
thread_list = list()

with open("/home/cny/.scripts/python/wallets", "r") as f:
    data = f.readlines()

N = len(data)  # Number of browsers to spawn


def test_logic(c):
    driver = webdriver.Chrome("./chromedriver")
    driver.get(url)

    # Test logic START
    textboxes = driver.find_elements_by_class_name(
        "quantumWizTextinputPaperinputInput")
    submit = driver.find_element_by_class_name(
        "appsMaterialWizButtonPaperbuttonLabel")
    time.sleep(1)
    for value in textboxes:
        value.send_keys(data[c])
    submit.click()
    time.sleep(1)
    # Logic END

    driver.quit()


# Start test
for i in range(N):
    t = threading.Thread(name=f"Wallet {data[i].strip()}",
                         target=test_logic,
                         args=(i, ))
    t.start()
    print(t.name + " started!")
    time.sleep(2)
    thread_list.append(t)
