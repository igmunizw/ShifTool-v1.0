#  shifTool - Conversor Universal CLI

O shifTool é uma ferramenta CLI (Command Line Interface) multifuncional desenvolvida em Python para conversão universal de arquivos locais e download de mídias da web de forma totalmente independente e *sem anúncios*.

##  Notas sobre o Desenvolvimento

Este projeto foi integralmente estruturado e desenvolvido com o auxílio de ferramentas de Inteligência Artificial
O aplicativo foi projetado para rodar em computadores com recursos limitados, mantendo um design leve, sem anúncios ou dependência de serviços web de terceiros. Ele conta com um sistema de gerenciamento automático de dependências, suporte a internacionalização (Português e Inglês) e preferências persistentes salvas localmente.
## Principais Funcionalidades

*    **Transformador Universal de Arquivos:** Converta facilmente entre diversos formatos de imagens, documentos, textos puros e planilhas.
*    **Baixador e Conversor do YouTube:** Baixe vídeos em MP4 (com opções de qualidade de até 1080p) ou extraia áudios em MP3 com alta qualidade diretamente de links do YouTube utilizando o `yt-dlp`.
*    **Conversor de Mídia Local:** Extraia o áudio (MP3) de vídeos armazenados no seu computador de forma rápida e limpa além do suporte a processamento em lote colando múltiplos links separados por espaço.
*    **Instalação Automática de Dependências:** Não se preocupe em rodar `pip install` manualmente! O shifTool verifica as bibliotecas ausentes na inicialização e oferece a instalação automática com uma interface visual agradável[cite: 2].
*    **Configurações de Salvamento Inteligentes:** Escolha entre sempre ser perguntado onde salvar o arquivo (via janelas de diálogo do sistema) ou defina uma pasta padrão para salvamento automático[cite: 2].
*    **Internacionalização (i18n):** Suporte nativo para os idiomas Português (pt) e Inglês (en), com fácil alternância pelo menu de configurações[cite: 2].
*    **Atualizador Integrado:** Verifique e atualize as ferramentas vitais do sistema (como `yt-dlp`, `pandas`, `rich`, etc.) diretamente pelo menu do aplicativo[cite: 2].

## Formatos Suportados

Atualmente, o aplicativo possui suporte nativo para realizar o intercâmbio entre os seguintes formatos[cite: 2]:

*   **Imagens:** Conversão entre PNG, JPG, WEBP, BMP, TIFF e exportação direta para PDF.
*   **Documentos e Textos:** Conversão de arquivos de texto (.txt, .md) e suporte a documentos de escritório (.docx, .doc, .odt) para PDF utilizando o LibreOffice ou docx2pdf.
*   **Planilhas e Dados:** Conversão cruzada entre arquivos XLSX, CSV e JSON utilizando pandas.
*   **Mídia:** MP4 (Vídeo), MP3 (Áudio)

## Requisitos do sistema

* Python 3.x
* O próprio aplicativo verifica, gerencia e oferece a instalação automática dos pacotes Python necessários (rich, yt-dlp, pymupdf, pillow, pandas, openpyxl, pypdf, etc.) na primeira execução.
* Para conversão de documentos de texto complexos (.docx, .odt), é recomendada a instalação do LibreOffice no sistema operacional.
* Para o processamento local de mídias, o aplicativo gerencia dependências auxiliares como o imageio-ffmpeg.

## Como Instalar e Usar

### No Linux (Terminal):

Abra o seu terminal e execute:
```
curl -sSL https://raw.githubusercontent.com/igmunizw/ShiftTool-v1.0/main/install.sh | bash
````
### No Windows (PowerShell):
Abra o PowerShell e execute:
```powershell
irm https://raw.githubusercontent.com/igmunizw/ShiftTool-v1.0/main/install.ps1 | iex
