import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.style import Style
from dotenv import load_dotenv

from utils.openrouter import UniversalLLMClient
from utils.commands import handle_command
from utils.ui import format_ai_response, create_chat_header
from utils.env_manager import EnvManager, CUSTOM_REPLIES

# Initialize console
console = Console()

def initialize_client(env_manager: EnvManager):
    """
    Initialize the LLM client
    
    Args:
        env_manager: Environment manager instance
        
    Returns:
        Initialized UniversalLLMClient or None
    """
    provider_config = env_manager.get_active_provider()
    
    if not provider_config:
        console.print(
            Panel(
                "[bold red]Error: No active provider configured![/]"
                "\nPlease use /addapi to add an API key and /switch to select a provider.",
                title="Configuration Error",
                border_style="red"
            )
        )
        return None
    
    return UniversalLLMClient(provider_config)

def main():
    """Main function to run the chatbot"""
    # Initialize environment manager
    env_manager = EnvManager()
    
    # Check if this is first run
    if not env_manager.check_env_exists():
        if not env_manager.setup_first_run():
            console.print("[bold red]Setup failed. Exiting...[/bold red]")
            sys.exit(1)
        
        # Reload environment after setup
        load_dotenv()
    
    # Initialize client
    client = initialize_client(env_manager)
    
    if not client:
        sys.exit(1)
    
    # Display welcome header
    create_chat_header(console)
    
    # Show active provider
    active_provider = env_manager.get_active_provider()
    if active_provider:
        console.print(
            Panel(
                f"[bold cyan]Active Provider:[/bold cyan] {active_provider['name']}\n"
                f"[bold cyan]Model:[/bold cyan] {active_provider['model']}\n\n"
                "[italic]Type your message to chat with the AI, or use [bold cyan]/help[/bold cyan]  to see available commands.[/]",
                border_style="blue",
                title="🤖 Ready to Chat"
            )
        )
    
    # Chat history
    chat_history = []
    
    # Main chat loop
    while True:
        user_input = Prompt.ask("\n[bold green]You[/bold green]")
        
        # Check if this is a command
        if user_input.startswith("/"):
            command_result = handle_command(user_input, console, chat_history, env_manager)
            
            if command_result == "exit":
                break
            elif command_result == "reload":
                # Reload environment and reinitialize client
                load_dotenv(override=True)
                new_client = initialize_client(env_manager)
                
                if new_client:
                    client = new_client
                    active_provider = env_manager.get_active_provider()
                    console.print(
                        Panel(
                            f"[bold green]✓[/bold green] Client reloaded!\n"
                            f"[bold cyan]Active Provider:[/bold cyan] {active_provider['name']}\n"
                            f"[bold cyan]Model:[/bold cyan] {active_provider['model']}",
                            border_style="green"
                        )
                    )
                else:
                    console.print(
                        Panel(
                            "[yellow]Warning: No active provider configured.\n"
                            "Please use /addapi to add an API key and /switch to select a provider.[/yellow]",
                            border_style="yellow"
                        )
                    )
            continue
        
        # Check for custom replies (to save tokens)
        user_input_lower = user_input.lower().strip()
        if user_input_lower in CUSTOM_REPLIES:
            console.print("\n[bold purple]AI Assistant[/bold purple]")
            format_ai_response(CUSTOM_REPLIES[user_input_lower], console)
            continue
            
        # Check if client is available
        if not client:
            console.print(
                Panel(
                    "[yellow]No active provider configured.\n"
                    "Please use /addapi to add an API key and /switch to select a provider.[/yellow]",
                    border_style="yellow"
                )
            )
            continue
        
        # Display thinking spinner
        with console.status("[blue]AI is thinking...", spinner="dots"):
            # Append user message to history
            chat_history.append({"role": "user", "content": user_input})
            
            # Get response from AI
            try:
                response = client.get_response(chat_history)
                chat_history.append({"role": "assistant", "content": response})
                
                # Display the formatted response
                console.print("\n[bold purple]AI Assistant[/bold purple]")
                format_ai_response(response, console)
                
            except Exception as e:
                console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
                # Remove the failed user message from history
                if chat_history and chat_history[-1]["role"] == "user":
                    chat_history.pop()

if __name__ == "__main__":
    main()
