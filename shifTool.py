import sys
import os
import subprocess
import importlib.util
import time
import json
import shutil
import platform
import webbrowser
import tkinter as tk
from tkinter import filedialog

# ==========================================
# CONFIGURAÇÕES GERAIS E INTERNACIONALIZAÇÃO (i18n)
# ==========================================
THEME_COLOR = "#FF6B6B"
CONFIG_FILE = "config.json"

# Gerenciador de Dependências do Projeto (Atualizado)
REQUIRED_PACKAGES = {
    "yt_dlp": {"pkg": "yt-dlp", "size": "~15 MB"},
    "fitz": {"pkg": "pymupdf", "size": "~35 MB"},
    "docx2pdf": {"pkg": "docx2pdf", "size": "~5 MB"},
    "rich": {"pkg": "rich", "size": "~10 MB"},
    "pyfiglet": {"pkg": "pyfiglet", "size": "~1 MB"},
    "PIL": {"pkg": "pillow", "size": "~10 MB"},
    "moviepy": {"pkg": "moviepy", "size": "~20 MB"},
    "imageio_ffmpeg": {"pkg": "imageio-ffmpeg", "size": "~40 MB"},
    "pandas": {"pkg": "pandas", "size": "~35 MB"},
    "openpyxl": {"pkg": "openpyxl", "size": "~3 MB"},
    "pypdf": {"pkg": "pypdf", "size": "~3 MB"}
}

def load_initial_lang():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                return loaded.get("language", "pt")
        except Exception:
            pass
    return "pt"

CURRENT_LANG = load_initial_lang()

