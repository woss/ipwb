FROM python:2-onbuild

LABEL maintainer="Sawood Alam <@ibnesayeed>"

RUN pip install .
EXPOSE 5000

CMD ["ipwb"]
