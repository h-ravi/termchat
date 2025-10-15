"""
Environment and API key management for TermChat
"""
import os
import getpass
from typing import Dict, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from dotenv import load_dotenv, set_key, unset_key

# Supported LLM providers with their configuration
LLM_PROVIDERS = {
    "1": {
        "name": "Google (Gemini)",
        "env_key": "GOOGLE_API_KEY",
        "api_url": "https://generativelanguage.googleapis.com/v1beta/models/",
        "model": "gemini-2.5-pro"
    },
    "2": {
        "name": "OpenRouter",
        "env_key": "OPENROUTER_API_KEY",
        "api_url": "https://openrouter.ai/api/v1/chat/completions",
        "model": "openai/gpt-oss-20b:free"
    },
    "3": {
        "name": "OpenAI",
        "env_key": "OPENAI_API_KEY",
        "api_url": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-3.5-turbo"
    },
    "4": {
        "name": "Anthropic (Claude)",
        "env_key": "ANTHROPIC_API_KEY",
        "api_url": "https://api.anthropic.com/v1/messages",
        "model": "claude-3-sonnet-20240229"
    },
    "5": {
        "name": "xAI (Grok)",
        "env_key": "XAI_API_KEY",
        "api_url": "https://api.x.ai/v1/chat/completions",
        "model": "grok-beta"
    },
    "6": {
        "name": "DeepSeek",
        "env_key": "DEEPSEEK_API_KEY",
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-chat"
    },
    "7": {
        "name": "Qwen",
        "env_key": "QWEN_API_KEY",
        "api_url": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
        "model": "qwen-turbo"
    },
    "8": {
        "name": "HuggingFace",
        "env_key": "HUGGINGFACE_API_KEY",
        "api_url": "https://api-inference.huggingface.co/models/",
        "model": "mistralai/Mistral-7B-Instruct-v0.2"
    }
}

# Custom replies to save tokens
CUSTOM_REPLIES = {
    'hello': 'Hello! Main aapki madad ke liye taiyaar hu. Kya main aapki koi madad kar sakta hu?',
    'hi': 'Hi! Kaise madad kar sakta hu?',
    'hey': 'Hey there! Kya help chahiye?',
    'help': '''Available Commands:
• /clear - Clear chat history
• /exit or /quit - Exit application
• /addapi - Add new LLM provider API key
• /switch - Switch between saved LLM providers
• /deleteapi - Delete saved API key
• /help - Show this help message

Ask me anything!''',
    'bye': 'Goodbye! Phir milenge! 👋',
    'goodbye': 'Goodbye! Dhanyavaad! 👋',
    'thanks': 'Aapka swagat hai! 😊',
    'thank you': 'Koi baat nahi! Khushi hui madad karke! 😊',
    'ok': 'Theek hai! Aur kuch chahiye?',
    'okay': 'Bilkul! Aur kya help chahiye?',
}

