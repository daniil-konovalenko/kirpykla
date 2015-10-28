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
        results_connection = sqlite3.connect('results.sqlite3')
        service_connection = sqlite3.connect('service.sqlite3')
        results_cursor = results_connection.cursor()
        service_cursor = service_connection.cursor()
        student_data = dict(
            first_name = request.form['first_name'],
            second_name = request.form['second_name'],
            last_name = request.form['last_name'],
            school_id = request.form['login_statgrad'].strip('sch')
        )
        logging.debug(student_data)
        results_response = get_results(student_data, results_cursor, service_cursor)
        service_connection.close()
        results_connection.close()
        if results_response['status'] == 'OK':
            return render_template('results.html', results_table=results_response['table'])
        else:
            return render_template('results.html')

    else:
        return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=True)