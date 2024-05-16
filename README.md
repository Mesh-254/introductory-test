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


## step-by-step installation instructions to run `server.py` as a service daemon:

1. **Prepare Your Python Script**:
   - Make sure your Python script (`server.py`) is located in a directory of your choice. Ensure the script is executable.

2. **Create a Log Directory**:
   - Create a directory to store log files. For example, create a directory named `logs` in your project directory (`/path/to/logs/`).

3. **Create a Service File**:
   - Create a new service file for your Python script. You can name it as `filename.service`.
   - Open a text editor and paste the service configuration provided in the sample below into the file.
        **SAMPLE SERVICE FILE**
        [Unit]
        Description=introductory_test.service


        [Service]
        Type=simple
        User=root
        Group=root
        ExecStart=/usr/bin/python3 /home/frosty/projects/introductory-test/src/server.py
        WorkingDirectory=/tmp
        Restart=always
        Nice=19
        LimitNOFILE=16384
        StandardOutput=file:/home/frosty/projects/introductory-test/logs/serveroutput.log
        StandardError=file:/home/frosty/projects/introductory-test/logs/server.log


        [Install]
        WantedBy=multi-user.target


4. **Adjust Service Configuration**:
   - Adjust the `ExecStart` directive in the service file to point to the location of your Python script (`server.py`).
   - Modify the `WorkingDirectory` directive to specify the directory containing your Python script.
   - Update the `StandardOutput` and `StandardError` directives to specify the path to your log file.

5. **Save the Service File**:
   - Save the service file (`introductory_test.service`) in the directory `/etc/systemd/system/`.
   OR you may use this command to create a symbolic link to place where you service file is located 
   
   sudo ln -s /home/frosty/projects/introductory-test/introductory_test.service  /usr/lib/systemd/system/introductory_test.service


6. **Set Permissions**:
   - Ensure that the service file has the correct permissions. It should be readable by everyone and writable only by root.
   - You can set the permissions using the following command:
     ```bash
     sudo chmod 644 /etc/systemd/system/introductory_test.service
     ```

7. **Reload systemd Manager Configuration**:
   - After creating or modifying a service file, you need to reload the systemd manager configuration to apply the changes:
     ```bash
     sudo systemctl daemon-reload
     ```

8. **Start the Service**:
   - Start the service using the following command:
     ```bash
     sudo systemctl start introductory_test.service
     ```
     or restart your service using this command 
     ```bash
     sudo systemctl restart introductory_test.service
     ```

9. **Check Service Status**:
   - You can check the status of your service to ensure it's running without errors:
     ```bash
     sudo systemctl status introductory_test.service
     ```

10. **Enable Automatic Start** (Optional):
    - If you want the service to start automatically at system boot, you can enable it using the following command:
      ```bash
      sudo systemctl enable introductory_test.service
      ```

11. **Verify Logs**:
    - After starting the service, verify that the log file (`server.log`) is being created in the specified directory (`/introductory-test/logs/`). You can check the log file for any output from your Python script.

That's it! Your Python script should now be running as a service daemon, and its output should be logged to the specified log file. You can monitor the service's status, stop or restart it, and view its logs using systemd commands.
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
