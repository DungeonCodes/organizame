from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Flask está rodando com sucesso no Railway!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Railway define a porta pela variável PORT
    app.run(host='0.0.0.0', port=port, debug=True)
