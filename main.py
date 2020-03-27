import requests 
from bs4 import BeautifulSoup 
from tabulate import tabulate 
import os 
import numpy as np 
import matplotlib.pyplot as plt 
import tkinter as tk
from tkinter import ttk


def show():
	# stats.sort(key=lambda e: e[1], reverse=True)

	for (sno,state,indian,foreign,cured,death) in stats:
		listBox.insert("", "end", values=(sno,state,indian,foreign,cured,death))

extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
URL = 'https://www.mohfw.gov.in/'

SHORT_HEADERS = ['SNo', 'State','Indian-Confirmed Cases', 
				'Foreign-Confirmed Cases','Number of people Cured','Death'] 

response = requests.get(URL).content 
soup = BeautifulSoup(response, 'html.parser') 
header = extract_contents(soup.tr.find_all('th')) 

stats = [] 
all_rows = soup.find_all('tr') 

for row in all_rows: 
	stat = extract_contents(row.find_all('td')) 
	if stat: 
		if len(stat) == 5: 
			# last row 
			stat = ['', *stat] 
			stats.append(stat) 
		elif len(stat) == 6: 
			stats.append(stat) 

stats[-1][1] = "Total Cases"

stats.remove(stats[-1]) 




objects = [] 
for row in stats : 
	objects.append(row[1]) 

y_pos = np.arange(len(objects)) 

performance = [] 
for row in stats : 
	performance.append(int(row[2]) + int(row[3])) 

cases = tk.Tk() 
cases.title("COVID-19 Updates")
label = tk.Label(cases, text="Corona Virus Cases in India", font=("Arial",30)).grid(row=0, columnspan=6)

listBox = ttk.Treeview(cases, columns=SHORT_HEADERS, show='headings')

for col in SHORT_HEADERS:
    listBox.heading(col, text=col)    
listBox.grid(row=1, column=0, columnspan=2)

# table = tabulate(stats, headers=SHORT_HEADERS,tablefmt="grid") 


show()

closeButton = tk.Button(cases, text="Close", width=15, command=exit).grid(row=4, column=0)

cases.mainloop()


# cases_output=open("output.csv","w")
# cases_output.write(cases)
# cases_output.close()

plt.barh(y_pos, performance, align='center', alpha=0.5, 
				color=(0/256.0, 0/256.0, 256/256.0), 
				edgecolor=(106/256.0, 27/256.0, 154/256.0)) 

plt.yticks(y_pos, objects) 
plt.xlim(1,200) 
plt.xlabel('Number of Cases') 
plt.title('Corona Virus Cases') 
plt.gcf().canvas.set_window_title('COVID-19 Live Updates')
plt.show() 
