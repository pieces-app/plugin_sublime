import sublime
import time

class ProgressBar:
    def __init__(self, label, width=10, update_interval=100, total=None):
        """
        Initialize the progress bar with a label, width, update interval, and total progress.
        
        :param label: The label to display with the progress bar.
        :param width: The width of the progress bar.
        :param update_interval: The interval (in milliseconds) between updates.
        :param total: The total amount of progress for measured progress bars.
        """
        self.label = label
        self.width = width
        self.update_interval = update_interval
        self.total = total
        self.current = 0
        self._done = False

    def start(self):
        """Start the progress bar."""
        self._done = False
        self._update()

    def stop(self):
        """Stop the progress bar and clear the status message."""
        sublime.status_message(f"{self.label} [✔ Complete]")
        self._done = True

    def update_progress(self, progress):
        """Update the current progress for measured progress bars."""
        if self.total is not None:
            self.current = progress
            if self.current >= self.total:
                self.stop()

    def _update(self, status=0):
        """Update the progress bar status."""
        if self._done:
            time.sleep(2)
            return
        
        if self.total is not None:
            # Measured progress bar
            percentage = int((self.current / self.total) * 100)
            before = int((self.current / self.total) * self.width)
            after = self.width - before
            progress_bar = f"[{'█' * before}{'░' * after}] {percentage}%"
        else:
            # Unmeasured progress bar
            status = status % (2 * self.width)
            before = min(status, (2 * self.width) - status)
            after = self.width - before
            progress_bar = f"[{'█' * before}{'░' * after}]"

        # Update the status message
        sublime.status_message(f"{self.label} {progress_bar}")
        
        # Schedule the next update
        if not self._done:
            sublime.set_timeout(lambda: self._update(status + 1), self.update_interval)
