# PROJETO.md --- Sistema de Identificação e Autenticação Biométrica

## 1. Objetivo do projeto

Desenvolver uma aplicação em Python que utilize a webcam do computador
para capturar rostos em tempo real, detectar faces com YuNet, extrair
características faciais com SFace e comparar essas características com
três usuários previamente cadastrados.

Cada usuário cadastrado deverá estar associado a um dos três níveis de
autorização definidos no trabalho:

-   **Nível 1:** acesso para indivíduos com permissão geral.
-   **Nível 2:** acesso restrito aos diretores de divisões específicas.
-   **Nível 3:** acesso exclusivo ao Ministro do Meio Ambiente.

Depois de identificar uma pessoa, o programa deverá consultar seu nível
de autorização e apresentar o resultado no terminal. Se não houver
correspondência adequada com os usuários cadastrados, deverá informar
que a pessoa não foi reconhecida e negar o acesso.

O projeto será executado localmente em um computador com Windows 10 ou
11. A interface principal será o terminal, e a captura facial será feita
por uma webcam.

## 2. Regras obrigatórias para a IA que desenvolverá o código

1.  Desenvolva o projeto **passo a passo**, seguindo as etapas deste
    documento na ordem.
2.  Antes de avançar para a etapa seguinte, explique o que foi criado,
    quais arquivos foram alterados, como executar e como testar a etapa
    atual.
3.  Não entregue todo o projeto de uma só vez. Aguarde a confirmação do
    usuário de que a etapa atual foi testada ou de que deseja
    prosseguir.
4.  Não altere o escopo, as tecnologias ou as regras de autorização sem
    perguntar ao usuário.
5.  Utilize Python, OpenCV, YuNet e SFace. Não substitua essas
    tecnologias por outra biblioteca ou serviço.
6.  Não utilize serviços em nuvem ou APIs externas para enviar imagens
    ou características faciais. O processamento deverá ocorrer
    localmente.
7.  Mantenha o programa simples, organizado e adequado a um projeto
    acadêmico. Não crie interface gráfica; a interação e as mensagens
    principais serão pelo terminal.
8.  Não invente nomes reais para os três usuários. Utilize dados de
    exemplo claramente identificados como placeholders e permita que o
    usuário informe os nomes durante o cadastro.
9.  Não cadastre a quarta pessoa de teste. Ela deverá permanecer fora
    dos registros para testar a negativa de acesso.
10. Não declare que o reconhecimento é infalível ou que o sistema
    oferece segurança de nível governamental. Explique as limitações
    observadas nos testes.
11. Não invente resultados de testes. Registre somente resultados que o
    usuário efetivamente observar.
12. Escreva código compatível com Windows 10 e 11 e forneça comandos de
    instalação e execução pelo terminal.
13. Antes de adicionar dependências, explique sua necessidade. Priorize
    Python e OpenCV.
14. Se houver uma dúvida que impeça uma decisão técnica importante,
    pergunte ao usuário em vez de presumir.

## 3. Tecnologias definidas

-   **Python:** linguagem utilizada para implementar a aplicação.
-   **OpenCV:** biblioteca utilizada para acessar a webcam, manipular
    imagens e integrar os modelos de visão computacional.
-   **YuNet:** modelo utilizado para detectar e localizar rostos nas
    imagens.
-   **SFace:** modelo utilizado para gerar representações numéricas das
    características faciais e permitir a comparação entre rostos.
-   **Terminal do Windows:** interface textual para iniciar o programa e
    apresentar identificação, nível de autorização e decisão de acesso.
-   **Arquivos locais:** armazenamento dos cadastros e das
    representações faciais, sem envio para serviços externos.

A implementação deverá utilizar as interfaces do OpenCV compatíveis com
os modelos escolhidos, como `cv2.FaceDetectorYN` para YuNet e
`cv2.FaceRecognizerSF` para SFace, após verificar a versão instalada e a
disponibilidade dessas classes.

## 4. Funcionamento esperado

O fluxo principal deverá ser:

1.  O usuário inicia a aplicação pelo terminal.
2.  O programa verifica se os arquivos de modelos e os registros locais
    estão disponíveis.
3.  O programa abre a webcam.
4.  A imagem capturada é enviada ao detector YuNet.
5.  Quando um rosto é detectado, o sistema prepara/alinha a região
    facial conforme necessário para o SFace.
