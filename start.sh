gunicorn -c ./config/config_gunicorn.py -w1 app:app.app&

ngrok http 1234

pkill gunicorn
