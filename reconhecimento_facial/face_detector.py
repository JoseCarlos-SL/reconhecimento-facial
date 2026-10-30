"""
face_detector.py — Carrega o modelo YuNet e localiza rostos nas imagens.
"""

import cv2
import config


def criar_detector(largura, altura):
    """
    Cria e retorna uma instância do detector facial YuNet.
    Recebe a largura e altura dos quadros da câmera.
    Retorna o detector ou None se o modelo não for encontrado.
    """
    try:
        detector = cv2.FaceDetectorYN.create(
            model=config.YUNET_MODEL_PATH,
            config="",
            input_size=(largura, altura),
            score_threshold=config.YUNET_SCORE_THRESHOLD,
            nms_threshold=config.YUNET_NMS_THRESHOLD,
            top_k=config.YUNET_TOP_K
        )
        print("[INFO] Detector YuNet carregado com sucesso.")
        return detector
    except cv2.error as e:
        print(f"[ERRO] Falha ao carregar o modelo YuNet: {e}")
        return None


def detectar_rosto(detector, quadro):
    """
    Detecta rostos no quadro fornecido.
    Retorna (True, detecções) se pelo menos um rosto for encontrado,
    ou (False, None) caso contrário.

    Cada detecção é um array com 15 valores:
    [x, y, w, h, x_olho_dir, y_olho_dir, x_olho_esq, y_olho_esq,
     x_nariz, y_nariz, x_boca_dir, y_boca_dir, x_boca_esq, y_boca_esq, confiança]
    """
    _, faces = detector.detect(quadro)

    if faces is None or len(faces) == 0:
        return False, None

    return True, faces


def desenhar_deteccoes(quadro, faces):
    """
    Desenha retângulos e pontos de referência nos rostos detectados.
    Útil para testes visuais. Modifica o quadro diretamente.
    """
    for face in faces:
        # Coordenadas do retângulo
        x, y, w, h = int(face[0]), int(face[1]), int(face[2]), int(face[3])
        confianca = face[14]

        # Retângulo ao redor do rosto
        cv2.rectangle(quadro, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Texto com confiança
        texto = f"{confianca:.2f}"
        cv2.putText(quadro, texto, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Pontos de referência: olhos, nariz, cantos da boca
        for i in range(5):
            px = int(face[4 + i * 2])
            py = int(face[5 + i * 2])
            cv2.circle(quadro, (px, py), 3, (0, 0, 255), -1)

    return quadro


# --- Teste independente ---
if __name__ == "__main__":
    import camera

    print("=== Teste de Detecção Facial (YuNet) ===")
    print("Pressione 'q' para encerrar.\n")

    cap = camera.abrir_camera()
    if cap is None:
        exit(1)

    largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    detector = criar_detector(largura, altura)
    if detector is None:
        camera.encerrar_camera(cap)
        exit(1)

    while True:
        sucesso, quadro = camera.capturar_quadro(cap)
        if not sucesso:
            break

        encontrou, faces = detectar_rosto(detector, quadro)

        if encontrou:
            desenhar_deteccoes(quadro, faces)
            cv2.putText(quadro, f"Rostos: {len(faces)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        else:
            cv2.putText(quadro, "Nenhum rosto detectado", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Deteccao Facial YuNet - Pressione 'q' para sair", quadro)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.encerrar_camera(cap)
    print("Teste concluído.")
