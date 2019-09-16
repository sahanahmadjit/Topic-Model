tel = {'jack':90,'shape':40}
tel['blah']=4321
sorted(tel)
#print(list(tel))

for k, v in tel.items():
    print(k,v)

for i, v in enumerate(tel):
    print(i,v)