I18N = {
    "pt": {
        # Dependências de Inicialização
        "dep_warning_title": "[AVISO] Dependências ausentes detectadas:",
        "dep_warning_desc": "Para o funcionamento completo do shifTool, estes pacotes são necessários.",
        "dep_prompt": "Deseja baixar e instalar as dependências ausentes agora? [S/N]",
        "dep_installing_start": "Instalando dependências ausentes...",
        "dep_installing_pkg": "[bold {theme}]Instalando {pkg}...[/bold {theme}]",
        "dep_success": "\n[bold green]✓ Dependências instaladas com sucesso![/bold green]\n",
        "dep_error": "\n[bold red]Erro ao instalar dependências automaticamente:[/] {error}",
        "dep_declined": "\n[bold yellow]Instalação recusada pelo usuário. Encerrando o aplicativo. Até logo![/bold yellow]\n",
        "config_save_error": "\n[bold red]Erro ao salvar arquivo de configuração:[/] {error}",
        "lo_convert_error": "Não foi possível realizar a conversão do documento.",
        "spreadsheet_error": "Erro ao processar a planilha/dados: {error}",

        # Geral & Erros
        "invalid_choice": "[bold red]Opção inválida![/bold red] Escolha uma das opções disponíveis no menu.",
        "press_enter": "\nPressione [bold]Enter[/bold] para continuar...",
        "press_enter_menu": "\nPressione [bold]Enter[/bold] para retornar ao menu principal...",
        "select_option": "Selecione uma opção",
        "goodbye": "\n[bold {theme}]Encerrando o shifTool. Até logo![/]",
        "interrupted": "\n\n[bold {theme}]Programa interrompido pelo usuário. Saindo...[/]",
        "op_canceled": "\n[bold {theme}]Operação cancelada pelo usuário. Retornando ao menu...[/]",
        
        # Menu Principal
        "menu_main_title": "[bold white]Menu Principal[/]",
        "menu_opt_1": " Transformador Universal de Documentos / Arquivos",
        "menu_opt_2": " Conversor de Mídia",
        "menu_opt_3": " Configurações",
        "menu_opt_4": " Sair / Encerrar o Aplicativo",

        # Submenu - Conversor de Mídia
        "media_menu_title": "[bold white]Conversor de Mídia[/]",
        "media_opt_1": " Converter mídia via link do YouTube",
        "media_opt_2": " Converter mídia local",
        "media_opt_0": " Voltar ao Menu Principal",
        
        "local_media_title": "[bold white]Converter Mídia Local[/]",
        "local_media_desc": "Selecione um arquivo de vídeo do seu computador para extrair o áudio em MP3 de forma rápida e limpa.",
        "local_media_prompt": "\nArraste e solte o arquivo de vídeo abaixo, digite o caminho ou [bold {theme}]0 para voltar[/]:",
        "local_media_converting": "Extraindo áudio (MP3)...",
        
        # Menu Configurações
        "menu_settings_title": "[bold white]Menu de Configurações[/]",
        "settings_status_ask": "Sempre perguntar onde salvar",
        "settings_status_auto": "Salvar automaticamente em: {dir}",
        "settings_current_status": " [dim]Salvamento Atual:[/] [bold white]{status}[/bold white]\n [dim]Idioma Atual:[/] [bold white]Português (pt)[/bold white]\n\n",
        "settings_opt_1": " Alterar Idioma / Change Language",
        "settings_opt_2": " Configurar Comportamento de Salvamento",
        "settings_opt_3": " Verificar e Atualizar Dependências",
        "settings_opt_4": " Sobre o shifTool / Créditos",
        "settings_opt_0": " Voltar ao Menu Principal",
        
        # Atualizador de Dependências
        "updater_check_title": "[bold white]Verificador de Dependências[/]",
        "updater_check_desc": "Fazendo varredura nas bibliotecas essenciais do sistema...",
        "updater_checking": "Verificando pacotes no PyPI...",
        "updater_up_to_date": "\n[bold green]✓ Todos os pacotes essenciais estão atualizados![/bold green]",
        "updater_needs_update": "\n[bold yellow]Pacotes com atualização disponível:[/] {pkgs}",
        "updater_ask_update": "\nDeseja baixar e atualizar estes pacotes agora? [S/N]",
        "updater_updating": "Atualizando pacotes...",
        "updater_success": "\n[bold green]✓ Ferramentas atualizadas com sucesso![/bold green]",
        "updater_error": "\n[bold red]Erro ao atualizar as ferramentas:[/bold red] {error}",

        # Sobre / Créditos
        "about_title": "[bold white]Sobre o shifTool[/]",
        "about_version": "[bold white]Versão:[/bold white] v1.1",
        "about_desc": "Ferramenta CLI multifuncional para conversão universal de arquivos.",
        "about_credits": "[bold white]Criado por:[/bold white] Igor\n[bold white]GitHub:[/bold white] [bold {theme}]https://github.com/igmunizw[/bold {theme}]",

        # Idiomas
        "lang_menu_title": "[bold white]Selecione o Idioma / Select Language[/]",
        "lang_opt_1": " Português (pt)",
        "lang_opt_2": " English (en)",
        "lang_opt_0": " Voltar ao Menu Anterior / Back to Previous Menu",
        "lang_changed": "\n[bold green]✓ Idioma alterado com sucesso para Português![/bold green]",
        
        # Salvamento
        "settings_behavior_title": "[bold white]Configurar Comportamento de Salvamento[/]",
        "settings_current_mode": "[bold white]Modo Atual de Salvamento:[/bold white]\n[bold {theme}]{status}[/bold {theme}]",
        "settings_desc_prompt": "\nEscolha como o sistema deve tratar os arquivos convertidos:",
        "settings_desc_A": " Sempre perguntar onde salvar (Abrir janela a cada conversão)",
        "settings_desc_B": " Salvar automaticamente em uma pasta padrão predefinida",
        "settings_desc_0": " Voltar ao Menu Anterior",
        "settings_saved_ask": "\n[bold green]✓ Configuração salva:[/] O aplicativo sempre perguntará onde salvar os arquivos.",
        "settings_saved_auto": "\n[bold green]✓ Configuração salva:[/] Arquivos serão salvos automaticamente em:\n[bold white]{dir}[/bold white]",
        "settings_no_folder": "\n[bold yellow]Nenhuma pasta foi selecionada. Mantendo configuração anterior.[/bold yellow]",
        
        # Conversor Universal
        "tool_title": "[bold white]Conversor Universal (shifTool)[/]",
        "tool_desc": "O shifTool converte imagens, documentos, textos puros e planilhas.\nFormatos suportados: [bold {theme}]PNG, JPG, WEBP, PDF, DOCX, TXT, MD, XLSX, CSV, JSON[/].",
        "prompt_file": "\nArraste e solte o arquivo abaixo, digite o caminho ou [bold {theme}]0 para voltar[/]:",
        "file_not_found": "\n[bold red]Erro:[/bold red] O arquivo '{filepath}' não foi encontrado.",
        "invalid_format": "\n[bold red]Erro:[/bold red] Formato de entrada não suportado.\nForneça uma imagem, documento de texto, planilha suportada ou PDF.",
        "file_detected": "\n[bold]Arquivo detectado:[/bold] {filename} [dim]({ext})[/dim]",
        
        "select_target": "[bold white]Selecione o formato de saída desejado:[/]\n",
        "target_opt_0": " Voltar ao Menu Anterior",
        "target_prompt": "\nOpção de destino",
        
        # YouTube ...
        "yt_title": "[bold white]Baixador do YouTube[/]",
        "yt_desc": "Baixe vídeos em MP4 ou extraia áudios em MP3 do YouTube com alta qualidade utilizando o yt-dlp.",
        "yt_prompt_url": "\nCole o link (URL) do vídeo do YouTube abaixo ou digite [bold {theme}]0 para voltar[/]:",
        "yt_format_title": "[bold white]Selecione o Formato de Download[/]",
        "yt_format_opt_1": " Baixar como Vídeo (MP4)",
        "yt_format_opt_2": " Baixar como Áudio (MP3)",
        "yt_format_opt_0": " Voltar ao Menu Anterior",
        "yt_video_quality_title": "[bold white]Selecionar Qualidade do Vídeo (MP4)[/]",
        "yt_vqual_1": " Melhor Qualidade Disponível (Best)",
        "yt_vqual_2": " Alta Definição (1080p)",
        "yt_vqual_3": " Padrão (720p)",
        "yt_vqual_0": " Voltar ao Menu Anterior",
        "yt_audio_quality_title": "[bold white]Selecionar Qualidade do Áudio (MP3)[/]",
        "yt_aqual_1": " Melhor Qualidade (Bitrate máximo)",
        "yt_aqual_2": " Alta Qualidade (192 kbps)",
        "yt_aqual_3": " Qualidade Padrão (128 kbps)",
        "yt_aqual_0": " Voltar ao Menu Anterior",
        "yt_downloading": "\n[bold {theme}]Iniciando o download do YouTube...[/bold {theme}]",
        "yt_downloading_progress": "Baixando...",
        "yt_processing_media": "Processando mídia...",
        "yt_plain_downloading": "Baixando: {percent}",
        "yt_plain_done": "\nConcluído!",
        "yt_label_video": "Vídeo MP4",
        "yt_label_audio": "Áudio MP3",
        "yt_success_title": "[bold white]Download Concluído[/]",
        "yt_success_msg": "[bold green]Download realizado com sucesso![/bold green]\n\n[bold]Título:[/bold] {title}\n[bold]Salvo em:[/bold] {dst}",
        "yt_error": "\n[bold red]Erro durante o processamento:[/bold red]\n{error}",
        "yt_missing_dep": "\n[bold red]Recurso Indisponível:[/bold red] Uma biblioteca necessária não está instalada.",
        
        # Dependências do LibreOffice
        "lo_title_win": "[bold white]Instruções de Instalação[/]",
        "lo_title_linux": "[bold white]Instalação no Linux[/]",
        "lo_title_mac": "[bold white]Instalação no macOS[/]",
        "lo_missing_win": "[bold red]Dependência Ausente: LibreOffice[/bold red]\n\nPara converter arquivos de texto ([bold {theme}].docx, .doc, .odt[/]) no Windows, é necessário instalar o LibreOffice.\n\n[bold white]Passo a passo para instalação:[/bold white]\n [bold {theme}]1.[/] O navegador foi aberto na página oficial do LibreOffice.\n [bold {theme}]2.[/] Clique no botão de download da versão mais recente.\n [bold {theme}]3.[/] Abra o arquivo baixado e siga os passos do instalador.\n [bold {theme}]4.[/] Reinicie este aplicativo após a instalação.",
        "lo_missing_linux": "[bold red]Dependência Ausente: LibreOffice[/bold red]\n\nPara converter arquivos de texto no Linux, o pacote LibreOffice precisa estar instalado.",
        "lo_missing_mac": "[bold red]Dependência Ausente: LibreOffice[/bold red]\n\nO navegador foi aberto para você baixar o LibreOffice correspondente ao seu sistema.",
        "lo_linux_try": "\n[bold yellow]Tentando instalar automaticamente via gerenciador de pacotes...[/bold yellow]",
        "lo_linux_fail": "\n[bold red]Não foi possível instalar automaticamente.[/bold red]\n\nExecute o comando manual no terminal referente à sua distribuição.",
        
        # Progresso e Sucesso
        "dialog_saving": "\n[dim]Abrindo caixa de diálogo para salvamento...[/dim]",
        "progress_reading": "[bold {theme}]Lendo/Processando arquivo...",
        "progress_converting": "[bold {theme}]Convertendo {src} -> {tgt}...",
        "progress_done": "[bold green]Concluído!",
        "success_title": "[bold white]Sucesso[/]",
        "success_msg": "[bold green]Conversão concluída com sucesso![/bold green]\n\n[bold]Origem:[/bold] {src}\n[bold]Conversão:[/bold] {ext_src} [bold {theme}]➔[/] {tgt}\n[bold]Salvo em:[/bold] {dst}",
        "error_unexpected": "\n[bold red]Erro inesperado durante a operação:[/bold red]\n{error}",
        
        # Caixa de Diálogo Tkinter
        "tk_save_title": "Salvar como {label}...",
        "tk_file_type": "Arquivo {label}",
        "tk_all_files": "Todos os arquivos",
        "tk_dir_title": "Selecione a pasta padrão para salvamento"
    },
    "en": {
        # Initial Dependencies
        "dep_warning_title": "[WARNING] Missing dependencies detected:",
        "dep_warning_desc": "For full functionality of shifTool, these packages are required.",
        "dep_prompt": "Do you want to download and install missing dependencies now? [Y/N]",
        "dep_installing_start": "Installing missing dependencies...",
        "dep_installing_pkg": "[bold {theme}]Installing {pkg}...[/bold {theme}]",
        "dep_success": "\n[bold green]✓ Dependencies successfully installed![/bold green]\n",
        "dep_error": "\n[bold red]Error installing dependencies automatically:[/] {error}",
        "dep_declined": "\n[bold yellow]Installation declined by user. Closing application. Goodbye![/bold yellow]\n",
        "config_save_error": "\n[bold red]Error saving configuration file:[/] {error}",
        "lo_convert_error": "Could not perform document conversion.",
        "spreadsheet_error": "Error processing spreadsheet/data: {error}",

        # General & Errors
        "invalid_choice": "[bold red]Invalid option![/bold red] Please choose one of the available options from the menu.",
        "press_enter": "\nPress [bold]Enter[/bold] to continue...",
        "press_enter_menu": "\nPress [bold]Enter[/bold] to return to the main menu...",
        "select_option": "Select an option",
        "goodbye": "\n[bold {theme}]Closing shifTool. Goodbye![/]",
        "interrupted": "\n\n[bold {theme}]Program interrupted by user. Exiting...[/]",
        "op_canceled": "\n[bold {theme}]Operation canceled by user. Returning to menu...[/]",
        
        # Main Menu
        "menu_main_title": "[bold white]Main Menu[/]",
        "menu_opt_1": " Universal Document / File Transformer",
        "menu_opt_2": " Media Converter",
        "menu_opt_3": " Settings",
        "menu_opt_4": " Exit / Close Application",

        # Media Converter
        "media_menu_title": "[bold white]Media Converter[/]",
        "media_opt_1": " Convert media via YouTube link",
        "media_opt_2": " Convert local media",
        "media_opt_0": " Back to Main Menu",
        
        "local_media_title": "[bold white]Convert Local Media[/]",
        "local_media_desc": "Select a video file from your computer to extract the audio to MP3 quickly and cleanly.",
        "local_media_prompt": "\nDrag and drop the video file below, type the path, or enter [bold {theme}]0 to go back[/]:",
        "local_media_converting": "Extracting audio (MP3)...",
        
        # Settings Menu
        "menu_settings_title": "[bold white]Settings Menu[/]",
        "settings_status_ask": "Always ask where to save",
        "settings_status_auto": "Save automatically to: {dir}",
        "settings_current_status": " [dim]Current Saving:[/] [bold white]{status}[/bold white]\n [dim]Current Language:[/] [bold white]English (en)[/bold white]\n\n",
        "settings_opt_1": " Change Language / Alterar Idioma",
        "settings_opt_2": " Configure Save Behavior",
        "settings_opt_3": " Check and Update Dependencies",
        "settings_opt_4": " About shifTool / Credits",
        "settings_opt_0": " Back to Main Menu",
        
        # Dependency Updater
        "updater_check_title": "[bold white]Dependency Checker[/]",
        "updater_check_desc": "Scanning shifTool essential libraries...",
        "updater_checking": "Checking packages on PyPI...",
        "updater_up_to_date": "\n[bold green]✓ All essential packages are up to date![/bold green]",
        "updater_needs_update": "\n[bold yellow]Packages with updates available:[/] {pkgs}",
        "updater_ask_update": "\nDo you want to download and update these packages now? [Y/N]",
        "updater_updating": "Updating packages...",
        "updater_success": "\n[bold green]✓ Tools successfully updated![/bold green]",
        "updater_error": "\n[bold red]Error updating tools:[/bold red] {error}",

        # About / Credits
        "about_title": "[bold white]About shifTool[/]",
        "about_version": "[bold white]Version:[/bold white] v1.1",
        "about_desc": "Multifunctional CLI tool for universal file conversion.",
        "about_credits": "[bold white]Created by:[/bold white] Igor\n[bold white]GitHub:[/bold white] [bold {theme}]https://github.com/igmunizw[/bold {theme}]",

        # Languages
        "lang_menu_title": "[bold white]Select Language / Selecione o Idioma[/]",
        "lang_opt_1": " Português (pt)",
        "lang_opt_2": " English (en)",
        "lang_opt_0": " Back to Previous Menu / Voltar ao Menu Anterior",
        "lang_changed": "\n[bold green]✓ Language successfully changed to English![/bold green]",
        
        # Saving
        "settings_behavior_title": "[bold white]Configure Save Behavior[/]",
        "settings_current_mode": "[bold white]Current Save Mode:[/bold white]\n[bold {theme}]{status}[/bold {theme}]",
        "settings_desc_prompt": "\nChoose how the system should handle converted files:",
        "settings_desc_A": " Always ask where to save (Open dialog box on every conversion)",
        "settings_desc_B": " Save automatically to a predefined default folder",
        "settings_desc_0": " Back to Previous Menu",
        "settings_saved_ask": "\n[bold green]✓ Setting saved:[/] The application will always ask where to save files.",
        "settings_saved_auto": "\n[bold green]✓ Setting saved:[/] Files will be saved automatically in:\n[bold white]{dir}[/bold white]",
        "settings_no_folder": "\n[bold yellow]No folder selected. Keeping previous settings.[/bold yellow]",
        
        # Universal Converter
        "tool_title": "[bold white]Universal Converter (shifTool)[/]",
        "tool_desc": "shifTool converts images, documents, pure texts, and spreadsheets.\nSupported formats: [bold {theme}]PNG, JPG, WEBP, PDF, DOCX, TXT, MD, XLSX, CSV, JSON[/].",
        "prompt_file": "\nDrag and drop the file below, type the path, or enter [bold {theme}]0 to go back[/]:",
        "file_not_found": "\n[bold red]Error:[/bold red] File '{filepath}' was not found.",
        "invalid_format": "\n[bold red]Error:[/bold red] Unsupported input format.\nPlease provide a supported image, document, spreadsheet, or PDF.",
        "file_detected": "\n[bold]File detected:[/bold] {filename} [dim]({ext})[/dim]",
        
        "select_target": "[bold white]Select the output format for conversion:[/]\n",
        "target_opt_0": " Back to Previous Menu",
        "target_prompt": "\nTarget format option",
        
        # YouTube Downloader ...
        "yt_title": "[bold white]YouTube Downloader[/]",
        "yt_desc": "Download videos as MP4 or extract audio as MP3 from YouTube in high quality using yt-dlp.",
        "yt_prompt_url": "\nPaste the YouTube video URL below or type [bold {theme}]0 to go back[/]:",
        "yt_format_title": "[bold white]Select Download Format[/]",
        "yt_format_opt_1": " Download as Video (MP4)",
        "yt_format_opt_2": " Download as Audio (MP3)",
        "yt_format_opt_0": " Back to Previous Menu",
        "yt_video_quality_title": "[bold white]Select Video Quality (MP4)[/]",
        "yt_vqual_1": " Best Available Quality (Best)",
        "yt_vqual_2": " High Definition (1080p)",
        "yt_vqual_3": " Standard Definition (720p)",
        "yt_vqual_0": " Back to Previous Menu",
        "yt_audio_quality_title": "[bold white]Select Audio Quality (MP3)[/]",
        "yt_aqual_1": " Best Quality (Max bitrate)",
        "yt_aqual_2": " High Quality (192 kbps)",
        "yt_aqual_3": " Standard Quality (128 kbps)",
        "yt_aqual_0": " Back to Previous Menu",
        "yt_downloading": "\n[bold {theme}]Starting YouTube download...[/bold {theme}]",
        "yt_downloading_progress": "Downloading...",
        "yt_processing_media": "Processing media...",
        "yt_plain_downloading": "Downloading: {percent}",
        "yt_plain_done": "\nDone!",
        "yt_label_video": "MP4 Video",
        "yt_label_audio": "MP3 Audio",
        "yt_success_title": "[bold white]Download Completed[/]",
        "yt_success_msg": "[bold green]Download completed successfully![/bold green]\n\n[bold]Title:[/bold] {title}\n[bold]Saved to:[/bold] {dst}",
        "yt_error": "\n[bold red]Error during process:[/bold red]\n{error}",
        "yt_missing_dep": "\n[bold red]Feature Unavailable:[/bold red] A required library is not installed.",
        
        # LibreOffice Dependencies
        "lo_title_win": "[bold white]Installation Instructions[/]",
        "lo_title_linux": "[bold white]Linux Installation[/]",
        "lo_title_mac": "[bold white]macOS Installation[/]",
        "lo_missing_win": "[bold red]Missing Dependency: LibreOffice[/bold red]\n\nTo convert text documents on Windows, LibreOffice must be installed.\n\n[bold white]Step-by-step installation:[/bold white]\n [bold {theme}]1.[/] Your browser opened to the official LibreOffice download page.\n [bold {theme}]2.[/] Click the download button for the latest version.\n [bold {theme}]3.[/] Run the installer and complete the setup wizard.\n [bold {theme}]4.[/] Restart this CLI app after installation.",
        "lo_missing_linux": "[bold red]Missing Dependency: LibreOffice[/bold red]\n\nTo convert text documents on Linux, the LibreOffice package must be installed.",
        "lo_missing_mac": "[bold red]Missing Dependency: LibreOffice[/bold red]\n\nYour browser was opened to download LibreOffice.",
        "lo_linux_try": "\n[bold yellow]Attempting automatic installation via package manager...[/bold yellow]",
        "lo_linux_fail": "\n[bold red]Could not install automatically.[/bold red]\n\nRun the manual terminal command for your distribution.",
        
        # Progress and Success
        "dialog_saving": "\n[dim]Opening file save dialog...[/dim]",
        "progress_reading": "[bold {theme}]Reading/Processing file...",
        "progress_converting": "[bold {theme}]Converting {src} -> {tgt}...",
        "progress_done": "[bold green]Done!",
        "success_title": "[bold white]Success[/]",
        "success_msg": "[bold green]Conversion completed successfully![/bold green]\n\n[bold]Source:[/bold] {src}\n[bold]Conversion:[/bold] {ext_src} [bold {theme}]➔[/] {tgt}\n[bold]Saved to:[/bold] {dst}",
        "error_unexpected": "\n[bold red]Unexpected error during operation:[/bold red]\n{error}",
        
        # Tkinter File Dialogs
        "tk_save_title": "Save as {label}...",
        "tk_file_type": "{label} File",
        "tk_all_files": "All Files",
        "tk_dir_title": "Select default directory for saving"
    }
}

