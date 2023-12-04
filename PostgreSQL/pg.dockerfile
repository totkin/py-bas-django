FROM postgres:15-alpine
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB postgres
COPY data_geraration_script.sql /docker-entrypoint-initdb.d/
CMD ["postgres"]