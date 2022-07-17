from flask import Flask
import os
import csv
import itertools
import operator
  
app = Flask(__name__)

@app.route('/patient/<id>')
def get_patient_data(id):
    if id == '123':
        data = []
        with open("sample_data.csv", "r") as f:
            reader = csv.reader(f, delimiter=",")
            for i, line in enumerate(reader):
                if i>1:
                    obj = {
                        "Date": line[0],
                        "Scale": line[1],
                        "Test type": line[2],
                        "Test parameter": line[3],
                        "Unit": line[4],
                        "Status": line[5],
                        "Score": {
                            "Patient": line[6],
                            "Normal": line[7],
                            "Scale": line[8]
                        },
                        "Video": line[9],
                        "Medicine": {
                            "Generic Name": line[10],
                            "Formulation": line[11],
                            "Dosage": line[12],
                            "Frequency": line[13]
                        }
                    }
                    data.append(obj)
        # group by date
        data_grouped_by_date = {}
        for obj in data:
            if obj["Date"] in data_grouped_by_date:
                data_grouped_by_date[obj["Date"]]["Tests"].append({
                    "Scale": obj["Scale"],
                    "Status": obj["Status"],
                    "Test type": obj["Test type"],
                    "Video": obj["Video"],
                    "Test parameter": obj["Test parameter"],
                    "Score": obj["Score"]
                })
            else:
                data_grouped_by_date[obj["Date"]] = {
                    "Date": obj["Date"],
                    "Medicine": obj["Medicine"],
                    "Tests": [{
                        "Scale": obj["Scale"],
                        "Status": obj["Status"],
                        "Test type": obj["Test type"],
                        "Video": obj["Video"],
                        "Test parameter": obj["Test parameter"],
                        "Score": obj["Score"]
                    }]
                }
        data_grouped_by_date = list(data_grouped_by_date.values())

        def group_by_test_type(obj):
            data_grouped = {}
            for obj in data:
                if obj["Test type"] in data_grouped:
                    data_grouped[obj["Test type"]]["Sub-tests"].append({
                        "Test parameter": obj["Test parameter"],
                        "Score": obj["Score"],
                        "Unit": obj["Unit"]
                    })
                else:
                    data_grouped[obj["Test type"]] = {
                        "Scale": obj["Scale"],
                        "Status": obj["Status"],
                        "Test type": obj["Test type"],
                        "Video": obj["Video"],
                        "Sub-tests": [{
                            "Test parameter": obj["Test parameter"],
                            "Score": obj["Score"],
                            "Unit": obj["Unit"]
                        }]
                    }
            data_grouped = list(data_grouped.values())
            return data_grouped

        # group by date and test type
        data_grouped_by_date_test_type = []
        for obj in data_grouped_by_date:
            data_grouped_by_test_type = {
                "Date": obj["Date"],
                "Medicine": obj["Medicine"],
                "Tests": group_by_test_type(obj)
            }
            data_grouped_by_date_test_type.append(data_grouped_by_test_type)

        return {"data": data_grouped_by_date_test_type}
    else:
        return "Patient not found"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))