import json
import csv

# Input
def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

# Output
def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)

# Input
def load_csv(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(row)   
    f.close()
    return output

# Output
def save_csv(file_name, data_send):
    with open(file_name, "w") as f:
        if len(data_send) == 0:
            f.close()
            return
        else:
            for item in data_send:
                csv.writer(f).writerow(item)
            f.close()
            return


## Make grid plotter with matplotlib

## Make easy clean image generator with no axis

## Add matplotlib numpy PyQT5 to requirements

## Maybe add the web generator for interactive plots