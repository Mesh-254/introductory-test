# Server Script README

This README provides an overview of the features, functionalities, and instructions for running and testing the server script.

## Features

- Binds to a port and handles an unlimited amount of concurrent connections.
- Receives a "String" in clear text from client connections.
- Reads the path to the file to search from a configuration file (`config.ini`), specified with `linuxpath=` prefix.
- Opens the file found in the path and searches for a full match of the string.
- Supports `REREAD_ON_QUERY` option to re-read the file contents on every search query.
- Handles a maximum payload size of 1024 bytes, stripping any `\x00` characters from the end.
- Responds on the TCP port with "STRING EXISTS" or "STRING NOT FOUND".
- Utilizes multithreading to accept a large number of requests in parallel.
- Works on Linux and supports files up to 250,000 rows.
- Logs search query, requesting IP, execution time, and timestamps in TCP output.

## Installation and Usage

1. Clone the repository:

    ```bash
    git clone <repository_url>
    ```

2. Navigate to the `src` directory:

    ```bash
    cd src
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the server script:

    ```bash
    python server.py
    ```

5. Modify the `config.ini` file to configure server settings, including the path to the file to search and the `REREAD_ON_QUERY` option.

6. Run the client script (`client.py`) for testing purposes to send queries to the server.
 ```bash
    python client.py
    ```

## Security

- Implements SSL authentication between the server and the client.
- Supports self-signed certificate or PSK authentication method.
- SSL authentication is configurable via the `config.ini` file (True/False).

## PEP8 Compliance and Documentation

- The codebase adheres to PEP8 and PEP20 standards.
- It is statically typed, documented with docstrings, and thoroughly documented.
- Robust exception handling and error messages are implemented.
- Unit tests cover different file sizes, execution times, and scenarios using pytest.

## Speed Testing Report

- A speed testing report in PDF format (`speed_testing_report.pdf`) is provided.
- The report compares the performance of at least 5 different file-search options and algorithms, including execution times and benchmarking against each other.

## License

- This project is licensed under the [MIT License](LICENSE).

---
