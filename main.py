import mysql.connector
import json
from mysql.connector import Error
from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
app = Flask(__name__)

app.config['CORS_ALLOW_HEADERS'] = '*'
app.config['CORS_ALLOW_ORIGIN'] = 'content-type,*'
app.config['CORS_EXPOSE_HEADERS'] = '*'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app,  supports_credentials=True)

def getConn():
    return mysql.connector.connect(user='root', password='Lab2dev@2022', host='localhost',database='danteboard')

class create_dict(dict): 
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value

def getTipoNota():
    try:
        connection = getConn()
        if connection.is_connected():
            select_employee = """SELECT * FROM tipo_nota"""
            cursor = connection.cursor()
            cursor.execute(select_employee)
            row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            json_data=[]
            for result in rv:
                    json_data.append(dict(zip(row_headers,result)))
            return json.dumps(json_data)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def getDashboard():
    try:
        connection = getConn()
        if connection.is_connected():
            select_dashboard = """SELECT 
                                colaborador.nome as nome, 
                                colaborador.email as email, 
                                count(nota.nota) as notas, 
                                count(notapos.nota) as notaspos, 
                                count(notaneg.nota) as notasneg, 
                                ifnull(DATE_FORMAT((select data from nota where colaborador = colaborador.email  order by data desc limit 1),'%d %b %y %h:%i'),'') as ultimanota,
                                CASE WHEN DATE((select data from nota where colaborador = colaborador.email  order by data desc limit 1) + INTERVAL 15 DAY) > NOW()
                                THEN
                                    'ATUALIZADO'
                                ELSE
                                    'ATRASADO'
                                END as status
                            FROM colaborador
                            LEFT JOIN nota
                            on nota.colaborador = colaborador.email
                            LEFT JOIN nota as notapos
                            on notapos.colaborador = colaborador.email
                            and notapos.tipo = '2'
                            LEFT JOIN nota as notaneg
                            on notaneg.colaborador = colaborador.email
                            and notaneg.tipo = '1'
                            group by colaborador.nome, colaborador.email"""
            cursor = connection.cursor()
            cursor.execute(select_dashboard)
            row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            json_data=[]
            for result in rv:
                    json_data.append(dict(zip(row_headers,result)))
            return json.dumps(json_data , indent=4, sort_keys=True, default=str)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def getColaborador():
    try:
        connection = getConn()
        if connection.is_connected():
            select_employee = """SELECT * FROM colaborador"""
            cursor = connection.cursor()
            cursor.execute(select_employee)
            row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            json_data=[]
            for result in rv:
                    json_data.append(dict(zip(row_headers,result)))
            return json.dumps(json_data)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def getNota(colab=False):
    try:
        connection = getConn()
        if connection.is_connected():
            select_employee = """SELECT * FROM nota """
            if colab != False:
                select_employee += f""" WHERE colaborador = '{colab}'"""
            select_employee += """ORDER BY data DESC """
            cursor = connection.cursor()
            cursor.execute(select_employee)
            row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            json_data=[]
            for result in rv:
                    json_data.append(dict(zip(row_headers,result)))
            return json.dumps(json_data, indent=4, sort_keys=True, default=str)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def getLogin(email, pasw):
    try:
        connection = getConn()
        if connection.is_connected():
            select_login = f"""SELECT * FROM login 
               WHERE email = '{email}' and senha = '{pasw}'"""
            cursor = connection.cursor()
            cursor.execute(select_login)
            row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            json_data=[]
            for result in rv:
                    json_data.append(dict(zip(row_headers,result)))
            return json.dumps(json_data, indent=4, sort_keys=True, default=str)
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def addNota(jObj):
    try:
        connection = getConn()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(
                """INSERT INTO `danteboard`.`nota`
                    (`data`,
                    `nota`,
                    `tipo`,
                    `colaborador`)
                    VALUES
                    (NOW(),
                    %s,
                    %s,
                    %s);""", (jObj['nota'], jObj['tipo'], jObj['colaborador']))
            connection.commit()
            return str(cursor.rowcount) + " record inserted."
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

@app.route('/api/get/colaboradores', methods=['GET'])
def apiGetColaboradores():
    try:
        content = getColaborador()
        print(content)
        return  Response(content,status=200, mimetype="application/json")
    except Exception as e:
       return(str(e))

@app.route('/api/get/tipo_nota', methods=['GET'])
def apiGetTipoNota():
    try:
        content = getTipoNota()
        print(content)
        return  Response(content,status=200, mimetype="application/json")
    except Exception as e:
       return(str(e))

@app.route('/api/get/nota', methods=['GET'])
def apiGetNota():
    try:
        colab = False 
        if request.args.get('$colaborador'):
            colab = request.args.get('$colaborador')
        content = getNota(colab)
        print(content)
        return  Response(content,status=200, mimetype="application/json")
    except Exception as e:
       return(str(e))

@app.route('/api/get/login', methods=['GET'])
def apiGetLogin():
    try:
        user,pasw = False, False
        if request.args.get('$email') and request.args.get('$pasw'):
            user = request.args.get('$email')
            pasw = request.args.get('$pasw')
            content = getLogin(user,pasw)
            print(content)
            return  Response(content,status=200, mimetype="application/json")
        else: 
            return  Response("NAO AUTORIZADO",status=401, mimetype="application/json")
        
        
        
    except Exception as e:
       return(str(e))

@app.route('/api/add/nota/', methods=['POST','OPTIONS'])
def apiAddNota():
    try:
        jRequest = request.get_json()
        resp = Response(addNota(jRequest),status=200, mimetype="application/json")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except Exception as e:
       return(str(e))

@app.route('/api/get/dashboard', methods=['GET'])
@cross_origin()
def apiGetDashboard():
    try:
        content = getDashboard()
        print(content)
        return  Response(content,status=200, mimetype="application/json")
    except Exception as e:
       return(str(e))


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=9090, debug=True)
