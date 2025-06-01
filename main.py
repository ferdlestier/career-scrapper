import requests
from bs4 import BeautifulSoup
import json
import subprocess
import os
import sys

CONFIG_FILE = "config.json"
DATA_FILE = "notified_jobs.json"
CAREERS_URL = "https://www.github.careers/careers-home/jobs?page=1&locations=,,Germany"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def load_notified_jobs():
    if not os.path.exists(DATA_FILE):
        return set()
    with open(DATA_FILE, "r") as f:
        return set(json.load(f))

def save_notified_jobs(job_ids):
    with open(DATA_FILE, "w") as f:
        json.dump(list(job_ids), f)

def fetch_jobs():
    resp = requests.get(CAREERS_URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []
    for job_card in soup.find_all("section", class_="job-card"):
        title_tag = job_card.find("h2")
        location_tag = job_card.find("span", class_="location")
        link_tag = job_card.find("a", href=True)
        if not (title_tag and location_tag and link_tag):
            continue
        title = title_tag.text.strip()
        location = location_tag.text.strip()
        link = link_tag["href"]
        jobs.append({
            "id": link,
            "title": title,
            "location": location,
            "link": link
        })
    return jobs

def send_signal_message(signal_number, recipients, message):
    for recipient in recipients:
        cmd = [
            "signal-cli", "-u", signal_number, "send",
            "-m", message, recipient
        ]
        try:
            subprocess.run(cmd, check=True)
        except Exception as e:
            print(f"Failed to send Signal message to {recipient}: {e}", file=sys.stderr)

def main():
    config = load_config()
    notified_jobs = load_notified_jobs()
    jobs = fetch_jobs()
    new_jobs = [job for job in jobs if job["id"] not in notified_jobs]
    if not new_jobs:
        print("No new jobs in Germany found.")
        return
    for job in new_jobs:
        message = f"New GitHub Careers job in Germany:\n\n{job['title']}\nLocation: {job['location']}\nLink: {job['link']}"
        send_signal_message(config["signal_number"], config["recipients"], message)
        print(f"Notified: {job['title']}")
        notified_jobs.add(job["id"])
    save_notified_jobs(notified_jobs)

if __name__ == "__main__":
    main()
