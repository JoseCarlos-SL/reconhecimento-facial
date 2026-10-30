"""
access_control.py — Consulta o nível do usuário identificado e
determina a decisão de acesso.

Identificação e autorização são etapas distintas:
  - Identificação: qual usuário corresponde ao rosto detectado.
  - Autorização: qual nível de acesso esse usuário possui.
"""

import face_recognizer
import user_database


# Descrições dos níveis de autorização
NIVEIS_DESCRICAO = {
    1: "Permissão geral",
    2: "Acesso restrito (diretores de divisões)",
    3: "Acesso exclusivo (Ministro do Meio Ambiente)"
}


def identificar_usuario(reconhecedor, caracteristicas_capturadas, usuarios):
    """
    Compara as características capturadas com todos os usuários cadastrados.
    Retorna (usuario, similaridade) do melhor match acima do threshold,
    ou (None, 0.0) se nenhum corresponder.

    Esta função realiza apenas a IDENTIFICAÇÃO (quem é a pessoa).
    """
    melhor_usuario = None
    melhor_similaridade = 0.0

    for usuario in usuarios:
        caract_cadastrada = face_recognizer.lista_para_caracteristicas(
            usuario["caracteristicas"]
        )

        similaridade, eh_mesmo = face_recognizer.comparar_faces(
            reconhecedor, caracteristicas_capturadas, caract_cadastrada
        )

        if eh_mesmo and similaridade > melhor_similaridade:
            melhor_similaridade = similaridade
            melhor_usuario = usuario

    return melhor_usuario, melhor_similaridade


def autorizar_acesso(usuario):
    """
    Consulta o nível do usuário identificado e retorna a decisão de acesso.
    Esta função realiza apenas a AUTORIZAÇÃO (qual acesso a pessoa tem).

    Retorna um dicionário com:
        - reconhecido: bool
        - nome: str
        - nivel: int
        - descricao_nivel: str
        - mensagem: str
    """
    if usuario is None:
        return {
            "reconhecido": False,
            "nome": None,
            "nivel": None,
            "descricao_nivel": None,
            "mensagem": "Pessoa não cadastrada — acesso negado"
        }

    nivel = usuario["nivel"]
    descricao = NIVEIS_DESCRICAO.get(nivel, "Nível desconhecido")

    mensagens = {
        1: f"Acesso concedido — {descricao}",
        2: f"Acesso concedido — {descricao}",
        3: f"Acesso concedido — {descricao}"
    }

    return {
        "reconhecido": True,
        "nome": usuario["nome"],
        "nivel": nivel,
        "descricao_nivel": descricao,
        "mensagem": mensagens.get(nivel, "Erro: nível inválido — acesso negado")
    }


def exibir_resultado(resultado, similaridade=0.0):
    """
    Exibe o resultado da identificação e autorização no terminal.
    """
    print()
    print("=" * 55)

    if resultado["reconhecido"]:
        print(f"  USUÁRIO IDENTIFICADO")
        print(f"  Nome:          {resultado['nome']}")
        print(f"  Nível:         {resultado['nivel']} — {resultado['descricao_nivel']}")
        print(f"  Similaridade:  {similaridade:.4f}")
        print(f"  Decisão:       {resultado['mensagem']}")
    else:
        print(f"  ACESSO NEGADO")
        print(f"  {resultado['mensagem']}")
        if similaridade > 0:
            print(f"  Maior similaridade encontrada: {similaridade:.4f} (abaixo do limiar)")

    print("=" * 55)
    print()


def processar_acesso(reconhecedor, caracteristicas_capturadas, usuarios):
    """
    Função principal que executa o fluxo completo:
    1. Identifica o usuário (quem é)
    2. Autoriza o acesso (qual nível tem)
    3. Exibe o resultado no terminal

    Retorna o dicionário de resultado.
    """
    # Etapa 1: Identificação
    usuario, similaridade = identificar_usuario(
        reconhecedor, caracteristicas_capturadas, usuarios
    )

    # Etapa 2: Autorização
    resultado = autorizar_acesso(usuario)

    # Etapa 3: Exibição
    exibir_resultado(resultado, similaridade)

    return resultado


def processar_erro(mensagem_erro):
    """
    Trata erros que impeçam a identificação.
    Em caso de erro, nunca concede acesso.
    """
    print()
    print("=" * 55)
    print(f"  ERRO — ACESSO NEGADO")
    print(f"  {mensagem_erro}")
    print("=" * 55)
    print()

    return {
        "reconhecido": False,
        "nome": None,
        "nivel": None,
        "descricao_nivel": None,
        "mensagem": f"Erro: {mensagem_erro} — acesso negado"
    }
