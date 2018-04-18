FROM ubuntu:latest 

# install masscan
RUN apt update && apt install -y git gcc make libpcap-dev clang python python-pip cron\
    && mkdir -p /root/masscan && git clone https://github.com/robertdavidgraham/masscan /root/masscan/ \
    && cd /root/masscan && make && ln -s /root/masscan/bin/masscan /usr/bin/masscan

COPY ./requirements.txt /tmp/

# install requirements
RUN pip install -U pip && pip install -r /tmp/requirements.txt

RUN mkdir -p /logs
VOLUME /logs

WORKDIR /opt/AssetsDiscovery

# Run the command on container startup
CMD python /opt/AssetsDiscovery/cron.py && tail -f /opt/AssetsDiscovery/assets.log
