FROM continuumio/anaconda3:2019.10

COPY installation/environment.yml /usr/src/installation/environment.yml

RUN conda env create -f /usr/src/installation/environment.yml && \
    conda clean --all -f -y && \
    rm /usr/src/installation/environment.yml

ENTRYPOINT ["tail", "-f", "/dev/null"]
# Make RUN commands use the new environment:
#