# Stock market data visualisation
import pandas as pd
import yfinance as yf
from pandas_datareader import data as wb
import tkinter as tk
from tkcalendar import Calendar
import mpl_finance as mpf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime as dt


def GetData(user_ticker, user_sdate, user_edate):
    
    yf.pdr_override()                                                                   #zastąpienie domyślnego pandasa przez yfinance
    ticker_info = wb.DataReader(user_ticker, start=user_sdate, end=user_edate)  
    index_reset = pd.DataFrame(ticker_info)
    index_reset.dropna().reset_index(drop = False, inplace = True)                      #usuwa puste wartości i wrzuca daty do kolumn
    index_reset['Date'] = index_reset.index.map(mdates.date2num)                        #zmienia format dat na float
    print(index_reset)
    return index_reset

def DisplayData():
   
    user_ticker = e1.get()
    user_sdate = cal1.get_date()
    user_edate = cal2.get_date()
    index_reset = GetData(user_ticker, user_sdate, user_edate)
    if frame2 !=None:
        for tk.widgets in frame2.winfo_children():
            tk.widgets.destroy()
       
    fig, (ax,ax2,ax3) = plt.subplots(figsize = (10,6), dpi = 100, nrows=3, ncols=1, sharex=True, facecolor='#D3D3D3', gridspec_kw={'height_ratios': [7, 2,3]})
    ax.set_title(user_ticker + ' Candlestick Chart')
    mpf.candlestick_ohlc(ax, index_reset[['Date', 'Open', 'High', 'Low', 'Close']].values, width=0.6, colorup='g', colordown='r', alpha = 1)
    volume = index_reset['Volume']
    pos = index_reset['Open']-index_reset['Close']<0
    neg = index_reset['Open']-index_reset['Close']>0
    ax2.bar(index_reset[pos]['Date'], volume[pos], color='g', width=0.8, align='center')
    ax2.bar(index_reset[neg]['Date'], volume[neg], color='r', width=0.8, align='center')
    yticks = ax2.get_yticks()
    ylabels = [int(ytick) for ytick in yticks]
    ax2.set_yticklabels(ylabels)
    ax2.yaxis.set_label_position("right")
    ax2.set_ylabel('Volume', size=10)
    ax.set_xlabel('Date')
    ax.yaxis.set_label_position("right")
    ax.set_ylabel('Price')
    DisplayRSI(ax3,index_reset)
    ax.tick_params(axis='x', labelbottom=False)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    ax.grid()
    ax2.grid()
    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas.draw()
    canvas.get_tk_widget().configure(bg="#C0C0C0")
    canvas.get_tk_widget().grid(padx = 0, sticky = tk.NS)

def CalcRSI(index_reset2):
    delta = index_reset2['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    average_gain = gain.rolling(window=14, min_periods=1).mean()
    average_loss = loss.rolling(window=14, min_periods=1).mean()
    relative_strength = average_gain / average_loss
    rsi = 100 - (100 / (1 + relative_strength))
    rsi[:14] = None
    return rsi

def DisplayRSI(ax,index_reset2):
    rsi = CalcRSI(index_reset2)
    ax.plot(index_reset2['Date'], rsi, color='blue')
    ax.axhline(30, color='red', linestyle='--')
    ax.axhline(70, color='red', linestyle='--')
    ax.set_ylabel('RSI')
    ax.yaxis.set_label_position("right")
    ax.xaxis_date()
    ax.grid()
    
def on_closing():
    root.destroy()  
    root.quit()  

root = tk.Tk()
root.title('Market Data')
root.protocol("WM_DELETE_WINDOW", on_closing)
frame1 = tk.Frame(root, highlightbackground="blue", highlightthickness=2)
frame2 = tk.Frame(root)
frame1.pack(side = tk.LEFT, padx = (20,0))
frame2.pack(side = tk.RIGHT)
frame1.columnconfigure(0, weight=1)
for i in range(0,8):
    frame1.rowconfigure(i, weight=1)

frame1.rowconfigure(7, weight=5)
frame1.rowconfigure(8, weight=5)
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
root.geometry(f"{width}x{height}")
root.configure(bg="#D3D3D3")

ticker_label = tk.Label(frame1, text = "Ticker: ", font= 15, fg="black")
ticker_label.grid(column=0, row=0, padx = 10, sticky = tk.W)
e1 = tk.Entry(frame1)
e1.grid(column=0, row=1, padx = 10, pady=(0,10), sticky = tk.W)
starting_label = tk.Label(frame1, text = "Starting date: ", font= 15, fg="black")
starting_label.grid(column=0, row=2, padx = 10,pady = 0, sticky = tk.W)
cal1 = Calendar(frame1, date_pattern='yyyy-mm-dd', font = "Arial 6", selectmode = 'day',
               year = dt.date.today().year, month = dt.date.today().month,
               day = dt.date.today().day-14)
cal1.grid(column=0, row=3, padx = 10,pady = (0,10), sticky = tk.W)
ending_label = tk.Label(frame1, text = "Ending date: ", font= 15, fg="black")
ending_label.grid(column=0, row=4, padx = 10, pady = 0,sticky = tk.W)
cal2 = Calendar(frame1, date_pattern='yyyy-mm-dd', font = "Arial 6", selectmode = 'day',
               year = dt.date.today().year, month = dt.date.today().month,
               day = dt.date.today().day)
cal2.grid(column=0, row=5,pady = (0,10), padx = 10, sticky = tk.W)
button1 = tk.Button(frame1, text = "Run", command = DisplayData, width = 23)
button1.grid(column=0, row=6, sticky = tk.W,padx = 10, pady = 10)

root.mainloop()