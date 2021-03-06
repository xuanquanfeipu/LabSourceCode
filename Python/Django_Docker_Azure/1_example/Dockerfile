#
# Dockerfile for Django
#
FROM ubuntu:16.04
MAINTAINER Azure App Service Container Images <appsvc-images@microsoft.com>

#
ENV DOCKER_BUILD_HOME "/dockerbuild"
WORKDIR $DOCKER_BUILD_HOME
RUN set -ex \
	&& apt-get update \
        && apt-get install -y -V --no-install-recommends supervisor \
        && rm -r /var/lib/apt/lists/*

# nginx
ENV NGINX_LOG_DIR "/home/LogFiles/nginx"
RUN set -ex \
	&& apt-get update \
	&& apt-get install -y -V --no-install-recommends nginx \
	&& rm -r /var/lib/apt/lists/*


# postgresql
ENV POSTGRESQL_DATA_DIR "/home/data/postgresql"
ENV POSTGRESQL_LOG_DIR "/home/LogFiles/postgresql"
ENV POSTGRESQL_SOURCE "/usr/local/postgresql"
RUN set -ex \
	&& mkdir -p $POSTGRESQL_SOURCE \
	&& apt-get update \
	&& apt-get install -y -V --no-install-recommends postgresql  \
	&& rm -r /var/lib/apt/lists/*

# phppgadmin
ENV PHPPGADMIN_HOME "/home/phppgadmin"
RUN set -ex \
	&& apt-get update \
	&& apt-get install -y -V --no-install-recommends phppgadmin php7.0-fpm \
	&& rm -r /var/lib/apt/lists/*

# python
RUN set -ex \
	&& apt-get update \
	&& apt-get install -y -V --no-install-recommends python3 python3-pip \
	&& pip3 install --upgrade pip \
	&& pip3 install -U setuptools \
	&& rm -r /var/lib/apt/lists/*

# django
ENV DJANGO_HOME "/home/site/wwwroot"
ENV UWSGI_SOURCE "/usr/local/uwsgi"
RUN set -ex \
	&& mkdir -p $UWSGI_SOURCE \
	&& apt-get update \
	&& apt-get install -y -V --no-install-recommends build-essential python3-dev \
	&& pip3 install uwsgi \
	&& pip3 install django

# install Postgres adapter for Python
RUN set -ex \
        && pip3 install psycopg2

# post-install
RUN set -ex \
	##
	&& rm -rf /var/log/nginx \
	&& ln -s $NGINX_LOG_DIR /var/log/nginx \
	&& test ! -d /home/data/nginx && mkdir -p /home/data/nginx \
	&& ln -s /etc/nginx /home/data/nginx \
	&& ln -s $UWSGI_SOURCE /home/data/uwsgi \
	##
	#&& rm -rf /var/log/postgresql \
	#&& ln -s $POSTGRESQL_LOG_DIR /var/log/postgresql \
	##
	&& ln -s  /usr/share/phppgadmin /var/www \
	&& ln -s  /usr/share/phppgadmin /home \
	##
	&& ln -s /home/site/wwwroot /var/www/default

#nginx scripts: set log path, set phppgadmin(http://domain_IP:port/phppgadmin) 
COPY nginx-sites-default /etc/nginx/sites-available/default
#postgresql scripts: create default user
COPY init.sql $POSTGRESQL_SOURCE
# uWSGI config
COPY uwsgi.ini $UWSGI_SOURCE
COPY uwsgi_params $UWSGI_SOURCE
# supervisor config
COPY supervisor.conf /etc/supervisor/conf.d/

# =====
# final
# =====
COPY entrypoint.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/entrypoint.sh
EXPOSE 80
ENTRYPOINT ["entrypoint.sh"]
