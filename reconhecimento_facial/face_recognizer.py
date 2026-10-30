"""
face_recognizer.py — Utiliza o SFace para alinhar/preparar a face,
extrair características faciais e comparar representações.
"""

import cv2
import numpy as np
import config


def criar_reconhecedor():
    """
    Cria e retorna uma instância do reconhecedor facial SFace.
    Retorna o reconhecedor ou None se o modelo não for encontrado.
    """
    try:
        reconhecedor = cv2.FaceRecognizerSF.create(
            model=config.SFACE_MODEL_PATH,
            config=""
        )
        print("[INFO] Reconhecedor SFace carregado com sucesso.")
        return reconhecedor
    except cv2.error as e:
        print(f"[ERRO] Falha ao carregar o modelo SFace: {e}")
        return None


def extrair_caracteristicas(reconhecedor, quadro, face):
    """
    Alinha o rosto e extrai a representação numérica (feature vector)
    usando o SFace.

    Parâmetros:
        reconhecedor: instância do FaceRecognizerSF
        quadro: imagem original (frame da câmera)
        face: array de detecção do YuNet (1 linha com 15 valores)

    Retorna:
        numpy array com a representação facial, ou None se falhar.
    """
    try:
        # alignCrop alinha e recorta o rosto conforme os pontos de referência
        rosto_alinhado = reconhecedor.alignCrop(quadro, face)

        # Extrai o vetor de características (embedding)
        caracteristicas = reconhecedor.feature(rosto_alinhado)

        return caracteristicas
    except cv2.error as e:
        print(f"[ERRO] Falha ao extrair características faciais: {e}")
        return None


def comparar_faces(reconhecedor, caract1, caract2):
    """
    Compara duas representações faciais usando similaridade de cosseno.

    Retorna:
        (similaridade, é_mesmo_rosto)
        - similaridade: float com o valor da similaridade de cosseno
        - é_mesmo_rosto: True se acima do threshold configurado
    """
    similaridade = reconhecedor.match(
        caract1, caract2,
        dis_type=cv2.FaceRecognizerSF_FR_COSINE
    )

    eh_mesmo = similaridade >= config.COSINE_SIMILARITY_THRESHOLD

    return similaridade, eh_mesmo


def caracteristicas_para_lista(caracteristicas):
    """
    Converte o numpy array de características para uma lista Python,
    permitindo salvar no JSON.
    """
    return caracteristicas.flatten().tolist()


def lista_para_caracteristicas(lista):
    """
    Converte uma lista Python de volta para numpy array,
    no formato esperado pelo OpenCV para comparação.
    """
    return np.array(lista, dtype=np.float32).reshape(1, -1)


# --- Teste independente ---
if __name__ == "__main__":
    import camera
    import face_detector

    print("=== Teste de Reconhecimento Facial (SFace) ===")
    print("Este teste captura dois rostos e compara suas características.")
    print("Pressione 'c' para capturar um rosto. Pressione 'q' para sair.\n")

    cap = camera.abrir_camera()
    if cap is None:
        exit(1)

    largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    detector = face_detector.criar_detector(largura, altura)
    reconhecedor = criar_reconhecedor()

    if detector is None or reconhecedor is None:
        camera.encerrar_camera(cap)
        exit(1)

    capturas = []  # Lista para guardar as características capturadas

    while True:
        sucesso, quadro = camera.capturar_quadro(cap)
        if not sucesso:
            break

        encontrou, faces = face_detector.detectar_rosto(detector, quadro)

        # Copia para desenhar sem alterar o original
        quadro_visual = quadro.copy()

        if encontrou:
            face_detector.desenhar_deteccoes(quadro_visual, faces)
            msg = f"Capturas: {len(capturas)}/2 | Pressione 'c' para capturar"
        else:
            msg = "Nenhum rosto detectado"

        cv2.putText(quadro_visual, msg, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        cv2.imshow("Teste SFace - 'c' captura, 'q' sai", quadro_visual)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord('q'):
            break
        elif tecla == ord('c') and encontrou:
            # Captura as características do primeiro rosto detectado
            caract = extrair_caracteristicas(reconhecedor, quadro, faces[0])
            if caract is not None:
                capturas.append(caract)
                print(f"[INFO] Captura {len(capturas)} realizada com sucesso.")

                if len(capturas) == 2:
                    # Compara as duas capturas
                    sim, mesmo = comparar_faces(reconhecedor, capturas[0], capturas[1])
                    print(f"\n--- Resultado da Comparação ---")
                    print(f"Similaridade (cosseno): {sim:.4f}")
                    print(f"Threshold configurado:  {config.COSINE_SIMILARITY_THRESHOLD}")
                    print(f"Mesmo rosto?            {'SIM' if mesmo else 'NÃO'}")
                    print(f"-------------------------------\n")

                    # Testa conversão JSON
                    lista = caracteristicas_para_lista(capturas[0])
                    reconstruido = lista_para_caracteristicas(lista)
                    sim_reconstruido, _ = comparar_faces(reconhecedor, capturas[0], reconstruido)
                    print(f"[TESTE JSON] Similaridade após conversão lista/numpy: {sim_reconstruido:.4f}")
                    print("(Deve ser 1.0000 ou muito próximo)\n")

                    capturas.clear()
                    print("Capturas resetadas. Pode capturar novamente ou 'q' para sair.")

    camera.encerrar_camera(cap)
    print("Teste concluído.")
