from cgitb import reset
from crypt import methods

from flask import Flask, request, jsonify
import json
import subprocess
import re
# from pyvelociraptor import

app = Flask(__name__)


def format_subprocess_output(output):
    """
    This function takes the raw output from the subprocess call, extracts the relevant JSON data,
    and returns a Python dictionary after fixing common formatting issues.
    """
    output_lines = output.split('\n')
    json_data = None

    # Extract the JSON-like part from the output
    for line in output_lines:
        if line.startswith('[{') or line.startswith('['):
            json_data = line
            break

    if json_data is not None:
        # Fix the JSON format (convert single quotes to double quotes, etc.)
        json_data = re.sub(r"'", '"', json_data)  # Replace single quotes with double quotes
        json_data = re.sub(r'None', 'null', json_data)  # Replace 'None' with 'null'
        json_data = re.sub(r'True', 'true', json_data)  # Replace 'True' with 'true'
        json_data = re.sub(r'False', 'false', json_data)  # Replace 'False' with 'false'

        # Convert to Python list of dictionaries
        try:
            return json.loads(json_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON: {str(e)}")
    else:
        # If there's no valid JSON data, return an empty list
        return []

@app.route('/api/info', methods=['GET'])
def get_client_info():
    try:
        command = ['pyvelociraptor', '--config', '../api.config.yaml', "SELECT * FROM info()"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            # Use the helper function to format the output
            clients_data = format_subprocess_output(result.stdout)

            # Return the JSON response
            return jsonify(clients_data)
    except Exception as e:
        return str(e), 500


@app.route('/api/client', methods=['GET'])
def list_clients():
    client_id = request.args.get('client_id')
    try:
        if client_id:
            command = ['pyvelociraptor', '--config', '../api.config.yaml',
                       f"SELECT * FROM clients(client_id='{client_id}')"]
        else:
            command = ['pyvelociraptor', '--config', '../api.config.yaml', "SELECT * FROM clients()"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            # Use the helper function to format the output
            clients_data = format_subprocess_output(result.stdout)

            # Check if clients_data is empty
            if isinstance(clients_data, list) and len(clients_data) == 0:
                return jsonify({"message": "No clients found"}), 404

            # Return the JSON response
            return jsonify(clients_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



#     LIST ALL ARTIFACTS USERS
@app.route('/api/artifacts-users', methods=['GET'])
def list_artifacts_users():
    try:
        command = ['pyvelociraptor', '--config', '../api.config.yaml', "SELECT * from Artifact.Linux.Sys.Users()"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            # Use the helper function to format the output
            clients_data = format_subprocess_output(result.stdout)

            # Check if clients_data is empty
            if isinstance(clients_data, list) and len(clients_data) == 0:
                return jsonify({"message": "No clients found"}), 404

            # Return the JSON response
            return jsonify(clients_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# LIST NETWORK INTERFACES
@app.route('/api/internet-interfaces', methods=['GET'])
def list_Internet_Interfaces():
    try:
        command = ['pyvelociraptor', '--config', '../api.config.yaml', "SELECT * from interfaces()"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            # Use the helper function to format the output
            clients_data = format_subprocess_output(result.stdout)

            # Check if clients_data is empty
            if isinstance(clients_data, list) and len(clients_data) == 0:
                return jsonify({"message": "No clients found"}), 404

            # Return the JSON response
            return jsonify(clients_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)