def get_text(key, **kwargs):
    lang_dict = I18N.get(CURRENT_LANG, I18N["pt"])
    text = lang_dict.get(key, I18N["pt"].get(key, key))
    if "{theme}" in text:
        kwargs["theme"] = THEME_COLOR
    try:
        return text.format(**kwargs)
    except Exception:
        return text

# ==========================================
# GERENCIADOR POLIDO DE DEPENDÊNCIAS
# ==========================================

def check_and_install_dependencies():
    missing_mods = []
    missing_display = []
    
    for mod_name, info in REQUIRED_PACKAGES.items():
        if importlib.util.find_spec(mod_name) is None:
            missing_mods.append(info["pkg"])
            missing_display.append(f" • {info['pkg']} ({info['size']})")
    
    if missing_mods:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*70)
        print(f" {get_text('dep_warning_title')}")
        for item in missing_display:
            print(item)
        print(f"\n {get_text('dep_warning_desc')}")
        print("="*70)
        
        prompt_str = f" {get_text('dep_prompt')}: "
        choice = input(prompt_str).strip().lower()
        if choice in ['s', 'sim', 'y', 'yes']:
            if importlib.util.find_spec("rich") is None:
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", "rich"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                except Exception:
                    pass
            
            has_rich_local = importlib.util.find_spec("rich") is not None
            if has_rich_local:
                from rich.console import Console as LocalConsole
                from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
                
                local_console = LocalConsole()
                print()
                try:
                    with Progress(
                        SpinnerColumn(style=THEME_COLOR),
                        TextColumn("[progress.description]{task.description}"),
                        BarColumn(complete_style=THEME_COLOR, finished_style=THEME_COLOR),
                        TimeElapsedColumn(),
                        console=local_console
                    ) as progress:
                        task = progress.add_task(get_text("dep_installing_start"), total=len(missing_mods))
                        for pkg in missing_mods:
                            progress.update(task, description=get_text("dep_installing_pkg", pkg=pkg))
                            subprocess.check_call(
                                [sys.executable, "-m", "pip", "install", pkg],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL
                            )
                            progress.advance(task, 1)
                    print(get_text("dep_success"))
                    time.sleep(1.5)
                except Exception as e:
                    print(get_text("dep_error", error=e))
                    sys.exit(1)
            else:
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", *missing_mods],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    print(get_text("dep_success"))
                    time.sleep(1.5)
                except Exception as e:
                    print(get_text("dep_error", error=e))
                    sys.exit(1)
        else:
            print(get_text("dep_declined"))
            sys.exit(0)

