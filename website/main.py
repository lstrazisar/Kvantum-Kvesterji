from flask import Flask, render_template, request, redirect

<<<<<<< Updated upstream
=======
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
brands, models = get_brands_and_models()
>>>>>>> Stashed changes
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about', methods=['POST'])
def about():
    if request.method == 'POST':
        print(request.form)
        email = request.form['email']
        kilometers_range_start = request.form['kilometers_range_start']
        kilometers_range_end = request.form['kilometers_range_end']
        price_range_start = request.form['price_range_start']
        price_range_end = request.form['price_range_end']
<<<<<<< Updated upstream
=======
        brand = request.form.get('brand')
        fuel_type = request.form.get('fuel_type')
        frequency = request.form.get('frequency')
>>>>>>> Stashed changes
        if kilometers_range_start == "":
            kilometers_range_start = 0
        if kilometers_range_end == "":
            kilometers_range_end = 10000000
        if price_range_start == "":
            price_range_start = 0
        if price_range_end == "":
            price_range_end = 10000000
        
        print(email)
        print(kilometers_range_start)
        print(kilometers_range_end)
        print(price_range_start)
        print(price_range_end)
<<<<<<< Updated upstream
=======
        print(brand)
        print(fuel_type)
        print(frequency)
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    return render_template('avtonet.html', carbrands=["Audi", "Toyota", "Bmw", "Volkwagen"])
=======
    return render_template('avtonet.html', carbrands=brands, models=models, fuel_types=["","Bencin", "Dizel", "Elektrika", "Hibrid", "Plin"] , frequency=["Immediate", "Daily", "Weekly", "Monthly", "Yearly"])
>>>>>>> Stashed changes
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
    app.run(debug=True)

