from datetime import date,time,datetime

# d1 = date (2018, 1, 1)
# print (d1)
# print(type(d1))
# #dia
# print ('DIA: ',d1.day)
# #mes
# print ('MES: ',d1.month)
# #año
# print ('AÑO: ',d1.year)

d1 = date.today()
print (d1)

#dia
print ('DIA: ',d1.day)
#mes
print ('MES: ',d1.month)
#año
print ('AÑO: ',d1.year)

t1 = time(12,30,10,40)
print (t1)
print (type(t1))

#hora
print ('HORA: ',t1.hour)
#minutos
print ('MINUTOS: ',t1.minute)
#segundos
print ('SEGUNDOS: ',t1.second)
#microsegundos
print ('MICROSEGUNDOS: ',t1.microsecond)

d2 = datetime.now()
print (d2)
print (type(d2))

d2 = datetime(2018,1,1,12,30,10,40)
print (d2)
print (type(d2))

#dia
print ('DIA: ',d2.day)
#mes
print ('MES: ',d2.month)
#año
print ('AÑO: ',d2.year)
#hora
print ('HORA: ',d2.hour)
#minutos
print ('MINUTOS: ',d2.minute)
#segundos
print ('SEGUNDOS: ',d2.second)
#microsegundos
print ('MICROSEGUNDOS: ',d2.microsecond)
#dia de la semana que cae la fecha d2 (0=lunes, 1=martes, etc)
print (d2.weekday())
#dia de la semana que cae la fecha d2 (0=domingo, 1=lunes, etc) ISO ARRANCA DE DOMINGO
print (d2.isoweekday())
#calendario
print (d2.isocalendar())

date2 = '22 marzo, 2022 13:30:10'
date3 = datetime.strptime(date2,'%d %B, %Y %H:%M:%S.%f')
print (date3)