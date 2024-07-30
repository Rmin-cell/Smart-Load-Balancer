from flask import Flask, jsonify, request, abort
import yaml
import itertools
import random

# Load config
def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Initialize Flask app
app = Flask(__name__)

# Load and parse the YAML file
config_file_path = '/config.yaml'
config = load_config(config_file_path)

# Extract addresses and weights based on types
def create_weighted_list(org_addresses):
    weighted_list = []
    for address in org_addresses:
        if isinstance(address, dict):
            addr, weight = list(address.items())[0]
            weighted_list.extend([addr] * weight)
    random.shuffle(weighted_list)
    return weighted_list

type_address_iterators = {}
for org, org_addresses in config.get('organizations', {}).items():
    addresses = [list(address.keys())[0] for address in org_addresses if isinstance(address, dict)]
    weighted_addresses = create_weighted_list(org_addresses)
    type_address_iterators[org] = {
        'round_robin': itertools.cycle(addresses),
        'weighted': itertools.cycle(weighted_addresses)
    }
# Extract all addresses and weights for default handling
all_addresses = [list(address.keys())[0] for org_addresses in config['organizations'].values() for address in org_addresses if isinstance(address, dict)]
all_weighted_addresses = create_weighted_list([address for org_addresses in config['organizations'].values() for address in org_addresses])
all_addresses_iterator = {
    'round_robin': itertools.cycle(all_addresses),
    'weighted': itertools.cycle(all_weighted_addresses)
}

# Endpoint to handle GET requests
@app.route('/', methods=['GET'])
def handle_request():
    req_type = request.args.get('type')
    weighted = request.args.get('weighted', 'false').lower() == 'true'
    
    if req_type:
        if req_type not in type_address_iterators:
            return abort(400, description="The specified type is not correct")
        if weighted:
            target_address = next(type_address_iterators[req_type]['weighted'])
        else:
            target_address = next(type_address_iterators[req_type]['round_robin'])
    else:
        if weighted:
            target_address = next(all_addresses_iterator['weighted'])
        else:
            target_address = next(all_addresses_iterator['round_robin'])
    
    # Simulate response from the target address
    response = {
        "message": "Request handled by",
        "address": target_address
    }
    return jsonify(response)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
