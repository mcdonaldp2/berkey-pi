from flask import Flask
from flask import render_template
import sqlite3
import os

app=Flask(__name__)

def getSQLiteConnection():
	return sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + '/../berkeydata')

def getFillsThisWeek():
	connection = getSQLiteConnection()
	cursor = connection.cursor()
	cursor.execute(
		"select FillId, FillTime, FillDayOfWeek from BerkeyFillLog where datetime(FillTime) >= datetime(date('now'), 'weekday 6', '-6 days') and datetime(FillTime) <= datetime(date('now'), 'weekday 6') order by datetime(FillTime) ASC;"
	)
	rows = cursor.fetchall()

	connection.close()
	return rows

def getFillsLastWeek():
        connection = getSQLiteConnection()
        cursor = connection.cursor()
        cursor.execute(
                "select FillId, FillTime, FillDayOfWeek from BerkeyFillLog where datetime(fillTime) >= datetime(date('now'), 'weekday 6', '-6 days', '-7 days') and datetime(FillTime) <= datetime(date('now'), 'weekday 6', '-6 days') order by datetime(FillTime) ASC;"
        )
        rows = cursor.fetchall()

        connection.close()
        return rows

def getTotalFills():
	connection = getSQLiteConnection()
	cursor = connection.cursor()

	cursor.execute(
		"select COUNT(*) from BerkeyFillLog"
	)
	rows = cursor.fetchall()
	connection.close()

	return rows[0][0]

def getYTDFills():
	connection = getSQLiteConnection()
	cursor = connection.cursor()

	cursor.execute(
			"select COUNT(*) from BerkeyFillLog where datetime(FillTime) >= datetime('now', 'start of year')"
	)
	rows = cursor.fetchall()
	connection.close()

	return rows[0][0]


@app.route('/')
def index():
	fillsThisWeek =	getFillsThisWeek()
	fillsLastWeek = getFillsLastWeek()
	totalFills = getTotalFills()
	ytdFills = getYTDFills()
	return render_template('index.html', title='Home', FillsLastWeek=fillsLastWeek, FillsThisWeek=fillsThisWeek, TotalFills=totalFills, YTDFills = ytdFills)

if  __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
