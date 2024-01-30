from shutil import rmtree
import time, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import run

class MyHandler(FileSystemEventHandler):
    def __init__(self, gen_folder):
        super().__init__()
        self.gen_folder = gen_folder

    def on_modified(self, event):
        if event.is_directory:
            return

        # Check if the modified file is outside the gen_folder
        if self.gen_folder not in event.src_path:
            print(f'File {event.src_path} has been modified. Running bundle.py...')
            run(['python', 'bundle.py'])

if __name__ == "__main__":
    path_to_watch = 'static'  # Change this to the directory where your CSS and JS files are located
    gen_folder = 'static/gen'  # Change this to the directory where your generated files are stored

    event_handler = MyHandler(gen_folder)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

    try:
        print(f"Watching for changes in {path_to_watch}. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
