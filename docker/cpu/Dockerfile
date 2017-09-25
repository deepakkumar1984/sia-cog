FROM deepakkumarb/sia-cog_base:cpu

RUN echo 'building CPU sia-cog image'

MAINTAINER Deepak Battini "deepak.battini@siadroid.com"
LABEL description="sia-cog cognitive and machine learning API / CPU version"

RUN apt-get update

WORKDIR /opt

RUN git clone https://github.com/deepakkumar1984/sia-cog.git
RUN wget https://github.com/deepakkumar1984/sia-cog-setup/files/1327381/SiaCog-Client_v1.0-beta.1.zip
RUN unzip -d siacogclientv1 SiaCog-Client_v1.0-beta.1.zip
WORKDIR /opt/sia-cog/vis
RUN make

WORKDIR /opt/sia-cog/data
VOLUME ["/data"]

WORKDIR /opt/sia-cog/data/__vision
RUN mkdir weights

RUN chown -R sia:sia /opt/sia-cog

WORKDIR /opt/siacogclientv1
RUN dotnet restore
RUN rm -r SiaCog-Client_v1.0*
RUN chown -R sia:sia /opt/siacogclientv1

USER sia
WORKDIR /opt/sia-cog
CMD python runserver.py
EXPOSE 5555

WORKDIR /opt/siacogclientv1
CMD dotnet SiaCog.Client.dll
EXPOSE 5000

