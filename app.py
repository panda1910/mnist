import os
from flask import Flask, request, redirect, url_for, render_template, jsonify
import base64
###
from tensorflow.keras.models import load_model
import numpy as np
from skimage import data, color, io
from skimage.transform import rescale, resize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
###

UPLOAD_FOLDER = f'{os.getcwd()}/static/upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    return render_template("index.html")


nseed = 10
tot_items = len(os.listdir(UPLOAD_FOLDER))


@app.route('/data', methods=['POST'])
def create_entry():
    global nseed, tot_items
    # POST request
    tot_items = len(os.listdir(UPLOAD_FOLDER))
    print("tot_items: ", tot_items)
    if tot_items >= 5:
        tot_items = 0
        items_inside = os.listdir(UPLOAD_FOLDER)
        for ele in items_inside:
            os.remove(UPLOAD_FOLDER + "/" + ele)
    if request.method == 'POST':
        # print('Incoming..')
        req = request.get_json(force=True)
        # print(req)  # parse as JSON

        s = base64.decodebytes(req['data'].encode('utf-8'))
        with open("uploads/image.png", "wb") as w:
            w.write(s)

        #####
        ret_val = str("NOPE")

        image = io.imread('uploads/image.png')
        image = color.rgb2gray(image)
        image_resized = resize(image, (28, 28, 1))

        final = 1 - np.array(image_resized)

        final = np.expand_dims(final, axis=0)
        print(final.shape)

        model = load_model("models/mnist_trained_99.h5")
        answer = model.predict(final)

        ret_val = answer.argmax()
        print(ret_val)
        ll = []
        name = "x"
        try:
            name = str(nseed)+ ".png"
            nseed+=1
            ll = [round(x*100, 2) for x in answer[0]]
            savePlot(ll, name)
            print(ll)
            conf = ll[ret_val]
            print("Conf: ", conf)
        except:
            print("ERROR")

        #####
        # return str(ret_val)
        p = {"number": str(ret_val), "predictions": ll, "link": name}
        return jsonify(p)
    else:
        message = {'message':'Had some error'}
        return jsonify(message)


def savePlot(ll, name):
    fig, ax = plt.subplots(nrows=1, ncols=1)  # create figure & 1 axis
    ax.bar([str(x) for x in range(10)], ll, color="#ff660d")
    plt.xlabel('Digits')
    plt.ylabel('Confidence in %')
    plt.title('Confidence Plot for the prediction')
    fig.patch.set_facecolor((240/255, 240/255, 240/255))
    ax.set_facecolor((240/255, 240/255, 240/255))
    xlocs = [i for i in range(10)]
    plt.ylim(0, 109)
    for i, v in enumerate(ll):
        if int(v) != 0:
            plt.text(xlocs[i]-0.20, v + 0.3, str(v)+"%")
    fig.savefig(f'static/upload/{name}')  # save the figure to file
    plt.close(fig)


if __name__ == '__main__':
    app.run(debug=True)
