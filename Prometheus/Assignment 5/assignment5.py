from flask import Response, Flask, request
import prometheus_client
from prometheus_client import Summary, Counter, Histogram, Gauge
import time
import random

app = Flask(__name__)

metrics_details = {}
metrics_details['c'] = Counter('python_total_invocation', 'Counter total number of requests')
metrics_details['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets=(1, 2, 5, 6, 10))

@app.route("/")
def hello():
    start = time.time()
    metrics_details['c'].inc()
    sleep_timer = random.randint(1,10)
    time.sleep(sleep_timer)
    end = time.time()
    metrics_details['h'].observe(end - start)
    return_statement = f"Python Flask app for prometheous monitoring is up and running. This time delay was {sleep_timer} sec" 
    return return_statement


@app.route("/metrics")
def requests_count():
    res = []
    for k,v in metrics_details.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")

if __name__ == '__main__':
    app.run()