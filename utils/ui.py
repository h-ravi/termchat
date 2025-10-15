"""
UI utilities for TermChat
"""
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.box import ROUNDED
from datetime import datetime
import random

# Color themes for response panels
THEMES = [
    {"border": "blue", "title": "blue"},
    {"border": "green", "title": "green"},
    {"border": "purple", "title": "purple"},
    {"border": "cyan", "title": "cyan"},
    {"border": "magenta", "title": "magenta"}
]

def create_chat_header(console: Console) -> None:
    """
    Create and display the chat header
    
    Args:
        console: Rich console instance
    """
    console.clear()
    
    # Get current date and time
    now = datetime.now().strftime("%B %d, %Y | %H:%M")
    
    # Create header table
    table = Table(show_header=False, box=ROUNDED, expand=True)
    table.add_column()
    
    table.add_row("[bold cyan]✨ TermChat[/bold cyan] [white]- Smart Terminal AI Chatbot[/white]")
    table.add_row(f"[dim italic]{now}[/dim italic]")
    
    console.print(table)
    console.print()

def format_ai_response(text: str, console: Console) -> None:
    """
    Format and display the AI's response in a nice panel with markdown support
    
    Args:
        text: The AI's response text
        console: Rich console instance
    """
    # Select a random theme
    theme = random.choice(THEMES)
    
    # Create panel with markdown-formatted text
    md = Markdown(text)
    panel = Panel(
        md,
        border_style=theme["border"],
        title="Response",
        title_align="left",
        padding=(1, 2)
    )
    
    # Print the panel
    console.print(panel)