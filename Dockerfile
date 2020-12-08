FROM python:3.8.6-slim

RUN pip install --pre gql[all] --no-cache

WORKDIR /src

ENTRYPOINT ["/entrypoint.sh"]
