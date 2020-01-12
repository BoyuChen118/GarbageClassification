import os
import pickle
from flask import Flask, render_template, request,send_file,redirect,flash,url_for
from werkzeug.utils import secure_filename
import numpy as np
from keras.preprocessing import image

# UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app = Flask(__name__)

# @app.route("/")
# def hello():
#     return render_template('index.html')

# @app.route('/', methods=['POST'])
# def getfile():
#     input = request.files['input']
#     filename = docs.save(request.files['input'])
#     return filename
#     # return render_template('pass.html', output=input)
    





# if __name__ == '__main__':
#     app.run(debug=True)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
             filename = secure_filename(file.filename)
             with open('grayscaletrash_classifier', 'rb') as f:
                    mode = pickle.load(f)
             
             img = image.load_img(file,grayscale=True, target_size = (128,128))
             img = image.img_to_array(img)
             img = np.expand_dims(img,axis=0)
             prediction = mode.predict(img)
             
             if(prediction[0,0]==1):
                print('cardboard')
                
                return render_template('pass.html',output='cardboard')
             elif(prediction[0,1]==1):
                print('glass')
                return render_template('pass.html',output='plastic/glass')
             elif(prediction[0,2]==1):
                print('metal')
                return render_template('pass.html',output='metal')
             elif(prediction[0,3]==1):
                print('plastic')
               
                return render_template('pass.html',output='plastic/glass')
             else:
                print('trash')
                return render_template('pass.html',output='trash')
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
             
    return render_template('main.html')
    
