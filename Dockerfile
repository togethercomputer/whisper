FROM 598726163780.dkr.ecr.us-west-2.amazonaws.com/together-node:latest AS together-node
FROM nvcr.io/nvidia/pytorch:22.09-py3 as base

ENV HOST docker
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
# https://serverfault.com/questions/683605/docker-container-time-timezone-will-not-reflect-changes
ENV TZ America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# All users can use /home/user as their home directory
ENV HOME=/home/user
WORKDIR /home/user

# Disable pip cache: https://stackoverflow.com/questions/45594707/what-is-pips-no-cache-dir-good-for
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && \
  pip install transformers \
  git+https://github.com/openai/whisper.git@8cf36f3508c9acd341a45eb2364239a3d81458b9 \
  together_web3 together_worker

COPY --from=together-node /usr/local/bin/together-node /usr/local/bin/
COPY local-cfg.yaml /home/user/cfg.yaml
COPY app app
COPY serve.sh serve.sh

CMD ./serve.sh