6.  O SFace gera a representação numérica do rosto.
7.  O programa compara essa representação com as representações dos três
    usuários cadastrados.
8.  Se houver correspondência acima do critério de reconhecimento
    configurado e validado nos testes, o programa identifica o usuário.
9.  O programa consulta o nível de autorização associado ao usuário.
10. O terminal informa a identidade reconhecida, o nível correspondente
    e a decisão de acesso.
11. Se não houver correspondência adequada, o terminal informa **"Pessoa
    não cadastrada --- acesso negado"**.
12. O usuário pode encerrar a captura de forma simples e segura.

**Importante:** identificação e autorização são decisões diferentes. O
reconhecimento indica qual usuário corresponde ao rosto; a autorização
consulta o nível associado a esse cadastro.

## 5. Cadastro dos usuários

O sistema deverá permitir cadastrar exatamente três usuários para a
demonstração do projeto, cada um associado a um dos três níveis de
autorização.

-   Um usuário associado ao Nível 1.
-   Um usuário associado ao Nível 2.
-   Um usuário associado ao Nível 3.

Os nomes e as imagens deverão ser fornecidos pelo usuário durante a
configuração/cadastro. Não invente identidades ou imagens de pessoas
reais.

O cadastro deverá capturar ou receber imagens de referência, detectar o
rosto, gerar a representação facial com SFace e salvar os dados
necessários localmente. O programa deverá validar se foi possível
detectar um rosto antes de concluir o cadastro.

A quarta pessoa será utilizada apenas como pessoa não cadastrada durante
os testes. Não deverá existir registro dela no arquivo de usuários.

## 6. Armazenamento local

Para manter o projeto simples, utilize inicialmente um arquivo JSON
local para armazenar os dados dos três usuários e suas representações
faciais. Cada registro deverá conter, no mínimo:

-   identificador interno;
-   nome informado no cadastro;
-   nível de autorização (1, 2 ou 3);
-   representação facial gerada pelo SFace.

As representações numéricas deverão ser convertidas para listas de
números antes de serem gravadas no JSON e convertidas novamente para o
formato numérico esperado pelo OpenCV durante a leitura.

Não armazene imagens faciais além do necessário para o cadastro e os
testes. Se for necessário manter imagens de referência, explique ao
usuário onde ficarão armazenadas e permita que ele escolha os arquivos.
Não envie imagens ou representações para a internet.

## 7. Organização sugerida dos arquivos

Organize o projeto de forma modular, mantendo cada responsabilidade em
um arquivo:

``` text
reconhecimento_facial/
│
├── main.py
├── config.py
├── camera.py
├── face_detector.py
├── face_recognizer.py
├── user_database.py
├── access_control.py
├── requirements.txt
├── README.md
│
├── models/
│   ├── yunet.onnx
│   └── sface.onnx
│
└── data/
    └── users.json
```

Responsabilidades:

-   `main.py`: coordena o fluxo da aplicação e a interação pelo
    terminal.
-   `config.py`: concentra caminhos dos modelos, configurações da câmera
    e parâmetros do reconhecimento.
-   `camera.py`: abre a webcam, captura quadros e encerra a câmera
    corretamente.
-   `face_detector.py`: carrega o YuNet e localiza rostos nas imagens.
-   `face_recognizer.py`: utiliza o SFace para alinhar/preparar a face,
    extrair características e comparar representações.
-   `user_database.py`: cadastra, consulta e salva os três usuários no
    JSON.
-   `access_control.py`: consulta o nível do usuário identificado e
    determina a decisão de acesso.
-   `requirements.txt`: lista as dependências Python necessárias.
-   `README.md`: explica instalação, configuração dos modelos, cadastro,
    execução e testes.
-   `models/`: contém os arquivos de modelo YuNet e SFace obtidos de
    fontes oficiais ou confiáveis.
-   `data/users.json`: contém os cadastros e as representações faciais
    locais.

Se a implementação demonstrar que algum arquivo separado é
desnecessário, a IA deverá explicar a razão antes de simplificar a
estrutura.

## 8. Critério de comparação e reconhecimento

O SFace deverá gerar as representações faciais e o OpenCV deverá ser
utilizado para compará-las por meio de uma métrica compatível com a
implementação, preferencialmente a similaridade de cosseno
disponibilizada pela API do SFace.

