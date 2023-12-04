# Overview

* Build a docker image based on mcr.microsoft.com/mssql/server
* Configure the `setup.sql` with the T-SQL you want to run after SQL Server has started.

# How to Run

## Modify the setup.sql file

modify the `mssql-docker/linux/preview/examples/mssql-customize/setup.sql` file with the TSQL that you want to customize the SQL Server container with.

## Build the image 
Build with `docker build`:
```
docker build -t mssql-custom .
```

## Run the container

Then spin up a new container using `docker run`
```
docker run --name s-sql5 --hostname s-sql5 `
    -p 1433:1433 `
    -v sqlvolume:/var/opt/mssql `
    -e "ACCEPT_EULA=Y" `
    -e "MSSQL_SA_PASSWORD=#ErrorNumber=0" `
    -e "MSSQL_PID=DEVELOPER" `
    -d mssql-custom
```

Note: MSSQL passwords must be at least 8 characters long, contain upper case, lower case and digits.  