from pathlib import Path
import shutil
import subprocess

from config.settings import settings
from data.catalogo_disciplinas import CATALOGO_DISCIPLINAS


class GitHubSyncService:

    CAMINHO_PROVAS = (
        settings.PROVAS_PATH
    )

    CAMINHO_REPOSITORIO = (
        settings.BASE_STORAGE
        / "github"
        / "repositorio-provas-faeterj"
    )

    PERIODOS = {
        "Primeiro Período": "01 - Primeiro Período",
        "Segundo Período": "02 - Segundo Período",
        "Terceiro Período": "03 - Terceiro Período",
        "Quarto Período": "04 - Quarto Período",
        "Quinto Período": "05 - Quinto Período",
    }

    @classmethod
    def obter_sigla_github(
        cls,
        periodo: str,
        nome_disciplina: str,
    ) -> str:
        """
        Obtém o código da disciplina através do catálogo
        e remove o número correspondente ao período.

        Aceita nomes de pasta no formato:

        Engenharia de Requisitos
        Engenharia de Requisitos (2REQ)

        Exemplo:

        1FAC
        ->
        FAC
        """

        disciplinas = CATALOGO_DISCIPLINAS.get(
            periodo,
            [],
        )

        # --------------------------------------------------
        # O acervo pode possuir o código da disciplina no
        # nome da pasta, enquanto o catálogo possui apenas
        # o nome da disciplina.
        #
        # Exemplo:
        #
        # Engenharia de Requisitos (2REQ)
        #
        # torna-se:
        #
        # Engenharia de Requisitos
        # --------------------------------------------------

        nome_catalogo = nome_disciplina

        if "(" in nome_catalogo:
            nome_catalogo = (
                nome_catalogo
                .rsplit("(", 1)[0]
                .strip()
            )

        for disciplina in disciplinas:

            if disciplina["nome"] == nome_catalogo:

                codigo = disciplina["codigo"]

                return codigo[1:]

        raise ValueError(
            f"Disciplina não encontrada no catálogo: "
            f"{nome_disciplina}"
        )

    @classmethod
    def gerar_mensagem_commit(
        cls,
        avaliacao: dict,
        operacao: str,
    ) -> str:
        """
        Gera automaticamente a mensagem padronizada
        do commit.

        Adição:

        feat: adiciona AV1 de FAC - Professor (2026.2 - Noite)

        Substituição:

        fix: substitui AV1 de FAC - Professor (2026.2 - Noite)

        Exceção para 1FAC:

        feat: adiciona AV1 de FAC-A - Professor (2026.2 - Noite)
        """

        if operacao == "adicionar":

            tipo = "feat"
            acao = "adiciona"

        elif operacao == "substituir":

            tipo = "fix"
            acao = "substitui"

        else:

            raise ValueError(
                f"Operação inválida: {operacao}"
            )

        periodo = avaliacao["periodo"]

        sigla = cls.obter_sigla_github(
            periodo,
            avaliacao["nome_disciplina"],
        )

        # --------------------------------------------------
        # Exceção da disciplina 1FAC
        # --------------------------------------------------

        if avaliacao["codigo_disciplina"] == "1FAC":

            turma = avaliacao.get(
                "turma_fac"
            )

            if not turma:

                raise ValueError(
                    "Turma da FAC não informada."
                )

            sigla = turma

        return (
            f"{tipo}: "
            f"{acao} "
            f"{avaliacao['avaliacao']} "
            f"de {sigla} "
            f"- {avaliacao['nome_professor']} "
            f"({avaliacao['ano']}."
            f"{avaliacao['semestre']} "
            f"- {avaliacao['turno']})"
        )

    @classmethod
    def ordenar_semestres(
        cls,
        diretorio: Path,
    ) -> None:
        """
        Ordena os semestres somente na cópia destinada
        ao GitHub.

        Exemplo:

        2024-1
        2026-1
        2026-2

        torna-se:

        01 - 2026-2
        02 - 2026-1
        03 - 2024-1

        A estrutura original do HD não é alterada.
        """

        semestres = []

        for item in diretorio.iterdir():

            if not item.is_dir():
                continue

            try:

                ano, semestre = item.name.split("-")

                ano = int(ano)
                semestre = int(semestre)

            except ValueError:

                continue

            if semestre not in (1, 2):
                continue

            semestres.append(
                (
                    ano,
                    semestre,
                    item,
                )
            )

        semestres.sort(
            key=lambda item: (
                item[0],
                item[1],
            ),
            reverse=True,
        )

        nomes_temporarios = []

        for indice, (
            ano,
            semestre,
            caminho,
        ) in enumerate(
            semestres,
            start=1,
        ):

            nome_temporario = (
                f".temp_semestre_{indice}"
            )

            caminho_temporario = (
                diretorio
                / nome_temporario
            )

            caminho.rename(
                caminho_temporario,
            )

            nomes_temporarios.append(
                (
                    caminho_temporario,
                    ano,
                    semestre,
                )
            )

        for indice, (
            caminho_temporario,
            ano,
            semestre,
        ) in enumerate(
            nomes_temporarios,
            start=1,
        ):

            nome_final = (
                f"{indice:02d} - "
                f"{ano}-{semestre}"
            )

            destino = (
                diretorio
                / nome_final
            )

            caminho_temporario.rename(
                destino,
            )

    @classmethod
    def organizar_semestres(
        cls,
        diretorio_periodo: Path,
    ) -> None:
        """
        Percorre disciplinas e professores de um período
        e ordena os semestres somente na cópia do GitHub.
        """

        if not diretorio_periodo.exists():
            return

        for disciplina in (
            diretorio_periodo.iterdir()
        ):

            if not disciplina.is_dir():
                continue

            for professor in (
                disciplina.iterdir()
            ):

                if not professor.is_dir():
                    continue

                cls.ordenar_semestres(
                    professor,
                )

    @classmethod
    def adicionar_gitkeep(
        cls,
        diretorio: Path,
    ) -> None:
        """
        Adiciona .gitkeep às pastas estruturais que não
        possuem arquivos diretamente.

        Isso mantém a estrutura navegável no GitHub.
        """

        if not diretorio.exists():
            return

        for pasta in diretorio.rglob("*"):

            if not pasta.is_dir():
                continue

            possui_arquivo = any(
                item.is_file()
                for item in pasta.iterdir()
            )

            if possui_arquivo:
                continue

            gitkeep = (
                pasta
                / ".gitkeep"
            )

            gitkeep.touch(
                exist_ok=True,
            )

    @classmethod
    def copiar_periodo_para_github(
        cls,
        periodo: str,
        destino_periodo: Path,
    ) -> None:
        """
        Copia um período do acervo para o repositório
        do GitHub, convertendo o nome das disciplinas
        para suas respectivas siglas.
        """

        origem_periodo = (
            cls.CAMINHO_PROVAS
            / periodo
        )

        if not origem_periodo.exists():
            return

        destino_periodo.mkdir(
            parents=True,
            exist_ok=True,
        )

        for disciplina in origem_periodo.iterdir():

            if not disciplina.is_dir():
                continue

            sigla = cls.obter_sigla_github(
                periodo,
                disciplina.name,
            )

            destino_disciplina = (
                destino_periodo
                / sigla
            )

            shutil.copytree(
                disciplina,
                destino_disciplina,
            )

    @classmethod
    def sincronizar(
        cls,
        avaliacao: dict,
        operacao: str,
    ) -> bool:

        if not cls.CAMINHO_PROVAS.exists():

            print(
                "Pasta de provas não encontrada."
            )

            return False

        if not cls.CAMINHO_REPOSITORIO.exists():

            print(
                "Repositório local do GitHub "
                "não encontrado."
            )

            return False

        # --------------------------------------------------
        # Limpa o conteúdo atual do repositório.
        #
        # O .git permanece intacto.
        # --------------------------------------------------

        for item in (
            cls.CAMINHO_REPOSITORIO.iterdir()
        ):

            if item.name == ".git":
                continue

            if item.is_dir():

                shutil.rmtree(
                    item,
                )

            else:

                item.unlink()

        # --------------------------------------------------
        # Copia os períodos.
        # --------------------------------------------------

        for (
            nome_periodo,
            nome_github,
        ) in cls.PERIODOS.items():

            destino = (
                cls.CAMINHO_REPOSITORIO
                / nome_github
            )

            cls.copiar_periodo_para_github(
                nome_periodo,
                destino,
            )

            cls.organizar_semestres(
                destino,
            )

        # --------------------------------------------------
        # Adiciona .gitkeep nas pastas estruturais.
        # --------------------------------------------------

        cls.adicionar_gitkeep(
            cls.CAMINHO_REPOSITORIO,
        )

        # --------------------------------------------------
        # Git add
        # --------------------------------------------------

        subprocess.run(
            [
                "git",
                "add",
                ".",
            ],
            cwd=cls.CAMINHO_REPOSITORIO,
            check=True,
        )

        # --------------------------------------------------
        # Verifica se realmente houve alteração.
        # --------------------------------------------------

        resultado = subprocess.run(
            [
                "git",
                "diff",
                "--cached",
                "--quiet",
            ],
            cwd=cls.CAMINHO_REPOSITORIO,
        )

        if resultado.returncode == 0:

            print(
                "Nenhuma alteração para "
                "sincronizar com o GitHub."
            )

            return True

        # --------------------------------------------------
        # Gera a mensagem do commit.
        # --------------------------------------------------

        mensagem_commit = (
            cls.gerar_mensagem_commit(
                avaliacao,
                operacao,
            )
        )

        # --------------------------------------------------
        # Commit
        # --------------------------------------------------

        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                mensagem_commit,
            ],
            cwd=cls.CAMINHO_REPOSITORIO,
            check=True,
        )

        # --------------------------------------------------
        # Push
        # --------------------------------------------------

        subprocess.run(
            [
                "git",
                "push",
                "origin",
                "main",
            ],
            cwd=cls.CAMINHO_REPOSITORIO,
            check=True,
        )

        print("=" * 60)
        print("SINCRONIZAÇÃO COM GITHUB")
        print("=" * 60)
        print("SINCRONIZAÇÃO REALIZADA!")
        print(
            f"Commit: {mensagem_commit}"
        )
        print("=" * 60)

        return True