import subprocess
from datetime import datetime, timedelta

def capture_browser_requests(interface='wlp1s0', start_time='09:00', end_time='17:00', threshold=10):
    command = ['tshark', '-i', interface, '-Y', 'http.request', '-T', 'fields', '-e', 'http.host', '-e', 'http.request.uri', '-e', 'frame.time']
    
    try:
        result = subprocess.check_output(command, text=True)
        output_lines = result.strip().split('\n')

        request_count = 0
        for line in output_lines:
            host, uri, timestamp = line.split('\t')
            request_time = datetime.strptime(timestamp, "%b %d, %Y %H:%M:%S.%f %Z")

            # Specify the time range
            start_time_obj = datetime.strptime(start_time, "%H:%M")
            end_time_obj = datetime.strptime(end_time, "%H:%M")

            if start_time_obj <= request_time.time() <= end_time_obj:
                request_count += 1
                print(f"Host: {host}, URI: {uri}, Time: {request_time}")

        if request_count > threshold:
            print(f"Sudden increase in requests: {request_count} requests within the time frame")

    except subprocess.CalledProcessError as e:
        print(f"Error capturing browser requests: {e}")

# Replace 'wlp1s0' with your actual wireless interface
# Set the desired time range and threshold
capture_browser_requests(start_time='09:00', end_time='17:00', threshold=10)
