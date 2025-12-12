import random
import feed_dog
from find_dog import find_dog_by_name
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from datetime import datetime

# Constants
MIN_DELAY = 1.0
MAX_DELAY = 2.0
TIMES_TO_FEED = 5000
HEADLESS = True

# Set up logging to both file and console
log_filename = f"dog_feeding_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create formatters
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# File handler
file_handler = logging.FileHandler(log_filename, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("Starting dog feeding process")

dog_names = ["Piorun", "Azorek", "Feniks", "Amadeo"]
for name in dog_names:
    dog = find_dog_by_name(name)
    if dog:
        logger.info(f"\n{'=' * 50}")
        logger.info(f"Found dog: {dog['name']}")
        logger.info(f"ID: {dog['id']}")
        logger.info(f"Votes: {dog['votes']}")
        logger.info(f"Percentage: {dog.get('percentage', 'N/A')}")
        logger.info(f"Profile URL: {dog.get('profile_url', 'N/A')}")
        logger.info(f"Image URL: {dog.get('image_url', 'N/A')}")
    else:
        logger.warning(f"Dog '{name}' not found")


# Generate feeding tasks automatically from dog_names
feeding_tasks = [
    {
        "dog_name": name.lower(),
        "num_feeds": TIMES_TO_FEED,
        "delay": random.uniform(MIN_DELAY, MAX_DELAY),
        "headless": HEADLESS
    }
    for name in dog_names
]


logger.info("Starting concurrent feeding tasks")

# Run all tasks concurrently
with ThreadPoolExecutor(max_workers=len(dog_names)) as executor:
    futures = {executor.submit(feed_dog.feed_dog, **task): task['dog_name'] for task in feeding_tasks}

    for future in as_completed(futures):
        dog_name = futures[future]
        try:
            result = future.result()
            logger.info(f"✓ Feeding task completed for {dog_name}: {result}")
        except Exception as e:
            logger.error(f"✗ Feeding task failed for {dog_name}: {e}", exc_info=True)

logger.info("All feeding tasks completed!")