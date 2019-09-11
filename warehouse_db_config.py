# -*- coding: utf-8 -*-
import os


def getWarehouseDbConfigDict():
    db_name = os.getenv('METER_WAREHOUSE_DB_NAME', 'db_name')
    db_username = os.getenv('METER_WAREHOUSE_DB_USERNAME', 'username')
    db_password = os.getenv('METER_WAREHOUSE_DB_PASSWORD', 'password')
    db_host = os.getenv('METER_WAREHOUSE_DB_HOST', 'hostip')
    db_port = os.getenv('METER_WAREHOUSE_DB_PORT', 'db_port')

    db_conn_dict = dict(
        db_name=db_name,
        db_username=db_username,
        db_password=db_password,
        db_host=db_host,
        db_port=db_port
    )
    return db_conn_dict