check_and_install_dependencies()

# ==========================================
# IMPORTAÇÕES SEGURAS E FLAGS DE DISPONIBILIDADE
# ==========================================
HAS_RICH = importlib.util.find_spec("rich") is not None
HAS_PYFIGLET = importlib.util.find_spec("pyfiglet") is not None
HAS_PIL = importlib.util.find_spec("PIL") is not None
HAS_YT_DLP = importlib.util.find_spec("yt_dlp") is not None
HAS_PYMUPDF = importlib.util.find_spec("fitz") is not None
HAS_DOCX2PDF = importlib.util.find_spec("docx2pdf") is not None
HAS_MOVIEPY = importlib.util.find_spec("moviepy") is not None
HAS_IMAGEIO_FFMPEG = importlib.util.find_spec("imageio_ffmpeg") is not None
HAS_PANDAS = importlib.util.find_spec("pandas") is not None
HAS_PYPDF = importlib.util.find_spec("pypdf") is not None

if HAS_RICH:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.align import Align
    from rich.progress import (
        Progress, SpinnerColumn, TextColumn, BarColumn,
        TimeElapsedColumn, TransferSpeedColumn, TimeRemainingColumn
    )
    console = Console()
else:
    class DummyConsole:
        def print(self, *args, **kwargs):
            print(*args)
        def input(self, prompt=""):
            return input(prompt)
    console = DummyConsole()

if HAS_PYFIGLET:
    import pyfiglet

if HAS_PIL:
    from PIL import Image

if HAS_YT_DLP:
    import yt_dlp

if HAS_IMAGEIO_FFMPEG:
    import imageio_ffmpeg

class QuietLogger:
    def debug(self, msg): pass
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    """Exibe o cabeçalho oficial do aplicativo com a logo ASCII shifTool."""
    if HAS_PYFIGLET:
        ascii_art = pyfiglet.figlet_format("shifTool", font="slant")
        ascii_art = "\n".join(line for line in ascii_art.splitlines() if line.strip())
        styled_title = Text(ascii_art, style=f"bold {THEME_COLOR}")
        console.print(Align.center(styled_title))
    else:
        console.print("=== shifTool ===")
    console.print()

def ask_choice(prompt_text, choices, show_choices=True):
    choices_display = "/".join(choices) if show_choices else ""
    prompt_suffix = f" [[bold {THEME_COLOR}]{choices_display}[/]]" if show_choices else ""
    full_prompt = f"{prompt_text}{prompt_suffix}: "
    
    while True:
        choice = console.input(full_prompt).strip()
        matching_choice = next((c for c in choices if c.lower() == choice.lower()), None)
        if matching_choice is not None:
            return matching_choice
        
        console.print()
        if HAS_RICH:
            console.print(Panel(get_text("invalid_choice"), border_style=THEME_COLOR))
        else:
            console.print(get_text("invalid_choice"))
        console.print()

# ==========================================
# GERENCIADOR DE CONFIGURAÇÕES (JSON & i18n)
# ==========================================

def load_config():
    global CURRENT_LANG
    
    # 1. Define o caminho dinâmico para a pasta "Documentos" do usuário
    default_docs = os.path.join(os.path.expanduser("~"), "Documents")
    # Se por acaso o Windows/Linux do usuário não tiver a pasta Documents, joga na pasta Home
    if not os.path.exists(default_docs):
        default_docs = os.path.expanduser("~") 

    config = {"save_mode": "ask", "default_dir": default_docs, "language": "pt"}
    
    # 2. Verifica se o arquivo já existe
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                config.update(loaded)
        except Exception:
            # Se o arquivo existir mas estiver corrompido/vazio, ele se auto-conserta
            save_config(config)
    else:
        # 3. SE NÃO EXISTIR: Cria o arquivo físico automaticamente na primeira execução!
        save_config(config)
            
    CURRENT_LANG = config.get("language", "pt")
    return config

def save_config(config_data):
    global CURRENT_LANG
    if "language" in config_data:
        CURRENT_LANG = config_data["language"]
        
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        console.print(get_text("config_save_error", error=e))

def open_save_dialog(default_filename, target_ext, target_label):
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    save_path = filedialog.asksaveasfilename(
        defaultextension=target_ext,
        initialfile=default_filename,
        title=get_text("tk_save_title", label=target_label),
        filetypes=[(get_text("tk_file_type", label=target_label), f"*{target_ext}"), (get_text("tk_all_files"), "*.*")]
    )
    
    root.destroy()
    return save_path

def open_folder_dialog():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    folder_path = filedialog.askdirectory(title=get_text("tk_dir_title"))
    root.destroy()
    return folder_path

def resolve_save_path(default_filename, target_ext, target_label):
    config = load_config()
    if config.get("save_mode") == "auto" and config.get("default_dir"):
        default_dir = config.get("default_dir")
        if os.path.exists(default_dir):
            return os.path.join(default_dir, default_filename)
            
    console.print(get_text("dialog_saving"))
    return open_save_dialog(default_filename, target_ext, target_label)

# ==========================================
# MENU DE CONFIGURAÇÕES E UTILIDADES
# ==========================================

