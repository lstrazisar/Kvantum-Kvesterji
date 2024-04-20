from flask import Flask, render_template, request, redirect

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
    return render_template('avtonet.html', carbrands=["Audi", "Toyota", "Bmw", "Volkwagen"])
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

