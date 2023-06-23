import export as export
from flask import Flask
from markupsafe import escape
import requests
from flask import request
from flask import render_template
import replicate
import os

os.environ["REPLICATE_API_TOKEN"] = "r8_cQHFmdoMCalpve4zRiM1elEEV6z9mlB4RnEa4"

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


#@app.route("/<name>")
#def hello(name):
#    return f"Hello, {escape(name)}"


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'


@app.route('/square/<int:number>')
def square_number(number):
    number *= number
    return f'number squared is {escape(str(number))}'

@app.route('/duck')
def duck():
    duck = requests.get('https://random-d.uk/api/v2/random')
    duckData = duck.json()
    #print(duckData)
    duckUrl = duckData['url']
    print(duckUrl)
    imgUrl = '<img src=' + duckUrl + '>'
    return imgUrl

@app.route('/rubber-duck')
def rubberDuck():

    output = replicate.run(
        "publu/rubberducky:8ab090227b436ce29a48230c167c81dc7b3022b35d0930121b210dbca5a614a0",
        input={"prompt": "a photo of a rubber duck ducky"}
    )
    print(output)
    imgUrl = '<img src=' + output[0] + '>'
    return imgUrl

# @app.get('/rubber-duck/<path:subpath>')
# def rubberDuckgenerator(subpath):
#
#     output = replicate.run(
#         "publu/rubberducky:8ab090227b436ce29a48230c167c81dc7b3022b35d0930121b210dbca5a614a0",
#         input={"prompt": f'{escape(subpath)}'}
#     )
#     print(output)
#     imgUrl = output[0]
#     print(imgUrl)
#     return render_template('duckGenerator.html', imgUrl=output[0])
#     #return imgUrl

@app.route('/rubber-duck/prompt', methods=['POST', 'GET'])
def rubberDuckgeneratorPost():


    if request.method == "POST":
        prompt = request.form['prompt']
        print(prompt)
        output = replicate.run(
            "publu/rubberducky:8ab090227b436ce29a48230c167c81dc7b3022b35d0930121b210dbca5a614a0",
            input={"prompt": f'{escape(prompt)}'}
        )

        print(output)
        imgUrl = output[0]
        print(imgUrl)
        return render_template('duckGenerator.html', imgUrl=output[0])
    else:
        return render_template('duckGeneratorGET.html', imgUrl='http://www.duckcreekboatclubandrentals.com/images/General/coolduk_down.jpg')

    #return imgUrl