FROM python

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY populate_db.py .

CMD [ "python", "./populate_db.py" ]

