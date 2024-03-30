# server.py

from flask import Flask, jsonify
import requests
import time
from collections import deque

app = Flask(__name__)

WINDOW_SIZE = 10
NUMBERS_ENDPOINTS = {
    'p': 'http://20.244.56.144/test/primes',
    'f': 'http://20.244.56.144/test/fibo',
    'e': 'http://20.244.56.144/test/even',
    'r': 'http://20.244.56.144/test/rand'
}

stored_numbers = deque()

def fetch_numbers(number_type):
    url = NUMBERS_ENDPOINTS[number_type]
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('numbers', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching numbers: {e}")
    return []

def calculate_average(numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

@app.route('/numbers/<number_type>')
def handle_number_request(number_type):
    global stored_numbers

    # Fetch numbers from third-party server
    numbers = fetch_numbers(number_type)

    # Filter out duplicates and maintain uniqueness
    new_numbers = list(set(numbers) - set(stored_numbers))
    
    # Ignore responses taking longer than 500 ms or encountering errors
    if len(new_numbers) == 0:
        return jsonify({"error": "No new numbers or error fetching numbers"})

    # Remove oldest numbers if exceeding window size
    while len(stored_numbers) + len(new_numbers) > WINDOW_SIZE:
        stored_numbers.popleft()

    # Add new numbers to stored numbers
    stored_numbers.extend(new_numbers)

    # Calculate average for the window
    if len(stored_numbers) >= WINDOW_SIZE:
        avg = calculate_average(list(stored_numbers)[-WINDOW_SIZE:])
    else:
        avg = calculate_average(list(stored_numbers))

    # Prepare response
    response = {
        "windowPrevState": list(stored_numbers)[-len(new_numbers) - WINDOW_SIZE : -len(new_numbers)],
        "windowCurrState": list(stored_numbers)[-len(new_numbers):],
        "numbers": new_numbers,
        "avg": avg
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=9876)
