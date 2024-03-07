with open("k.txt") as f:
    lines = f.readlines()

#del lines[1:len(lines)-1]


lines_out = []
for line in lines:
    try:
        temp = []
        x = 0
        lines2 = []
        while x < len(line):

            if line[x] == " ":
                x += 1
                continue
            else:
                while line[x] != " " and line[x] != "(" and line[x] != ")" and x < len(line) and line[x] != "\n":
                    temp.append(line[x])
                    x += 1
                joined = ''.join(temp)
                if joined != '':
                    lines2.append(float(joined))

                temp = []
            x += 1

        lines_out.append(lines2)
    except:
        continue

print(len(lines_out))
print(lines_out[0])

from csv import writer
import csv

with open("output_file.csv", "w") as f_out:
    for line in lines_out:
        write_obj = writer(f_out)
        write_obj.writerow(line)
    f_out.close()
