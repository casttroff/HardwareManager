import json, requests, copy
from flask import flash
from Models import Get_payload_to_create, Get_payload_to_modify, Asset_id

def get_asset_id(serial_number):
        url = "https://mercadoenvio.snipe-it.io/api/v1/hardware/bytag/" + str(serial_number)
        headers = {
            'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjQ1ZDZmODVmN2U5Y2U4YmVkZTIzNTU4MTQ5ZWI4ZmUwODg3NTczZWEzMmZiZjFiMWUxMWRhMzdiNjE5NDdkNzM5YzIwMTBiZDlkMWU2NTM3In0.eyJhdWQiOiIxIiwianRpIjoiNDVkNmY4NWY3ZTljZThiZWRlMjM1NTgxNDllYjhmZTA4ODc1NzNlYTMyZmJmMWIxZTExZGEzN2I2MTk0N2Q3MzljMjAxMGJkOWQxZTY1MzciLCJpYXQiOjE1ODkyNzMyODAsIm5iZiI6MTU4OTI3MzI4MCwiZXhwIjoxNjIwODA5MjgwLCJzdWIiOiIyIiwic2NvcGVzIjpbXX0.KqL6QfN6olnzFVE3QnCerkQWX6KFzdMxiJS2VmWcoPjovdVPorfluQ5gkWvDSCUL4VINk8O7eXdwv4w4ORa91AfI4Yx61NvPpvUfiDYKOUo9o4GhOmHv59qus1cFZ_nR9HYz0xZ6GTltYEQs0DgFGFfz63kTy8-CspIUWH-sZtPr8s8vleq1TvAm-OxlStSOCUWb1LK4aubLkZbPeO_1xkcU10KdT1gz3gr8lx8ANScG2DQ3N8TjtT2-LK210ePtvEGsNoq-vC2yRYEJmeFlxQ_Ou4O1azfZcuk_2oc0rwMbCf62cpTT3d8yOBb6AEubyTxpdyDpKmqhww5AOhEqkoXZo7aIijnvVr403BlDLlfxPPHZ7zUgliUbEXCjUtRSBcVSby5YaTbWhnSLJDuimafR2FUW8L9ySzfUXjjE9OKGrUIxFx0-mDUvPu__Vi_oLOErVTZ7gn0KQT4gqCzbMtUz7QUpq7mh0tWSboX4-81xn1Cyvk1xkS65oKtpULpv56jw8DIXHokCUIQEP5W-2v6q-vWABMl_04GfC4UEJfcWeLZHV2n7pGXBS-hKulG-jL-vLZ9Mk0-V5PWJ8fNwlDnaiC14M6Ok7oUPbkgYC8G0w5CSVVvfrDevXW8SbvOcEyLoFDsIbUQfmmGqgfqrz4OrsYT3u5QJ-EOc9t-WO-o",
            'accept': "application/json",
            'content-type': "application/json"
            }
        response = requests.request("GET", url, headers=headers)
        data = response.json()
        try:
            if data['status'] == "error":
                flash('No se encontró el asset')
        except KeyError: 
            #Si no existe data['status'] (KeyError) entonces encontró el id
            return (data['id'])


def createassets(assets_sn, assets_desc):
    assets_id_arr = []; data_arr = []
    url = "https://mercadoenvio.snipe-it.io/api/v1/hardware"
    headers = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjQ1ZDZmODVmN2U5Y2U4YmVkZTIzNTU4MTQ5ZWI4ZmUwODg3NTczZWEzMmZiZjFiMWUxMWRhMzdiNjE5NDdkNzM5YzIwMTBiZDlkMWU2NTM3In0.eyJhdWQiOiIxIiwianRpIjoiNDVkNmY4NWY3ZTljZThiZWRlMjM1NTgxNDllYjhmZTA4ODc1NzNlYTMyZmJmMWIxZTExZGEzN2I2MTk0N2Q3MzljMjAxMGJkOWQxZTY1MzciLCJpYXQiOjE1ODkyNzMyODAsIm5iZiI6MTU4OTI3MzI4MCwiZXhwIjoxNjIwODA5MjgwLCJzdWIiOiIyIiwic2NvcGVzIjpbXX0.KqL6QfN6olnzFVE3QnCerkQWX6KFzdMxiJS2VmWcoPjovdVPorfluQ5gkWvDSCUL4VINk8O7eXdwv4w4ORa91AfI4Yx61NvPpvUfiDYKOUo9o4GhOmHv59qus1cFZ_nR9HYz0xZ6GTltYEQs0DgFGFfz63kTy8-CspIUWH-sZtPr8s8vleq1TvAm-OxlStSOCUWb1LK4aubLkZbPeO_1xkcU10KdT1gz3gr8lx8ANScG2DQ3N8TjtT2-LK210ePtvEGsNoq-vC2yRYEJmeFlxQ_Ou4O1azfZcuk_2oc0rwMbCf62cpTT3d8yOBb6AEubyTxpdyDpKmqhww5AOhEqkoXZo7aIijnvVr403BlDLlfxPPHZ7zUgliUbEXCjUtRSBcVSby5YaTbWhnSLJDuimafR2FUW8L9ySzfUXjjE9OKGrUIxFx0-mDUvPu__Vi_oLOErVTZ7gn0KQT4gqCzbMtUz7QUpq7mh0tWSboX4-81xn1Cyvk1xkS65oKtpULpv56jw8DIXHokCUIQEP5W-2v6q-vWABMl_04GfC4UEJfcWeLZHV2n7pGXBS-hKulG-jL-vLZ9Mk0-V5PWJ8fNwlDnaiC14M6Ok7oUPbkgYC8G0w5CSVVvfrDevXW8SbvOcEyLoFDsIbUQfmmGqgfqrz4OrsYT3u5QJ-EOc9t-WO-o",
        "Content-Type": "application/json"
    }

    for asset in assets_sn:
        payload = Get_payload_to_create(asset['serial_number'], assets_desc['selectedStatus'], assets_desc['selectedModel'] , assets_desc['name'], asset['serial_number'])
        response = requests.request("POST", url, json=payload.to_dict(), headers=headers)
        data = response.json()
        print(data)
        if data['status'] == "error":
            asset_id = Asset_id(asset['serial_number'], asset['serial_number'], get_asset_id(asset['serial_number']), asset['mac_address'],'dup')
        else:
            asset_id = Asset_id(asset['serial_number'], asset['serial_number'], get_asset_id(asset['serial_number']), asset['mac_address'],'no_dup')
        assets_id_arr.append(copy.copy(asset_id.to_dict()))

    for asset in assets_id_arr:
        url_modify_asset = "https://mercadoenvio.snipe-it.io/api/v1/hardware/" + str(asset['id'])
        payload = Get_payload_to_modify(asset['serial_number'], assets_desc['notes'], assets_desc['selectedStatus'], assets_desc['selectedModel'], assets_desc['warrantyMonths'], assets_desc['price'], assets_desc['orderNumber'], assets_desc['name'], asset['mac_address'], 1)
        response = requests.request("PUT", url_modify_asset, json=payload.to_dict(), headers=headers)
        print(payload.to_dict())
        data = response.json()
        print(data)
        data_arr.append(copy.copy(data))
