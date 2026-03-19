import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=API_KEY)

def ler_codigo_fonte(caminho_arquivo):
    """Lê o arquivo de código que queremos analisar."""
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        return file.read()

def extrair_requisitos(codigo_fonte):
    """Envia o código para a LLM e pede a extração dos requisitos."""
    
    # Engenharia de Prompt
    prompt_sistema = """
    Você é um Engenheiro de Requisitos Sênior e Analista de Sistemas. 
    Sua tarefa é realizar a Engenharia Reversa de Requisitos a partir do código-fonte fornecido.
    
    Por favor, analise o código e identifique:
    1. O Objetivo Principal deste módulo/classe.
    2. Os Requisitos Funcionais (o que o sistema faz, regras de negócio implementadas). Escreva no formato "O sistema deve..." ou usando o formato de User Stories.
    3. Exceções e Regras de Validação encontradas (ex: tratamento de erros, limites de variáveis).
    
    Seja claro, objetivo e não invente funcionalidades que não estão explicitamente codificadas.
    """

    prompt_usuario = f"Aqui está o código-fonte para análise:\n\n{codigo_fonte}"

    print("Enviando código para a LLM. Aguarde...")
    
    # Gemini 2.5 Flash
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Content(role="user", parts=[
                types.Part.from_text(text=prompt_sistema),
                types.Part.from_text(text=prompt_usuario)
            ])
        ]
    )
    
    return response.text


if __name__ == "__main__":
    
    caminho_do_seu_codigo = 'C:/Users/caiog/Documents/Projetos/Mangoo-Front/src/app/(login)/login/page.tsx' 
    
    try:
        
        codigo = ler_codigo_fonte(caminho_do_seu_codigo)
        
        
        resultado = extrair_requisitos(codigo)
        
        #  Markdown 
        with open('requisitos_extraidos.md', 'w', encoding='utf-8') as f:
            f.write(resultado)
            
        print("✅ Sucesso! Os requisitos foram extraídos e salvos em 'requisitos_extraidos.md'.")
        
    except FileNotFoundError:
        print(f"Erro: O arquivo {caminho_do_seu_codigo} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao processar: {e}")