def check_and_update_all_dependencies():
    """Verifica todos os pacotes chave e oferece opção elegante de atualização."""
    clear_screen()
    show_header()
    
    if HAS_RICH:
        console.print(Panel(get_text("updater_check_desc"), title=get_text("updater_check_title"), border_style=THEME_COLOR))
    else:
        console.print(get_text("updater_check_title"))
        console.print(get_text("updater_check_desc"))
        
    console.print()
    
    packages_to_check = ["yt-dlp", "imageio-ffmpeg", "rich", "pymupdf", "docx2pdf", "pillow", "moviepy", "pyfiglet", "pandas", "openpyxl", "pypdf"]
    outdated_pkgs = []
    
    try:
        if HAS_RICH:
            with Progress(
                SpinnerColumn(style=THEME_COLOR),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task(get_text("updater_checking"), total=None)
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "list", "--outdated", "--format=json", "--disable-pip-version-check"],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                
                if result.returncode == 0 and result.stdout.strip():
                    try:
                        data = json.loads(result.stdout)
                        for item in data:
                            if item["name"].lower() in [p.lower() for p in packages_to_check]:
                                outdated_pkgs.append(item["name"])
                    except json.JSONDecodeError:
                        outdated_pkgs = packages_to_check
        else:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--outdated", "--format=json", "--disable-pip-version-check"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                try:
                    data = json.loads(result.stdout)
                    for item in data:
                        if item["name"].lower() in [p.lower() for p in packages_to_check]:
                            outdated_pkgs.append(item["name"])
                except Exception:
                    outdated_pkgs = packages_to_check
                    
    except Exception as e:
        console.print(get_text("updater_error", error=e))
        console.print(get_text("press_enter"))
        console.input()
        return
        
    if not outdated_pkgs:
        console.print(get_text("updater_up_to_date"))
        console.print(get_text("press_enter"))
        console.input()
        return
        
    outdated_str = ", ".join(outdated_pkgs)
    console.print(get_text("updater_needs_update", pkgs=outdated_str))
    
    choice = console.input(get_text("updater_ask_update") + " ").strip().lower()
    if choice in ['s', 'sim', 'y', 'yes']:
        try:
            if HAS_RICH:
                with Progress(
                    SpinnerColumn(style=THEME_COLOR),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(complete_style=THEME_COLOR, finished_style=THEME_COLOR),
                    TimeElapsedColumn(),
                    console=console
                ) as progress:
                    task = progress.add_task(get_text("updater_updating"), total=None)
                    cmd = [sys.executable, "-m", "pip", "install", "--upgrade"] + outdated_pkgs
                    update_result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    
                    if update_result.returncode == 0:
                        progress.update(task, completed=100, total=100, description=f"[bold green]{get_text('progress_done')}")
                        console.print(get_text("updater_success"))
                    else:
                        progress.update(task, description=f"[bold red]Erro!")
                        console.print(get_text("updater_error", error=update_result.stderr))
            else:
                console.print(get_text("updater_updating"))
                cmd = [sys.executable, "-m", "pip", "install", "--upgrade"] + outdated_pkgs
                update_result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if update_result.returncode == 0:
                    console.print(get_text("updater_success"))
                else:
                    console.print(get_text("updater_error", error=update_result.stderr))
                    
        except Exception as e:
            console.print(get_text("updater_error", error=e))
    else:
        console.print(get_text("op_canceled"))
        
    console.print(get_text("press_enter"))
    console.input()

def show_about_credits():
    clear_screen()
    show_header()
    
    ascii_text = "shifTool"
    if HAS_PYFIGLET:
        ascii_text = pyfiglet.figlet_format("shifTool", font="slant")
        ascii_text = "\n".join(line for line in ascii_text.splitlines() if line.strip())
        
    content = (
        f"[bold {THEME_COLOR}]{ascii_text}[/]\n\n"
        f"{get_text('about_version')}\n\n"
        f"{get_text('about_desc')}\n\n"
        f"{get_text('about_credits')}"
    )
    
    if HAS_RICH:
        panel = Panel(Align.center(content), title=get_text("settings_opt_4").strip(), border_style=THEME_COLOR, padding=(1, 4))
        console.print(Align.center(panel))
    else:
        console.print(content)
        
    console.print(get_text("press_enter_menu"))
    console.input()

def change_language_menu():
    clear_screen()
    show_header()
    
    menu_text = (
        f" [[bold {THEME_COLOR}]1[/]]" + get_text("lang_opt_1") + "\n" +
        f" [[bold {THEME_COLOR}]2[/]]" + get_text("lang_opt_2") + "\n" +
        f" [[bold {THEME_COLOR}]0[/]]" + get_text("lang_opt_0")
    )
    
    if HAS_RICH:
        panel = Panel(menu_text, title=get_text("lang_menu_title"), border_style=THEME_COLOR, expand=False, padding=(1, 4))
        console.print(Align.center(panel))
    else:
        console.print(menu_text)
    console.print()
    
    choice = ask_choice(get_text("select_option"), choices=["0", "1", "2"], show_choices=False)
    if choice == "0": return
        
    config = load_config()
    if choice == "1": config["language"] = "pt"
    elif choice == "2": config["language"] = "en"
        
    save_config(config)
    console.print(get_text("lang_changed"))
    console.print(get_text("press_enter"))
    console.input()

def configure_save_behavior():
    clear_screen()
    show_header()
    
    config = load_config()
    current_mode = config.get("save_mode", "ask")
    current_dir = config.get("default_dir", "")
    
    status_str = get_text("settings_status_ask") if current_mode == "ask" else get_text("settings_status_auto", dir=current_dir)
    
    if HAS_RICH:
        console.print(Panel(get_text("settings_current_mode", status=status_str), title=get_text("settings_behavior_title"), border_style=THEME_COLOR))
    else:
        console.print(get_text("settings_current_mode", status=status_str))
    
    console.print(get_text("settings_desc_prompt"))
    console.print(f" [[bold {THEME_COLOR}]A[/]]" + get_text("settings_desc_A"))
    console.print(f" [[bold {THEME_COLOR}]B[/]]" + get_text("settings_desc_B"))
    console.print(f" [[bold {THEME_COLOR}]0[/]]" + get_text("settings_desc_0") + "\n")
    
    choice = ask_choice(get_text("select_option"), choices=["A", "B", "0"], show_choices=False)
    if choice == "0": return
        
    if choice == "A":
        config["save_mode"] = "ask"
        save_config(config)
        console.print(get_text("settings_saved_ask"))
    elif choice == "B":
        console.print("\n[dim]...")
        selected_folder = open_folder_dialog()
        
        if selected_folder:
            config["save_mode"] = "auto"
            config["default_dir"] = selected_folder
            save_config(config)
            console.print(get_text("settings_saved_auto", dir=selected_folder))
        else:
            console.print(get_text("settings_no_folder"))

    console.print(get_text("press_enter"))
    console.input()

def settings_menu():
    while True:
        clear_screen()
        show_header()
        
        config = load_config()
        mode_desc = get_text("settings_status_ask") if config.get("save_mode") == "ask" else get_text("settings_status_auto", dir=config.get("default_dir"))
        
        menu_text = (
            get_text("settings_current_status", status=mode_desc) +
            f" [[bold {THEME_COLOR}]1[/]]" + get_text("settings_opt_1") + "\n" +
            f" [[bold {THEME_COLOR}]2[/]]" + get_text("settings_opt_2") + "\n" +
            f" [[bold {THEME_COLOR}]3[/]]" + get_text("settings_opt_3") + "\n" +
            f" [[bold {THEME_COLOR}]4[/]]" + get_text("settings_opt_4") + "\n" +
            f" [[bold {THEME_COLOR}]0[/]]" + get_text("settings_opt_0")
        )
        
        if HAS_RICH:
            panel = Panel(menu_text, title=get_text("menu_settings_title"), border_style=THEME_COLOR, expand=False, padding=(1, 4))
            console.print(Align.center(panel))
        else:
            console.print(menu_text)
        console.print()
        
        choice = ask_choice(get_text("select_option"), choices=["0", "1", "2", "3", "4"], show_choices=False)
        
        if choice == "1": change_language_menu()
        elif choice == "2": configure_save_behavior()
        elif choice == "3": check_and_update_all_dependencies()
        elif choice == "4": show_about_credits()
        elif choice == "0": break

def find_libreoffice_binary():
    cmd = shutil.which("libreoffice") or shutil.which("soffice")
    if cmd: return cmd
        
    system = platform.system()
    if system == "Windows":
        possible_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
        ]
        for path in possible_paths:
            if os.path.exists(path): return path
    elif system == "Darwin":
        mac_path = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
        if os.path.exists(mac_path): return mac_path
    return None

