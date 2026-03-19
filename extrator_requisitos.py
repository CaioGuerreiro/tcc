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
    Você atua como um Engenheiro de Requisitos Sênior e Analista de Sistemas Especialista.
    Sua missão é realizar a Engenharia Reversa de Requisitos com extremo rigor técnico a partir do código-fonte fornecido.

    DIRETRIZES DE EXTRAÇÃO (CRÍTICO):
    1. Baseie-se ESTRITAMENTE no código fornecido. Não faça suposições, não deduza funcionalidades futuras e não invente regras que não estejam explicitamente programadas.
    2. Rastreabilidade: Para cada requisito ou regra, você DEVE indicar o nome do método, função ou classe de onde a informação foi extraída.

    Apresente sua análise OBRIGATORIAMENTE no seguinte formato estruturado em Markdown:

    ### 1. Visão Geral
    * **Objetivo Principal:** (Descreva em 1 ou 2 frases o propósito central deste arquivo/módulo).
    * **Dependências/Integrações:** (Liste bibliotecas, APIs ou outros módulos externos que o código importa ou consome).

    ### 2. Requisitos Funcionais (RF)
    (Descreva o que o sistema faz de forma ativa. Use o formato: "RF[Número]: O sistema deve...")
    * Exemplo: **RF01:** O sistema deve validar a autenticação do usuário antes de processar a requisição. [Método: check_auth]

    ### 3. Regras de Negócio (RN) e Validações
    (Condições, cálculos, limites, tratamento de exceções ou restrições impostas pelo código)
    * Exemplo: **RN01:** Se o saldo for menor que o valor da transferência, o sistema deve lançar a exceção 'InsufficientFundsError'. [Método: transferir_fundos]

    ### 4. Estrutura de Dados (Entradas/Saídas)
    * **Principais Entradas:** (Quais dados ou parâmetros o código recebe para funcionar).
    * **Saídas/Efeitos Colaterais:** (O que o código retorna ou onde ele salva os dados - ex: Banco de Dados, Arquivo, Retorno de API).
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