# Axyoma Bot

Bot de Discord para rolagem de dados. Ele lê mensagens com expressões como `2d6+3`, `d20` ou `30#d20` e responde com o total e cada dado rolado.

## Funcionalidades

- Rolagem de dados no formato `XdY`, com modificador opcional (`+N` ou `-N`).
- Quantidade de dados omitida vale 1 (`d20` é o mesmo que `1d20`).
- Repetição de rolagens com o prefixo `N#` (`5#d20` rola 5 vezes).
- Espaços e maiúsculas são aceitos (`2 D 6 + 3`).
- Mensagem de erro clara quando a expressão é inválida ou passa dos limites.
- Rota HTTP `/` que responde `ok`, útil para serviços de hospedagem que verificam se a aplicação está ativa.

## Exemplos

| Mensagem   | Resposta do bot                                      |
|------------|------------------------------------------------------|
| `2d6+3`    | `11 ⟵ [4, 4] 2d6 + 3`                                |
| `d20`      | `14 ⟵ [14] 1d20`                                     |
| `4d8-2`    | `15 ⟵ [3, 6, 1, 7] 4d8 - 2`                          |
| `3#d20`    | Três linhas, uma para cada rolagem de `1d20`         |
| `abc`      | Sem resposta (a mensagem não é uma expressão de dado) |
| `0d6`      | `❌ Qtd de dados deve ser 1..200`                     |

Os números dos exemplos são ilustrativos, pois cada rolagem é aleatória.

## Limites

| Item                     | Valor              |
|--------------------------|--------------------|
| Dados por rolagem        | 1 a 200            |
| Lados do dado            | 2 a 10000          |
| Repetições (`N#`)        | 1 a 50             |
| Tamanho da resposta      | até 1800 caracteres |

## Requisitos

- Python 3.9 ou superior (o código usa anotações como `list[int]`).
- Um bot criado no [Discord Developer Portal](https://discord.com/developers/applications).
- Dependências do `requirements.txt`: `discord.py` e `flask`.

## Configuração no Discord

1. Crie uma aplicação no Developer Portal e adicione um bot a ela.
2. Copie o token do bot. Ele é secreto e nunca deve ir para o repositório.
3. Na aba **Bot**, ative o **Message Content Intent**. O bot precisa ler o texto das mensagens para reconhecer as expressões.
4. Em **OAuth2 > URL Generator**, marque o escopo `bot` e as permissões **Send Messages** e **Read Message History**.
5. Abra a URL gerada e adicione o bot ao seu servidor.

## Como rodar

```bash
git clone https://github.com/ogbraiaaa/axyoma-bot.git
cd axyoma-bot

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt

export DISCORD_TOKEN="cole_o_token_aqui"   # Windows (PowerShell): $env:DISCORD_TOKEN="cole_o_token_aqui"
python bot.py
```

Quando a conexão der certo, o terminal mostra `ONLINE: <nome do bot>`.

## Variáveis de ambiente

| Variável        | Obrigatória | Descrição                                                        |
|-----------------|-------------|------------------------------------------------------------------|
| `DISCORD_TOKEN` | Sim         | Token do bot. Sem ele, o programa encerra com `Faltou DISCORD_TOKEN`. |
| `PORT`          | Não         | Porta da rota HTTP `/`. Padrão: `10000`.                          |

O código lê as variáveis direto do ambiente. Um arquivo `.env` é ignorado pelo Git, mas não é carregado automaticamente pelo programa.

## Estrutura

```
axyoma-bot/
├── bot.py             # Bot do Discord, leitura das mensagens e servidor Flask
├── dado.py            # Função roll() e classe RollResult, lógica de rolagem sem Discord
├── requirements.txt   # Dependências
└── .gitignore
```

## Como funciona

1. **Gatilho:** uma mensagem de usuário (não de bot) chega em um canal em que o bot está presente.
2. **Entrada:** o texto da mensagem.
3. **O que acontece:** o bot confere se o texto bate com o padrão `[N]dY[+/-M]` ou `N#<expressão>`. Se bater, sorteia os dados com `random.randint` e soma o modificador.
4. **Saída:** uma resposta à mensagem original, sem mencionar o autor. Se a expressão passar dos limites, o bot responde com `❌` e o motivo.

## Autor

Brayan Silva · [github.com/ogbraiaaa](https://github.com/ogbraiaaa)
