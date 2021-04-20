import time
import requests
from bs4 import BeautifulSoup
import re
import smtplib, ssl


def read_creds():
    user = passw = reciever = ""
    with open("credentials.txt", "r") as f:
        file = f.readlines()
        user = file[0].strip()
        passw = file[1].strip()
        recieve = file[2].strip()
    return user, passw, recieve


def get_site(html):
    site = requests.get(html)
    soup = BeautifulSoup(site.content, 'html.parser')
    content = str(soup.select("dd")).split(" ")[0]
    return content


def get_free_slots(text: str):
    temp = re.findall(r'\d+', text)
    res = list(map(int, temp))
    return int(res[0])


def send_mail(number):
    sender, password, recieve = read_creds()
    port = 465
    message = f"""\
Subject: Parking!


Number of free slots down to: {number}.
Hurry Hurry!
"""
    context = ssl.create_default_context()
    print(f"warning, number is {number}, sending mail")
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, recieve, message)
    print("Email sent")


def main():
    url = "https://www.parkeringgoteborg.se/uthyrningsomraden/k/karl-johansg-kv-hyppeln-3029/"
    while True:
        content = get_site(url)
        number = get_free_slots(content)
        if number < 10:
            send_mail(number)
        else:
            print(f"number is = {number}")
        time.sleep(3600)


if __name__ == '__main__':
    main()
