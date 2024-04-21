from helper.cdc_template import create_replication_connection
import psycopg2
from decouple import config
import requests
import time
from helper.insert_data_to_html import html_mail


def notification_cdc(data: str):

    conn = psycopg2.connect(host=config("LOCALHOST"), database=config("DB_DATABASE"), user=config("DB_ADMIN_USERNAME"), password=config("DB_ADMIN_PASSWORD"), 
                             port=config("DB_PORT"))
    
    cur = conn.cursor()
    if data:
        for change in data:
            print(f'Handling change {change["kind"]}', flush=True)
            if change["kind"] == "insert":
                to_be_searched = dict(zip(change["columnnames"], change["columnvalues"]))
                print(to_be_searched, flush=True)
                search = f"""
                        SELECT *
                        FROM ads
                        WHERE brand = '{to_be_searched["brand"]}' AND model = '{to_be_searched["model"]}' 
                        AND gas_type = '{to_be_searched["gas_type"]}' 
                        AND kilometers BETWEEN {to_be_searched["from_kilometers"]} AND {to_be_searched["to_kilometers"]}
                        AND price BETWEEN {to_be_searched["from_price"]} AND {to_be_searched["to_price"]};
                    """
                cur.execute(search)
                results = cur.fetchall()

                names = ("id", "ad_link", "image_link", "first_registry", "brand", "model", "gas_type", "kilometers", "price")

                if type(results) == list:
                    try:
                        data = list()
                        for result in results:
                            print(names, flush=True)
                            print(result, flush=True)
                            data.append(dict(zip(names, result)))
                        print(data, flush=True)
                        body = html_mail(data)

                        email = to_be_searched["email"]
                        url = f'http://{config("LOCALHOST")}:8000/send_message'
                        payload = {
                            "receiver": email,
                            "subject": "Current Ads Notification",
                            "body": body
                        }
                        output = requests.post(url, json=payload)
                        print(output.json(), flush=True)

                    except Exception as e:
                        print(f"Error occured while sending email: \n{e}", flush=True)

    cur.close()

time.sleep(10)
create_replication_connection("notification_slot", notification_cdc)


