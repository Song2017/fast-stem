import os
from concurrent.futures import as_completed, ProcessPoolExecutor

import arrow
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker  # , Session

from src.pkg import json_dumps_unicode, encrypt, decrypt

# pg_sql_str = "postgresql://postgres:postgres@192.168.1.1:5432/db_one"
pg_sql_str = os.getenv("PG_LOGISTICS_CONN")
CRYPT_KEY = os.getenv('CRYPT_KEY')
CRYPT_IV = os.getenv('CRYPT_IV')
assert pg_sql_str is not None, "PG_LOGISTICS_DEV is not found"


def main():
    engine = create_engine(pg_sql_str)
    session = scoped_session(sessionmaker(bind=engine))
    session.execute(
        " INSERT INTO tests(name, school, score) VALUES ('name2', 'cb', 22);")
    session.commit()
    flights = session.execute(
        "SELECT date, name, can_drive, school, score FROM tests").fetchall()
    for flight in flights:
        print(flight)


def crypt_order(where_txt: str = ""):
    """
    update pilot_logistics set ship_to = ship_to::jsonb || '{"address2": "address2"}'::jsonb
    where carrier = 'samarkand.sfexpress.tests' and seller_order_ref = 'Iceland1688369392'
    and ship_to->>'tin' like '1%'
    """
    o_engine = create_engine(pg_sql_str)
    session = scoped_session(sessionmaker(bind=o_engine))
    batch_size = 1000  # 13s
    where_txt = where_txt or ""  # " where pilot_logistics_id = 40431"
    sql_count = "SELECT count(1) FROM pilot_logistics " + where_txt
    waybills_count = session.execute(sql_count).fetchall()
    for i in range(waybills_count[0][0] // batch_size + 1):
        sql_select = "SELECT modify_time, pilot_logistics_id, order_ref, seller_order_ref, " \
                     "tracking_reference, ship_to, bill FROM pilot_logistics "
        sql_select += where_txt
        sql_select += "order by pilot_logistics_id "
        sql_select += f"offset {i * batch_size} "
        sql_select += f"limit {batch_size} "
        waybills = session.execute(sql_select).fetchall()
        print("pid", os.getpid(), ", waybills processed", i * batch_size,
              "processing", len(waybills), arrow.now())
        # print([waybill.pilot_logistics_id for waybill in waybills])
        for waybill in waybills:
            # print(waybill.pilot_logistics_id, waybill.tracking_reference)
            if not isinstance(waybill.ship_to, dict) or not isinstance(waybill.bill, dict):
                print("crypto data error,", waybill.pilot_logistics_id,
                      type(waybill.ship_to), type(waybill.bill))
                continue
            sql_update = get_sql_update_encrypt(
                waybill.ship_to, waybill.bill, waybill.pilot_logistics_id)
            # print(sql_update)
            if sql_update:
                session.execute(sql_update)
        session.commit()
    return str(os.getpid()), arrow.now()


def multi_crypt_order():
    print("multi processing", arrow.now())
    where_sqls = []
    for i in range(20):
        where_sqls.append(
            f" where pilot_logistics_id >= {i * 10000} "
            f" and pilot_logistics_id < {(i + 1) * 10000} ")
    executor = ProcessPoolExecutor(max_workers=min(os.cpu_count(), 5))
    create_tasks = [executor.submit(
        crypt_order, where_sql) for where_sql in where_sqls]
    for future in as_completed(create_tasks):
        print(future.result())
    print("multi processing ending", arrow.now())


def get_sql_update_encrypt(ship_to_ori: dict, bill_ori: dict, pilot_logistics_id) -> str:
    keys = ("address1", "tin", "id_card", "first_name", "phone")
    ship_to = ship_to_ori or dict()
    ship_to_f = {key: ship_to.get(key) for key in keys if ship_to.get(key)}
    ship_to_str = json_dumps_unicode(encrypt(ship_to_f, CRYPT_KEY, CRYPT_IV))
    bill = bill_ori or dict()
    bill_f = {key: bill.get(key) for key in keys if bill.get(key)}
    bill_str = json_dumps_unicode(encrypt(bill_f, CRYPT_KEY, CRYPT_IV))
    if not ship_to_str and not bill_str:
        return ""

    _update = f"update pilot_logistics set "
    if ship_to_str and bill_str:
        _update += f"ship_to = ship_to::jsonb || '{ship_to_str}'::jsonb, " \
                   f"bill = bill::jsonb || '{bill_str}'::jsonb "
    elif ship_to_str:
        _update += f"ship_to = ship_to::jsonb || '{ship_to_str}'::jsonb "
    elif bill_str:
        _update += f"bill = bill::jsonb || '{bill_str}'::jsonb "
    _update += f"where pilot_logistics_id={pilot_logistics_id} "
    return _update


def get_sql_update_decrypt(ship_to_ori: dict, bill_ori: dict, pilot_logistics_id) -> str:
    keys = ("address1", "tin", "id_card", "first_name", "phone")
    ship_to = ship_to_ori or dict()
    ship_to_f = {key: ship_to.get(key) for key in keys if ship_to.get(key)}
    ship_to_str = json_dumps_unicode(decrypt(ship_to_f, CRYPT_KEY, CRYPT_IV))
    bill = bill_ori or dict()
    bill_f = {key: bill.get(key) for key in keys if bill.get(key)}
    bill_str = json_dumps_unicode(decrypt(bill_f, CRYPT_KEY, CRYPT_IV))
    if not ship_to_str and not bill_str:
        return ""

    _update = f"update pilot_logistics set "
    if ship_to_str and bill_str:
        _update += f"ship_to = ship_to::jsonb || '{ship_to_str}'::jsonb, " \
                   f"bill = bill::jsonb || '{bill_str}'::jsonb "
    elif ship_to_str:
        _update += f"ship_to = ship_to::jsonb || '{ship_to_str}'::jsonb "
    elif bill_str:
        _update += f"bill = bill::jsonb || '{bill_str}'::jsonb "
    _update += f"where pilot_logistics_id={pilot_logistics_id} "
    return _update


def run_codegen():
    """
    pip install sqlacodegen
    """
    args = 'sqlacodegen --outfile ' \
           f'./test_model.py {pg_sql_str} --tables pilot_logistics '
    os.system(args)


if __name__ == "__main__":
    print("PG utils")
    # crypt_order()
    # multi_crypt_order()
    print("PG utils end")
