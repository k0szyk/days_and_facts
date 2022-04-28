FROM python:3.6

WORKDIR /var/www

ADD ./requirements.txt /var/www/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
ADD . /var/www/
RUN pip install gunicorn

EXPOSE 5002

CMD [ "gunicorn", "-w", "2", "--bind", "0.0.0.0:5002", "wsgi"]

