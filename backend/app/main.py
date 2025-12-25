from app.scheduler.harvester import run_forever

if __name__ == "__main__":
    run_forever(interval_minutes=60)
