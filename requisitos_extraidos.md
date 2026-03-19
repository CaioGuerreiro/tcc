### 1. Visão Geral
*   **Objetivo Principal:** O sistema permite que usuários (estudantes ou professores) realizem login utilizando credenciais (e-mail/username e senha), autenticando-se contra um backend e recebendo um token de autenticação, além de redirecionar para a área de usuário apropriada. O backend valida a autenticação de token e verifica a expiração do acesso.
*   **Dependências/Integrações:**
    *   **Frontend (`login/page.tsx`):** `react`, `next/image`, `next/navigation`, `react-icons/fa`, `LoadingScreen`, `NavBar`, `InputSimple`, `Button`, `CarouselStudent`, `AlertModal`, `getApiUrl`.
    *   **Backend (`token.py`):** `django.utils.translation`, `rest_framework.authentication.TokenAuthentication`, `rest_framework.exceptions.AuthenticationFailed`.
    *   **Backend (`views.py`):** `django.http`, `django.conf`, `django.views.defaults`, `rest_framework.request`, `os`, `mangoo.users.token.ExpiringTokenAuthentication`.

### 2. Requisitos Funcionais (RF)
*   **RF01:** O sistema deve exibir um formulário de login com campos para e-mail/username e senha. [Componente: `StudentLogin` em `login/page.tsx`]
*   **RF02:** O sistema deve permitir ao usuário inserir o e-mail/username no campo designado. [Componente: `InputSimple` em `login/page.tsx`, Estado: `email`]
*   **RF03:** O sistema deve permitir ao usuário inserir a senha no campo designado. [Componente: `InputSimple` em `login/page.tsx`, Estado: `password`]
*   **RF04:** O sistema deve ocultar o texto da senha por padrão e permitir a alternância de visibilidade da senha. [Componentes: `FaEye`, `FaEyeSlash` em `login/page.tsx`, Estado: `showPassword`]
*   **RF05:** O sistema deve tentar autenticar o usuário ao clicar no botão 'Login'. [Método: `handleLogin` em `login/page.tsx`, Componente: `Button.Focused`]
*   **RF06:** O sistema deve tentar autenticar o usuário ao pressionar a tecla 'Enter' nos campos de e-mail/username ou senha. [Método: `handleLogin` em `login/page.tsx`, Componente: `InputSimple`]
*   **RF07:** O sistema deve enviar uma requisição POST para o endpoint `auth-token/` com `username` e `password` para autenticação. [Método: `handleLogin` em `login/page.tsx`]
*   **RF08:** O sistema deve, em caso de autenticação bem-sucedida, armazenar o `authToken` e `userType` recebidos em `localStorage`. [Método: `handleLogin` em `login/page.tsx`]
*   **RF09:** O sistema deve redirecionar o usuário para `/student-home` se o `userType` for 'S' após o login bem-sucedido. [Método: `handleLogin` em `login/page.tsx`]
*   **RF10:** O sistema deve redirecionar o usuário para `/teacher-home` se o `userType` não for 'S' após o login bem-sucedido. [Método: `handleLogin` em `login/page.tsx`]
*   **RF11:** O sistema deve exibir uma tela de carregamento (`LoadingScreen`) durante as operações de redirecionamento ou autenticação. [Estado: `isLoading` em `login/page.tsx`]
*   **RF12:** O sistema deve permitir que o usuário navegue para uma página de recuperação de senha. [Método: `handleForgotClick` em `login/page.tsx`]
*   **RF13:** O sistema deve permitir que o usuário navegue para uma página de registro de nova conta. [Método: `handleRegisterClick` em `login/page.tsx`]
*   **RF14:** O sistema (backend) deve autenticar credenciais de token, verificando a validade do token e o status de acesso do usuário. [Classe: `ExpiringTokenAuthentication`, Método: `authenticate_credentials` em `token.py`]
*   **RF15:** O sistema (backend) deve tentar autenticar usuários via token DRF em views Django comuns. [Função: `_authenticate_via_token` em `views.py`]
*   **RF16:** O sistema (backend) deve proteger views exigindo que o usuário esteja autenticado e ativo. [Decorator: `login_required_or_404` em `views.py`]
*   **RF17:** O sistema (backend) deve proteger views exigindo que o usuário seja `staff` e ativo. [Decorator: `staff_member_required_or_404` em `views.py`]
*   **RF18:** O sistema (backend) deve permitir acesso a arquivos de mídia protegidos apenas para usuários autenticados. [Função: `protected_media`, Decorator: `@login_required_or_404` em `views.py`]

