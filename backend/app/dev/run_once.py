from app.application.use_cases.run_ingestion import run_ingestion_once

if __name__ == "__main__":
    res = run_ingestion_once(max_events=20)
    print(f"run_id={res.run_id} events_count={res.events_count} error={res.error}")
