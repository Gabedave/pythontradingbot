from iqoptionbot.starter import start

@wsgi.route('/')

app = start()

if __name__ == "__main__":
   app
   
