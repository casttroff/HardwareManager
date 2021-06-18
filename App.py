from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from Models import Asset_description
from Func import createassets
import copy, requests, uuid


assetsArr = []
snipeModelsArr = []
snipeStatusArr = []
assetDict = {
	'id' : uuid.uuid4(),
	'serial_number' : '',
	'mac_address' : ''
}
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'assets'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
	global assetsArr
	#cursor = mysql.connection.cursor()
	#cursor.execute('SELECT * FROM descripcion_assets')
	#data = cursor.fetchall()
	return render_template('index.html', assets=assetsArr)


@app.route('/add_asset', methods=['POST'])
def add_asset():
	global assetsArr, assetDict
	if request.method == 'POST':
		if request.form['serial_number'] == '':
			flash('Ingrese S/N')
		elif request.form['mac_address'] == '':
			flash('Ingrese un formato correcto de MAC address')
		else:
			assetDict['serial_number'] = request.form['serial_number']
			assetDict['mac_address'] = request.form['mac_address']	
			assetsArr.append(copy.copy(assetDict))			
		#cursor = mysql.connection.cursor()
		#cursor.execute('INSERT INTO descripcion_assets (serial_number, mac_address) VALUES (%s, %s)',
		#		 (serial_number, mac_address))
		#mysql.connection.commit()
		return redirect(url_for('Index'))


@app.route('/atributes')
def atributes():
	global assetsArr; snipeModelsArr; snipeStatusArr
	infoModels = {
		"model" : "",
		"model_id" : ""
		}
	infoStatus = {
		"status" : "",
		"status_id" : ""
		}
	urlModels = "https://xyz.snipe-it.io/api/v1/models"
	urlStatus = "https://xyz.snipe-it.io/api/v1/statuslabels"
	querystring1 = {"limit":"50","offset":"0","sort":"created_at","order":"asc"}
	querystring2 = {"limit":"500","offset":"0","sort":"name","order":"asc"}
	headers = {"Authorization": "Bearer xyz.xyz.KqL6QfN6olnzFVE3QnCerkQWX6KFzdMxiJS2VmWcoPjovdVPorfluQ5gkWvDSCUL4VINk8O7eXdwv4w4ORa91AfI4Yx61NvPpvUfiDYKOUo9o4GhOmHv59qus1cFZ_nR9HYz0xZ6GTltYEQs0DgFGFfz63kTy8-CspIUWH-sZtPr8s8vleq1TvAm-OxlStSOCUWb1LK4aubLkZbPeO_1xkcU10KdT1gz3gr8lx8ANScG2DQ3N8TjtT2-LK210ePtvEGsNoq-vC2yRYEJmeFlxQ_Ou4O1azfZcuk_2oc0rwMbCf62cpTT3d8yOBb6AEubyTxpdyDpKmqhww5AOhEqkoXZo7aIijnvVr403BlDLlfxPPHZ7zUgliUbEXCjUtRSBcVSby5YaTbWhnSLJDuimafR2FUW8L9ySzfUXjjE9OKGrUIxFx0-mDUvPu__Vi_oLOErVTZ7gn0KQT4gqCzbMtUz7QUpq7mh0tWSboX4-81xn1Cyvk1xkS65oKtpULpv56jw8DIXHokCUIQEP5W-2v6q-vWABMl_04GfC4UEJfcWeLZHV2n7pGXBS-hKulG-jL-vLZ9Mk0-V5PWJ8fNwlDnaiC14M6Ok7oUPbkgYC8G0w5CSVVvfrDevXW8SbvOcEyLoFDsIbUQfmmGqgfqrz4OrsYT3u5QJ-EOc9t-WO-o"}
	statusResponse = requests.request("GET", urlStatus, headers=headers, params=querystring1)
	modelsResponse = requests.request("GET", urlModels, headers=headers, params=querystring2)
	snipeModels = modelsResponse.json()
	snipeStatus = statusResponse.json()

	for model in snipeModels['rows']:
		infoModels['model'] = model['name']
		infoModels['model_id'] = model['id']
		snipeModelsArr.append(copy.copy(infoModels))

	for status in snipeStatus['rows']:
		infoStatus['status'] = status['name']
		infoStatus['status_id'] = status['id']
		snipeStatusArr.append(copy.copy(infoStatus))

	return render_template('atributes.html', assetsArr=assetsArr, snipeModelsArr=snipeModelsArr, snipeStatusArr=snipeStatusArr)

