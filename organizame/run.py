from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Pega a porta definida pelo Railway
    app.run(host='0.0.0.0', port=port, debug=True)  # Expõe para o exterior
