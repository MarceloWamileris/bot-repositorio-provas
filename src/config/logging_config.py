import logging


def configurar_logging():
    """
    Configuração central de logging do bot.

    Deve ser chamada uma única vez, no início da
    aplicação (main.py), antes de qualquer outro
    módulo gerar logs.
    """

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s "
            "[%(levelname)s] "
            "%(name)s: %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Bibliotecas de terceiros tendem a ser muito
    # verbosas em nível INFO/DEBUG, silencia um pouco.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.WARNING)

    # O apscheduler loga toda execução das filas
    # (a cada 10s), mesmo quando não há nada a
    # processar. Isso deixa o terminal poluído sem
    # agregar informação útil no dia a dia.
    logging.getLogger("apscheduler").setLevel(logging.WARNING)