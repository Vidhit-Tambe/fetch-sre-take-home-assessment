import requests
import time
import yaml

def send_http_request(endpoint):
    # Extract endpoint properties
    method = endpoint.get('method', 'GET')
    url = endpoint['url']
    headers = endpoint.get('headers', {})
    body = endpoint.get('body')

    # Send HTTP request to the endpoint
    response = requests.request(method, url, headers=headers, data=body)

    return response

def calculate_availability_percentage(domain, up_count, total_count):
    # Calculate the availability percentage for the domain
    if total_count == 0:
        return 0
    return (up_count / total_count) * 100

def main(config_file_path):
    while True:
        # Read the YAML configuration file
        with open(config_file_path, 'r') as f:
            endpoints = yaml.safe_load(f)

        # Extract unique domains from endpoints
        domains = set(endpoint['url'].split('/')[2] for endpoint in endpoints)

        # Initialize availability data for each domain
        availability_data = {domain: {'up_count': 0, 'total_count': 0} for domain in domains}

        try:
            # Perform health checks for each domain
            for domain in domains:
                up_count = 0
                total_count = 0
                for endpoint in endpoints:
                    # Check if endpoint belongs to the current domain
                    if domain in endpoint['url']:
                        total_count += 1
                        # Send HTTP request to the endpoint
                        response = send_http_request(endpoint)
                        # Check if the endpoint is UP based on response status code and latency
                        if 200 <= response.status_code < 300 and response.elapsed.total_seconds() < 0.5:
                            up_count += 1
                # Update the availability data for the domain
                availability_data[domain]['up_count'] += up_count
                availability_data[domain]['total_count'] += total_count

            # Calculate and print availability percentage for each domain
            for domain, data in availability_data.items():
                availability_percentage = calculate_availability_percentage(domain, data['up_count'], data['total_count'])
                print(f"{domain} has {availability_percentage:.0f}% availability percentage")

            # Wait for 15 seconds before the next test cycle
            time.sleep(15)
        except KeyboardInterrupt:
            # Break the loop if the user interrupts the program
            break

if __name__ == "__main__":
    config_file_path = "endpoints.yaml"  # Replace with the actual path to your YAML configuration file
    main(config_file_path)
