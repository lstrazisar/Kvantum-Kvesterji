from helper.cdc_template import create_replication_connection
import psycopg2
from decouple import config


def notification_cdc(data: dict):
    to_be_searched = dict(zip(data["columnnames"], data["columnvalues"]))
    search = f"""
        SELECT *
        FROM ads
        WHERE brand = '{to_be_searched["brand"]}' AND model = '{to_be_searched["model"]}' 
        AND gas_type = '{to_be_searched["gas_type"]}' 
        AND kilometers BETWEEN {to_be_searched["from_kilometers"]} AND {to_be_searched["to_kilometers"]};
        AND price BETWEEN {to_be_searched["from_price"]} AND {to_be_searched["to_price"]};
        """
    conn = psycopg2.connect(database=config("DB_DATABASE"), user=config("DB_ADMIN_USERNAME"), password=config("DB_ADMIN_PASSWORD"), 
                        host="0.0.0.0", port=config("DB_PORT"))
    
    cur = conn.cursor()
    cur.execute(search)
    results = cur.fetchall()
    print(results)
    cur.close()


create_replication_connection("notification_slot", lambda data: print(data))

