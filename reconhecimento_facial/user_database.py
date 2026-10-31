"""
user_database.py — Cadastra, consulta e salva os três usuários no JSON.
"""

import json
import os
import uuid

import cv2
import numpy as np

import config
import camera
import face_detector
import face_recognizer


def carregar_usuarios():
    """
    Carrega o banco de dados de usuários do arquivo JSON.
    Retorna uma lista de dicionários, ou lista vazia se o arquivo
    não existir ou estiver inválido.
    """
    if not os.path.exists(config.USERS_DB_PATH):
        return []

    try:
        with open(config.USERS_DB_PATH, "r", encoding="utf-8") as f:
            dados = json.load(f)

        if not isinstance(dados, list):
            print("[ERRO] Arquivo de usuários com formato inválido.")
            return []

        return dados
    except (json.JSONDecodeError, IOError) as e:
        print(f"[ERRO] Falha ao ler arquivo de usuários: {e}")
        return []


def salvar_usuarios(usuarios):
    """
    Salva a lista de usuários no arquivo JSON.
    Cria o diretório data/ se não existir.
    """
    os.makedirs(os.path.dirname(config.USERS_DB_PATH), exist_ok=True)

    try:
        with open(config.USERS_DB_PATH, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=2)
        print(f"[INFO] Dados salvos em {config.USERS_DB_PATH}")
    except IOError as e:
        print(f"[ERRO] Falha ao salvar arquivo de usuários: {e}")


def validar_banco(usuarios):
    """
    Verifica se o banco de dados possui exatamente 3 usuários,
    cada um com um nível diferente (1, 2 e 3).
    Retorna (True, mensagem) ou (False, mensagem).
    """
    if len(usuarios) != 3:
        return False, f"Esperados 3 usuários, encontrados {len(usuarios)}."

    niveis = set()
    for u in usuarios:
        campos = ["id", "nome", "nivel", "caracteristicas"]
        for campo in campos:
            if campo not in u:
                return False, f"Usuário '{u.get('nome', '?')}' sem campo '{campo}'."

        if u["nivel"] not in [1, 2, 3]:
            return False, f"Nível inválido ({u['nivel']}) para '{u['nome']}'."

        niveis.add(u["nivel"])

    if niveis != {1, 2, 3}:
        return False, f"Níveis encontrados: {niveis}. Esperados: {{1, 2, 3}}."

    return True, "Banco de dados válido: 3 usuários, níveis 1, 2 e 3."


def obter_caracteristicas_usuario(usuarios, user_id):
    """
    Retorna o vetor de características (numpy array) de um usuário pelo ID.
    Retorna None se não encontrado.
    """
    for u in usuarios:
        if u["id"] == user_id:
            return face_recognizer.lista_para_caracteristicas(u["caracteristicas"])
    return None


def listar_usuarios(usuarios):
    """
    Exibe no terminal os usuários cadastrados.
    """
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    print(f"\n{'='*50}")
    print(f"{'USUÁRIOS CADASTRADOS':^50}")
    print(f"{'='*50}")
    for u in usuarios:
        print(f"  Nome:  {u['nome']}")
        print(f"  Nível: {u['nivel']}")
        print(f"  ID:    {u['id']}")
        print(f"  {'-'*46}")
    print()


def carregar_imagem_disco(caminho):
    """
    Carrega uma imagem com tratamento para:
    - Aspas e caracteres invisíveis do Windows (\u202a, etc.)
    - Caminhos relativos (pasta do projeto ou pasta raiz)
    - Suporte a caminhos com acentos e OneDrive usando np.fromfile + cv2.imdecode
    """
    if not caminho:
        return None, ""

    # Remove aspas e caracteres invisíveis de controle do Windows
    caminho_limpo = caminho.strip(" \t\r\n\"'\u202a\u202b\u202c\u202d\u202e\u200e\u200f")

    # Se não existir diretamente, procura em caminhos prováveis
    if not os.path.exists(caminho_limpo):
        # 1. Tenta relativo ao BASE_DIR (pasta reconhecimento_facial)
        tentativa_base = os.path.join(config.BASE_DIR, caminho_limpo)
        if os.path.exists(tentativa_base):
            caminho_limpo = tentativa_base
        else:
            # 2. Tenta na pasta raiz do projeto (Aps_reconhecimento_facial)
            pasta_raiz = os.path.dirname(config.BASE_DIR)
            tentativa_raiz = os.path.join(pasta_raiz, caminho_limpo)
            if os.path.exists(tentativa_raiz):
                caminho_limpo = tentativa_raiz

    if not os.path.exists(caminho_limpo):
        return None, caminho_limpo

    # Leitura segura via numpy para caminhos do Windows / OneDrive
    try:
        dados = np.fromfile(caminho_limpo, dtype=np.uint8)
        imagem = cv2.imdecode(dados, cv2.IMREAD_COLOR)
        return imagem, caminho_limpo
    except Exception:
        imagem = cv2.imread(caminho_limpo)
        return imagem, caminho_limpo


