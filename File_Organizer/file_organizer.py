'''This script organizes files in a specified directory by moving them into subdirectories based on their file extensions.'''
'''This script organizes files after analysis of the directory structure and file types.'''
'''This script creates a structured directory layout for better file management.'''

# Classes, functions, and imports


import os
import time


class FileOrganizer:
    def welcome_message(self):
        # This function prints a welcome message to the user.
        print("Welcome to the File Organizer!")
        print()
        time.sleep(2)
        print("This script will help you organize files in a specified directory by their extensions.")
        print()
        time.sleep(2)

    def add_directory(self, directory):
        # Ask user for a directory to organize files
        if not os.path.exists(directory):
            print(f"The directory {directory} does not exist.")
            return

    def scan_directory(self, directory):
        # This function scans the specified directory and returns a list of files.
        print(f"Scanning directory: {directory}")
        if not os.path.isdir(directory):
            print(f"The path {directory} is not a valid directory.")
            return []
        files = []
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                files.append(filename)
        return files

    def sort_files_by_extension(self, files):
        # This function sorts files by their extensions [.jpg, .png, .txt].
        images = ['.jpg', '.jpeg', '.png', '.gif']
        documents = ['.txt', '.pdf', '.docx', '.xlsx']
        audio = ['.mp3', '.wav', '.aac']
        video = ['.mp4', '.avi', '.mkv']
        sorted_files = {
            'images': [],
            'documents': [],
            'audio': [],
            'video': [],
            'others': []
        }
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in images:
                sorted_files['images'].append(file)
            elif ext in documents:
                sorted_files['documents'].append(file)
            elif ext in audio:
                sorted_files['audio'].append(file)
            elif ext in video:
                sorted_files['video'].append(file)
            else:
                sorted_files['others'].append(file)
        return sorted_files

    def organize_files(self, directory):
        # This function organizes files in the specified directory by their extensions.
        files = self.scan_directory(directory)
        if not files:
            print("No files found to organize.")
            return

        sorted_files = self.sort_files_by_extension(files)

        for category, files in sorted_files.items():
            category_dir = os.path.join(directory, category)
            if not os.path.exists(category_dir):
                os.makedirs(category_dir)
                print(f"Created directory: {category_dir}")

            for filename in files:
                source_path = os.path.join(directory, filename)
                base, ext = os.path.splitext(filename)
                target_filename = filename
                target_path = os.path.join(category_dir, target_filename)
                counter = 1
                # check for duplicate filenames
                while os.path.exists(target_path):
                    target_filename = f"{base}_{counter}{ext}"
                    target_path = os.path.join(category_dir, target_filename)
                    counter += 1
                os.rename(source_path, target_path)
                print(f"Moved {target_filename} to {category_dir}")

    def end_message(self, sorted_files):
        # This function prints a message how much files and directories were organized.
        print("File organization complete.")
        print()
        time.sleep(2)
        print(
            f"Total files organized: {sum(len(files) for files in sorted_files.values())}")
        print()
        time.sleep(2)
        print(f"Total directories created: {len(sorted_files)}")
        print()
        time.sleep(2)
        print("Thank you for using the File Organizer!")
        print()
        time.sleep(2)

    def run(self):
        # This function runs the file organizer.
        self.welcome_message()
        directory = input("Please enter the directory to organize: ")
        self.add_directory(directory)
        self.scan_directory(directory)
        sorted_files = self.sort_files_by_extension(
            self.scan_directory(directory))
        self.organize_files(directory)
        self.end_message(sorted_files)

# Main execution block


if __name__ == "__main__":
    organizer = FileOrganizer()
    organizer.run()
