from app.application.use_cases.run_ingestion import run_ingestion_once

if __name__ == "__main__":
    run_ingestion_once(max_events=20)
