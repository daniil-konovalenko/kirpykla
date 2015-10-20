from flask import Flask, request, render_template
from service import get_results
import sqlite3
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        logging.debug('Post sent')

        connection = sqlite3.connect('results.sqlite3')
        cursor = connection.cursor()
        logging.debug(request.form)
        student_data = dict(
            first_name = request.form['first_name'],
            second_name = request.form['second_name'],
            last_name = request.form['last_name'],
            school_id = request.form['login_statgrad'].strip('sch')
        )
        logging.debug(student_data)
        results_table = get_results(student_data, cursor)
        connection.close()
        logging.debug(results_table)
        return render_template('results.html', results_table=results_table)

    else:
        return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=True)