@app.route('/drop_arr_sn')
def drop_arr_sn():
	global assetsArr
	for asset in assetsArr[:]:
		assetsArr.remove(asset)

	return redirect(url_for('Index'))


@app.route('/edit/<idx>')
def get_asset(idx):
	global assetsArr
	for asset in assetsArr:
		if str(asset['id']) == idx:
			data = asset

	#cursor = mysql.connection.cursor()
	#cursor.execute('SELECT * FROM descripcion_assets WHERE id = "{}"'.format(id))
	#data = cursor.fetchall()
	return render_template('edit-asset.html', asset=data)


@app.route('/update/<id>', methods=['POST'])
def update_asset(id):
	global assetsArr
	if request.method == 'POST':
		serial_number = request.form['serial_number']
		mac_address = request.form['mac_address']
		for asset in assetsArr:
			if str(asset['id']) == id:
				asset['serial_number'] = serial_number
				asset['mac_address'] = mac_address

		#cursor = mysql.connection.cursor()
		#cursor.execute('UPDATE descripcion_assets SET serial_number = %s, mac_address = %s WHERE id = %s', (serial_number, mac_address, id))
		#mysql.connection.commit()
		flash('Asset actualizado')
		return redirect(url_for('Index'))


@app.route('/delete/<string:idx>')
def delete_asset(idx):
	global assetsArr
	for asset in assetsArr:
		if str(asset['id']) == idx:
			assetsArr.remove(asset)
	#cursor = mysql.connection.cursor()
	#cursor.execute('DELETE FROM descripcion_assets WHERE id = "{}"'.format(id))
	#mysql.connection.commit()
	return redirect(url_for('Index'))


@app.route('/add_snipe', methods=['POST'])
def add_snipe():
	global assetsArr; snipeModelsArr; snipeStatusArr
	flag = ''
	if request.method == 'POST':
		inputName = request.form['name']
		selectedModel = request.form['model_select']
		selectedStatus = request.form['status_select']
		inputPrice = request.form['price']
		inputWarrantyMonths = request.form['warranty_months']
		inputOrderNumber= request.form['order_number']
		inputNote = request.form['notes']
		modelIndex = int(selectedModel.partition(".")[0])-1
		statusIndex = int(selectedStatus.partition(".")[0])-1
		model = snipeModelsArr[modelIndex]['model_id']
		status = snipeStatusArr[statusIndex]['status_id']
		if inputName == '':
			render_template('atributes.html')
			flash('Ingrese nombre de los equipos')
		elif selectedModel == 'Seleccione modelo':
			flash('Seleccione un modelo')
		elif selectedStatus == 'Seleccione estado':
			flash('Seleccione un estado')
		elif selectedStatus == 'Seleccione estado':
			flash('Seleccione un estado')
		try:
			warrantyMonths = float(inputWarrantyMonths)
		except ValueError:
			flash('El campo ''Precio'' solo recibe valores numericos')
			flag = 'err'
		try:
			orderNumber = float(inputOrderNumber)
		except ValueError:
			flash('El campo ''Precio'' solo recibe valores numericos')
			flag = 'err'
		try:
			price = float(inputPrice)
		except ValueError:
			flash('El campo ''Precio'' solo recibe valores numericos')
			flag = 'err'
		if flag != 'err':
			assetsDescription = Asset_description(inputName, status, model, inputNote, price, warrantyMonths, orderNumber)
			createassets(assetsArr, assetsDescription.to_dict())
			for asset in assetsArr[:]:
				assetsArr.remove(asset)

	flash('Agregado a Snipe con exito')
	return redirect(url_for('Index'))


if __name__ == '__main__':
	app.run(port = 3000, debug = True)