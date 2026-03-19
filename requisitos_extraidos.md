Excelente! Como Engenheiro de Requisitos Sênior e Analista de Sistemas, farei a engenharia reversa dos requisitos a partir do código-fonte fornecido.

---

### Análise de Engenharia Reversa de Requisitos - `StudentLogin`

**1. O Objetivo Principal deste módulo/classe:**

O objetivo principal deste módulo é fornecer uma interface de login para usuários (presumidamente estudantes e professores) através da autenticação de credenciais (e-mail e senha) e, subsequentemente, redirecioná-los para o dashboard apropriado (`/student-home` ou `/teacher-home`) com base no seu tipo de usuário, enquanto gerencia o estado de carregamento e exibe alertas de erros.

**2. Requisitos Funcionais:**

*   **RF1: Autenticação de Usuário**
    *   **O sistema deve** permitir ao usuário inserir seu e-mail (tratado como `username` na API) e senha para autenticação.
    *   **O sistema deve** enviar as credenciais (e-mail e senha) para o endpoint de autenticação `/auth-token/` via requisição POST.
    *   **O sistema deve** extrair o token de autenticação e o tipo de usuário (`user_type`) da resposta bem-sucedida da API.
    *   **O sistema deve** armazenar o `authToken` e o `userType` no `localStorage` do navegador após uma autenticação bem-sucedida.

*   **RF2: Redirecionamento Pós-Login**
    *   **O sistema deve** redirecionar o usuário para a página `/student-home` se o `user_type` retornado pela API for 'S' (Estudante).
    *   **O sistema deve** redirecionar o usuário para a página `/teacher-home` se o `user_type` retornado pela API não for 'S' (implica ser professor ou outro tipo de usuário).

*   **RF3: Gerenciamento de Visibilidade da Senha**
    *   **O sistema deve** exibir um ícone (olho) para permitir ao usuário alternar a visibilidade da senha no campo de entrada.
    *   **O sistema deve** alternar o tipo do campo de senha entre 'password' (oculto) e 'text' (visível) ao clicar no ícone correspondente.

*   **RF4: Navegação Relacionada ao Login**
    *   **O sistema deve** fornecer um link "Esqueceu sua senha?" que, ao ser clicado, redireciona o usuário para a página `/forgot-password` após um breve atraso.
    *   **O sistema deve** fornecer um link "Não possui conta? Realize seu cadastro aqui" que, ao ser clicado, redireciona o usuário para a página `/register` após um breve atraso.
    *   **O sistema deve** tentar realizar o login quando o usuário pressionar a tecla 'Enter' nos campos de e-mail ou senha.

*   **RF5: Feedback Visual e UI**
    *   **O sistema deve** exibir uma barra de navegação (`NavBar`) no topo da página.
    *   **O sistema deve** exibir uma tela de carregamento (`LoadingScreen`) em tela cheia sempre que uma operação assíncrona (como login ou redirecionamento) estiver em andamento.
    *   **O sistema deve** exibir um componente de carrossel (`CarouselStudent`) na seção introdutória da página.
    *   **O sistema deve** exibir um formulário de login com um ícone "Mangoo" e o título "Faça seu Login".
    *   **O sistema deve** exibir campos de entrada para "E-mail" e "Senha", com placeholders informativos.
    *   **O sistema deve** exibir um botão "Login" que, ao ser clicado, inicia o processo de autenticação.
    *   **O sistema deve** exibir um modal de alerta (`AlertModal`) com uma mensagem específica em caso de erros durante o processo de login ou outras operações.
    *   **O sistema deve** permitir ao usuário fechar o modal de alerta.

**3. Exceções e Regras de Validação encontradas:**

*   **RV1: Validação de Resposta da API:**
    *   **Exceção:** O sistema deve verificar se a resposta da requisição de autenticação da API (`response.ok`) foi bem-sucedida (status code 2xx).
    *   **Tratamento:** Caso a resposta não seja bem-sucedida, o sistema deve lançar um erro e exibir um modal de alerta com a mensagem "Erro ao fazer login.".

*   **RV2: Tratamento de Erro na Requisição:**
    *   **Exceção:** Em caso de qualquer erro durante a requisição de `fetch` (e.g., erro de rede, formato de resposta inválido), o sistema deve capturá-lo.
    *   **Tratamento:** O sistema deve exibir um modal de alerta com a mensagem "Erro ao fazer login." e garantir que `isLoading` seja definido como `false`.

*   **RV3: Limpeza de Dados em Caso de Falha:**
    *   **Regra:** Se o processo de login falhar (seja por resposta da API não `ok` ou erro de requisição), o sistema deve remover quaisquer `authToken` e `userType` armazenados no `localStorage` para evitar dados de sessão inválidos.

*   **RV4: Campos Obrigatórios (Implícito na UI):**
    *   **Regra:** Os campos de e-mail e senha são visualmente indicados como obrigatórios (`<span className='asterisk'>*</span>`). No entanto, o código não implementa uma validação explícita de preenchimento *antes* da chamada à API. A validação de "vazio" seria tratada pela API ou resultaria em um erro genérico "Erro ao fazer login.".