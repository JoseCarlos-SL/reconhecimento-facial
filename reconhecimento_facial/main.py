"""
main.py — Coordena o fluxo da aplicação e a interação pelo terminal.

Sistema de Identificação e Autenticação Biométrica
Projeto acadêmico — Reconhecimento facial com YuNet e SFace
"""

import sys
import os
import cv2

# Garante que os imports funcionem a partir do diretório do projeto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
import camera
import face_detector
import face_recognizer
import user_database
import access_control


def exibir_menu():
    """Exibe o menu principal no terminal."""
    print()
    print("=" * 55)
    print("  SISTEMA DE IDENTIFICAÇÃO E AUTENTICAÇÃO BIOMÉTRICA")
    print("=" * 55)
    print()
    print("  [1] Cadastrar usuários")
    print("  [2] Iniciar reconhecimento facial")
    print("  [3] Listar usuários cadastrados")
    print("  [0] Sair")
    print()


def verificar_modelos():
    """
    Verifica se os arquivos de modelos YuNet e SFace existem.
    Retorna True se ambos forem encontrados.
    """
    if not os.path.exists(config.YUNET_MODEL_PATH):
        print(f"[ERRO] Modelo YuNet não encontrado: {config.YUNET_MODEL_PATH}")
        return False

    if not os.path.exists(config.SFACE_MODEL_PATH):
        print(f"[ERRO] Modelo SFace não encontrado: {config.SFACE_MODEL_PATH}")
        return False

    print("[INFO] Modelos YuNet e SFace encontrados.")
    return True


def opcao_cadastrar():
    """Executa o fluxo de cadastro dos 3 usuários."""
    resultado = user_database.cadastrar_todos()
    if resultado is None:
        print("[AVISO] Cadastro não foi concluído.")


def opcao_listar():
    """Lista os usuários cadastrados."""
    usuarios = user_database.carregar_usuarios()
    user_database.listar_usuarios(usuarios)

    if usuarios:
        valido, msg = user_database.validar_banco(usuarios)
        print(f"[VALIDAÇÃO] {msg}")


def opcao_reconhecimento():
    """
    Executa o fluxo principal de reconhecimento facial em tempo real.
    Captura quadros da webcam, detecta rostos, extrai características
    e compara com os usuários cadastrados.
    """
    # Verifica cadastro
    usuarios = user_database.carregar_usuarios()
    valido, msg = user_database.validar_banco(usuarios)

    if not valido:
        print(f"[ERRO] {msg}")
        print("[INFO] Cadastre os 3 usuários antes de iniciar o reconhecimento.")
        return

    print(f"[INFO] {msg}")

    # Carrega modelos
    detector = face_detector.criar_detector(config.CAMERA_WIDTH, config.CAMERA_HEIGHT)
    reconhecedor = face_recognizer.criar_reconhecedor()

    if detector is None or reconhecedor is None:
        access_control.processar_erro("Falha ao carregar modelos de IA")
        return

    # Abre câmera
    cap = camera.abrir_camera()
    if cap is None:
        access_control.processar_erro("Câmera indisponível")
        return

    largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    detector.setInputSize((largura, altura))

    print()
    print("─" * 55)
    print("  RECONHECIMENTO FACIAL ATIVO")
    print("  Pressione 'r' para identificar o rosto na tela")
    print("  Pressione 'q' para voltar ao menu")
    print("─" * 55)
    print()

    while True:
        sucesso, quadro = camera.capturar_quadro(cap)
        if not sucesso:
            access_control.processar_erro("Falha na captura da câmera")
            break

        encontrou, faces = face_detector.detectar_rosto(detector, quadro)

        quadro_visual = quadro.copy()

        if encontrou:
            face_detector.desenhar_deteccoes(quadro_visual, faces)
            cv2.putText(quadro_visual, "'r' identifica | 'q' sai",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        else:
            cv2.putText(quadro_visual, "Nenhum rosto detectado | 'q' sai",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow("Reconhecimento Facial - 'r' identifica, 'q' sai", quadro_visual)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord('q'):
            break

        elif tecla == ord('r'):
            if not encontrou:
                print("[AVISO] Nenhum rosto detectado no quadro atual.")
                continue

            # Extrai características do rosto detectado
            caracteristicas = face_recognizer.extrair_caracteristicas(
                reconhecedor, quadro, faces[0]
            )

            if caracteristicas is None:
                access_control.processar_erro("Falha ao extrair características faciais")
                continue

            # Processa identificação + autorização + exibição
            access_control.processar_acesso(
                reconhecedor, caracteristicas, usuarios
            )

    camera.encerrar_camera(cap)


def main():
    """Função principal — loop do menu."""
    print("\n" + "=" * 55)
    print("  Inicializando sistema...")
    print("=" * 55)

    # Verifica modelos
    if not verificar_modelos():
        print("\n[ERRO] Verifique se os modelos estão na pasta 'models/'.")
        print("Encerrando.")
        return

    while True:
        exibir_menu()
        opcao = input("  Escolha uma opção: ").strip()

        if opcao == "1":
            opcao_cadastrar()
        elif opcao == "2":
            opcao_reconhecimento()
        elif opcao == "3":
            opcao_listar()
        elif opcao == "0":
            print("\n[INFO] Sistema encerrado. Até logo!\n")
            break
        else:
            print("[AVISO] Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
