import mysql.connector
import sys

class Stats():

    def return_dna_list(self):
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'mysql',
            'port': '3306',
            'database': 'db_dna'
        }
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(buffered=True, dictionary=True)
        query = 'SELECT SUM(dna_status = 1) AS dna_status_mutant, SUM(dna_status = 0) AS dna_status_human ' \
                'FROM db_dna.dna_data WHERE dna_status = 0 OR dna_status = 1'
        result = cursor.execute(query)
        if cursor.rowcount == 1:
            records = cursor.fetchall()
            if records[0]['dna_status_human'] is None:
                cursor.close()
                connection.close()
                return {'result': False, 'dna_status_human': 0, 'dna_status_mutant': 0}
            else:
                cursor.close()
                connection.close()
                return {'result': True, 'dna_status_human': records[0]['dna_status_human'], 'dna_status_mutant': records[0]['dna_status_mutant']}
        else:
            cursor.close()
            connection.close()
            return {'result': False, 'dna_status_human': 0, 'dna_status_mutant': 0}