def handle_libreoffice_dependency():
    current_os = platform.system()
    if current_os == "Windows":
        url = "https://www.libreoffice.org/download/download/"
        webbrowser.open(url)
        if HAS_RICH:
            console.print(Panel(get_text("lo_missing_win"), title=get_text("lo_title_win"), border_style=THEME_COLOR))
        else:
            console.print(get_text("lo_missing_win"))
    elif current_os == "Linux":
        if HAS_RICH:
            console.print(Panel(get_text("lo_missing_linux"), title=get_text("lo_title_linux"), border_style=THEME_COLOR))
        else:
            console.print(get_text("lo_missing_linux"))
        console.print(get_text("lo_linux_try"))

        installed = False
        try:
            if shutil.which("apt"):
                res = subprocess.run("sudo apt update && sudo apt install -y libreoffice", shell=True)
                installed = (res.returncode == 0)
            elif shutil.which("dnf"):
                res = subprocess.run("sudo dnf install -y libreoffice", shell=True)
                installed = (res.returncode == 0)
            elif shutil.which("pacman"):
                res = subprocess.run("sudo pacman -S --noconfirm libreoffice-fresh", shell=True)
                installed = (res.returncode == 0)
        except Exception:
            installed = False

        if not installed:
            console.print(get_text("lo_linux_fail"))
    else:
        url = "https://www.libreoffice.org/download/download/"
        webbrowser.open(url)
        if HAS_RICH:
            console.print(Panel(get_text("lo_missing_mac"), title=get_text("lo_title_mac"), border_style=THEME_COLOR))
        else:
            console.print(get_text("lo_missing_mac"))

    console.print(get_text("press_enter_menu"))
    console.input()
    return False

# ==========================================
# FUNÇÕES DE CONVERSÃO (Novo & Antigo)
# ==========================================

# Textos e Markdown
def convert_text_format(filepath, save_path):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(content)

