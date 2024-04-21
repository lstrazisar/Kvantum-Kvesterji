from helper.cdc_template import create_replication_connection
import psycopg2
from decouple import config
import requests
import time


def notification_cdc(data: str):

    conn = psycopg2.connect(host=config("LOCALHOST"), database=config("DB_DATABASE"), user=config("DB_ADMIN_USERNAME"), password=config("DB_ADMIN_PASSWORD"), 
                             port=config("DB_PORT"))
    
    cur = conn.cursor()
    if data:
        for change in data:
            if change["kind"] == "insert":
                to_be_searched = dict(zip(change["columnnames"], change["columnvalues"]))
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
                print("results: \n")
                print(results)
                if results:
                    try:
                        body = ""
                        for result in results:
                            body += f"Ad Link: {result[0]}\nImage Link: {result[1]}\nFirst Registry: {result[2]}\nBrand: {result[3]}\nModel: {result[4]}\nGas Type: {result[5]}\nKilometers: {result[6]}\nPrice: {result[7]}\n\n"
                        email = to_be_searched["email"]
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
create_replication_connection("notification_slot", notification_cdc)


