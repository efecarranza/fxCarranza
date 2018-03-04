import psycopg2

class DBConnection(object):
    def connect(self, query):
        try:
            print('Connecting to the PostgreSQL database...')

            conn = psycopg2.connect(host="localhost",database="fxcarranza",
                user="efecarranza", password="efecarranza")
            cur = conn.cursor()

            cur.execute(query)

            data = cur.fetchall()

            cur.close()

            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def get_historical_prices(self, table, number_of_records):
        query = "SELECT Date, Close FROM %s LIMIT %s") % (table, number_of_records)
        return self.connect(query)

if __name__ == '__main__':
    DBConnection.connect()