class EnvManager:
    """Manage environment variables and API keys"""
    
    def __init__(self, env_path: str = ".env"):
        """
        Initialize the environment manager
        
        Args:
            env_path: Path to the .env file
        """
        self.env_path = env_path
        self.console = Console()
        
        # Load existing environment
        if os.path.exists(self.env_path):
            load_dotenv(self.env_path)
    
    def setup_first_run(self) -> bool:
        """
        Setup environment on first run
        
        Returns:
            True if setup was successful, False otherwise
        """
        self.console.print(
            Panel(
                "[bold cyan]Welcome to TermChat![/bold cyan]\n\n"
                "[white]Pehli baar setup kar rahe hain. Kripya apna LLM provider chunen.[/white]",
                title="🎉 First Time Setup",
                border_style="cyan"
            )
        )
        
        # Show available providers with cancel option
        self._display_providers(show_cancel=True)
        
        # Get user selection with cancel option
        choices = list(LLM_PROVIDERS.keys()) + ['0']
        choice = Prompt.ask(
            "\n[bold green]Apna LLM provider chunen (0 - Cancel)[/bold green]",
            choices=choices
        )
        
        # Check if user wants to cancel
        if choice == '0':
            self.console.print("[yellow]Setup cancel ho gaya. Aap baad mein setup kar sakte hain.[/yellow]")
            return False
        
        provider = LLM_PROVIDERS[choice]
        
        # Get API key with masked input
        self.console.print(f"\n[bold yellow]{provider['name']} ka API key dalen[/bold yellow]")
        self.console.print("[dim]Note: API key stars (***) ke roop mein dikhega[/dim]")
        self.console.print("[dim]Cancel karne ke liye khali chhod kar Enter dabaye[/dim]\n")
        
        api_key = getpass.getpass("API Key: ")
        
        if not api_key.strip():
            self.console.print("[yellow]API key nahi dala gaya. Setup cancel ho gaya.[/yellow]")
            return False
        
        # Show masked API key for confirmation
        masked_key = '*' * len(api_key)
        self.console.print(f"[green]✓ API key received: {masked_key}[/green]")
        
        # Get model name with cancel option
        self.console.print(
            f"\n[dim]Default model: {provider['model']}[/dim]"
        )
        self.console.print("[dim]Khali chhod kar Enter dabane par default model use hoga[/dim]")
        self.console.print("[dim]'cancel' likhkar cancel kar sakte hain[/dim]\n")
        
        model_name = Prompt.ask(
            f"[bold yellow]Model name dalen[/bold yellow]",
            default=provider['model']
        )
        
        if model_name.lower() == 'cancel':
            self.console.print("[yellow]Setup cancel ho gaya.[/yellow]")
            return False
        
        # Create .env file and save API key
        try:
            # Create .env file if it doesn't exist
            if not os.path.exists(self.env_path):
                open(self.env_path, 'w').close()
            
            # Save API key
            set_key(self.env_path, provider['env_key'], api_key)
            
            # Save model name
            model_key = provider['env_key'].replace('_API_KEY', '_MODEL')
            set_key(self.env_path, model_key, model_name)
            
            # Save active provider
            set_key(self.env_path, "ACTIVE_PROVIDER", choice)
            
            # Save provider name
            set_key(self.env_path, "ACTIVE_PROVIDER_NAME", provider['name'])
            
            self.console.print(
                Panel(
                    f"[bold green]✓[/bold green] API key successfully save ho gaya!\n"
                    f"[white]Active Provider:[/white] [bold cyan]{provider['name']}[/bold cyan]\n"
                    f"[white]Model:[/white] [bold cyan]{model_name}[/bold cyan]",
                    border_style="green",
                    title="Success"
                )
            )
            
            return True
            
        except Exception as e:
            self.console.print(
                Panel(
                    f"[bold red]Error:[/bold red] {str(e)}",
                    border_style="red"
                )
            )
            return False
    
    def add_api_key(self) -> None:
        """Add a new API key for a provider"""
        self.console.print(
            Panel(
                "[bold cyan]Naya API Key Add Karein[/bold cyan]",
                border_style="cyan"
            )
        )
        
        # Show available providers with cancel option
        self._display_providers(show_cancel=True)
        
        # Get user selection with cancel option
        choices = list(LLM_PROVIDERS.keys()) + ['0']
        choice = Prompt.ask(
            "\n[bold green]Provider chunen (0 - Cancel)[/bold green]",
            choices=choices
        )
        
        # Check if user wants to cancel
        if choice == '0':
            self.console.print("[yellow]Operation cancel ho gaya.[/yellow]")
            return
        
        provider = LLM_PROVIDERS[choice]
        
        # Check if API key already exists
        existing_key = os.getenv(provider['env_key'])
        if existing_key:
            overwrite = Confirm.ask(
                f"\n[yellow]{provider['name']} ka API key pehle se saved hai. Kya overwrite karein?[/yellow]"
            )
            if not overwrite:
                self.console.print("[yellow]Operation cancel ho gaya.[/yellow]")
                return
        
        # Get API key with masked input
        self.console.print(f"\n[bold yellow]{provider['name']} ka API key dalen[/bold yellow]")
        self.console.print("[dim]Note: API key stars (***) ke roop mein dikhega[/dim]")
        self.console.print("[dim]Cancel karne ke liye khali chhod kar Enter dabaye[/dim]\n")
        
        api_key = getpass.getpass("API Key: ")
        
        if not api_key.strip():
            self.console.print("[yellow]API key nahi dala gaya. Operation cancel ho gaya.[/yellow]")
            return
        
        # Show masked API key for confirmation
        masked_key = '*' * len(api_key)
        self.console.print(f"[green]✓ API key received: {masked_key}[/green]")
        
        # Get model name with cancel option
        self.console.print(
            f"\n[dim]Default model: {provider['model']}[/dim]"
        )
        self.console.print("[dim]Khali chhod kar Enter dabane par default model use hoga[/dim]")
        self.console.print("[dim]'cancel' likhkar cancel kar sakte hain[/dim]\n"
        )
        model_name = Prompt.ask(
            f"[bold yellow]Model name dalen[/bold yellow]",
            default=provider['model']
        )
        
        if model_name.lower() == 'cancel':
            self.console.print("[yellow]Operation cancel ho gaya.[/yellow]")
            return
        
        try:
            # Save API key
            set_key(self.env_path, provider['env_key'], api_key)
            
            # Save model name
            model_key = provider['env_key'].replace('_API_KEY', '_MODEL')
            set_key(self.env_path, model_key, model_name)
            
            self.console.print(
                Panel(
                    f"[bold green]✓[/bold green] {provider['name']} ka API key successfully save ho gaya!\n"
                    f"[white]Model:[/white] [bold cyan]{model_name}[/bold cyan]",
                    border_style="green"
                )
            )
            
            # Ask if they want to switch to this provider
            switch = Confirm.ask(
                f"\n[cyan]Kya aap {provider['name']} ko active provider banana chahte hain?[/cyan]"
            )
            
            if switch:
                set_key(self.env_path, "ACTIVE_PROVIDER", choice)
                set_key(self.env_path, "ACTIVE_PROVIDER_NAME", provider['name'])
                self.console.print(
                    f"[bold green]✓[/bold green] Active provider change ho gaya: [bold cyan]{provider['name']}[/bold cyan] ({model_name})"
                )
                
        except Exception as e:
            self.console.print(
                Panel(
                    f"[bold red]Error:[/bold red] {str(e)}",
                    border_style="red"
                )
            )
    
    def switch_provider(self) -> None:
        """Switch active LLM provider"""
        self.console.print(
            Panel(
                "[bold cyan]Active Provider Change Karein[/bold cyan]",
                border_style="cyan"
            )
        )
        
        # Get all saved providers
        saved_providers = self._get_saved_providers()
        
        if not saved_providers:
            self.console.print(
                Panel(
                    "[yellow]Koi bhi API key save nahi hai!\n"
                    "Pehle /addapi command use karke API key add karein.[/yellow]",
                    border_style="yellow"
                )
            )
            return
        
        # Display saved providers with models
        table = Table(title="Saved API Keys", box=None)
        table.add_column("Number", style="bold cyan")
        table.add_column("Provider", style="bold")
        table.add_column("Model", style="dim")
        table.add_column("Status", style="bold")
        
        active_provider = os.getenv("ACTIVE_PROVIDER")
        
        for idx, provider_id in saved_providers.items():
            provider = LLM_PROVIDERS[provider_id]
            model_key = provider['env_key'].replace('_API_KEY', '_MODEL')
            model_name = os.getenv(model_key, provider['model'])
            status = "[green]✓ Active[/green]" if provider_id == active_provider else ""
            table.add_row(idx, provider['name'], model_name, status)
        
        # Add cancel option
        table.add_row("0", "[yellow]Cancel[/yellow]", "", "")
        
        self.console.print(Panel(table, border_style="blue"))
        
        # Get user selection with cancel option
        choices = list(saved_providers.keys()) + ['0']
        choice = Prompt.ask(
            "\n[bold green]Kis provider ko active karna hai? (0 - Cancel)[/bold green]",
            choices=choices
        )
        
        # Check if user wants to cancel
        if choice == '0':
            self.console.print("[yellow]Operation cancel ho gaya.[/yellow]")
            return
        
        provider_id = saved_providers[choice]
        provider = LLM_PROVIDERS[provider_id]
        model_key = provider['env_key'].replace('_API_KEY', '_MODEL')
        model_name = os.getenv(model_key, provider['model'])
        
        try:
            set_key(self.env_path, "ACTIVE_PROVIDER", provider_id)
            set_key(self.env_path, "ACTIVE_PROVIDER_NAME", provider['name'])
            
            self.console.print(
                Panel(
                    f"[bold green]✓[/bold green] Active provider successfully change ho gaya!\n"
                    f"[white]Naya Active Provider:[/white] [bold cyan]{provider['name']}[/bold cyan]\n"
                    f"[white]Model:[/white] [bold cyan]{model_name}[/bold cyan]",
                    border_style="green"
                )
            )
            
        except Exception as e:
            self.console.print(
                Panel(
                    f"[bold red]Error:[/bold red] {str(e)}",
                    border_style="red"
                )
            )
    
    def delete_api_key(self) -> None:
        """Delete a saved API key"""
        self.console.print(
            Panel(
                "[bold red]API Key Delete Karein[/bold red]",
                border_style="red"
            )
        )
        
        # Get all saved providers
        saved_providers = self._get_saved_providers()
        
        if not saved_providers:
            self.console.print(
                Panel(
                    "[yellow]Koi bhi API key save nahi hai![/yellow]",
                    border_style="yellow"
                )
            )
            return
        
        # Display saved providers with models
        table = Table(title="Saved API Keys", box=None)
        table.add_column("Number", style="bold cyan")
        table.add_column("Provider", style="bold")
        table.add_column("Model", style="dim")
        table.add_column("Status", style="bold")
        
        active_provider = os.getenv("ACTIVE_PROVIDER")
        
        for idx, provider_id in saved_providers.items():
            provider = LLM_PROVIDERS[provider_id]
            model_key = provider['env_key'].replace('_API_KEY', '_MODEL')
            model_name = os.getenv(model_key, provider['model'])
            status = "[green]✓ Active[/green]" if provider_id == active_provider else ""
            table.add_row(idx, provider['name'], model_name, status)
        
        # Add cancel option
        table.add_row("0", "[yellow]Cancel[/yellow]", "", "")
        
        self.console.print(Panel(table, border_style="blue"))
        
        # Get user selection with cancel option
        choices = list(saved_providers.keys()) + ['0']
        choice = Prompt.ask(
            "\n[bold yellow]Kis provider ka API key delete karna hai? (0 - Cancel)[/bold yellow]",
            choices=choices
        )
        
        # Check if user wants to cancel
        if choice == '0':
            self.console.print("[yellow]Operation cancel ho gaya.[/yellow]")
            return
        
        provider_id = saved_providers[choice]
        provider = LLM_PROVIDERS[provider_id]
        
        # Confirm deletion
        confirm = Confirm.ask(
            f"\n[bold red]Kya aap {provider['name']} ka API key delete karna chahte hain?[/bold red]"
        )
        
        if not confirm:
            self.console.print("[dim]Operation cancelled.[/dim]")
            return
        
        try:
            # Delete API key
            unset_key(self.env_path, provider['env_key'])
            
            # Delete model name
            model_key = provider['env_key'].replace('_API_KEY', '_MODEL')
            unset_key(self.env_path, model_key)
            
            # If this was the active provider, clear it
            if provider_id == active_provider:
                unset_key(self.env_path, "ACTIVE_PROVIDER")
                unset_key(self.env_path, "ACTIVE_PROVIDER_NAME")
                
                self.console.print(
                    Panel(
                        f"[bold green]✓[/bold green] {provider['name']} ka API key delete ho gaya!\n"
                        f"[yellow]Note:[/yellow] Koi active provider nahi hai. Kripya /switch command use karein.",
                        border_style="green"
                    )
                )
            else:
                self.console.print(
                    Panel(
                        f"[bold green]✓[/bold green] {provider['name']} ka API key delete ho gaya!",
                        border_style="green"
                    )
                )
                
        except Exception as e:
            self.console.print(
                Panel(
                    f"[bold red]Error:[/bold red] {str(e)}",
                    border_style="red"
                )
            )
    
    def get_active_provider(self) -> Optional[Dict[str, str]]:
        """
        Get the active provider configuration
        
        Returns:
            Provider configuration dict or None if not set
        """
        active_id = os.getenv("ACTIVE_PROVIDER")
        if not active_id or active_id not in LLM_PROVIDERS:
            return None
        
        provider = LLM_PROVIDERS[active_id].copy()
        provider['api_key'] = os.getenv(provider['env_key'])
        
        # Get the saved model name or use default
        model_key = provider['env_key'].replace('_API_KEY', '_MODEL')
        saved_model = os.getenv(model_key)
        if saved_model:
            provider['model'] = saved_model
        
        return provider if provider['api_key'] else None
    
    def _display_providers(self, show_cancel: bool = False) -> None:
        """
        Display available LLM providers
        
        Args:
            show_cancel: Whether to show cancel option
        """
        table = Table(title="Available LLM Providers", box=None)
        table.add_column("Number", style="bold cyan")
        table.add_column("Provider", style="bold")
        
        for key, provider in LLM_PROVIDERS.items():
            table.add_row(key, provider['name'])
        
        if show_cancel:
            table.add_row("0", "[yellow]Cancel / Skip[/yellow]")
        
        self.console.print(Panel(table, border_style="blue"))
    
    def _get_saved_providers(self) -> Dict[str, str]:
        """
        Get list of providers with saved API keys
        
        Returns:
            Dict mapping display number to provider ID
        """
        saved = {}
        idx = 1
        
        for provider_id, provider in LLM_PROVIDERS.items():
            if os.getenv(provider['env_key']):
                saved[str(idx)] = provider_id
                idx += 1
        
        return saved
    
    def check_env_exists(self) -> bool:
        """Check if .env file exists with required configuration"""
        if not os.path.exists(self.env_path):
            return False
        
        # Check if at least one API key is configured
        load_dotenv(self.env_path)
        active_provider = self.get_active_provider()
        
        return active_provider is not None