O limite de aceitação (threshold) não deverá ser escolhido como se fosse
universal. A IA deverá explicar o parâmetro, indicar o valor inicial
recomendado pela documentação da implementação utilizada, se disponível,
e orientar o usuário a validar o comportamento com os três usuários
cadastrados e com a pessoa não cadastrada.

O sistema deverá tratar ausência de rosto detectado, falha na leitura
dos modelos, câmera indisponível, arquivo de cadastro ausente ou
inválido e ausência de correspondência. Em caso de erro que impeça a
identificação, não deverá conceder acesso.

## 9. Etapas de desenvolvimento

### Etapa 1 --- Preparação do ambiente ✅ CONCLUÍDA

-   ✅ Verificar a instalação do Python. → **Python 3.15.2**
-   ✅ Criar a pasta do projeto e o ambiente virtual. → `venv/` criado
-   ✅ Instalar a dependência OpenCV necessária. → **opencv-contrib-python 5.0.0**, **numpy 2.5.4**
-   ✅ Verificar se as classes de YuNet e SFace estão disponíveis na versão
    instalada. → `cv2.FaceDetectorYN` ✅ | `cv2.FaceRecognizerSF` ✅
-   ✅ Criar `requirements.txt`. → criado em `reconhecimento_facial/requirements.txt`
-   ✅ Testar a instalação. → importação do OpenCV confirmada

**Progresso:** Parado na **Etapa 5 --- Cadastro e armazenamento** (próxima a ser implementada).

### Etapa 2 --- Modelos e câmera ✅ CONCLUÍDA

-   ✅ Criar a estrutura de pastas. → `reconhecimento_facial/models/` e `data/`
-   ✅ Obter os arquivos de modelo YuNet e SFace de fontes oficiais. →
    Baixados do **OpenCV Zoo** (GitHub oficial):
    `yunet.onnx` (233 KB) | `sface.onnx` (37 MB)
-   ✅ Criar `config.py` → caminhos, parâmetros da câmera e thresholds
-   ✅ Criar `camera.py` → funções abrir, capturar e encerrar câmera
-   ✅ Testar se a webcam abre, captura imagens e encerra corretamente.

### Etapa 3 --- Detecção facial com YuNet ✅ CONCLUÍDA

-   ✅ Criar `face_detector.py`. → `criar_detector()`, `detectar_rosto()`, `desenhar_deteccoes()`
-   ✅ Carregar o modelo YuNet. → via `cv2.FaceDetectorYN.create()`
-   ✅ Detectar rostos nos quadros da webcam. → retorna array de detecções
-   ✅ Mostrar visualmente a região detectada durante o teste. → retângulo verde + pontos de referência
-   ✅ Tratar quadros sem rosto detectado. → exibe "Nenhum rosto detectado"

### Etapa 4 --- Extração e comparação com SFace ✅ CONCLUÍDA

-   ✅ Criar `face_recognizer.py`. → `criar_reconhecedor()`, `extrair_caracteristicas()`,
    `comparar_faces()`, `caracteristicas_para_lista()`, `lista_para_caracteristicas()`
-   ✅ Integrar o SFace. → via `cv2.FaceRecognizerSF.create()`
-   ✅ Preparar/alinhar a face detectada conforme a API do OpenCV. → `alignCrop()`
-   ✅ Gerar a representação facial. → `feature()` retorna vetor numpy
-   ✅ Testar a comparação. → teste independente com captura de 2 rostos + validação de conversão JSON

### Etapa 5 --- Cadastro e armazenamento ✅ CONCLUÍDA

-   ✅ Criar `user_database.py`. → `carregar_usuarios()`, `salvar_usuarios()`,
    `validar_banco()`, `cadastrar_usuario()`, `cadastrar_todos()`, `listar_usuarios()`
-   ✅ Implementar o cadastro dos três usuários, um por nível. → fluxo interativo
    com captura via webcam, impede repetição de nível
-   ✅ Salvar as representações faciais e os dados no JSON. → `data/users.json`
-   ✅ Implementar leitura e validação do arquivo. → verifica 3 usuários,
    níveis {1,2,3}, campos obrigatórios
-   ✅ Verificar que existem três cadastros e que cada um possui um nível
    válido. → função `validar_banco()`

**Progresso:** Parado na **Etapa 8 --- Testes e ajustes** (próxima a ser implementada).

