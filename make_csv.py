import csv
fields = ['ID', 'CATEGORY', 'SUBCATEGORY', 'TITLE', 'PRICE','BARCODE']
filename = "data.csv"
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
