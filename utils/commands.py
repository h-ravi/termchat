"""
Command handler for TermChat
"""
import random
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table

# Jokes for the /joke command
JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the developer go broke? Because he used up all his cache!",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
    "Why do programmers always confuse Halloween and Christmas? Because Oct 31 = Dec 25!",
    "A SQL query walks into a bar, walks up to two tables and asks, 'Can I join you?'",
    "What's a programmer's favorite place? The Foo Bar.",
    "Why don't programmers like nature? It has too many bugs and no debugging tool.",
    "Why do programmers hate nature? Too many bugs, not enough doc!"
]

def handle_command(command: str, console: Console, chat_history: List[Dict[str, str]], 
                   env_manager=None) -> Optional[str]:
    """
    Handle chat commands
    
    Args:
        command: The command string (starting with /)
        console: Rich console instance
        chat_history: The chat history
        env_manager: Environment manager instance for API management
        
    Returns:
        "exit" if the user wants to exit, "reload" to reload client, None otherwise
    """
    cmd = command.split()[0].lower()
    
    if cmd == "/help":
        show_help(console)
    elif cmd == "/exit":
        console.print(Panel("Thank you for using TermChat! Goodbye!", border_style="green"))
        return "exit"
    elif cmd == "/clear":
        console.clear()
        chat_history.clear()
    elif cmd == "/joke":
        joke = random.choice(JOKES)
        console.print(Panel(joke, border_style="yellow", title="Joke"))
    elif cmd == "/history":
        show_history(console, chat_history)
    elif cmd == "/addapi":
        if env_manager:
            env_manager.add_api_key()
            return "reload"  # Signal to reload the client
        else:
            console.print(Panel("[red]Error: Environment manager not available[/red]", border_style="red"))
    elif cmd == "/switch":
        if env_manager:
            env_manager.switch_provider()
            return "reload"  # Signal to reload the client
        else:
            console.print(Panel("[red]Error: Environment manager not available[/red]", border_style="red"))
    elif cmd == "/deleteapi":
        if env_manager:
            env_manager.delete_api_key()
            return "reload"  # Signal to reload the client
        else:
            console.print(Panel("[red]Error: Environment manager not available[/red]", border_style="red"))
    else:
        console.print(Panel(f"Unknown command: {cmd}\nType /help to see available commands.", 
                           border_style="red"))
    
    return None

def show_help(console: Console) -> None:
    """
    Show help information
    
    Args:
        console: Rich console instance
    """
    table = Table(title="Available Commands", box=None)
    table.add_column("Command", style="bold cyan")
    table.add_column("Description")
    
    table.add_row("/help", "Show this help message")
    table.add_row("/exit", "Exit the chatbot")
    table.add_row("/clear", "Clear the chat history and screen")
    table.add_row("/joke", "Tell a random programming joke")
    table.add_row("/history", "Show your chat history")
    table.add_row("/addapi", "Add a new LLM provider API key")
    table.add_row("/switch", "Switch active LLM provider")
    table.add_row("/deleteapi", "Delete a saved API key")
    
    console.print(Panel(table, border_style="blue", title="Help"))

def show_history(console: Console, chat_history: List[Dict[str, str]]) -> None:
    """
    Show chat history
    
    Args:
        console: Rich console instance
        chat_history: The chat history
    """
    if not chat_history:
        console.print(Panel("No chat history yet.", border_style="yellow"))
        return
    
    table = Table(title="Chat History", expand=True)
    table.add_column("Role", style="bold")
    table.add_column("Message")
    
    for message in chat_history:
        role = message["role"]
        content = message["content"]
        
        # Truncate very long messages for display
        if len(content) > 100:
            content = content[:97] + "..."
        
        role_style = "green" if role == "user" else "purple"
        table.add_row(f"[{role_style}]{role.capitalize()}[/{role_style}]", content)
    
    console.print(Panel(table, border_style="blue"))