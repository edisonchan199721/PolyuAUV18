import csv
import storage as storage

with open('data.csv', 'w') as csvfile:
    fieldnames = ['time','depth','Pitch','Roll']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in range (10):
        writer.writerow({'time':int(i),'depth':storage.depth,'Pitch':storage.pitch,'Roll':storage.roll})
   
