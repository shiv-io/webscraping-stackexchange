from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import smtplib
from email.mime.text import MIMEText

def scrape_stackExchange():
    url = "https://stackexchange.com/questions?tab=hot"

    webpage = Request(url, headers = {'User-Agent': 'Mozilla/5.0'})

    page = urlopen(webpage) # downloads the url

    page_html = page.read()

    page.close()

    page_soup = soup(page_html, "html.parser")

    list_of_headlines = []

    for counter, link in enumerate(page_soup.find_all('div', 'question question-hot')):
        for item in link.find_all('a', 'question-link'):
            headline = item.text
            list_of_headlines.append(headline)
            headline_url = item.get('href')
            list_of_headlines.append(headline_url)

    headlines_string = ''
    for i in range(len(list_of_headlines)):
        headlines_string += list_of_headlines[i] + ' \n'

    ### SEND EMAIL ###

    gmail_user = input("Enter your email address: ")
    gmail_password = input("Enter your password: ")

    sent_from = gmail_user
    to = gmail_user

    msg = MIMEText(headlines_string)

    msg['Subject'] = "Today's Top StackExchange Questions..."
    msg['From'] = gmail_user
    msg['To'] = gmail_user

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, msg.as_string())
        server.close()
        print('Email sent!')
    except Exception as e:
        print("Error, try again")

scrape_stackExchange()