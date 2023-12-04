FROM mcr.microsoft.com/mssql/server:2019-CU22-ubuntu-20.04
USER root
# Create a config directory
RUN mkdir -p /usr/config
WORKDIR /usr/config
RUN echo "WORKDIR complete"
# Bundle config source
COPY . /usr/config

# Grant permissions for to our scripts to be executable
RUN chmod +x /usr/config/entrypoint.sh
RUN chmod +x /usr/config/configure-db.sh
RUN chmod +x /usr/config/setup.sql
RUN echo "chmod *.sh complete"

USER mssql
ENTRYPOINT /bin/bash /usr/config/entrypoint.sh