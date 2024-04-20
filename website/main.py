from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', content="Hello My Dear friend", djdjds="YOU CAN DO THISSSSS", badboy=["a", "b", "c", "d"])

@app.route('/about', methods=['POST'])
def about():
    if request.method == 'POST':
        user = request.form['name']
        email = request.form['email']
        print(user)
        print(email)
        return redirect('/')
    
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)

