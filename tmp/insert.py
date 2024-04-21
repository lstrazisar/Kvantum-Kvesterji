import psycopg2
from decouple import config

notifications_sql = """
INSERT INTO notifications (email, brand, model, gas_type, from_kilometers, to_kilometers, from_price, to_price, frequency)
VALUES 
    (%(email)s, %(brand)s, %(model)s, %(gas_type)s, %(from_kilometers)s, %(to_kilometers)s, %(from_price)s, %(to_price)s, %(frequency)s) 
"""

notifications_list = [
    {
        "email": "papez.luka@gmail.com",
        "brand": "Toyota",
        "model": "Corolla",
        "gas_type": "Petrol",
        "from_kilometers": 10000,
        "to_kilometers": 20000,
        "from_price": 10000,
        "to_price": 20000,
        "frequency": "Weekly"
    },
    {
        "email": "test@example.com",
        "brand": "Toyota",
        "model": "Corolla",
        "gas_type": "Petrol",
        "from_kilometers": 10000,
        "to_kilometers": 20000,
        "from_price": 10000,
        "to_price": 20000,
        "frequency": "Weekly"
    },
    {
        "email": "test2@example.com",
        "brand": "Honda",
        "model": "Civic",
        "gas_type": "Petrol",
        "from_kilometers": 15000,
        "to_kilometers": 25000,
        "from_price": 15000,
        "to_price": 25000,
        "frequency": "Monthly"
    },
    {
        "email": "test3@example.com",
        "brand": "Ford",
        "model": "Mustang",
        "gas_type": "Petrol",
        "from_kilometers": 20000,
        "to_kilometers": 30000,
        "from_price": 20000,
        "to_price": 30000,
        "frequency": "Daily"
    }
]

ads_sql = """
INSERT INTO ads (ad_link, image_link, first_registry, brand, model, gas_type, kilometers, price)
VALUES 
    (%(ad_link)s, %(image_link)s, %(first_registry)s, %(brand)s, %(model)s, %(gas_type)s, %(kilometers)s, %(price)s) ON CONFLICT DO NOTHING
"""

ads_list = [
    {
        "ad_link": "http://example.com/ad1",
        "image_link": "http://example.com/image1",
        "first_registry": 2000,
        "brand": "Toyota",
        "model": "Corolla",
        "gas_type": "Petrol",
        "kilometers": 10000,
        "price": 20000
    },
    {
        "ad_link": "http://example.com/ad2",
        "image_link": "http://example.com/image2",
        "first_registry": 2005,
        "brand": "Honda",
        "model": "Civic",
        "gas_type": "Diesel",
        "kilometers": 15000,
        "price": 25000
    }
    # Add more dictionaries as needed
]

conn = psycopg2.connect(database=config("DB_DATABASE"), user=config("DB_ADMIN_USERNAME"), password=config("DB_ADMIN_PASSWORD"), 
                        host="0.0.0.0", port=config("DB_PORT"))
cur = conn.cursor()

cur.executemany(notifications_sql,notifications_list)
conn.commit()

cur.executemany(ads_sql, ads_list)
conn.commit()


cur.close()
conn.close()

