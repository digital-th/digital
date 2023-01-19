import tkinter
import tkinter.messagebox
import Othello_Board
import Calculating_Board
import ReadNumber

app = tkinter.Tk()
app.title('10puzzle')
app.geometry("840x420")
app.minsize(width=840, height=420)
app.maxsize(width=840, height=420)

filepath = "is_make10.csv"
n = ReadNumber.ReadNumber(filepath).get_number()

frame1 = tkinter.Frame(app)
frame2 = tkinter.Frame(app)

calc_board = Calculating_Board.calcBoard(frame2)
othello_borad = Othello_Board.Othello(frame1, n, calc_board)

frame1.grid(column=0,row=0)
frame2.grid(column=1,row=0)
app.mainloop()
