import requests
import time
import yaml

def send_http_request(endpoint):
    method = endpoint.get('method', 'GET')
    url = endpoint['url']
    headers = endpoint.get('headers', {})
    body = endpoint.get('body')

    response = requests.request(method, url, headers=headers, data=body)

    return response

def calculate_availability_percentage(domain, up_count, total_count):
    if total_count == 0:
        return 0
    return (up_count / total_count) * 100

def main(config_file_path):
    while True:
        with open(config_file_path, 'r') as f:
            endpoints = yaml.safe_load(f)

        domains = set(endpoint['url'].split('/')[2] for endpoint in endpoints)
        availability_data = {domain: {'up_count': 0, 'total_count': 0} for domain in domains}

        try:
            for domain in domains:
                up_count = 0
                total_count = 0
                for endpoint in endpoints:
                    if domain in endpoint['url']:
                        total_count += 1
                        response = send_http_request(endpoint)
                        if 200 <= response.status_code < 300 and response.elapsed.total_seconds() < 0.5:
                            up_count += 1
                availability_data[domain]['up_count'] += up_count
                availability_data[domain]['total_count'] += total_count

            for domain, data in availability_data.items():
                availability_percentage = calculate_availability_percentage(domain, data['up_count'], data['total_count'])
                print(f"{domain} has {availability_percentage:.0f}% availability percentage")

            time.sleep(15)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    config_file_path = "endpoints.yaml"  # Replace with the actual path to your YAML configuration file
    main(config_file_path)