### 3. Regras de Negócio (RN) e Validações
*   **RN01:** A requisição de login deve ser do tipo `POST` e ter o cabeçalho `Content-Type` definido como `application/json`. [Método: `handleLogin` em `login/page.tsx`]
*   **RN02:** Se a resposta da requisição de login não for `ok` (status HTTP de sucesso), o sistema deve considerar um erro. [Método: `handleLogin` em `login/page.tsx`]
*   **RN03:** Em caso de erro na requisição de login (incluindo falha de rede ou status `!response.ok`), o sistema deve exibir uma mensagem de erro genérica "Erro ao fazer login.". [Método: `handleLogin` em `login/page.tsx`]
*   **RN04:** Em caso de erro na requisição de login, quaisquer `authToken` ou `userType` previamente armazenados no `localStorage` devem ser removidos. [Método: `handleLogin` em `login/page.tsx`]
*   **RN05:** Após qualquer tentativa de login (sucesso ou falha), o indicador de carregamento deve ser desativado. [Método: `handleLogin` em `login/page.tsx`]
*   **RN06:** O token de autenticação fornecido deve estar válido e o acesso do usuário não deve ter expirado para que a autenticação seja bem-sucedida. [Classe: `ExpiringTokenAuthentication`, Método: `authenticate_credentials` em `token.py`]
*   **RN07:** Se o token de autenticação estiver expirado, o sistema (backend) deve levantar uma exceção `AuthenticationFailed` com a mensagem "Token expired. Please log in again.". [Classe: `ExpiringTokenAuthentication`, Método: `authenticate_credentials` em `token.py`]
*   **RN08:** Após uma autenticação de token bem-sucedida no backend, o timestamp de expiração do acesso do usuário deve ser atualizado. [Classe: `ExpiringTokenAuthentication`, Método: `authenticate_credentials` em `token.py`]
*   **RN09:** Para acessar uma view protegida por `login_required_or_404`, o usuário deve estar autenticado (`is_authenticated`) e ativo (`is_active`). Caso contrário, a requisição resultará em `page_not_found`. [Decorator: `login_required_or_404` em `views.py`]
*   **RN10:** Se a autenticação padrão falhar, a view `login_required_or_404` tentará autenticar o usuário via token DRF. Se essa autenticação for bem-sucedida e o usuário estiver ativo, a requisição será permitida. [Decorator: `login_required_or_404`, Função: `_authenticate_via_token` em `views.py`]
*   **RN11:** Para acessar uma view protegida por `staff_member_required_or_404`, o usuário deve ser `staff` (`is_staff`) e ativo (`is_active`). Caso contrário, a requisição resultará em `page_not_found`. [Decorator: `staff_member_required_or_404` em `views.py`]
*   **RN12:** A funcionalidade de login deve esperar 1 segundo antes de redirecionar para `/` (home), `/forgot-password` ou `/register` para exibir a tela de carregamento. [Métodos: `handleBackToHome`, `handleForgotClick`, `handleRegisterClick` em `login/page.tsx`]

### 4. Estrutura de Dados (Entradas/Saídas)
*   **Principais Entradas:**
    *   **Frontend para Backend (Requisição de Login via `handleLogin`):**
        *   `username` (string): E-mail ou nome de usuário do usuário.
        *   `password` (string): Senha do usuário.
    *   **Backend (Autenticação de Token via `ExpiringTokenAuthentication.authenticate_credentials`):**
        *   `key` (string): O token de autenticação.
    *   **Backend (Autenticação em views Django via `_authenticate_via_token` e decoradores):**
        *   `request` (HttpRequest): Objeto da requisição HTTP contendo, potencialmente, cabeçalhos de autenticação.
*   **Saídas/Efeitos Colaterais:**
    *   **Backend para Frontend (Resposta de Login Bem-sucedida via `handleLogin`):**
        *   `token` (string): Token JWT ou de sessão para autenticações futuras.
        *   `user_type` (string): Tipo de usuário ('S' para estudante, outro valor para professor).
    *   **Frontend (Armazenamento Local via `handleLogin`):**
        *   `localStorage['authToken']` (string): Armazena o token de autenticação.
        *   `localStorage['userType']` (string): Armazena o tipo de usuário.
    *   **Frontend (Interface do Usuário):**
        *   Redirecionamento para `/student-home`, `/teacher-home`, `/`, `/forgot-password`, `/register`. [Métodos: `handleLogin`, `handleBackToHome`, `handleForgotClick`, `handleRegisterClick` em `login/page.tsx`]
        *   Exibição/Ocultação de `LoadingScreen`. [Estado: `isLoading` em `login/page.tsx`]
        *   Exibição de `AlertModal` com mensagem de erro. [Estados: `AlertIsOpen`, `AlertMessage` em `login/page.tsx`]
    *   **Backend (Autenticação):**
        *   Lançamento de `AuthenticationFailed` em caso de token inválido ou expirado. [Classe: `ExpiringTokenAuthentication` em `token.py`]
        *   Atualização do `user.access_expires` no modelo de usuário. [Classe: `ExpiringTokenAuthentication` em `token.py`]
        *   Retorno de `HttpResponseNotFound` (erro 404) para acessos não autorizados a views protegidas. [Decoradores: `login_required_or_404`, `staff_member_required_or_404` em `views.py`]
        *   Modificação do objeto `request.user` para o usuário autenticado via token. [Função: `_authenticate_via_token` em `views.py`]