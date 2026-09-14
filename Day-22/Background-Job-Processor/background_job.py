import logging
import time
from pathlib import Path
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI, HTTPException, status
from pydantic import BaseModel


LOG_FILE = Path(__file__).with_name("execution.log")
jobs = {}

logger = logging.getLogger("background_job")
logger.setLevel(logging.INFO)
logger.propagate = False
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)

app = FastAPI(title="Background Job Processor")


class JobRequest(BaseModel):
    report_name: str = "daily_report"
    force_failure: bool = False


def process_job(job_id: str, report_name: str, force_failure: bool):
    jobs[job_id]["status"] = "running"
    logger.info("Job started - job_id=%s report=%s", job_id, report_name)

    try:
        time.sleep(3)
        if force_failure:
            raise RuntimeError("The report generation was requested to fail.")

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = f"Report '{report_name}' generated successfully."
        logger.info("Job completed - job_id=%s report=%s", job_id, report_name)
    except Exception as error:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(error)
        logger.error("Job failed - job_id=%s error=%s", job_id, error)


@app.get("/")
def read_root():
    return {"message": "Background Job Processor is running."}


@app.post("/jobs", status_code=status.HTTP_202_ACCEPTED)
def submit_job(job_request: JobRequest, background_tasks: BackgroundTasks):
    job_id = f"job-{uuid4().hex[:8]}"
    jobs[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "report_name": job_request.report_name,
    }
    logger.info("Job submitted - job_id=%s report=%s", job_id, job_request.report_name)
    background_tasks.add_task(
        process_job,
        job_id,
        job_request.report_name,
        job_request.force_failure,
    )
    return jobs[job_id]


@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    job = jobs.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job