from watchdog import events, observers
import os

class FileWatcher(events.FileSystemEventHandler):
    def on_modified(self, event) -> None:
        print(event.src_path)
        self.is_modified = True
    
    is_modified = False
    ob = observers.Observer()