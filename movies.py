from flask import Flask, jsonify
import boto3
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# Connection for DynamoDB
client = boto3.client('dynamodb')
response = client.scan(
    TableName='app001Movies'
    )

entries = response["Items"]
list001 = {}

for entry in entries:
    list001[entry['uuid']['S']] = {'uuid': entry['uuid']['S'], 'title': entry['title']['S']}

@app.route('/', methods=['GET'])
def hello():
    return jsonify({
        "uri": "/",
        "subresource_uris": {
            "names": "/movies",
            "name": "/movies/<id>"
        }
    })

@app.route('/test911', methods=['GET'])
def yo():
    return jsonify({
        "uri": "/",
        "subresource_uris": {
            "names": "/testing002",
            "name": "/testing002/<id>"
        }
    })

@app.route('/movies', methods=['GET'])
def records():
    return jsonify(list001)

@app.route("/movies/<id>", methods=['GET'])
def name_info(id):
    if id not in list001:
        raise NotFound
        return "not found"
    result = list001[id]
    return jsonify(result)

#@app.route("/names/<title>", methods=['PUT'])
#def putrecord(title):


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
