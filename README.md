# NagiFront
The tidy web frontend project for Nagios.

## System Dependency

    sudo apt-get install python-dev
    sudo apt-get install python3-dev # for python3
    sudo apt-get install libmysqlclient-dev

See https://github.com/PyMySQL/mysqlclient-python for mysqlclient

## DB Setting

Make two copy of `db\_settings.cnf.example`.
Rename one to `db\_settings.cnf`, the other to `ndoutils\_db\_settings.cnf`.

    cp db_settings.cnf.example db_settings.cnf
    cp db_settings.cnf.example ndoutils_db_settings.cnf

Revise the contents of both files correctly.


