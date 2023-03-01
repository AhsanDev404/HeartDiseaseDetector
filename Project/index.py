from django.http import HttpResponse
from django.shortcuts import render

import pickle
import numpy as np

knn_model = pickle.load(open('HDP/knn_trained_model.pkl', 'rb'))
dt_model = pickle.load(open('HDP/dt_trained_model.pkl', 'rb'))
cnb_model = pickle.load(open('HDP/cnb_trained_model.pkl', 'rb'))

def index(req):
    return render(req, 'index.html')
def model(req):
    gender = req.GET.get('gender','default')
    chestPain = req.GET.get('chestPain','default')
    bp = req.GET.get('bp','default')
    cholestrol = req.GET.get('cholestrol','default')
    bs = req.GET.get('bs','default')
    ecg = req.GET.get('ecg','default')
    hr = req.GET.get('hr','default')
    ea = req.GET.get('ea','default')
    oldpeak = req.GET.get('oldpeak','default')
    st = req.GET.get('st','default')
    vessel = req.GET.get('vessel','default')
    thalassemia = req.GET.get('thalassemia','default')
    
    final_inputs = [gender,chestPain, bp,cholestrol,bs,ecg,hr,ea,oldpeak,st,vessel,thalassemia]
    final_inputs=[int(float(items)) for items in final_inputs]
    final_inputs=[np.array(final_inputs)]
    prediction_dt = dt_model.predict(final_inputs)
    prediction_cnb = cnb_model.predict(final_inputs)
    prediction_knn = knn_model.predict(final_inputs)
    healthy = 0
    defected = 0
    if prediction_knn[0] == 1:
        knn = "Defective Heart"
        defected += 1
    if prediction_knn[0] == 0:
        knn = "Healthy Heart"
        healthy += 1
    if prediction_dt[0] == 1:
        dt = "Defective Heart"
        defected += 1
    if prediction_dt[0] == 0:
        dt = "Healthy Heart"
        healthy += 1
    if prediction_cnb[0] == 1:
        cnb = "Defective Heart"
        defected += 1
    if prediction_cnb[0] == 0:
        cnb = "Healthy Heart"
        healthy += 1
    if gender == '1':
        gender = "Male"
    if gender == '0':
        gender = "Female"

    if chestPain == '0':
        chestPain = 'ASY'
    if chestPain == '1':
        chestPain = 'ATA'
    if chestPain == '2':
        chestPain = 'NAP'
    if chestPain == '3':
        chestPain = 'TA'

    if bs == '1':
        bs = '> 120'
    if bs =='0':
        bs = 'other'

    if ecg == '0':
        ecg = 'LVH'
    if ecg == '1':
        ecg = 'Normal'
    if ecg == '2':
        ecg = 'ST'

    if ea == '0':
        ea = 'No'
    if ea == '1':
        ea = 'Yes'

    if st == '0':
        st = 'Down'
    if st == '1':
        st = 'Flat'
    if st == '2':
        st = 'Up'
    if thalassemia =='0':
        thalassemia = 'Normal'
    if thalassemia =='1':
        thalassemia = 'Fixed Defected'
    if thalassemia =='2':
        thalassemia = 'Reversible Defected'
    result = ''
    if healthy>defected:
        result = 'Healthy Heart'
    if defected>healthy:
        result = 'Defected Heart'
    
    context ={
    'gender': gender,
    'chestPain':chestPain, 
    'bp':bp, 
    'cholestrol': cholestrol,
    'bs': bs,
    'ecg': ecg,
    'hr': hr,
    'ea': ea,
    'oldpeak':oldpeak, 
    'st': st,
    'vessel': vessel,
    'thalassemia': thalassemia,
    'cnb':cnb,
    'dt':dt,
    'knn':knn,
    'result': result
    }
    return render(req, 'index.html',context)