### Etapa 6 --- Controle de acesso ✅ CONCLUÍDA

-   ✅ Criar `access_control.py`. → `identificar_usuario()`, `autorizar_acesso()`,
    `exibir_resultado()`, `processar_acesso()`, `processar_erro()`
-   ✅ Relacionar o usuário reconhecido ao nível salvo. → consulta nível e descrição
-   ✅ Implementar as mensagens e decisões de acesso. → mensagens para níveis 1, 2, 3
-   ✅ Garantir que pessoa sem correspondência receba acesso negado. →
    "Pessoa não cadastrada — acesso negado"
-   ✅ Manter reconhecimento e autorização como etapas distintas. →
    `identificar_usuario()` (quem é) separado de `autorizar_acesso()` (qual nível)

### Etapa 7 --- Integração em `main.py` ✅ CONCLUÍDA

-   ✅ Integrar câmera, YuNet, SFace, cadastro, comparação e controle de
    acesso. → tudo coordenado pelo `main.py`
-   ✅ Criar o fluxo de execução pelo terminal. → menu com 3 opções + sair
-   ✅ Permitir iniciar e encerrar a análise. → 'r' identifica, 'q' volta ao menu
-   ✅ Apresentar nome, nível e decisão quando houver reconhecimento. →
    via `access_control.processar_acesso()`

### Etapa 8 --- Testes e ajustes

-   Testar individualmente os três usuários cadastrados.
-   Testar uma quarta pessoa não cadastrada.
-   Observar variações de iluminação e posicionamento.
-   Ajustar o critério de comparação com base nos testes, sem inventar
    resultados.
-   Corrigir falhas e documentar limitações.

### Etapa 9 --- Documentação e entrega

-   Atualizar o `README.md` com instalação, modelos, cadastro, execução
    e testes.
-   Revisar a organização dos arquivos.
-   Confirmar que o programa funciona em execução local pelo terminal.
-   Preparar a apresentação demonstrando os três usuários cadastrados e
    a pessoa não cadastrada.

## 10. Regras de autorização e mensagens

O programa deverá respeitar exatamente esta relação:

  -----------------------------------------------------------------------
  Situação                            Resultado esperado
  ----------------------------------- -----------------------------------
  Usuário reconhecido com Nível 1     Exibir identificação, Nível 1 e
                                      acesso concedido conforme permissão
                                      geral

  Usuário reconhecido com Nível 2     Exibir identificação, Nível 2 e
                                      acesso correspondente à permissão
                                      restrita

  Usuário reconhecido com Nível 3     Exibir identificação, Nível 3 e
                                      acesso exclusivo

  Pessoa sem correspondência adequada Informar pessoa não cadastrada e
                                      negar acesso

  Erro que impeça a identificação     Informar falha e não conceder
                                      acesso
  -----------------------------------------------------------------------

Não implemente hierarquia adicional, permissões extras ou regras
diferentes das descritas sem autorização do usuário.

## 11. Critérios de conclusão

O projeto estará implementado quando:

-   a aplicação iniciar pelo terminal no Windows 10 ou 11;
-   a webcam puder capturar imagens;
-   YuNet detectar os rostos;
-   SFace gerar e comparar representações faciais;
-   os três usuários puderem ser cadastrados, cada um com um nível
    diferente;
-   o sistema identificar os usuários cadastrados nos testes realizados;
-   o sistema apresentar o nível associado ao usuário reconhecido;
-   uma pessoa não cadastrada for tratada como não reconhecida e receber
    acesso negado;
-   erros básicos forem tratados sem conceder acesso indevidamente;
-   a documentação explicar como instalar, cadastrar, executar e testar
    o programa.

## 12. Limites do projeto

Este projeto tem finalidade acadêmica e demonstrativa. O reconhecimento
facial pode apresentar erros em razão de iluminação, ângulo, qualidade
da câmera, diferenças entre as imagens de cadastro e teste e semelhança
entre indivíduos. Os resultados deverão ser avaliados nas condições
efetivamente testadas.

A aplicação não deverá ser apresentada como solução pronta para proteger
instalações reais ou como sistema de segurança governamental. O objetivo
é demonstrar a aplicação dos conceitos de processamento digital de
imagens e visão computacional em um sistema simples de identificação e
controle de acesso.
