import mysql.connector
import numpy as np
import sys


class Mutant:
    def __init__(self, dna_chain):
        self.dna_chain = dna_chain

    @staticmethod
    def get_dna(dna_chain):
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'mysql',
            'port': '3306',
            'database': 'db_dna'
        }
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(buffered=True, dictionary=True)
        query = 'SELECT * FROM dna_data WHERE dna="' + dna_chain + '"'
        result = cursor.execute(query)
        if cursor.rowcount == 1:
            records = cursor.fetchall()
            cursor.close()
            connection.close()
            return {'result': True, 'status': records[0]['dna_status']}
        else:
            cursor.close()
            connection.close()
            return {'result': False, 'status': 3}


    # Value to get the row or the given columns of the matrix data and check if is mutant or if not the diagonal is it.
    # Value that recive
    @staticmethod
    def get_row_and_columns_data(data, dna_matrix, type):
        i = 0
        # Iterate over the letter inside data variable, example of data: ['A' 'T' 'G' 'C' 'G' 'A']
        while len(data) > i:
            result = Mutant.check_mutant(data, i)
            if result:
                return True
            elif i == 2:
                break
            elif type == 'rows':
                result = Mutant.check_mutant_diagonal(i, dna_matrix)
            i = 1 + i
        return False

    @staticmethod
    # Function to create a matrix from a list
    def convert_list_to_matrix(dna_chain):
        new_matrix_dna = []
        for dna in dna_chain:
            single_dna = []
            for letter in dna:
                new_letter = letter
                single_dna.append(new_letter)
            new_matrix_dna.append(single_dna)
        return new_matrix_dna

    @staticmethod
    # Function to check if the chain is mutant or not
    def check_mutant(chain, i):
        if np.all(chain[i:4 + i] == chain[i]):
            return True
        else:
            return False

    def create_dna_chain(self):
        dna = self.dna_chain
        dna_matrix = Mutant.convert_list_to_matrix(dna)
        dna_numpy_matrix = np.asarray(dna_matrix)
        result = Mutant.check_mutant_rows(dna_numpy_matrix)
        if result:
            return True
        else:
            result = Mutant.check_mutant_columns(dna_numpy_matrix)
            if result:
                return True
        return False

    # Funcion que itera por la matriz via a la fila
    @staticmethod
    def check_mutant_rows(dna_matrix):
        i = 0
        while 6 > i:
            result = Mutant.get_row_and_columns_data(dna_matrix[i], dna_matrix[i:, :], 'rows')
            if result:
                return True
                break
            i = 1 + i
        return False

    # Funcion que itera por la matriz a traves de las columnas de la misma
    @staticmethod
    def check_mutant_columns(dna_matrix):
        i = 0
        while 6 > i:
            result = Mutant.get_row_and_columns_data(dna_matrix[:, i], dna_matrix[i:, :], 'columns')
            if result:
                return True
                break
            i = 1 + i
        return False

    # Funcion que toma la matriz y saca la diagonal a partir de la posicion de la misma
    @staticmethod
    def check_mutant_diagonal(i, dna_matrix):
        diagonal = dna_matrix.diagonal(i)
        if len(diagonal) > 3:
            result = Mutant.check_mutant(diagonal, i)
            if result:
                return True
        return False

    # Function to validate that all the chain have all the characters and the exact length
    def validate_adn_chain(self):
        dna_join = ''.join(self.dna_chain)
        list_dna = list(dna_join)
        result = Mutant.validate_lenght(list_dna)
        if result:
            result = Mutant.validate_letters(list_dna)
            if result:
                return True
        return False

    @staticmethod
    def validate_lenght(list_dna):
        try:
            if len(list_dna) % 6 == 0:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def validate_letters(list_dna):
        dna_ch = ('A', 'C', 'G', 'T')
        try:
            for ch in list_dna:
                if ch not in dna_ch:
                    return False
                    break
            else:
                return True
        except Exception as e:
            print(e)
            return False


    #Llama a la consulta de la BD para ver si existe o no el ADN
    def validate_exist_dna(self):
        dna_join = ''.join(self.dna_chain)
        result = Mutant.get_dna(dna_join)
        # devuelve si existe y en tal caso si es mutante o no
        if result['result']:
            return result
        else:
            return result

    def save_dna(self, dna_status):
        dna_join = ''.join(self.dna_chain)
        config = {
                'user': 'root',
                'password': 'root',
                'host': 'mysql',
                'port': '3306',
                'database': 'db_dna'
            }
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(buffered=True, dictionary=True)
        query = "INSERT INTO db_dna.dna_data( dna, dna_status, created_at) VALUES ('" + dna_join + "','" + str(dna_status) + "', now())"
        result = cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        return True

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
            cursor.close()
            connection.close()
            return {'result': True, 'dna_status_human': records[0]['dna_status_human'], 'dna_status_mutant': records[0]['dna_status_mutant']}
        else:
            cursor.close()
            connection.close()
            return {'result': False, 'status': 3}
