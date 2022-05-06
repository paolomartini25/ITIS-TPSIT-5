import flask 
import sqlite3

serverweb = flask.Flask(__name__)

def getOperation(id):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    print(id)

    data = cur.execute(f""" SELECT id, operation 
                            FROM operazioni 
                            WHERE id_client ='{id}' and 
                            operazioni.id NOT IN (SELECT id_op FROM risultati)
                            """).fetchall()
    con.close()
    return data

def setResult(ris, idOp):
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    cur.execute(f"INSERT INTO risultati VALUES (?, ?, ?)", (None, ris, idOp))
    con.commit()
    con.close()

@serverweb.route("/operation", methods = ["GET"])
def operation():
    result = {"err" : 0}
    if flask.request.method == "GET":
        id = flask.request.args.get("id")
        data = getOperation(id)
        print(data)
    result['data'] = data
    return flask.jsonify(result)

@serverweb.route("/response", methods = ["GET"])
def response():
    result = {"err" : 0}
    if flask.request.method == "GET":
        ris = flask.request.args.get("ris")
        idOp = flask.request.args.get("idOp")
        print(f"{ris}::{idOp}")
        result["risultatoOp"] = ris
        setResult(ris, idOp)

    return flask.jsonify(result)

serverweb.run(debug=True, host="localhost")        
