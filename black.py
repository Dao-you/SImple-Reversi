#import random
#import time
class gameboard:
    
    '''
    黑色 = -1
    空位 = 0
    白色 = 1
    '''

    # n 順序、s 棋盤、amount 棋子數量
    n = -1
    s = []
    avaliable = []

    def __init__(self):
        self.s = []
        for i in range(8):
            self.s.append([0,0,0,0,0,0,0,0])
        
        self.s[3][3] =  1
        self.s[3][4] = -1
        self.s[4][3] = -1
        self.s[4][4] =  1

        self.avaliable = [ [2, 3], [3, 2], [4, 5], [5, 4] ]

    def check(self):#更新avaliable
        t=[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        self.avaliable=[]# 可下座標
        for i in range(8):# 爆搜可下座標
            for j in range(8):
                if(self.s[i][j]==0):
                    b=False
                    for k in range(8):
                        x=1
                        if(i+t[k][0]>=0 and i+t[k][0]<=7 and j+t[k][1]>=0 and j+t[k][1]<=7):
                            if(self.s[i+t[k][0]][j+t[k][1]]==-1*self.n):
                                while True:
                                    x+=1
                                    if(i+t[k][0]*x>=0 and i+t[k][0]*x<=7 and j+t[k][1]*x>=0 and j+t[k][1]*x<=7):
                                        if(self.s[i+t[k][0]*x][j+t[k][1]*x]==self.n):
                                            b=True
                                            break
                                        elif(self.s[i+t[k][0]*x][j+t[k][1]*x]==0):
                                            break
                                    else:
                                        break
                        if(b):
                            break
                    if(b):
                        self.avaliable.append([i,j])
                        
    def update(self,position):
        t=[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        ret=[]# 應改變座標
        for k in range(8):# 紀錄需改變座標
            x=1
            if(position[0]+t[k][0]>=0 and position[0]+t[k][0]<=7 and position[1]+t[k][1]>=0 and position[1]+t[k][1]<=7):
                if(self.s[position[0]+t[k][0]][position[1]+t[k][1]]==-1*self.n):
                    while True:
                        x+=1
                        if(position[0]+t[k][0]*x>=0 and position[0]+t[k][0]*x<=7 and position[1]+t[k][1]*x>=0 and position[1]+t[k][1]*x<=7):
                            if(self.s[position[0]+t[k][0]*x][position[1]+t[k][1]*x]==self.n):
                                for i in range(1,x,1):
                                    ret.append([position[0]+t[k][0]*i,position[1]+t[k][1]*i])
                                    self.s[position[0]+t[k][0]*i][position[1]+t[k][1]*i]=self.n#順便更新棋盤
                                break
                            elif(self.s[position[0]+t[k][0]*x][position[1]+t[k][1]*x]==0):
                                break
                        else:
                            break
        ret.append([position[0],position[1]])
        self.s[position[0]][position[1]]=self.n
        return(ret)

    def win(self):#continue的情況放在action
        if sum(sum(i) for i in self.s) < 0:#大小於我修正了
            return 'black win'
        elif sum(sum(i) for i in self.s) > 0:
            return 'white win'
        else:
            return 'tie'

    # position 輸入為一個座標串列，共兩項，例如 [3, 4]
    def action(self, position):
        ret=self.update(position)
        flag = self.n
        self.n = -1 * self.n
        self.check()
        if self.avaliable == []:
            self.n = -1 * self.n
            self.check()
            if self.avaliable == []:#雙方皆無法下，進行結算
                stat=self.win()
            else:
                stat="continue"
        else:
            stat="continue"
            
        # 伺服器端棋盤更新與資料
        if(flag == -1):
     
            return {
                    'white': [],
                    'black': ret,
                    'avalible': self.avaliable,
                    'stat': stat,
                    'flag': self.n
                    }
        else:

            return {
                    'white': ret,
                    'black': [],
                    'avalible': self.avaliable,
                    'stat': stat,
                    'flag': self.n
                    }

    # 輸出棋盤至終端機
    def output(self):
        for i in range(8):
            for j in range(8):
                if(self.s[i][j]==0):
                    print("囗",end="")
                elif(self.s[i][j]==1):
                    print("掰",end="")
                else:
                    print("黑",end="")
            print()
        print(self.avaliable)
        if self.n == 1:
            print("白色：", end=" ")
        else:
            print("黑色：", end=" ")

if __name__ == "__main__":
    game = gameboard()
    game.output()

    while True:
        l=input().split()#玩家輸入座標
        #l=game.avaliable[random.randint(0,len(game.avaliable)-1)]
        #time.sleep(0.1)
        l[0]=int(l[0])
        l[1]=int(l[1])

        if( [ l[0],l[1] ] in game.avaliable ):
            re = game.action([l[0],l[1]])
            print(re)
            game.output()
        else:
            print("error")

        if re['stat'] != 'continue':
            print(re['stat'])
            break