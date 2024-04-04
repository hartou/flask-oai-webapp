import requests
import json
import os
import ssl

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
app = Flask(__name__)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   question = request.form.get('name')
   if question:
       print('Question received with name=%s' % question)
       
       url = ''
       # Replace this with the primary/secondary key or AMLToken for the endpoint
       api_key = ''
       if not api_key:
           raise Exception("A key should be provided to invoke the endpoint")
       headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'gpt4turbo-openai-ffx-deployment' }

       response = requests.post(url, json={'question': question}, headers=headers)
       response_value = json.loads(response.content.decode('utf-8'))
       output = {}
       if response.status_code != 200:
           print('Error: {}'.format(response_value))
           output['txt'] = 'Error: {}'.format(response_value)
           output['question']=question
           return render_template('hello.html', name = output)
       if response.status_code == 200:
           if len(response_value[0])==0 or response_value[0]['code_info'] == None:
               output['txt'] = 'Error: {}'.format(response_value)
               output['question']=question
               return render_template('hello.html', name = output)
           
           if response_value[0]['code_info'] != None:
               response_item= response_value[0]
               output['test'] = question
               txt_res1 = str(response_item['code_info']['code_execute_result']['data']['columns'])
               txt_res2 = str(response_item['code_info']['code_execute_result']['data']['data'])
               # ToDo: use the utils 'module' to the parse the response
               output['txt'] = str(txt_res1 + ': ' + txt_res2).replace('[','').replace(']','').replace('\'','')
               
               output['sql'] = response_item['code_info']['code_block']['source']
               #content=response_item['content']
               #output['content'] = content.replace('<Cell>', '').replace('</Cell>', '').replace('>','')
               output['question']=question
       return render_template('hello.html', name = output)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
