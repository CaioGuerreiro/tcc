Como Engenheiro de Requisitos Sênior e Analista de Sistemas Especialista, realizei a engenharia reversa dos requisitos do código-fonte fornecido com o máximo rigor técnico, conforme as diretrizes estabelecidas.

---

### 1. Visão Geral
*   **Objetivo Principal:** Este módulo visa fornecer uma interface de login para usuários, permitindo a autenticação através de uma API externa, o gerenciamento de sessões com base no tipo de usuário e o redirecionamento para áreas específicas da aplicação (estudante ou professor).
*   **Dependências/Integrações:**
    *   **React:** `useEffect`, `useState` (gerenciamento de estado e ciclo de vida).
    *   **Next.js:** `Image` (otimização de imagens), `useRouter` de `next/navigation` (navegação entre rotas).
    *   **Estilização:** `./style.css` (estilos locais).
    *   **Componentes Internos:**
        *   `LoadingScreen` (exibição de tela de carregamento).
        *   `NavBar` (barra de navegação).
        *   `InputSimple` (campo de entrada genérico).
        *   `Button` (botões estilizados).
        *   `CarouselStudent` (componente de carrossel).
        *   `AlertModal` (modal de alerta).
    *   **Ícones:** `FaEye`, `FaEyeSlash` de `react-icons/fa` (ícones de visibilidade de senha).
    *   **Assets Estáticos:** `MangooIcon` (ícone da aplicação).
    *   **Utilitários:** `getApiUrl` de `@/utils/api` (função para obter URLs de API).
    *   **API Externa:** Endpoint `/auth-token/` para autenticação de usuário.

### 2. Requisitos Funcionais (RF)
*   **RF01:** O sistema deve exibir um formulário de login contendo campos para inserção de e-mail e senha. [Componente: `StudentLogin` (JSX render)]
*   **RF02:** O sistema deve permitir ao usuário inserir o e-mail no campo designado e armazená-lo internamente. [Componente: `InputSimple`, Estado: `email`, Método: `setEmail`]
*   **RF03:** O sistema deve permitir ao usuário inserir a senha no campo designado e armazená-la internamente. [Componente: `InputSimple`, Estado: `password`, Método: `setPassword`]
*   **RF04:** O sistema deve permitir ao usuário alternar a visibilidade da senha no campo de entrada entre texto e oculto. [Estado: `showPassword`, Componente: `FaEye`, `FaEyeSlash`, Método: `setShowPassword`]
*   **RF05:** O sistema deve iniciar o processo de login ao clicar no botão "Login". [Método: `handleLogin`, Componente: `Button.Focused`]
*   **RF06:** O sistema deve iniciar o processo de login ao pressionar a tecla 'Enter' nos campos de e-mail ou senha. [Método: `handleLogin`, Componente: `InputSimple` `onKeyDown`]
*   **RF07:** O sistema deve enviar uma requisição HTTP POST para o endpoint de autenticação `/auth-token/` com as credenciais fornecidas. [Método: `handleLogin`, `fetch`]
*   **RF08:** O sistema deve armazenar o token de autenticação recebido da API no `localStorage` sob a chave 'authToken'. [Método: `handleLogin`, `localStorage.setItem`]
*   **RF09:** O sistema deve armazenar o tipo de usuário (`user_type`) recebido da API no `localStorage` sob a chave 'userType'. [Método: `handleLogin`, `localStorage.setItem`]
*   **RF10:** O sistema deve redirecionar o usuário para a rota `/student-home` se o `user_type` retornado pela API for 'S'. [Método: `handleLogin`, `router.push`]
*   **RF11:** O sistema deve redirecionar o usuário para a rota `/teacher-home` se o `user_type` retornado pela API for diferente de 'S'. [Método: `handleLogin`, `router.push`]
*   **RF12:** O sistema deve exibir uma tela de carregamento (`LoadingScreen`) durante o processamento de requisições e redirecionamentos. [Estado: `isLoading`, Componente: `LoadingScreen`]
*   **RF13:** O sistema deve exibir um modal de alerta com uma mensagem específica em caso de erro na requisição de login. [Estado: `AlertIsOpen`, `AlertMessage`, Componente: `AlertModal`]
*   **RF14:** O sistema deve permitir que o usuário feche o modal de alerta. [Método: `onCloseAlertModal`]
*   **RF15:** O sistema deve permitir a navegação para a página inicial da aplicação (`/`). [Método: `handleBackToHome`, `router.push`]
*   **RF16:** O sistema deve permitir a navegação para a página de recuperação de senha (`/forgot-password`). [Método: `handleForgotClick`, `router.push`]
*   **RF17:** O sistema deve permitir a navegação para a página de registro de nova conta (`/register`). [Método: `handleRegisterClick`, `router.push`]

