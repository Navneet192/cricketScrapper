import logging
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import time

from cricket_scraper.scrapers.fixtures_scraper import scrape_fixtures
from cricket_scraper.scrapers.scorecard_scraper import scrape_scorecard
from cricket_scraper.scrapers.live_scraper import scrape_live

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def parse_start_time(start_time_str):
    try:
        return datetime.strptime(start_time_str, "%a, %d %b %Y")
    except ValueError:
        pass
    try:
        t = datetime.strptime(start_time_str, "%I:%M %p").time()
        today = datetime.today()
        return datetime.combine(today, t)
    except ValueError:
        pass
    raise ValueError(f"Unrecognized date/time format: {start_time_str}")

def is_future_time(dt):
    return dt > datetime.now()

def schedule_match_jobs():
    fixtures = scrape_fixtures()
    scheduler = BackgroundScheduler()
    scheduled = set()
    for fixture in fixtures:
        match_url = fixture.get("match_url")
        start_time_str = fixture.get("start_time")
        title = fixture.get("title", "Unknown Match")
        if not match_url or not start_time_str:
            logging.warning(f"Skipping fixture with missing data: {fixture}")
            continue
        try:
            start_time = parse_start_time(start_time_str)
        except Exception as e:
            logging.error(f"Could not parse start time '{start_time_str}': {e}")
            continue
        if not is_future_time(start_time):
            logging.info(f"Skipping past match: {title} at {start_time}")
            continue
        job_id = f"{match_url}-{start_time.isoformat()}"
        if job_id in scheduled:
            logging.info(f"Duplicate job detected for {title}, skipping.")
            continue
        job_time = start_time - timedelta(minutes=1)
        logging.info(f"Scheduling jobs for {title} at {job_time}")
        scheduler.add_job(scrape_scorecard, 'date', run_date=job_time, args=[match_url], id=f"scorecard-{job_id}")
        scheduler.add_job(scrape_live, 'date', run_date=job_time, args=[match_url], id=f"live-{job_id}")
        scheduled.add(job_id)
    scheduler.start()
    logging.info("Scheduler started. Waiting for jobs to run...")
    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logging.info("Scheduler shut down gracefully.")

if __name__ == "__main__":
    schedule_match_jobs()
