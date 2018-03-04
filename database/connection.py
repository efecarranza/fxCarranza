import psycopg2

def connect():
    print('Connecting to the PostgreSQL database...')


    conn = psycopg2.connect(host="localhost",database="fxcarranza", user="efecarranza", password="efecarranza")
    print conn

if __name__ == '__main__':
    connect()