# Extração de PDF para Texto (Usando pypdf leve)
def extract_text_from_pdf(filepath, save_path):
    if not HAS_PYPDF: raise RuntimeError("Dependência 'pypdf' necessária para extrair texto.")
    import pypdf
    text = ""
    with open(filepath, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(text)

# Dados e Planilhas (Usando pandas robusto)
def convert_spreadsheet(filepath, target_ext, save_path):
    if not HAS_PANDAS: raise RuntimeError("Dependência 'pandas' não está instalada.")
    import pandas as pd
    source_ext = os.path.splitext(filepath)[1].lower()

    try:
        if source_ext == ".xlsx":
            df = pd.read_excel(filepath)
        elif source_ext == ".csv":
            df = pd.read_csv(filepath)
        elif source_ext == ".json":
            df = pd.read_json(filepath)
        else:
            raise ValueError(f"Formato de entrada não suportado: {source_ext}")

        if target_ext == ".xlsx":
            df.to_excel(save_path, index=False)
        elif target_ext == ".csv":
            df.to_csv(save_path, index=False)
        elif target_ext == ".json":
            df.to_json(save_path, orient="records", indent=4, force_ascii=False)
        else:
            raise ValueError(f"Formato de saída não suportado: {target_ext}")
    except Exception as e:
        raise RuntimeError(get_text("spreadsheet_error", error=str(e)))

# Imagens e Documentos Clássicos
def convert_image_to_image(filepath, target_ext, save_path):
    if not HAS_PIL: raise RuntimeError("Pillow dependency is missing.")
    with Image.open(filepath) as img:
        if target_ext in [".jpg", ".jpeg", ".bmp"]:
            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P": img = img.convert("RGBA")
                if img.mode in ("RGBA", "LA"):
                    background.paste(img, mask=img.split()[-1])
                    output_img = background
                else:
                    output_img = img.convert("RGB")
            else:
                output_img = img.convert("RGB")
        else:
            output_img = img.convert("RGBA") if img.mode == "P" else img
                
        output_img.save(save_path)

def convert_image_to_pdf(filepath, save_path):
    if not HAS_PIL: raise RuntimeError("Pillow dependency is missing.")
    with Image.open(filepath) as img:
        pdf_image = img.convert("RGB")
        pdf_image.save(save_path, "PDF", resolution=100.0)

def convert_pdf_to_image(filepath, target_ext, save_path):
    if not HAS_PYMUPDF: raise RuntimeError("PyMuPDF dependency is required.")
    try:
        import fitz
        doc = fitz.open(filepath)
        page = doc[0]
        pix = page.get_pixmap(dpi=150)
        pil_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        doc.close()
    except ImportError:
        raise ImportError("PyMuPDF dependency is required.")

    if target_ext in [".jpg", ".jpeg", ".bmp"]:
        pil_image = pil_image.convert("RGB")
    elif target_ext in [".png", ".webp", ".tiff"]:
        if pil_image.mode not in ("RGB", "RGBA"):
            pil_image = pil_image.convert("RGBA")
            
    pil_image.save(save_path)

def convert_doc_to_pdf(filepath, save_path):
    libreoffice_cmd = find_libreoffice_binary()
    abs_input = os.path.abspath(filepath)
    abs_output = os.path.abspath(save_path)

    if libreoffice_cmd:
        temp_dir = os.path.dirname(abs_output)
        cmd = [libreoffice_cmd, "--headless", "--convert-to", "pdf", abs_input, "--outdir", temp_dir]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            generated_pdf = os.path.join(temp_dir, os.path.splitext(os.path.basename(abs_input))[0] + ".pdf")
            if os.path.exists(generated_pdf) and os.path.abspath(generated_pdf) != abs_output:
                if os.path.exists(abs_output): os.remove(abs_output)
                os.rename(generated_pdf, abs_output)
            return
        else:
            raise RuntimeError(f"LibreOffice Error: {result.stderr.decode('utf-8', errors='ignore')}")
            
    ext = os.path.splitext(filepath)[1].lower()
    if ext in [".docx", ".doc"] and HAS_DOCX2PDF:
        try:
            from docx2pdf import convert
            convert(abs_input, abs_output)
            if os.path.exists(abs_output): return
        except Exception:
            pass

    raise RuntimeError(get_text("lo_convert_error"))

# ==========================================
# FLUXO DO CONVERSOR UNIVERSAL (Expandido)
# ==========================================

def tool_transformador_universal():
    clear_screen()
    show_header()
    
    if HAS_RICH:
        console.print(Panel(get_text("tool_desc"), title=get_text("tool_title"), border_style=THEME_COLOR))
    else:
        console.print(get_text("tool_desc"))
    console.print(get_text("prompt_file"))
    
    raw_path = console.input(f"[bold {THEME_COLOR}]>[/] ").strip()
    if raw_path == "0": return
        
    filepath = raw_path
    if filepath.startswith("&"): filepath = filepath[1:].strip()
    filepath = filepath.strip("'\"")
    
    if not os.path.exists(filepath):
        console.print(get_text("file_not_found", filepath=filepath))
        time.sleep(2.5)
        return
        
    source_ext = os.path.splitext(filepath)[1].lower()
    
    # Categorias suportadas
    valid_image_exts = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif")
    valid_doc_exts = (".docx", ".doc", ".odt")
    valid_text_exts = (".txt", ".md")
    valid_data_exts = (".xlsx", ".csv", ".json")
    
    is_image = source_ext in valid_image_exts
    is_doc = source_ext in valid_doc_exts
    is_text = source_ext in valid_text_exts
    is_data = source_ext in valid_data_exts
    is_pdf = (source_ext == ".pdf")
    
    if not any([is_image, is_doc, is_text, is_data, is_pdf]):
        console.print(get_text("invalid_format"))
        time.sleep(2.5)
        return

    if is_doc and not find_libreoffice_binary():
        handle_libreoffice_dependency()
        return
    
    console.print(get_text("file_detected", filename=os.path.basename(filepath), ext=source_ext.upper()))
    console.print(get_text("select_target"))
    
    valid_options = []
    target_map = {}
    opt_idx = 1
    
    # Construção Dinâmica das Opções baseada no arquivo
    if is_doc:
        console.print(f" [[bold {THEME_COLOR}]{opt_idx}[/]] PDF (.pdf)")
        valid_options.append(str(opt_idx))
        target_map[str(opt_idx)] = (".pdf", "PDF")
        opt_idx += 1
    elif is_pdf:
        targets = [(".png", "PNG"), (".jpg", "JPG"), (".webp", "WEBP"), (".bmp", "BMP"), (".tiff", "TIFF"), (".txt", "Extrair Texto Puro (.txt)")]
        for ext, label in targets:
            console.print(f" [[bold {THEME_COLOR}]{opt_idx}[/]] {label}")
            valid_options.append(str(opt_idx))
            target_map[str(opt_idx)] = (ext, label)
            opt_idx += 1
    elif is_data:
        targets = [ext for ext in [(".xlsx", "Excel (.xlsx)"), (".csv", "CSV (.csv)"), (".json", "JSON (.json)")] if ext[0] != source_ext]
        for ext, label in targets:
            console.print(f" [[bold {THEME_COLOR}]{opt_idx}[/]] {label}")
            valid_options.append(str(opt_idx))
            target_map[str(opt_idx)] = (ext, label)
            opt_idx += 1
    elif is_text:
        targets = [ext for ext in [(".txt", "Texto (.txt)"), (".md", "Markdown (.md)")] if ext[0] != source_ext]
        for ext, label in targets:
            console.print(f" [[bold {THEME_COLOR}]{opt_idx}[/]] {label}")
            valid_options.append(str(opt_idx))
            target_map[str(opt_idx)] = (ext, label)
            opt_idx += 1
    else: # is_image
        targets = [(".png", "PNG"), (".jpg", "JPG"), (".webp", "WEBP"), (".bmp", "BMP"), (".tiff", "TIFF"), (".pdf", "PDF")]
        for ext, label in targets:
            if ext != source_ext and not (source_ext in [".jpg", ".jpeg"] and ext == ".jpg"):
                console.print(f" [[bold {THEME_COLOR}]{opt_idx}[/]] {label}")
                valid_options.append(str(opt_idx))
                target_map[str(opt_idx)] = (ext, label)
                opt_idx += 1
        
    console.print(f" [[bold {THEME_COLOR}]0[/]]" + get_text("target_opt_0"))
    valid_options.append("0")
    
    target_choice = ask_choice(get_text("target_prompt"), choices=valid_options, show_choices=False)
    if target_choice == "0": return
        
    target_ext, target_label = target_map[target_choice]
    default_name = os.path.splitext(os.path.basename(filepath))[0] + target_ext
    save_path = resolve_save_path(default_name, target_ext, target_label)
    
    if not save_path:
        console.print(get_text("op_canceled"))
        time.sleep(1.5)
        return
        
    try:
        if HAS_RICH:
            with Progress(
                SpinnerColumn(style=THEME_COLOR), TextColumn("[progress.description]{task.description}"),
                BarColumn(complete_style=THEME_COLOR, finished_style=THEME_COLOR), TimeElapsedColumn(), console=console
            ) as progress:
                task = progress.add_task(get_text("progress_reading"), total=100)
                time.sleep(0.2)
                progress.update(task, advance=40, description=get_text("progress_converting", src=source_ext.upper(), tgt=target_label))
                
                # Encaminhamento da conversão adequado
                if is_doc: convert_doc_to_pdf(filepath, save_path)
                elif is_pdf:
                    if target_ext == ".txt": extract_text_from_pdf(filepath, save_path)
                    else: convert_pdf_to_image(filepath, target_ext, save_path)
                elif is_data: convert_spreadsheet(filepath, target_ext, save_path)
                elif is_text: convert_text_format(filepath, save_path)
                elif target_ext == ".pdf": convert_image_to_pdf(filepath, save_path)
                else: convert_image_to_image(filepath, target_ext, save_path)
                    
                progress.update(task, advance=60, description=get_text("progress_done"))
                time.sleep(0.2)
        else:
            if is_doc: convert_doc_to_pdf(filepath, save_path)
            elif is_pdf:
                if target_ext == ".txt": extract_text_from_pdf(filepath, save_path)
                else: convert_pdf_to_image(filepath, target_ext, save_path)
            elif is_data: convert_spreadsheet(filepath, target_ext, save_path)
            elif is_text: convert_text_format(filepath, save_path)
            elif target_ext == ".pdf": convert_image_to_pdf(filepath, save_path)
            else: convert_image_to_image(filepath, target_ext, save_path)
            
        if HAS_RICH:
            console.print(Panel(get_text("success_msg", src=filepath, ext_src=source_ext.upper(), tgt=target_label, dst=save_path), title=get_text("success_title"), border_style="green"))
        else:
            console.print(get_text("success_msg", src=filepath, ext_src=source_ext.upper(), tgt=target_label, dst=save_path))
        
    except Exception as e:
        console.print(get_text("error_unexpected", error=e))
        
    console.print(get_text("press_enter"))
    console.input()

# ==========================================
# SUBMENU & FLUXOS DE MÍDIA (YOUTUBE / LOCAL)
# ==========================================

def tool_youtube_downloader():
    if not HAS_YT_DLP:
        clear_screen()
        show_header()
        console.print(get_text("yt_missing_dep"))
        console.print(get_text("press_enter"))
        console.input()
        return

    while True:
        clear_screen()
        show_header()
        
        if HAS_RICH:
            console.print(Panel(get_text("yt_desc"), title=get_text("yt_title"), border_style=THEME_COLOR))
        else:
            console.print(get_text("yt_desc"))
        console.print(get_text("yt_prompt_url"))
        
        url = console.input(f"[bold {THEME_COLOR}]>[/] ").strip()
        if url == "0" or not url: return
            
        clear_screen()
        show_header()
        
        fmt_text = (
            f" [[bold {THEME_COLOR}]1[/]]" + get_text("yt_format_opt_1") + "\n" +
            f" [[bold {THEME_COLOR}]2[/]]" + get_text("yt_format_opt_2") + "\n" +
            f" [[bold {THEME_COLOR}]0[/]]" + get_text("yt_format_opt_0")
        )
        if HAS_RICH:
            panel_fmt = Panel(fmt_text, title=get_text("yt_format_title"), border_style=THEME_COLOR, expand=False, padding=(1, 4))
            console.print(Align.center(panel_fmt))
        else:
            console.print(fmt_text)
        console.print()
        
        fmt_choice = ask_choice(get_text("select_option"), choices=["0", "1", "2"], show_choices=False)
        if fmt_choice == "0": continue
            
        clear_screen()
        show_header()
        
        if fmt_choice == "1":
            qual_text = (
                f" [[bold {THEME_COLOR}]1[/]]" + get_text("yt_vqual_1") + "\n" +
                f" [[bold {THEME_COLOR}]2[/]]" + get_text("yt_vqual_2") + "\n" +
                f" [[bold {THEME_COLOR}]3[/]]" + get_text("yt_vqual_3") + "\n" +
                f" [[bold {THEME_COLOR}]0[/]]" + get_text("yt_vqual_0")
            )
            if HAS_RICH: panel_qual = Panel(qual_text, title=get_text("yt_video_quality_title"), border_style=THEME_COLOR, expand=False, padding=(1, 4))
        else:
            qual_text = (
                f" [[bold {THEME_COLOR}]1[/]]" + get_text("yt_aqual_1") + "\n" +
                f" [[bold {THEME_COLOR}]2[/]]" + get_text("yt_aqual_2") + "\n" +
                f" [[bold {THEME_COLOR}]0[/]]" + get_text("yt_aqual_0")
            )
            if HAS_RICH: panel_qual = Panel(qual_text, title=get_text("yt_audio_quality_title"), border_style=THEME_COLOR, expand=False, padding=(1, 4))
            
        if HAS_RICH: console.print(Align.center(panel_qual))
        else: console.print(qual_text)
        console.print()
        
        qual_choice = ask_choice(get_text("select_option"), choices=["0", "1", "2", "3"], show_choices=False)
        if qual_choice == "0": continue
            
        try:
            silent_opts = {'quiet': True, 'no_warnings': True, 'logger': QuietLogger()}
            with yt_dlp.YoutubeDL(silent_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'youtube_media')
        except Exception as e:
            console.print(get_text("yt_error", error=e))
            console.print(get_text("press_enter"))
            console.input()
            continue
            
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '.', '_', '-')).strip()
        target_ext = ".mp4" if fmt_choice == "1" else ".mp3"
        target_label = get_text("yt_label_video") if fmt_choice == "1" else get_text("yt_label_audio")
        
        config = load_config()
        if config.get("save_mode") == "auto" and config.get("default_dir"):
            default_dir = config.get("default_dir")
            if os.path.exists(default_dir):
                outtmpl_path = os.path.join(default_dir, '%(title)s')
                final_file_path = os.path.join(default_dir, safe_title + target_ext)
            else:
                outtmpl_path = '%(title)s'
                final_file_path = safe_title + target_ext
        else:
            console.print(get_text("dialog_saving"))
            save_path = open_save_dialog(safe_title + target_ext, target_ext, target_label)
            if not save_path:
                console.print(get_text("op_canceled"))
                time.sleep(1.5)
                continue
            outtmpl_path = os.path.splitext(save_path)[0]
            final_file_path = save_path
            
        ydl_opts = {
            'outtmpl': outtmpl_path + '.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'noprogress': True,
            'logger': QuietLogger()
        }
        
        if HAS_IMAGEIO_FFMPEG:
            try: ydl_opts['ffmpeg_location'] = imageio_ffmpeg.get_ffmpeg_exe()
            except Exception: pass
        
        if fmt_choice == "1":
            ydl_opts['merge_output_format'] = 'mp4'
            if qual_choice == "1": ydl_opts['format'] = 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b'
            elif qual_choice == "2": ydl_opts['format'] = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4] / best[height<=1080]'
            elif qual_choice == "3": ydl_opts['format'] = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4] / best[height<=720]'
        else:
            ydl_opts['format'] = 'bestaudio'
            postprocessor = {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}
            if qual_choice == "2": postprocessor['preferredquality'] = '192'
            elif qual_choice == "3": postprocessor['preferredquality'] = '128'
            else: postprocessor['preferredquality'] = '0'
            ydl_opts['postprocessors'] = [postprocessor]
            
        console.print(get_text("yt_downloading"))
        
        try:
            if HAS_RICH:
                with Progress(
                    SpinnerColumn(style=THEME_COLOR),
                    TextColumn(f"[bold {THEME_COLOR}]{get_text('yt_downloading_progress')}[/bold {THEME_COLOR}]"),
                    BarColumn(complete_style=THEME_COLOR, finished_style=THEME_COLOR),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    TransferSpeedColumn(), TimeRemainingColumn(), console=console
                ) as progress:
                    task_id = progress.add_task("download", total=None)
                    def rich_progress_hook(d):
                        if d.get('status') == 'downloading':
                            total = d.get('total_bytes') or d.get('total_bytes_estimate')
                            downloaded = d.get('downloaded_bytes', 0)
                            if total: progress.update(task_id, total=total, completed=downloaded)
                        elif d.get('status') == 'finished':
                            progress.update(task_id, description=f"[bold green]{get_text('yt_processing_media')}[/bold green]")
                    ydl_opts['progress_hooks'] = [rich_progress_hook]

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
            else:
                def plain_progress_hook(d):
                    if d.get('status') == 'downloading':
                        percent = d.get('_percent_str', '').strip()
                        print(f"\r{get_text('yt_plain_downloading', percent=percent)}", end="", flush=True)
                    elif d.get('status') == 'finished':
                        print(get_text("yt_plain_done"))

                ydl_opts['progress_hooks'] = [plain_progress_hook]
                with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])

            console.print()
            if HAS_RICH:
                console.print(Panel(get_text("yt_success_msg", title=title, dst=final_file_path), title=get_text("yt_success_title"), border_style="green"))
            else:
                console.print(get_text("yt_success_msg", title=title, dst=final_file_path))
        except Exception as e:
            console.print(get_text("yt_error", error=e))
            
        console.print(get_text("press_enter"))
        console.input()
        break


