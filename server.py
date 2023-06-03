from flask import Flask, request, render_template
from black import gameboard

app = Flask(__name__)
flag = False

@app.route("/", methods=['GET', 'POST'])
def home():
    global game, flag
    if request.method == 'GET':
        game = gameboard()
        print('initialize............')
        print(game.avaliable)
        return render_template("page.html")
    if request.method == 'POST':
        user = request.get_json()
        print(user)
        position = [int(user['buttonId'].split('-')[1]), 
                    int(user['buttonId'].split('-')[2]) ]
        response = game.action(position=position)
        print(response)
        return response

if __name__ == "__main__":
    # app.debug = True
    app.run()