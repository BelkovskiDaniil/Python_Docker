FROM gherman/python-selenium-firefox

COPY . .

RUN pip install selenium 
RUN pip install telebot
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]