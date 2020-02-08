FROM continuumio/anaconda3:2019.10

RUN conda env create -f environment.yml && \
    conda activate wiki_ml

RUN /opt/conda/bin/conda install jupyter -y --quiet && \ 
    mkdir /opt/notebooks && \
    /opt/conda/bin/jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --port=8888 --no-browser

