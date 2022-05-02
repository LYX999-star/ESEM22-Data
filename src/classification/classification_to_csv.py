import csv
import os

if __name__ == '__main__':

    read_path = r'E:\opensource\Indirect Dependency\indirect-dependency\subspace\classification\res'

    res = []

    for file in os.listdir(read_path):
        print(file)
        res.append([file.split('.')[0]])
        file_path = read_path + '\\' + file
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            i = 0
            while i+5 < len(lines):
                i += 3
                res.append(['','','',float(lines[i][:-1].split(':')[-1]), float(lines[i+1][:-1].split(':')[-1])])
                i += 3
            print(res)

    output_path = r'E:\opensource\Indirect Dependency\indirect-dependency\subspace\classification\classification.csv'
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        for record in res:
            csv_writer.writerow(record)


