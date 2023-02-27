FROM registry.access.redhat.com/ubi9/ubi

USER root

RUN dnf install -y python3 python3-pip git; dnf clean all
RUN python3 -m pip install --upgrade pip


WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

RUN git clone --branch v3.2 --recurse-submodules https://github.com/thingsboard/thingsboard-gateway.git 
    
RUN cd thingsboard-gateway  &&  pip install -r requirements.txt

RUN mkdir thingsboard-gateway/logs && mkdir thingsboard-gateway/certs

COPY ./tb_gateway.yaml ./rest.json /app/thingsboard-gateway/thingsboard_gateway/config/

RUN chown -R 1001:0 /app && \
    chmod -R g=u /app

WORKDIR /app/thingsboard-gateway
VOLUME certs

USER 1001
EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["./thingsboard_gateway/tb_gateway.py"]