from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

cars = [
    {
        'id': 1,
        'make': 'Ford',
        'model': 'Focus',
        'year': 2018,
        'fuel': 'gasoline',
        'price': 120
    },
    {
        'id': 2,
        'make': 'Volkswagen',
        'model': 'Golf',
        'year': 2017,
        'fuel': 'diesel',
        'price': 90
    },
    {
        'id': 3,
        'make': 'Audi',
        'model': 'A4',
        'year': 2018,
        'fuel': 'gasoline',
        'price': 100
    }
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/cars', methods=['GET', 'POST'])
def get_cars():
    if request.method == 'POST':
        add_car()
    return jsonify({'cars': cars})

@app.route('/cars/<int:id>', methods=['GET', 'DELETE', 'PUT'])
def get_car(id):
    car = [car for car in cars if car['id'] == id]
    if request.method == 'GET':
        if len(car) == 0:
            abort(404)
        return jsonify(car)
    elif request.method == 'DELETE':
        if len(car) == 0:
            abort(404)
        else:
            cars.remove(car[0])
            return jsonify({'car': 'Deleted'})
    elif request.method == 'PUT':
        update_car(id)
    else:
        return jsonify({'error': 'Method not allowed.'})

def add_car():
    if request.json:
        car = {
            'id': cars[-1]['id'] + 1,
            'make': request.json['make'],
            'model': request.json['model'],
            'fuel': request.json['fuel'],
            'year': request.json['year'],
            'price': request.json['price']
        }

        cars.append(car)
        return jsonify({'car': car}), 201
    else:
        abort(400)

def update_car(id):
    car = [car for car in cars if car['id'] == id]
    
    if len(car) == 0:
        abort(404)

    if not request.json:
        abort(404)

    if 'make' in request.json and type(request.json['make']) != str:
        abort(400)
    
    if 'model' in request.json and type(request.json['make']) != str:
        abort(400)

    if 'fuel' in request.json and type(request.json['make']) != str:
        abort(400)

    if 'price' in request.json and type(request.json['make']) != int:
        abort(400)

    if 'year' in request.json and type(request.json['make']) != int:
        abort(400)

    car[0]['make'] = request.json.get('make', car[0]['make'])
    car[0]['model'] = request.json.get('model', car[0]['model'])
    car[0]['fuel'] = request.json.get('fuel', car[0]['fuel'])
    car[0]['price'] = request.json.get('price', car[0]['price'])
    car[0]['year'] = request.json.get('year', car[0]['year'])

    return jsonify(car)

if __name__ == '__main__':
    app.run(debug=True)