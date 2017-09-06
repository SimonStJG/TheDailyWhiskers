import schedule
import time

from prometheus_client import start_http_server, Summary, Counter

from dailywhiskers import main

run_time = Summary('run_time_seconds', 'Time spent on a run in seconds')
fatal_errors = Counter('fatal_errors', 'Fatal Errors')

@run_time.time()
def tick():
  try:
    main()
  except Exception:
    fatal_errors.inc()  
    pass


if __name__ == "__main__":
  start_http_server(8000)
  schedule.every().day.at("09:00").do(tick);
  while True:
    schedule.run_pending()
    time.sleep(1)
