# Nakarm Psa Dog Feeder 🐕

An automated Python tool for interacting with the Nakarm Psa (Feed the Dog) website. This project allows you to search for dogs and automatically feed them through browser automation.

## Features

- 🔍 **Dog Search**: Find dogs by name and retrieve their information
- 🍖 **Automated Feeding**: Feed dogs automatically using browser automation
- 🔄 **Concurrent Operation**: Feed multiple dogs simultaneously
- 📝 **Detailed Logging**: Track all operations with timestamped logs
- 🍪 **Cookie Management**: Automatic cookie handling to simulate new visitors

## Project Structure

```
nakarm-psa-feeder/
├── feed_dog.py      # Browser automation for feeding dogs
├── find_dog.py      # Web scraping to find dog information
├── main.py          # Main orchestration script
├── requirements.txt # Project dependencies
├── README.md        # This file
└── .gitignore       # Git ignore patterns
```

## Requirements

- Python 3.7+
- Chrome/Chromium browser (installed automatically with Playwright)

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**:
   ```bash
   playwright install chromium
   ```

## Usage

### Basic Usage

Run the main script to feed dogs automatically:

```bash
python main.py
```

This will:
- Search for dogs named "Piorun" and "Azorek"
- Feed each dog 1000 times concurrently
- Log all operations to console and a timestamped log file

### Custom Configuration

Edit the constants in `main.py` to customize behavior:

```python
TIMES_TO_FEED = 1000  # Number of times to feed each dog
DELAY = 1             # Delay between feeds (seconds)
HEADLESS = True       # Run browser in headless mode (no GUI)
```

### Using Individual Modules

#### Finding a Dog

```python
from find_dog import find_dog_by_name

dog = find_dog_by_name("Piorun")
if dog:
    print(f"Found {dog['name']} with {dog['votes']} votes")
    print(f"Profile: {dog['profile_url']}")
```

#### Feeding a Dog

```python
from feed_dog import feed_dog

# Feed a dog 10 times with 2 second delay between feeds
feed_dog("piorun", num_feeds=10, delay=2.0, headless=True)
```

#### Using the DogFeeder Class

```python
from feed_dog import DogFeeder

with DogFeeder(headless=True) as feeder:
    feeder.feed_once("piorun")
    # or
    feeder.feed_multiple("piorun", num_feeds=5, delay=2.0)
```

## Module Documentation

### feed_dog.py

**DogFeeder Class**
- `start_browser()`: Initialize Playwright browser
- `close_browser()`: Clean up browser resources
- `accept_cookies()`: Handle cookie consent banners
- `feed_once(dog_name)`: Feed a dog once
- `feed_multiple(dog_name, num_feeds, delay)`: Feed a dog multiple times

**feed_dog() Function**
Convenience function for quick feeding operations.

### find_dog.py

**find_dog_by_name(dog_name) Function**
- Searches for a dog by name on the website
- Returns dictionary with dog information:
  - `name`: Dog's name
  - `id`: Unique identifier
  - `votes`: Current vote count
  - `type`: Dog type
  - `image_url`: Profile image URL
  - `profile_url`: Link to dog's profile
  - `percentage`: Vote percentage

### main.py

Main orchestration script that:
- Configures logging to both file and console
- Searches for configured dogs
- Feeds multiple dogs concurrently using ThreadPoolExecutor
- Provides detailed execution logs

## Logging

All operations are logged with timestamps. Logs are written to:
- **Console**: Real-time progress
- **Log File**: `dog_feeding_YYYYMMDD_HHMMSS.log`

Log levels:
- `INFO`: Successful operations
- `WARNING`: Non-critical issues (dog not found, etc.)
- `ERROR`: Failed operations

## Configuration

### Adjusting Feed Count

Modify `TIMES_TO_FEED` in `main.py`:
```python
TIMES_TO_FEED = 500  # Feed each dog 500 times
```

### Changing Dogs

Edit the `feeding_tasks` list in `main.py`:
```python
feeding_tasks = [
    {"dog_name": "piorun", "num_feeds": TIMES_TO_FEED, "delay": DELAY, "headless": HEADLESS},
    {"dog_name": "azorek", "num_feeds": TIMES_TO_FEED, "delay": DELAY, "headless": HEADLESS},
    {"dog_name": "another_dog", "num_feeds": 100, "delay": 1.5, "headless": True}
]
```

### Browser Visibility

Set `HEADLESS = False` to see the browser in action (useful for debugging).

## Technical Details

### How Cookie Bypass Works

The script simulates new visitors by:
1. Clearing cookies before each feed
2. Accepting cookie consent on each page load
3. Waiting between feeds to avoid rate limiting

### Concurrent Execution

Uses `ThreadPoolExecutor` with 2 workers by default to feed multiple dogs simultaneously.

## Troubleshooting

### Playwright Installation Issues

If Playwright fails to install:
```bash
python -m playwright install --force chromium
```

### Timeout Errors

If you encounter timeout errors:
- Increase delays in `main.py`
- Check your internet connection
- Verify the website is accessible

### Cookie Banner Not Found

This is normal if cookies were already accepted. The script handles this gracefully.

## Ethical Considerations

This tool is for educational purposes. Please:
- Use responsibly and respect the website's terms of service
- Don't overwhelm the server with excessive requests
- Consider the impact on other users

## License

This project is provided as-is for educational purposes.

## Contributing

Feel free to submit issues or pull requests to improve the project.

## Disclaimer

This tool interacts with a third-party website. The authors are not responsible for any consequences of using this tool. Use at your own risk and ensure compliance with the website's terms of service.