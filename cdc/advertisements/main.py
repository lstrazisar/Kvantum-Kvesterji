from helper.cdc_template import create_replication_connection
import psycopg2
from decouple import config
import requests
import time


def ads_cdc(data: str):
    print(config("LOCALHOST"), config("DB_DATABASE"), config("DB_ADMIN_USERNAME"), config("DB_ADMIN_PASSWORD"), config("DB_PORT"), flush=True)
    conn = psycopg2.connect(host=config("LOCALHOST"), database=config("DB_DATABASE"), user=config("DB_ADMIN_USERNAME"), password=config("DB_ADMIN_PASSWORD"), 
                            port=config("DB_PORT"))
    
    cur = conn.cursor()
    if data:
        print("data: \n", data)
        for change in data:
            if change["kind"] == "insert":
                to_be_searched = dict(zip(change["columnnames"], change["columnvalues"]))
                print(to_be_searched)
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

                body = f"""Ad Link: {to_be_searched["ad_link"]}\nImage Link: 
                {to_be_searched["image_link"]}\nFirst Registry: {to_be_searched["first_registry"]}\nBrand: 
                {to_be_searched["brand"]}\nModel: {to_be_searched["model"]}\nGas Type: {to_be_searched["gas_type"]}\n
                Kilometers: {to_be_searched["kilometers"]}\n Price: {to_be_searched["price"]}\n\n"""

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
                            print("output: \n")
                            print(output.status_code)
                            print(output.json())
                        except Exception as e:
                            print(f"Error occured while sending email: \n{e}", flush=True)

    cur.close()

time.sleep(10)
create_replication_connection("ads_slot", ads_cdc)


