from itertools import zip_longest
import tkinter


#キャンバスの横方向・縦方向のサイズ（px）
CANVAS_SIZE_WIDTH = 400
CANVAS_SIZE_HEIGHT = 150
# 色の設定
BOARD_COLOR = 'green'  # 盤面の背景色

class calcBoard():
    def __init__(self, master):
        self.master = master
        #self.othelloBoard = NULL
        self.n = 0 # クリックされた箇所の数字を保持する
        self.x = 0 # クリックされた箇所の位置を保持する
        self.y = 0 # クリックされた箇所の位置を保持する
        self.value = 0 #　演算結果を管理する
        self.operators = [] #入力された演算子を管理する

        self.PlusButton = tkinter.Button(
            master,
            text="+",
            width=4,
            height=5,
        )
        self.MinusButton = tkinter.Button(
            master,
            text="-",
            width=4,
            height=5,
        )
        self.TimesButton = tkinter.Button(
            master,
            text="×",
            width=4,
            height=5,
        )
        self.DividedButton = tkinter.Button(
            master,
            text="÷",
            width=4,
            height=5,
        )

        self.GoButton = tkinter.Button(
            master,
            text="GO!",
            width=4,
            height=5,
        )

        self.createWidgets() # ウィジェットの作成
        self.initCalc() # 計算部の初期化
        self.setEvents() # ボタンクリックイベントの設定

    def createWidgets(self):
        # キャンバスの作成
        self.canvas = tkinter.Canvas(
            self.master,
            bg=BOARD_COLOR,
            width=CANVAS_SIZE_WIDTH, 
            height=CANVAS_SIZE_HEIGHT,  
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)   
        
        # ボタンの作成
        self.PlusButton.pack(padx=10, side="left")
        self.MinusButton.pack(padx=0, side="left")
        self.TimesButton.pack(padx=10, side="left")
        self.DividedButton.pack(padx=0, side="left")
        self.GoButton.pack(padx=10, side="left")

    def initCalc(self):
        self.canvas.create_rectangle(
            20, 20, #左上の座標
            380, 100 #右下の座標
        )   

    def setEvents(self):
        # ボタンのマウスクリックを受け付ける
        self.PlusButton.bind('<ButtonPress>', self.btn_click)
        self.MinusButton.bind('<ButtonPress>', self.btn_click)
        self.TimesButton.bind('<ButtonPress>', self.btn_click)
        self.DividedButton.bind('<ButtonPress>', self.btn_click)
        self.GoButton.bind('<ButtonPress>', self.btn_click)
        
    def displayNumber(self, n, x, y): # 数字の表示
        self.n = n
        self.x = x
        self.y = y
        for idx, v in enumerate(str(n)):
            self.canvas.create_text(
                50+100*idx, 57, text=v,
                font=("HG丸ｺﾞｼｯｸM-PRO", 40), fill="black", tag="number"
            )     

    def displayOperator(self, operator, idx): # 演算子の表示
        self.canvas.create_text(
                0+100*idx, 57, text=operator,
                font=("HG丸ｺﾞｼｯｸM-PRO", 40), fill="black", tag="operator"
        )  

    def displayMessage(self, message): # フィードバックの表示
        self.canvas.create_text(
            200, 125, text=message,
            font=("HG丸ｺﾞｼｯｸM-PRO", 20), fill="black", tag="message"
        ) 

    def deleteText(self, tag): #タグ名のテキストを消す
        self.canvas.delete(tag)

    def calc(self): #式の値を計算
        formula = ""
        for n, o in zip_longest(str(self.n), self.operators, fillvalue=""):
            formula = formula + n + o
        try:    
            return eval(formula) 
        except:
            return "0で割ることはできません"            

    def getInstance(self, instance):
        self.othelloBoard = instance

    def btn_click(self, event):
        type = event.widget.cget("text")  
        if type != "GO!" and len(self.operators) < 3:
            if type == "×":
                self.operators.append("*")
            elif type == "÷":
                self.operators.append("/")  
            else:
                self.operators.append(type)
            self.displayOperator(type, len(self.operators)) 

        elif type == "GO!" and len(self.operators) == 3:
            self.deleteText("operator")
            self.deleteText("message")
            self.value = self.calc()
            self.displayMessage(self.value)
            if self.value == 10:
                # 次に石を置けるなら石を置く
                self.othelloBoard.place(self.x, self.y, self.othelloBoard.color[self.othelloBoard.player])
            self.operators = []
