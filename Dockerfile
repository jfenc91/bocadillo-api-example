FROM python:3.6

ENV PYTHONUNBUFFERED=1
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN mkdir -p /var/log/nginx/
RUN mkdir -p /tmp
RUN apt-get -o Acquire::Check-Valid-Until=false update && apt-get install -y nginx
# Add requirements now (allows caching of pip dependencies for faster builds)
ADD requirements.txt ${ROOT}/requirements.txt

# Install requirements
RUN pip install -r ${ROOT}/requirements.txt

# Add everything else the app may need
# into the container.
ADD . ${ROOT}

CMD ["python", "-m", "serve"]