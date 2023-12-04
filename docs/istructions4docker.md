## Установка docker MS SQL Server 2019

[Ссылка](https://learn.microsoft.com/ru-ru/sql/linux/quickstart-install-connect-docker?view=sql-server-ver15&preserve-view=true&pivots=cs1-powershell) на руководство.
<br>Ниже приведена проверенная часть для Windows и PowerShell

### Шаг 1
Запустите Docker Desktop.

Извлеките образ контейнера SQL Server 2019 (15.x) на Linux из Реестра контейнеров Майкрософт командой:
```powershell
docker pull mcr.microsoft.com/mssql/server:2019-latest
```
скачается примерно 1.5Gb

### Шаг 2
Чтобы запустить образ контейнера на Linux с помощью Docker, выполните следующую команду в командной строке
PowerShell с повышенными привилегиями:
```powershell
docker run --name s-sql5 --hostname s-sql5 `
    -p 1433:1433 `
    -v sqlvolume:/var/opt/mssql `
    -e "ACCEPT_EULA=Y" `
    -e "MSSQL_SA_PASSWORD=#ErrorNumber=0" `
    -e "MSSQL_PID=DEVELOPER" `
    -d mcr.microsoft.com/mssql/server:2019-latest
```

<b>МЕНЯЕМ</b><br>
Пароль: <span style="color:tomato">#ErrorNumber=0</span><br>
Хост: <span style="color:tomato">s-sql5</span>

### Шаг 3
Подключение к SQL Server
```PowerShell
docker exec -it s-sql5 "bash"
```
после этого, появится новое приглашение <br>
<span style="color:tomato">mssql@s-sql5:/$:</span> <br>
подключитесь с паролем:
```
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "#ErrorNumber=0"
```
Всё готово, можно вводить команды SQL. <br>
Не забываем для проведения операций вводить команду <span style="color:tomato">GO</span> <br>
Пример:
```SQL
1> CREATE DATABASE AODATA;
2> SELECT Name from sys.databases;
3> GO
```

### Резюме
[Ссылка](https://learn.microsoft.com/ru-ru/sql/linux/quickstart-install-connect-docker?view=sql-server-ver15&preserve-view=true&pivots=cs1-powershell) на руководство Microsoft.