def tool_local_media_converter():
    if not HAS_IMAGEIO_FFMPEG:
        clear_screen()
        show_header()
        console.print(get_text("yt_missing_dep"))
        console.print(get_text("press_enter"))
        console.input()
        return

    clear_screen()
    show_header()
    
    if HAS_RICH:
        console.print(Panel(get_text("local_media_desc"), title=get_text("local_media_title"), border_style=THEME_COLOR))
    else:
        console.print(get_text("local_media_desc"))
        
    console.print(get_text("local_media_prompt"))
    
    raw_path = console.input(f"[bold {THEME_COLOR}]>[/] ").strip()
    if raw_path == "0" or not raw_path: return
        
    filepath = raw_path
    if filepath.startswith("&"): filepath = filepath[1:].strip()
    filepath = filepath.strip("'\"")
    
    if not os.path.exists(filepath):
        console.print(get_text("file_not_found", filepath=filepath))
        time.sleep(2.5)
        return

    safe_title = os.path.splitext(os.path.basename(filepath))[0]
    target_ext = ".mp3"
    target_label = "Áudio MP3"
    
    save_path = resolve_save_path(safe_title + target_ext, target_ext, target_label)
    if not save_path:
        console.print(get_text("op_canceled"))
        time.sleep(1.5)
        return
        
    try:
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [
            ffmpeg_path, '-y', '-i', filepath,
            '-vn', '-acodec', 'libmp3lame', '-q:a', '2', save_path
        ]
        
        if HAS_RICH:
            with Progress(
                SpinnerColumn(style=THEME_COLOR),
                TextColumn(f"[bold {THEME_COLOR}]{get_text('local_media_converting')}[/bold {THEME_COLOR}]"),
                TimeElapsedColumn(),
                console=console
            ) as progress:
                task = progress.add_task("convert", total=None)
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                progress.update(task, completed=100)
        else:
            console.print(get_text("local_media_converting"))
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            
        if HAS_RICH:
            console.print(Panel(get_text("success_msg", src=filepath, ext_src="Vídeo Local", tgt="MP3", dst=save_path), title=get_text("success_title"), border_style="green"))
        else:
            console.print(get_text("success_msg", src=filepath, ext_src="Vídeo Local", tgt="MP3", dst=save_path))
            
    except Exception as e:
        console.print(get_text("error_unexpected", error=e))
        
    console.print(get_text("press_enter"))
    console.input()


def tool_media_menu():
    while True:
        clear_screen()
        show_header()
        
        menu_text = (
            f" [[bold {THEME_COLOR}]1[/]]" + get_text("media_opt_1") + "\n" +
            f" [[bold {THEME_COLOR}]2[/]]" + get_text("media_opt_2") + "\n" +
            f" [[bold {THEME_COLOR}]0[/]]" + get_text("media_opt_0")
        )
        if HAS_RICH:
            panel = Panel(menu_text, title=get_text("media_menu_title"), border_style=THEME_COLOR, expand=False, padding=(1, 4))
            console.print(Align.center(panel))
        else:
            console.print(menu_text)
        console.print()
        
        choice = ask_choice(get_text("select_option"), choices=["0", "1", "2"], show_choices=False)
        
        if choice == "1":
            tool_youtube_downloader()
        elif choice == "2":
            tool_local_media_converter()
        elif choice == "0":
            break


# ==========================================
# CICLO PRINCIPAL
# ==========================================

def main():
    load_config()
    while True:
        clear_screen()
        show_header()
        
        menu_text = (
            f" [[bold {THEME_COLOR}]1[/]]" + get_text("menu_opt_1") + "\n" +
            f" [[bold {THEME_COLOR}]2[/]]" + get_text("menu_opt_2") + "\n" +
            f" [[bold {THEME_COLOR}]3[/]]" + get_text("menu_opt_3") + "\n" +
            f" [[bold {THEME_COLOR}]4[/]]" + get_text("menu_opt_4")
        )
        if HAS_RICH:
            panel = Panel(menu_text, title=get_text("menu_main_title"), border_style=THEME_COLOR, expand=False, padding=(1, 4))
            console.print(Align.center(panel))
        else:
            console.print(menu_text)
        console.print()
        
        choice = ask_choice(get_text("select_option"), choices=["1", "2", "3", "4"], show_choices=False)
        
        if choice == "1":
            tool_transformador_universal()
        elif choice == "2":
            tool_media_menu()
        elif choice == "3":
            settings_menu()
        elif choice == "4":
            clear_screen()
            sys.stdout.write("\033[3J\033[H\033[2J")
            sys.stdout.flush()
            clear_screen()
            console.print(get_text("goodbye"))
            time.sleep(0.6)
            clear_screen()
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        sys.stdout.write("\033[3J\033[H\033[2J")
        sys.stdout.flush()
        clear_screen()
        console.print(get_text("interrupted"))
        sys.exit(0)