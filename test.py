from datetime import datetime

a = "10:00"
b = "11:00"

a1 = datetime.strptime(a,'%H:%S')
b1 = datetime.strptime(b,'%H:%S')

c = b1 - a1 
print(c.total_seconds()/60.0)