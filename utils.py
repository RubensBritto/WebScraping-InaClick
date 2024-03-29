import uuid
import os
import time
import pandas as pd
import json
from selenium.webdriver.common.by import By

def getQuestions(driver, jdata):

    name = str(uuid.uuid4())

    jdata["files"].append(name)

    with open("config.json", "w") as outfile:
        outfile.write(json.dumps(jdata))

    data = []

    driver.get("https://www.qconcursos.com/questoes-de-concursos/questoes?discipline_ids%5B%5D=4&subject_ids%5B%5D=15446")

    for i in range(jdata["lastPage"], jdata["lastPage"] + 20):

        if(jdata["lastPage"] == 300):
            os.system("shutdown")

        time.sleep(2)

        t = driver.find_elements(By.CLASS_NAME, "q-id")

        for x in t:
            data.append(x.get_attribute('innerHTML'))

        driver.get(f"https://www.qconcursos.com/questoes-de-concursos/questoes?discipline_ids%5B%5D=4&page={i+1}&subject_ids%5B%5D=15446")

        time.sleep(2)

        nd = pd.DataFrame(data, columns=['link'])

        nd.to_csv(str(name)+".csv")

        print(i)

        jdata["lastPage"] = i

        with open("config.json", "w") as outfile:
            outfile.write(json.dumps(jdata))

def getInfo(driver, href):
    driver.get("https://www.qconcursos.com"+str(href))

    try:
        descricao = driver.find_element(By.CLASS_NAME, "q-question-enunciation").get_attribute('innerHTML')

        a = driver.find_element(By.XPATH, "/html/body/div[2]/main/article/div[1]/div/div/div/div[1]/div[4]/div[3]/fieldset/div[1]/label/div").get_attribute('innerHTML')

        b = driver.find_element(By.XPATH, "/html/body/div[2]/main/article/div[1]/div/div/div/div[1]/div[4]/div[3]/fieldset/div[2]/label/div").get_attribute('innerHTML')

        c = driver.find_element(By.XPATH, "/html/body/div[2]/main/article/div[1]/div/div/div/div[1]/div[4]/div[3]/fieldset/div[3]/label/div").get_attribute('innerHTML')

        d = driver.find_element(By.XPATH, "/html/body/div[2]/main/article/div[1]/div/div/div/div[1]/div[4]/div[3]/fieldset/div[4]/label/div").get_attribute('innerHTML')

        e = driver.find_element(By.XPATH, "/html/body/div[2]/main/article/div[1]/div/div/div/div[1]/div[4]/div[3]/fieldset/div[5]/label/div").get_attribute('innerHTML')

        return {"descricao": descricao, "a": a, "b": b, "c": c, "d": d, "e": e}

    except:

        descricao = driver.find_element(By.CLASS_NAME, "q-question-enunciation").get_attribute('innerHTML')

        a = driver.find_element(By.XPATH, "/html/body/div[2]/main/article/div[1]/div/div/div/div[1]/div[4]/div[4]/fieldset/div[1]/label/div").get_attribute('innerHTML')

        b = driver.find_element(By.XPATH, "/html/body/div[2]/main/article/div[1]/div/div/div/div[1]/div[4]/div[4]/fieldset/div[2]/label/div").get_attribute('innerHTML')

        return {"descricao": descricao, "a": a, "b": b, "c": "none", "d": "none", "e": "none"}
