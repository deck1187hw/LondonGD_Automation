# Docker file for setting up an image with tools required for web-scraping.

FROM	ubuntu:16.04


# Install dependencies

RUN buildDeps='python-pip build-essential python-dev libjpeg-dev libxml2-dev libxslt-dev zlib1g-dev libffi-dev libssl-dev' \
    && set -x \
    && apt-get update && apt-get install -y $buildDeps --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Scrapy, selenium webdriver, pymongo and pillow modules

RUN pip install -U scrapy selenium pymongo pillow

CMD ["/bin/bash"]

