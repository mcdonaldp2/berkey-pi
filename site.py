 #!/usr/bin/python3


from flask import Flask
from flask import render_template, redirect, url_for, request
from flask_wtf.csrf import CSRFProtect
import os
import berkeydb

app=Flask(__name__)

def get_tanksize(berkey_config, berkey_models):
	tanksize = None
	if (berkey_config.model_id != None):
		for model in berkey_models:
			if model.model_id == berkey_config.model_id:
				tanksize = model.tank_size
	return tanksize


@app.route('/set-config', methods = ['POST'])
def set_config():
	response = berkeydb.upsert_berkeyconfig(request.form)
	return redirect(url_for('index', isSuccess = response.is_success, errorMessage = response.error_message))

@app.route('/')
def index():
	berkey_config = berkeydb.get_berkeyconfig()
	berkey_models = berkeydb.get_berkeymodels()
	fills_this_week = berkeydb.get_fills_this_week()
	fills_last_week = berkeydb.get_fills_last_week()
	total_fills = berkeydb.get_total_fills()
	ytd_fills = berkeydb.get_ytd_fills()
	tank_size = get_tanksize(berkey_config, berkey_models)
	return render_template(
		'index.html', 
		title='Home', 
		BerkeyConfig=berkey_config,
		BerkeyModels=berkey_models,
		FillsLastWeek=fills_last_week, 
		FillsThisWeek=fills_this_week, 
		TotalFills=total_fills, 
		YTDFills = ytd_fills,
		TankSize = tank_size)

if  __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

