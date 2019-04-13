from flask import Flask, render_template
from src.utils import *
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/api/values', methods=['GET'])
def apiGetData():
    response = {
        'sensors': [],
        'code': 200
    }
    with connectDB() as con:
        with con.cursor() as cur:
            cur.execute("select * from sensor")
            sensors = cur.fetchall()
            print(sensors)
            values = []
            for sensor in sensors:
                cur.execute("select * from sensor_value where sensor='{id}' order by date desc limit 1".format(
                    id=sensor[SENSOR_ID]
                ))
                value = cur.fetchall()[0]
                response['sensors'].append({
                    'id': sensor[SENSOR_ID],
                    'name': sensor[SENSOR_NAME],
                    'location': sensor[SENSOR_LOCATION],
                    'value': value[SENSORVAL_VALUE],
                    'date': value[SENSORVAL_DATE].strftime("%Y-%m-%d %H:%M:%S")
                })
                #print(value)
                #print(type(value[SENSORVAL_DATE]))
                value = list(value)
                value[SENSORVAL_DATE] = value[SENSORVAL_DATE].strftime("%Y-%m-%d %H:%M:%S")
                values.append(value)


    print(response)
    return json.dumps(response)

if __name__ == '__main__':
    app.run()
