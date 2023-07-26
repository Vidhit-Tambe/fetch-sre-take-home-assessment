## fetch-sre-take-home-assessment

**Problem Overview:**
The problem is to implement a program that checks the health of a set of HTTP endpoints. The program should read an input argument, which is the file path to a list of HTTP endpoints in YAML format. It will then test the health of these endpoints every 15 seconds and keep track of the availability percentage of each domain. After each 15-second test cycle, the program should log the cumulative availability percentage for each domain to the console.

**Prompt - Sample Input YAML File:**
The prompt provides an example of a valid YAML configuration file. The configuration file contains a list of HTTP endpoints, and each endpoint has the following properties:
* name: A free-text name to describe the HTTP endpoint.
* url: The URL of the HTTP endpoint.
* method: The HTTP method of the endpoint (optional, default is GET).
* headers: The HTTP headers to include in the request (optional).
* body: The HTTP body to include in the request (optional).

**Parsing the Program Input:**
The program should accept a single required input argument, which is the path to the configuration file in YAML format. The configuration file contains a list of HTTP endpoints, each with its properties described above. The program should be able to handle an arbitrary file path as its input.

**Running the Health Checks:**
The main part of the program involves sending HTTP requests to each endpoint every 15 seconds to check their health. To determine if an endpoint is UP or DOWN, we use the following criteria:
* UP: The HTTP response code is in the 2xx range (any 200–299 response code), and the response latency is less than 500 ms.
* DOWN: The endpoint is not UP (does not meet the above criteria).
The program will keep testing the endpoints every 15 seconds until the user manually exits the program.

**Logging the Results:**
After testing all the endpoints in the configuration file, the program should log the availability percentage of each URL domain over the lifetime of the program to the console. The availability percentage is calculated as follows:

Availability percentage = 100 * (number of HTTP requests that had an outcome of UP / total number of HTTP requests)

The example YAML file provided in the prompt contains two URL domains: "fetch.com" and "www.fetchrewards.com." The availability percentage for each domain will be logged after each 15-second test cycle.

**Step-by-Step Explanation of the Code:**
Now, let's go through the Python code step by step:
* Importing the necessary libraries:
    * requests: A popular library for making HTTP requests.
    * time: To introduce a delay of 15 seconds between each test cycle.
    * yaml: To parse the YAML configuration file.
* Defining the send_http_request function:
    * This function takes an endpoint (a dictionary) as an argument.
    * It extracts the HTTP method, URL, headers, and body from the endpoint dictionary.
    * It then sends an HTTP request using the requests.request method.
    * The function returns the response object.
* Defining the calculate_availability_percentage function:
    * This function calculates the availability percentage for a domain based on the number of successful (UP) HTTP requests and the total number of HTTP requests.
    * It avoids division by zero by returning 0 if the total count is zero.
* The main function:
    * This function is the main entry point of the program.
    * It takes the config_file_path as an argument.
    * It opens the YAML configuration file, reads the list of endpoints, and stores the unique domains in a set.
    * It initializes the availability_data dictionary to keep track of the number of UP and total requests for each domain.
* The try-except block for running the tests:
    * The program continuously runs the tests until the user manually exits the program by pressing Ctrl+C (KeyboardInterrupt).
    * Within each test cycle, the program iterates over each domain.
    * For each domain, it iterates through all the endpoints and sends HTTP requests to the endpoints belonging to that domain.
    * It checks the response status code and response latency to determine if an endpoint is UP or DOWN.
* Calculating the availability percentage for each domain:
    * After each test cycle, the program calculates the availability percentage for each domain based on the data accumulated during the test cycle.
    * It logs the availability percentage for each domain to the console.
* Running the main function:
    * The program runs the main function with the provided config_file_path as the input argument.
