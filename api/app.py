from flask import Flask, request, jsonify, render_template
from mutant import Mutant
from stats import Stats
import sys
import json
import os


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return """<h1>Distant Reading Archive</h1>
    <p>A prototype API for distant reading of science fiction novels</p>
    """


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/stats/", methods=['GET'])
def stats_mutant():
    stats_classes = Stats()
    #verificaciones de ADN: {“count_mutant_dna”:40, “count_human_dna”:100: “ratio”:0.4}
    result = stats_classes.return_dna_list()

    if result['result']:
        dna_status_human = int(result['dna_status_human'])
        dna_status_mutant = int(result['dna_status_mutant'])
        ratio = round(float(dna_status_mutant/dna_status_human), 2)

        dict_response = {"count_mutant_dna": dna_status_mutant, "count_human_dna": dna_status_human, "ratio": ratio}
        response = app.response_class(
            status=200,
            mimetype='application/json',
            response=json.dumps(dict_response)
        )
        return response
    else:
        response = app.response_class(
            status=403,
            mimetype='application/json',
            response=json.dumps(False)
        )
        return response


@app.route("/mutant/", methods=['POST'])
def api_mutant():
    try:
        content = request.get_json()
        print(content, file=sys.stderr)
        adn = content.get('dna')
        mutant_classes = Mutant(adn)
    except Exception as e:
        print(e)
        result = False
        response = json.dumps({'error': result}), 400, {'ContentType': 'application/json'}
        return response
    # Function que valida que la cadena de ADN tenga la longitud y las letras correctas: devuelve True cuando tiene
    # el formato correcto y False cuando no
    result = mutant_classes.validate_adn_chain()
    if result:
        # funcion para validar si la en la BD ya tenemos dicha cadena de ADN salvada
        result = mutant_classes.validate_exist_dna()
        #Si es verdadera devolvemos el estatus, sino lo creamos
        if result['status'] == 0:
            response = app.response_class(
                status=403,
                mimetype='application/json',
                response=json.dumps(False)
            )
            return response

        elif result['status'] == 1:
            response = app.response_class(
                status=200,
                mimetype='application/json',
                response=json.dumps(True)
            )
            return response
        else:
            result = mutant_classes.create_dna_chain()
            if result:
                mutant_classes.save_dna(dna_status=1)
                response = app.response_class(
                    status=200,
                    mimetype='application/json',
                    response=json.dumps(True)
                )
                return response
            else:
                mutant_classes.save_dna(dna_status=0)
                response = app.response_class(
                    status=403,
                    mimetype='application/json',
                    response=json.dumps(False)
                )
                return response
    else:
        response = json.dumps({'error': result}), 403, {'ContentType': 'application/json'}

    return response


if __name__ == '__main__':
    if os.environ.get('PORT') is not None:
        app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT'))
    else:
        app.run(debug=True, host='0.0.0.0') 

