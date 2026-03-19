import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=API_KEY)

def ler_multiplos_arquivos(lista_caminhos):
    """Lê uma lista de arquivos e os junta em uma única string estruturada."""
    codigo_completo = ""
    
    for caminho in lista_caminhos:
        try:
            with open(caminho, 'r', encoding='utf-8') as file:
                conteudo = file.read()
                # Cria um cabeçalho claro para a IA saber qual arquivo está lendo
                codigo_completo += f"\n\n{'='*50}\n"
                codigo_completo += f"ARQUIVO: {caminho}\n"
                codigo_completo += f"{'='*50}\n\n"
                codigo_completo += conteudo
                print(f"Lido com sucesso: {caminho}")
        except FileNotFoundError:
            print(f"Aviso: O arquivo '{caminho}' não foi encontrado e será ignorado.")
        except Exception as e:
            print(f"Erro ao ler o arquivo '{caminho}': {e}")
            
    return codigo_completo

def extrair_requisitos(codigo_fonte_unificado):
    """Envia o código para a LLM e pede a extração dos requisitos."""
    
    # Engenharia de Prompt
    prompt_sistema = """
    Você atua como um Engenheiro de Requisitos Sênior e Analista de Sistemas Especialista.
    Sua missão é realizar a Engenharia Reversa de Requisitos com extremo rigor técnico a partir do código-fonte fornecido.
    

    DIRETRIZES DE EXTRAÇÃO (CRÍTICO):
    1. Baseie-se ESTRITAMENTE no código fornecido. Não faça suposições, não deduza funcionalidades futuras e não invente regras que não estejam explicitamente programadas.
    2. Rastreabilidade: Para cada requisito ou regra, você DEVE indicar o nome do método, função ou classe de onde a informação foi extraída.
    3. Faça análise SOMENTE de requisitos baseados no LOGIN

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

    prompt_usuario = f"Aqui está os código-fontes para análise:\n\n{codigo_fonte_unificado}"

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

    lista_de_arquivos = [
        'C:/Users/caiog/Documents/Projetos/Mangoo-Front/src/app/(login)/login/page.tsx',
        'C:/Users/caiog/Documents/Projetos/backend-api/mangoo/users/token.py',
        'C:/Users/caiog/Documents/Projetos/backend-api/config/views.py'

    ]
    
    
    
    
    # 2. Lê todos os arquivos e junta tudo
    codigo_unificado = ler_multiplos_arquivos(lista_de_arquivos)
    
    # 3. Só processa se conseguiu ler algum código
    if codigo_unificado.strip():
        try:
            resultado = extrair_requisitos(codigo_unificado)
            
            # Salva o Markdown
            with open('requisitos_extraidos.md', 'w', encoding='utf-8') as f:
                f.write(resultado)
                
            print("\n✅ Sucesso! Os requisitos cruzados foram extraídos e salvos em 'requisitos_extraidos.md'.")
            
        except Exception as e:
            print(f"\n❌ Ocorreu um erro ao processar com a IA: {e}")
    else:
        print("\n❌ Nenhum código válido foi lido. Verifique os caminhos dos arquivos.") 