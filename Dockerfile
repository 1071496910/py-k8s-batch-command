FROM reg.local:5000/common/centos7-s6-base:1.0
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python get-pip.py \
    && pip install kubernetes
ADD batch-command.py /batch-command.py
ENTRYPOINT ["/batch-command.py"]
CMD []
