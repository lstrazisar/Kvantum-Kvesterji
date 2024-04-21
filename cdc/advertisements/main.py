from helper.cdc_template import create_replication_connection
import psycopg2
from decouple import config
import requests
import time
from helper.insert_data_to_html import html_mail


def ads_cdc(data: str):
    conn = psycopg2.connect(host=config("LOCALHOST"), database=config("DB_DATABASE"), user=config("DB_ADMIN_USERNAME"), password=config("DB_ADMIN_PASSWORD"), 
                            port=config("DB_PORT"))
    
    cur = conn.cursor()
    if data:
        for change in data:
            print(f'Handling change {change["kind"]}', flush=True)
            if change["kind"] == "insert":
                to_be_searched = dict(zip(change["columnnames"], change["columnvalues"]))
                search = f"""
                        SELECT *
                        FROM notifications
                        WHERE brand = '{to_be_searched["brand"]}' AND model = '{to_be_searched["model"]}' 
                        AND gas_type = '{to_be_searched["gas_type"]}' 
                        AND {to_be_searched["kilometers"]} BETWEEN from_kilometers AND to_kilometers
                        AND {to_be_searched["price"]} BETWEEN from_price AND to_price;
                    """
                cur.execute(search)
                results = cur.fetchall()

                body = html_mail([to_be_searched])

                if results:      
                    for result in results:
                        try:
                            email = result[1]
                            url = f'http://{config("LOCALHOST")}:8000/send_message'
                            payload = {
                                "receiver": email,
                                "subject": "Current Ads Notification",
                                "body": body
                            }
                            output = requests.post(url, json=payload)
                        except Exception as e:
                            print(f"Error occured while sending email: \n{e}", flush=True)

    cur.close()

time.sleep(10)
create_replication_connection("ads_slot", ads_cdc)


