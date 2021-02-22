# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG BASE_CONTAINER=jupyter/scipy-notebook
FROM $BASE_CONTAINER
# Maintainer of the base container: LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER $NB_UID
COPY requirements.txt /tmp/
RUN pip install --default-timeout=15000 --requirement /tmp/requirements.txt && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

COPY cheat_detector cheat_detector
COPY cheat_detector.ipynb .

# cache model in the docker image
RUN python -c "from cheat_detector.model import TextSimilarityModel; m = TextSimilarityModel()"

