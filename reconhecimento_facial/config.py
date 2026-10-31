"""
config.py — Concentra caminhos dos modelos, configurações da câmera
e parâmetros do reconhecimento facial.
"""

import os

# Diretório base do projeto (onde este arquivo está)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Caminhos dos modelos ---
MODELS_DIR = os.path.join(BASE_DIR, "models")
YUNET_MODEL_PATH = os.path.join(MODELS_DIR, "yunet.onnx")
SFACE_MODEL_PATH = os.path.join(MODELS_DIR, "sface.onnx")

# --- Caminho do banco de dados de usuários ---
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_DB_PATH = os.path.join(DATA_DIR, "users.json")

# --- Configurações da câmera ---
# Pode ser o índice da webcam (ex: 0, 1) ou a URL do IP Webcam
# Exemplo IP Webcam: "http://192.168.1.15:8080/video"
CAMERA_SOURCE = 0        # Url da camera
CAMERA_WIDTH = 640        # Largura do quadro capturado
CAMERA_HEIGHT = 480       # Altura do quadro capturado

# --- Parâmetros do YuNet (detecção facial) ---
# 0.6 é o valor padrão recomendado pela documentação do OpenCV Zoo
YUNET_SCORE_THRESHOLD = 0.6    # Confiança mínima para considerar uma detecção
YUNET_NMS_THRESHOLD = 0.3      # Supressão de não-máximos
YUNET_TOP_K = 5000             # Número máximo de candidatos antes do NMS

# --- Parâmetros do SFace (reconhecimento facial) ---
# Limiar de similaridade de cosseno para considerar que dois rostos
# pertencem à mesma pessoa. Valor inicial recomendado pela documentação
# do OpenCV. Deve ser ajustado durante os testes (Etapa 8).
COSINE_SIMILARITY_THRESHOLD = 0.363
