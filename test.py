from datetime import datetime

a = "10:00"
b = "10:40"

a1 = datetime.strptime(a,'%H:%M')
b1 = datetime.strptime(b,'%H:%M')

c = b1 - a1 
print(c.total_seconds()/60.0)
print(int(c.total_seconds()/60.0))