def extrair_de_arquivo(caminho_imagem, detector, reconhecedor):
    """
    Carrega uma imagem do disco, detecta o rosto e extrai as características.
    Retorna o vetor de características ou None se falhar.
    """
    imagem, caminho_resolvido = carregar_imagem_disco(caminho_imagem)

    if imagem is None:
        if not os.path.exists(caminho_resolvido):
            print(f"[ERRO] Arquivo não encontrado: {caminho_resolvido}")
        else:
            print(f"[ERRO] Não foi possível decodificar a imagem: {caminho_resolvido}")
        return None

    altura, largura = imagem.shape[:2]
    detector.setInputSize((largura, altura))
    detector.setScoreThreshold(config.YUNET_SCORE_THRESHOLD)

    encontrou, faces = face_detector.detectar_rosto(detector, imagem)
    if not encontrou or faces is None:
        print(f"[ERRO] Nenhum rosto detectado na imagem: {caminho_resolvido}")
        return None

    if len(faces) > 1:
        print(f"[AVISO] Mais de um rosto detectado ({len(faces)}). Utilizando o primeiro rosto detectado.")

    caracteristicas = face_recognizer.extrair_caracteristicas(reconhecedor, imagem, faces[0])
    if caracteristicas is not None:
        print(f"[INFO] Rosto extraído com sucesso de '{os.path.basename(caminho_resolvido)}' ({largura}x{altura}).")
    return caracteristicas


