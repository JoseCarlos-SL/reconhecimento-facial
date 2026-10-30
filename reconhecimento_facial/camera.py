"""
camera.py — Abre a webcam, captura quadros e encerra a câmera corretamente.
"""

import cv2
import config


def abrir_camera():
    """
    Abre a webcam configurada e define a resolução.
    Retorna o objeto VideoCapture ou None se falhar.
    """
    cap = cv2.VideoCapture(config.CAMERA_INDEX)

    if not cap.isOpened():
        print("[ERRO] Não foi possível abrir a câmera.")
        return None

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)

    largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"[INFO] Câmera aberta com sucesso ({largura}x{altura}).")

    return cap


def capturar_quadro(cap):
    """
    Captura um único quadro da câmera.
    Retorna (True, quadro) em caso de sucesso ou (False, None) em caso de falha.
    """
    ret, frame = cap.read()
    if not ret:
        print("[ERRO] Falha ao capturar quadro da câmera.")
        return False, None
    return True, frame


def encerrar_camera(cap):
    """
    Libera a câmera e fecha todas as janelas do OpenCV.
    """
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Câmera encerrada.")


# --- Teste independente ---
if __name__ == "__main__":
    print("=== Teste da Câmera ===")
    print("Pressione 'q' para encerrar.\n")

    cap = abrir_camera()
    if cap is None:
        exit(1)

    while True:
        sucesso, quadro = capturar_quadro(cap)
        if not sucesso:
            break

        cv2.imshow("Teste da Camera - Pressione 'q' para sair", quadro)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    encerrar_camera(cap)
    print("Teste concluído.")
