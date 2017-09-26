FROM deepakkumarb/sia-cog_base:cpu

RUN echo 'building CPU sia-cog image'

MAINTAINER Deepak Battini "deepak.battini@siadroid.com"
LABEL description="sia-cog cognitive and machine learning API / CPU version"

RUN apt-get update

WORKDIR /opt
RUN git clone https://github.com/deepakkumar1984/sia-cog.git
WORKDIR /opt/sia-cog/vis
RUN make

WORKDIR /opt/sia-cog/data
VOLUME ["/data"]

WORKDIR /opt/sia-cog/data/__vision
RUN mkdir weights

RUN chown -R sia:sia /opt/sia-cog

USER sia
WORKDIR /opt/sia-cog
CMD python runserver.py
EXPOSE 5555

