
ARG BASE_CONTAINER=ucsdets/datahub-base-notebook:2022.3-stable

FROM $BASE_CONTAINER

LABEL maintainer="UC San Diego ITS/ETS <ets-consult@ucsd.edu>"

USER root

RUN apt update

RUN apt-get -y install aria2 nmap traceroute

USER jovyan

RUN pip install aif360['all']
RUN pip install pandas numpy matplotlib scipy
RUN pip install multi-label-pigeon
RUN pip install config openai Pillow
RUN pip install urllib3

CMD ["/bin/bash"]