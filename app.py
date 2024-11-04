from flask import Flask, request, jsonify, render_template_string
from geopy.distance import geodesic

app = Flask(__name__)

# Predefined primary location (latitude, longitude)
primary_location = (12.9692,  79.1559)  # Example: New York (latitude, longitude)
threshold_distance = 1.0  # 1 km safe radius

# HTML content for the home page
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blind Assistance Safety Checker</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            text-align: center;
            padding-top: 50px;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        .image-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .image-container img {
            width: 150px;
            height: auto;
            border-radius: 50%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .btn-check-location {
            margin-top: 20px;
            padding: 10px 20px;
            font-size: 18px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .btn-check-location:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 20px;
            font-size: 22px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="image-container">
            <!-- Small image of a blind person -->
            <img src="https://www.google.com/imgres?q=blind%20help%20photos&imgurl=https%3A%2F%2Fmedia.istockphoto.com%2Fid%2F1179580864%2Fphoto%2Fyoung-man-and-blind-senior-with-white-cane-walking-in-city-crossing-street.jpg%3Fs%3D612x612%26w%3D0%26k%3D20%26c%3D_vyts5wPAqIyWnb2Hm8C5FsAFekvb-7GelbQTyXipaQ%3D&imgrefurl=https%3A%2F%2Fwww.istockphoto.com%2Fphotos%2Fhelping-blind-person&docid=M6J3DgEMQFME8M&tbnid=kPLBMbZs8UIX7M&vet=12ahUKEwjUv4XUptSIAxWDzjgGHWKzAQcQM3oECBgQAA..i&w=612&h=408&hcb=2&ved=2ahUKEwjUv4XUptSIAxWDzjgGHWKzAQcQM3oECBgQAA" alt="Blind person">
        </div>
        <h1>Blind Assistance Safety Checker</h1>
        <p>Check if the person is in a safe location.</p>

        <button class="btn-check-location" onclick="checkLocation()">Check if Safe</button>

        <div class="result" id="result"></div>
    </div>

    <!-- Bootstrap JS and Popper.js -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>

    <script>
        function checkLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    fetch('/check_location', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            latitude: latitude,
                            longitude: longitude
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        const resultDiv = document.getElementById('result');
                        if (data.is_safe) {
                            resultDiv.textContent = `Safe! Distance from primary location: ${data.distance} km.`;
                            resultDiv.style.color = 'green';
                        } else {
                            resultDiv.textContent = `Not Safe! Distance from primary location: ${data.distance} km.`;
                            resultDiv.style.color = 'red';
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                });
            } else {
                alert('Geolocation is not supported by this browser.');
            }
        }
    </script>
</body>
</html>

'''

@app.route('/')
def home():
    return render_template_string(html_content)

@app.route('/check_location', methods=['POST'])
def check_location():
    data = request.json
    current_location = (data['latitude'], data['longitude'])
    
    # Calculate distance
    distance = geodesic(primary_location, current_location).kilometers
    
    # Check if within the safe range
    is_safe = distance <= threshold_distance
    
    return jsonify({
        'is_safe': is_safe,
        'distance': round(distance, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
