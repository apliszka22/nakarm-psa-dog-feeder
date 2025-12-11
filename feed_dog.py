from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DogFeeder:
    """Class to handle feeding dogs on Nakarm Psa website"""

    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def __enter__(self):
        """Context manager entry"""
        self.start_browser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_browser()

    def start_browser(self):
        """Initialize browser and context"""
        try:
            logger.info("Starting browser...")
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            logger.info("Browser started successfully")
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise

    def close_browser(self):
        """Clean up browser resources"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")

    def accept_cookies(self):
        """Accept cookies on page load"""
        try:
            # Wait for and click cookie accept button with timeout
            self.page.click("#onetrust-accept-btn-handler", timeout=5000)
            logger.info("Cookies accepted")
            time.sleep(0.5)  # Short wait after accepting
            return True
        except PlaywrightTimeout:
            logger.debug("Cookie banner not found or already accepted")
            return False
        except Exception as e:
            logger.debug(f"Error accepting cookies: {e}")
            return False

    def feed_once(self, dog_name: str) -> bool:
        """
        Feed a dog once

        Args:
            dog_name: Name of the dog to feed

        Returns:
            True if successful, False otherwise
        """
        try:
            # Navigate to dog's page
            url = f'https://nakarmpsa.olx.pl/blog/pet/{dog_name}/'
            logger.info(f"Navigating to {url}")
            self.page.goto(url, wait_until='domcontentloaded', timeout=15000)

            # Accept cookies if banner appears (IMPORTANT: Do this after each navigation)
            self.accept_cookies()

            # Click feed button
            self.page.click(".single-pet-control-feed_button", timeout=10000)
            logger.info(f"Successfully fed {dog_name}")
            return True

        except PlaywrightTimeout as e:
            logger.error(f"Timeout while feeding {dog_name}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error feeding {dog_name}: {e}")
            return False

    def feed_multiple(self, dog_name: str, num_feeds: int, delay: float = 2.0):
        """
        Feed a dog multiple times

        Args:
            dog_name: Name of the dog to feed
            num_feeds: Number of times to feed
            delay: Delay between feeds in seconds
        """
        successful_feeds = 0
        failed_feeds = 0

        logger.info(f"Starting to feed {dog_name} {num_feeds} times...")

        for i in range(num_feeds):
            logger.info(f"Feed attempt {i + 1}/{num_feeds}")

            # Clear cookies to simulate new visitor
            self.context.clear_cookies()

            # Feed the dog (cookie acceptance happens inside feed_once)
            if self.feed_once(dog_name):
                successful_feeds += 1
            else:
                failed_feeds += 1

            # Wait between feeds (except on last iteration)
            if i < num_feeds - 1:
                logger.info(f"Waiting {delay} seconds before next feed...")
                time.sleep(delay)

        logger.info(f"\n{'=' * 50}")
        logger.info(f"Feeding complete!")
        logger.info(f"Successful feeds: {successful_feeds}/{num_feeds}")
        logger.info(f"Failed feeds: {failed_feeds}/{num_feeds}")
        logger.info(f"{'=' * 50}\n")


def feed_dog(dog_name: str, num_feeds: int = 10, delay: float = 2.0, headless: bool = True):
    """
    Convenience function to feed a dog

    Args:
        dog_name: Name of the dog to feed
        num_feeds: Number of times to feed (default: 10)
        delay: Delay between feeds in seconds (default: 2.0)
        headless: Run browser in headless mode (default: True)
    """
    with DogFeeder(headless=headless) as feeder:
        feeder.feed_multiple(dog_name, num_feeds, delay)


if __name__ == "__main__":
    # Test feeding a dog 5 times
    feed_dog("piorun", num_feeds=5, delay=2.0, headless=False)