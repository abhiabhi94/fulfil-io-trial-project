FROM ubuntu:focal

ENV PYTHONUNBUFFERED 1 PYTHONDONTWRITEBYTECODE 1

RUN : \
  && apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    --no-install-recommends \
    build-essential \
    python3.9-venv \
    netcat \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  &&:

WORKDIR /usr/src/app

COPY requirements ./requirements

ENV PATH=/venv/bin:$PATH
RUN : \
  && python3.9 -m venv /venv \
  && python -m pip install -U pip \
  && pip install --no-cache-dir -r requirements/prod.txt \
  &&:

COPY . .

RUN mv wait-for.sh /bin/wait-for && chmod a+x /bin/wait-for

ENTRYPOINT ["bash", "docker-entrypoint.sh"]