### 3. Regras de Negócio (RN) e Validações
*   **RN01:** A requisição de autenticação deve ser feita para o endpoint `/auth-token/`, utilizando o método HTTP POST. [Método: `handleLogin`, `fetch`, `getApiUrl`]
*   **RN02:** O cabeçalho `Content-Type` da requisição de autenticação deve ser definido como `application/json`. [Método: `handleLogin`, `fetch`]
*   **RN03:** O corpo da requisição de autenticação deve ser um objeto JSON contendo as propriedades `username` (mapeada do e-mail) e `password` (mapeada da senha). [Método: `handleLogin`, `JSON.stringify`]
*   **RN04:** Se a resposta da API de autenticação indicar um erro HTTP (status não-OK), o sistema deve lançar uma exceção com a mensagem de status da resposta. [Método: `handleLogin`, `response.ok`]
*   **RN05:** Em caso de exceção durante o processo de login (incluindo falhas de rede ou erros da API), o sistema deve definir a mensagem do modal de alerta para 'Erro ao fazer login.'. [Método: `handleLogin` (bloco `catch`), `setAlertMessage`]
*   **RN06:** Em caso de exceção durante o processo de login, o sistema deve exibir o modal de alerta. [Método: `handleLogin` (bloco `catch`), `setAlertIsOpen`]
*   **RN07:** Em caso de exceção durante o processo de login, o sistema deve remover quaisquer valores previamente armazenados para 'authToken' e 'userType' do `localStorage`. [Método: `handleLogin` (bloco `catch`), `localStorage.removeItem`]
*   **RN08:** A tela de carregamento (`LoadingScreen`) deve ser ativada antes de iniciar operações de navegação e login bem-sucedido. [Método: `handleBackToHome`, `handleLogin`, `handleForgotClick`, `handleRegisterClick`, Estado: `setIsLoading`]
*   **RN09:** A tela de carregamento (`LoadingScreen`) deve ser desativada após a conclusão da operação de login, independentemente do sucesso ou falha. [Método: `handleLogin` (bloco `finally`), `setIsLoading`]
*   **RN10:** As operações de redirecionamento para a página inicial, recuperação de senha e registro devem ter um atraso fixo de 1000 milissegundos antes de efetivar a mudança de rota. [Método: `handleBackToHome`, `handleForgotClick`, `handleRegisterClick`, `setTimeout`]
*   **RN11:** O modal de alerta será ocultado quando a função `onCloseAlertModal` for invocada, alterando seu estado para não visível. [Método: `onCloseAlertModal`, `setAlertIsOpen`]

### 4. Estrutura de Dados (Entradas/Saídas)
*   **Principais Entradas:**
    *   `email`: String (entrada do usuário via `InputSimple` para o estado `email`).
    *   `password`: String (entrada do usuário via `InputSimple` para o estado `password`).
    *   Eventos de interação do usuário: cliques em botões (`Login`), links (`Esqueceu sua senha?`, `Realize seu cadastro aqui`), ícones (`FaEye`, `FaEyeSlash`).
    *   Evento de teclado: `onKeyDown` para a tecla 'Enter' nos campos de e-mail e senha.
    *   Respostas da API de autenticação: JSON contendo `token` (string) e `user_type` (string).
*   **Saídas/Efeitos Colaterais:**
    *   **Requisição HTTP POST:** Enviada para o endpoint `/auth-token/` com o corpo `{ username: string, password: string }`.
    *   **Armazenamento Local:** `localStorage.setItem('authToken', token)` e `localStorage.setItem('userType', userType)`.
    *   **Navegação:** Redirecionamento para rotas como `/student-home`, `/teacher-home`, `/`, `/forgot-password`, ou `/register`.
    *   **Estado da Interface:**
        *   `isLoading`: Booleano (controla a visibilidade do `LoadingScreen`).
        *   `AlertIsOpen`: Booleano (controla a visibilidade do `AlertModal`).
        *   `AlertMessage`: String (mensagem exibida no `AlertModal`).
        *   `showPassword`: Booleano (controla o tipo do input de senha `text` ou `password`).
    *   **Limpeza de Armazenamento:** `localStorage.removeItem('authToken')` e `localStorage.removeItem('userType')` em caso de erro de login.