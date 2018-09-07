FROM reg.local:5000/common/centos7-s6-base:1.0
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python get-pip.py \
    && pip install kubernetes
ADD list_pod.py /list_pod.py
ENTRYPOINT ["/list_pod.py"]
CMD []
