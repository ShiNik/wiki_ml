FROM python:3.7

RUN mkdir wikiml

COPY ./dependencies/requirements.txt ./wikiml/tmp/requirements.txt

RUN pip install -r /wikiml/tmp/requirements.txt

CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"