def cadastrar_usuario(detector, reconhecedor):
    """
    Realiza o cadastro interativo de um único usuário.
    Solicita nome, nível e permite capturar pela câmera OU carregar de arquivo de foto.

    Retorna o dicionário do usuário cadastrado, ou None se falhar.
    """
    print("\n--- Cadastro de Novo Usuário ---\n")

    # Solicita o nome
    nome = input("Digite o nome do usuário: ").strip()
    if not nome:
        print("[ERRO] Nome não pode ser vazio.")
        return None

    # Solicita o nível
    while True:
        nivel_str = input("Digite o nível de autorização (1, 2 ou 3): ").strip()
        if nivel_str in ["1", "2", "3"]:
            nivel = int(nivel_str)
            break
        print("[AVISO] Nível inválido. Digite 1, 2 ou 3.")

    # Escolhe a fonte da imagem
    print("\nComo deseja fornecer o rosto do usuário?")
    print("  [1] Capturar pela câmera / webcam")
    print("  [2] Carregar arquivo de foto/imagem do computador")
    opcao_fonte = input("Escolha uma opção (1 ou 2) [padrão: 1]: ").strip()

    caracteristicas = None

    if opcao_fonte == "2":
        # Carregar via arquivo de imagem
        caminho = input("Digite o caminho do arquivo de imagem (ex: foto.jpg): ").strip()
        caracteristicas = extrair_de_arquivo(caminho, detector, reconhecedor)
    else:
        # Captura via câmera
        print("\n[INFO] A câmera será aberta para capturar seu rosto.")
        print("[INFO] Posicione o rosto na frente da câmera e pressione 'c' para capturar.")
        print("[INFO] Pressione 'q' para cancelar.\n")

        cap = camera.abrir_camera()
        if cap is None:
            return None

        largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        detector.setInputSize((largura, altura))

        while True:
            sucesso, quadro = camera.capturar_quadro(cap)
            if not sucesso:
                break

            encontrou, faces = face_detector.detectar_rosto(detector, quadro)

            quadro_visual = quadro.copy()

            if encontrou:
                face_detector.desenhar_deteccoes(quadro_visual, faces)
                cv2.putText(quadro_visual, f"Cadastrando: {nome} | 'c' captura, 'q' cancela",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            else:
                cv2.putText(quadro_visual, "Nenhum rosto detectado",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            cv2.imshow("Cadastro - 'c' captura, 'q' cancela", quadro_visual)

            tecla = cv2.waitKey(1) & 0xFF

            if tecla == ord('q'):
                print("[INFO] Cadastro cancelado pelo usuário.")
                break
            elif tecla == ord('c'):
                if not encontrou:
                    print("[AVISO] Nenhum rosto detectado. Tente novamente.")
                    continue

                caracteristicas = face_recognizer.extrair_caracteristicas(
                    reconhecedor, quadro, faces[0]
                )

                if caracteristicas is not None:
                    print(f"[INFO] Rosto de '{nome}' capturado com sucesso!")
                    break
                else:
                    print("[ERRO] Falha ao extrair características. Tente novamente.")

        camera.encerrar_camera(cap)

    if caracteristicas is None:
        return None

    usuario = {
        "id": str(uuid.uuid4()),
        "nome": nome,
        "nivel": nivel,
        "caracteristicas": face_recognizer.caracteristicas_para_lista(caracteristicas)
    }

    return usuario


def cadastrar_todos():
    """
    Fluxo completo para cadastrar os 3 usuários do sistema.
    Cada um será associado a um nível diferente.
    """
    print("\n" + "=" * 50)
    print("  CADASTRO DOS TRÊS USUÁRIOS DO SISTEMA")
    print("=" * 50)
    print("\nVocê irá cadastrar 3 usuários, cada um com um nível diferente.")
    print("Níveis disponíveis:")
    print("  Nível 1: acesso com permissão geral")
    print("  Nível 2: acesso restrito (diretores de divisões)")
    print("  Nível 3: acesso exclusivo (Ministro do Meio Ambiente)")

    # Carrega usuários existentes
    usuarios = carregar_usuarios()

    if len(usuarios) >= 3:
        valido, msg = validar_banco(usuarios)
        if valido:
            print(f"\n[INFO] {msg}")
            listar_usuarios(usuarios)
            resp = input("Deseja recadastrar todos? (s/n): ").strip().lower()
            if resp != 's':
                print("[INFO] Cadastro mantido.")
                return usuarios
            usuarios = []

    # Cria detector e reconhecedor
    detector = face_detector.criar_detector(config.CAMERA_WIDTH, config.CAMERA_HEIGHT)
    reconhecedor = face_recognizer.criar_reconhecedor()

    if detector is None or reconhecedor is None:
        print("[ERRO] Não foi possível carregar os modelos.")
        return None

    niveis_usados = set()
    novos_usuarios = []

    for i in range(3):
        print(f"\n{'─'*50}")
        print(f"  Usuário {i + 1} de 3")
        print(f"  Níveis já usados: {niveis_usados if niveis_usados else 'nenhum'}")
        print(f"{'─'*50}")

        while True:
            usuario = cadastrar_usuario(detector, reconhecedor)

            if usuario is None:
                resp = input("\nCadastro falhou. Tentar novamente? (s/n): ").strip().lower()
                if resp != 's':
                    print("[INFO] Cadastro interrompido.")
                    return None
                continue

            if usuario["nivel"] in niveis_usados:
                print(f"[AVISO] Nível {usuario['nivel']} já foi usado. Escolha outro.")
                continue

            niveis_usados.add(usuario["nivel"])
            novos_usuarios.append(usuario)
            print(f"[OK] '{usuario['nome']}' cadastrado com nível {usuario['nivel']}.")
            break

    # Salva no JSON
    salvar_usuarios(novos_usuarios)

    # Valida
    valido, msg = validar_banco(novos_usuarios)
    print(f"\n[VALIDAÇÃO] {msg}")
    listar_usuarios(novos_usuarios)

    return novos_usuarios


# --- Teste independente ---
if __name__ == "__main__":
    print("=== Cadastro de Usuários ===\n")
    resultado = cadastrar_todos()

    if resultado:
        print("\nCadastro finalizado com sucesso!")
    else:
        print("\nCadastro não foi concluído.")
