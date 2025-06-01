# GitHub Careers Germany Job Notifier

A command-line tool that scrapes [GitHub Careers Jobs](https://www.github.careers/careers-home/jobs) and notifies you via Signal when there's a new open role in Germany.

## Features

- Scrapes GitHub Careers for job postings
- Filters for roles located in Germany
- Sends notifications via Signal messenger
- Remembers notified jobs to avoid duplicates
- Easy CLI usage

## Setup

### 1. Clone this repository

```sh
git clone https://github.com/ferdlestier/career-scrapper.git
cd career-scrapper
```

### 2. Python Environment

It's recommended to use a virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Install and Set Up signal-cli

- [signal-cli GitHub](https://github.com/AsamK/signal-cli)
- Download the latest release for your OS and extract the binary.
- Make it executable and move it to a directory in your PATH, e.g., `/usr/local/bin`.

#### Register your Signal sender account

```sh
signal-cli --username +YOUR_PHONE_NUMBER register
```

You'll receive a code on Signal. Complete registration:

```sh
signal-cli --username +YOUR_PHONE_NUMBER verify CODE_FROM_SIGNAL
```

#### Add a trusted recipient

The script will send notifications to this number. Make sure the recipient has an active Signal account.

### 5. Configure the app

Copy the config template and edit it:

```sh
cp config.example.json config.json
```

Edit `config.json`:

- `signal_number`: The phone number (with +countrycode) you registered with signal-cli
- `recipients`: List of recipient numbers (with +countrycode)

### 6. Run the app

```sh
python main.py
```

You can schedule it (e.g., with `cron`) for periodic checks.

## Troubleshooting

- If signal-cli fails, check your Java installation (signal-cli requires Java).
- More info: [signal-cli Wiki](https://github.com/AsamK/signal-cli/wiki)

## License

MIT
