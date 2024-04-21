from flask import Flask, render_template, request, redirect
import csv
import psycopg2
from decouple import config
import time

app = Flask(__name__)


def get_brands_and_models():
    brands=[]
    models=[]
    with open('static/Tables/znamke_modeli.csv', mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            brands.append(row[0])
            models.append(row[1])
    models = models[:]
    brands=list(set(brands))
    return brands, models


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about', methods=['POST'])
def about():
    notifications_sql = """
                INSERT INTO notifications (email, brand, model, gas_type, from_kilometers, to_kilometers, from_price, to_price, frequency)
                VALUES 
                    (%(email)s, %(brand)s, %(model)s, %(gas_type)s, %(from_kilometers)s, %(to_kilometers)s, %(from_price)s, %(to_price)s, %(frequency)s) 
                """
    if request.method == 'POST':
        conn = psycopg2.connect(database=config("DB_DATABASE"), user=config("DB_ADMIN_USERNAME"), password=config("DB_ADMIN_PASSWORD"), 
                                host=config("LOCALHOST"), port=config("DB_PORT"))
        cur = conn.cursor()

        km_range = [request.form['kilometers_range_start'], request.form['kilometers_range_end']]
        price_range = [request.form['price_range_start'], request.form['price_range_end']]

        for i in range(2):
            if km_range[i] == "":
                km_range[i] = i * 10000000
            if price_range[i] == "":
                price_range[i] = i * 10000000

        data = {
            'email': request.form['email'],
            'brand': request.form.get('carbrands'),
            'model': request.form.get('models'),
            'gas_type': request.form.get('fuel_types'),
            'from_kilometers': km_range[0],
            'to_kilometers': km_range[1],
            'from_price': price_range[0],
            'to_price': price_range[1],
            'frequency': request.form.get('frequency')
        }
        
        cur.execute(notifications_sql, data)
        conn.commit()

        cur.close()
        conn.close()

        return redirect('avtonet')
    
    return render_template('avtonet.html')


@app.route('/avtonet', methods=['GET', 'POST'])
def avtonet():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('avtonet.html', carbrands=brands, models=models, fuel_types=["bencinski motor", "diesel motor", "Elektro pogon", "Hibridni pogon", "Plin"] , frequency=["Immediate", "Daily", "Weekly", "Monthly", "Yearly"])
@app.route('/nepremicnine', methods=['GET', 'POST'])
def nepremicnine():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('nepremicnine.html')


if __name__ == "__main__":
    time.sleep(10)
    brands, models = get_brands_and_models()
    app.run(host="0.0.0.0", debug=True)

