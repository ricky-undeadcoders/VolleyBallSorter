FROM rascaltat/alpine
MAINTAINER Ricky Whitaker

# set up app directory and pull in application files
RUN mkdir /application
COPY /application /application
RUN chown -R nginx:nginx /application
WORKDIR /application

# setup environment
COPY setup.py /setup.py
COPY requirements.txt /requirements.txt
COPY render_db.py /render_db.py
COPY nginx.conf /etc/nginx/nginx.conf
COPY app.ini /app.ini
RUN chmod 777 /app.ini
RUN apk update
RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev
#ENV LIBRARY_PATH=/lib:/usr/lib

RUN pip2 install -e /

# exectute start up script
ENTRYPOINT ["/entrypoint.sh"]
