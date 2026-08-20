# 🤖 Einar

> Um bot para Telegram desenvolvido para automatizar a organização e a preservação de provas acadêmicas.

## 📚 Sobre o projeto

O **Einar** é um projeto desenvolvido para resolver um problema que encontrei durante minha graduação: a dificuldade de encontrar provas de semestres anteriores organizadas em um único lugar.

A ideia surgiu a partir da necessidade de criar um acervo que permitisse aos estudantes contribuir com avaliações anteriores de forma simples, enquanto o sistema fosse responsável pela maior parte do processo de organização.

O projeto utiliza um bot no Telegram como interface principal para o recebimento das contribuições.

Após o envio de uma avaliação, o sistema coleta suas informações, organiza os arquivos, identifica possíveis duplicatas e encaminha as contribuições para revisão.

As avaliações aprovadas são então publicadas automaticamente no canal do projeto e sincronizadas com o repositório responsável por preservar o acervo.

---

## 🎯 Objetivo

O objetivo do Einar é reduzir o trabalho manual necessário para manter um acervo de provas organizado.

Em vez de depender de uma pessoa para receber arquivos, renomeá-los, criar diretórios, identificar duplicatas e realizar uploads manualmente, o sistema automatiza grande parte desse processo.

O fluxo geral é:

```text
Aluno
  ↓
Envio da avaliação pelo Telegram
  ↓
Coleta das informações
  ↓
Verificação e organização
  ↓
Detecção de possíveis duplicatas
  ↓
Revisão administrativa
  ↓
Publicação no Telegram
  ↓
Sincronização com o GitHub
```

---

## ✨ Funcionalidades

Atualmente, o Einar possui funcionalidades como:

* 📥 Recebimento de provas através do Telegram;
* 📝 Coleta das informações da avaliação por meio de botões;
* 🗂️ Organização automática dos arquivos;
* 🔎 Identificação de possíveis provas duplicadas;
* ♻️ Agrupamento de diferentes versões de uma mesma prova;
* 👀 Revisão administrativa das contribuições;
* 📤 Publicação automática das avaliações aprovadas;
* 📢 Integração com um canal do Telegram;
* 🐙 Sincronização automática com um repositório no GitHub;
* 🧾 Geração automática de mensagens de commit;
* 🗃️ Padronização da estrutura do acervo;
* 🔒 Verificações e limites para o envio de arquivos;
* 💾 Preservação do acervo por meio de backups.

---

## ♻️ Detecção de duplicatas

Uma das principais funcionalidades do projeto é o tratamento de avaliações duplicadas.

Se diferentes pessoas enviarem versões da mesma prova, o objetivo não é simplesmente armazenar várias cópias idênticas.

O sistema identifica possíveis duplicatas e agrupa as contribuições relacionadas.

Isso permite comparar diferentes versões de uma mesma avaliação e selecionar a versão mais adequada para o acervo.

Esse processo também permite que uma prova já existente seja substituída por uma versão de melhor qualidade ou mais completa após revisão.

A ideia é manter o acervo organizado e evitar o acúmulo desnecessário de cópias da mesma avaliação.

---

## 🤖 Como funciona

O usuário inicia uma conversa com o bot e envia o arquivo da avaliação.

Em seguida, o Einar solicita as informações necessárias para identificar e organizar aquela contribuição.

Grande parte do processo de preenchimento é realizada através de botões, reduzindo a necessidade de digitação manual.

Após a confirmação das informações, a contribuição segue para processamento.

Dependendo da situação, a avaliação pode:

* ser identificada como uma nova prova;
* ser agrupada com outras versões semelhantes;
* ser identificada como uma possível duplicata de uma prova já existente;
* ser encaminhada para revisão.

---

## 👀 Revisão das contribuições

O Einar não publica automaticamente qualquer arquivo recebido.

As contribuições podem passar por uma etapa de revisão antes de serem incorporadas ao acervo.

Essa etapa permite verificar, por exemplo:

* se a avaliação está correta;
* se o arquivo possui qualidade adequada;
* se existem versões melhores da mesma prova;
* se a prova está completa;
* se a contribuição deve ser adicionada ou utilizada para substituir uma versão existente.

Após a aprovação, o restante do processo é automatizado.

---

## 📤 Publicação e sincronização

Quando uma avaliação é aprovada, o Einar automatiza sua distribuição para os serviços utilizados pelo projeto.

A prova pode ser publicada no canal do Telegram e incorporada ao acervo armazenado no GitHub.

A sincronização também mantém uma estrutura organizada por informações como:

```text
Período
└── Disciplina
    └── Professor
        └── Semestre
            └── Turno
                └── Avaliação
                    └── Arquivos
```

Durante esse processo, os arquivos podem receber uma nomenclatura padronizada e os semestres são organizados para facilitar a navegação no repositório.

---

## 🛠️ Tecnologias utilizadas

O projeto utiliza principalmente:

* **Python**
* **python-telegram-bot**
* **Git**
* **GitHub**
* **JSON**
* **Telegram Bot API**

---

## 🧩 Arquitetura

O projeto foi desenvolvido com uma separação de responsabilidades entre diferentes componentes.

De forma geral, existem módulos responsáveis por tarefas como:

```text
Bot
├── Interação com o usuário
├── Recebimento de arquivos
└── Coleta de informações

Serviços
├── Organização de arquivos
├── Detecção e tratamento de duplicatas
├── Filas de publicação
├── Publicação no Telegram
└── Sincronização com GitHub

Administração
├── Revisão de contribuições
├── Aprovação
├── Rejeição
└── Comparação de versões
```

---

## 🚧 Próximas funcionalidades

O Einar continua em desenvolvimento.

Algumas ideias para futuras versões incluem:

* 🔍 Sistema de busca de provas diretamente pelo bot;
* 🤖 Assistência por IA para interpretar informações presentes nas avaliações;
* 📝 Preenchimento automático de informações a partir do cabeçalho da prova;
* 🔐 Sistema de autenticação;
* 🗄️ Evolução da estrutura de armazenamento e consulta;
* 📈 Novas ferramentas para administração e manutenção do acervo.

---

## 🏫 Contexto

A versão atual do Einar foi desenvolvida para a **FAETERJ**, como uma iniciativa voltada à criação e preservação de um acervo organizado de provas acadêmicas.

A continuidade e a evolução do projeto dependem da participação dos estudantes e do crescimento do acervo.

---

> **Einar. Transformando um problema que encontrei como aluno em uma solução que pode ajudar outros alunos.**