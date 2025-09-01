import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.base_agent import BaseAgent
import os

try:
    from PyPDF2 import PdfReader
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

class ReminderAgent(BaseAgent):
    def __init__(self, file_path=None, **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path
        self.content = self.load_file() if file_path else ""

    def load_file(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} not found")
        if self.file_path.endswith('.pdf'):
            if not PDF_SUPPORT:
                raise ImportError("PyPDF2 is required to read PDF files. Please install it with: pip install PyPDF2")
            reader = PdfReader(self.file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        else:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()

    def run(self):
        if not self.content:
            return "No file loaded. Please provide a file path."
        prompt = f"Extract all reminders, deadlines, tasks, or important dates from the following content:\n\n{self.content}"
        return super().ask(prompt)