'''
Created on Dec 21, 2017

@author: gustavo
'''


pts = [[(177,271),(717,718)],
       [(626,231),(1118,393)],
       #[(407,245),(960,541)],
       #[(302,264),(953,677)],
       #[(978,207),(-92,32)],
       [(1120,604),(874,719)],
       ]

ms = []
bs = []

xm = [[0,0,0],[0,0,0],[0,0,0]]
ym = [[0,0,0],[0,0,0],[0,0,0]]

for pair in pts:
    
    dy = pair[0][1] - pair[1][1]
    dx = pair[0][0] - pair[1][0]
    
    print("dx: %d, dy: %d" % (dx,dy))
    
    m = float(dy)/dx
    b = pair[0][1] - m*pair[0][0]
    
    ms.append(m)
    bs.append(b)
    
    print("y = %s x+%4.5f" % (m,b))

for i, m in enumerate(ms):
    for j, mt in enumerate(ms):
        
        if i != j:
            db = (bs[j]-bs[i])
            print("db: ",db)
            xm[i][j] = db/(m-mt)
            ym[i][j] = xm[i][j]*m + bs[i]

print(xm)
print(ym)
            