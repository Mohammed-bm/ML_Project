from flask import Flask, request, jsonify
import util

app = Flask(__name__)


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    if request.method == 'POST':
        try:
            total_sqft = float(request.form['total_sqft'])
            location = request.form['location']
            bhk = int(request.form['bhk'])
            bath = int(request.form['bath'])

            print(f"Received data: total_sqft = {total_sqft}, location={location}, bhk={bhk}, bath={bath}")

            estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

            response = jsonify({
                'estimated_price': estimated_price
            })
            response.headers.add('Access-Control-Allow-Origin', '*')

            return response

        except Exception as e:
            print(f"Error in prediction route: {e}")
            return jsonify({'error': 'Invalid input data'}), 400
    else:
        return jsonify({'error': 'Only POST requests are supported for this endpoint'}), 405


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run()
