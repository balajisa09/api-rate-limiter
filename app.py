from flask import Flask, jsonify, request
from datetime import datetime, timedelta

app = Flask(__name__)

# Configure the rate limit (in requests per second)
RATE_LIMIT = 2
WINDOW_SIZE = 60  # In seconds

# Dictionaries to store the request count and last request time for each IP address
request_count = {}
last_request_time = {}


@app.route('/api')
def api():
    ip_address = request.remote_addr

    # Check if the IP address has exceeded the rate limit
    if ip_address in request_count and ip_address in last_request_time:
        requests = request_count[ip_address]
        last_time = last_request_time[ip_address]
        elapsed_time = (datetime.now() - last_time).total_seconds()

        if elapsed_time < WINDOW_SIZE:
            if requests >= RATE_LIMIT:
                return jsonify({'error': 'Rate limit exceeded.'}), 429

            request_count[ip_address] += 1

        else:
            request_count[ip_address] = 1
            last_request_time[ip_address] = datetime.now()

    else:
        request_count[ip_address] = 1
        last_request_time[ip_address] = datetime.now()

    # Do the API work here...
    return jsonify({'success': 'API response.'}), 200


if __name__ == '__main__':
    app.run(debug=True)
