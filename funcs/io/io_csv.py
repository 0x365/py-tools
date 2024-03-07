import csv

def csv_input(file_name):
    '''
    Open a csv file and return an array
    '''
    with open(file_name, "r") as f:
        read_obj = csv.reader(f, delimter=' ')
        output = []
        for row in read_obj:
            try:
                temp = []
                for item in row:
                    temp.append(eval(row))
                output.append(temp)
            except:
                try:
                    output.append(eval(row))
                except:
                    try:
                        output.append(row)
                    except:
                        output = row    
    f.close()
    return output

def csv_output(file_name, data_send):
    '''
    Open a csv and add the sent data
    '''
    with open(file_name, "w") as f:
        if len(data_send) == 0:
            f.close()
            return
        elif len(data_send) == 1:
            csv.writer(f).writerow(data_send)
            f.close()
            return
        else:
            for item in data_send:
                csv.writer(f).writerow(item)
            f.close()
            return
