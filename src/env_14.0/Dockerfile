# <OOW> : Copy of https://github.com/odoo/odoo/blob/14.0/setup/package.dfsrc
FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y locales && \
    rm -rf /var/lib/apt/lists/*

# Reconfigure locales such that postgresql uses UTF-8 encoding
RUN dpkg-reconfigure locales && \
    locale-gen C.UTF-8 && \
    /usr/sbin/update-locale LANG=C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update -qq &&  \
    apt-get upgrade -qq -y && \
    apt-get install \
        unzip \
        curl \
        postgresql \
        postgresql-server-dev-all \
        postgresql-client \
        adduser \
        libldap2-dev \
        libsasl2-dev \
        python3-pip \
        python3-wheel \
        build-essential \
        python3 -y && \
    rm -rf /var/lib/apt/lists/*

# <OOW> Install Debian packages
COPY extra_debian_requirements.txt /extra_debian_requirements.txt
RUN apt-get update -qq \
    && apt-get install -y git \
    && xargs apt-get install -y --no-install-recommends <extra_debian_requirements.txt \
    && rm -rf /var/lib/apt/lists/*

#ENV ODOO_VERSION 14.0
#ARG ODOO_RELEASE=20220826
#ARG ODOO_SHA=fe6467ecb51a5b5bf831a2c1021e77b2a890a01d

#RUN curl -o odoo.deb -sSL http://nightly.odoo.com/${ODOO_VERSION}/nightly/deb/odoo_${ODOO_VERSION}.${ODOO_RELEASE}_all.deb \
#    && echo "${ODOO_SHA} odoo.deb" | sha1sum -c - \
#    && apt-get update \
#    && apt-get -y install --no-install-recommends ./odoo.deb \
#    && rm -rf /var/lib/apt/lists/* odoo.deb
ADD ./src/odoo-core-installer.zip /odoo-core-installer.zip
RUN unzip /odoo-core-installer.zip
RUN mv /odoo /odoo-core-installer
RUN python3 /odoo-core-installer/setup.py install

# <OOW> Install Python librairies
COPY ./src/odoo/requirements.txt /odoo_python_requirements.txt
COPY extra_python_requirements.txt /extra_python_requirements.txt
RUN pip3 install --upgrade pip \
    && python3 -m pip install --no-cache-dir setuptools-scm \
    && python3 -m pip install --no-cache-dir -r /odoo_python_requirements.txt \
    && python3 -m pip install --no-cache-dir -r /extra_python_requirements.txt

# <OOW> Get local user id and set it to the odoo user
ARG LOCAL_USER_ID

RUN useradd --uid $LOCAL_USER_ID --non-unique odoo

USER odoo
