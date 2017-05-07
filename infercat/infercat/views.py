from django.http import HttpResponse
from django.template import loader

import sys, os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir + '/../../script')

import pickle
from nbm import NBM

def index(request):
  try:
    url = request.POST['url']

    try:
      with open(script_dir + '/../../model/nbm.pkl', 'rb') as f:
        model_data = pickle.load(f)

      model = NBM(model_data, script_dir + '/../../dataset/')
      category = model.calc(url)  
    except:
      category = 'エラー'

    context = {'url': url, 'category': category}
  except:
    context = {'url': None}
  
  template = loader.get_template('index.html')
  return HttpResponse(template.render(context, request))