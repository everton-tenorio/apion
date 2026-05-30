# Apion

HTTP client desktop with interface gráfica para testes de API. Construído com Python, ttkbootstrap e curl.

---

## Requisitos

- Python 3.7+
- curl instalado no sistema
- pip

---

## Instalação

**Linux / macOS**

```bash
git clone https://github.com/yourusername/apion.git
cd apion
chmod +x install-unix.sh
./install-unix.sh
```

**Windows**

```cmd
git clone https://github.com/yourusername/apion.git
cd apion
install-windows.bat
```

**Dependências manualmente**

```bash
pip install -r requirements.txt
```

---

## Execução

**Linux / macOS**

```bash
./apion
```

**Windows**

```cmd
apion.bat
```

**Direto via Python**

```bash
python http_client_stable.py
```

---

## Build (executável)

```bash
pip install pyinstaller
pyinstaller apion.spec
```

O binário gerado estará em `dist/`.

---

## Funcionalidades

- Métodos HTTP: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- Content-Types: JSON, XML, Form Data, Plain Text
- Autenticação: Bearer Token, Basic Auth, API Key
- Headers customizados
- Query parameters
- Auto-formatação de JSON na resposta
- Tempo de resposta e status code na UI

---

## Interface

```
[GET v] [URL________________________] [SEND]

[Headers] [Body] [Auth] [Params]

Status: 200   Time: 0.234s
----------------------------------------
Headers                  | Body
-------------------------|---------------
content-type: app/json   | {
x-request-id: abc123     |   "id": 1,
                         |   "name": "..."
                         | }
```

**Painel esquerdo:** status code, tempo de resposta, headers da resposta.  
**Painel direito:** body da resposta formatado.

---

## Configuração de headers

Insira um header por linha, no formato `Chave: Valor`:

```
Authorization: Bearer eyJhbGci...
X-API-Key: sua-chave
Accept: application/json
```

---

## Configuração de query parameters

Insira um parâmetro por linha, no formato `chave=valor`:

```
page=1
limit=50
sort=desc
```

São concatenados automaticamente à URL antes do envio.

---

## Autenticação

| Tipo | Campo(s) |
|------|----------|
| Bearer Token | Token |
| Basic Auth | Username, Password |
| API Key | Header name, Value |

---

## Troubleshooting

**curl não encontrado**

```bash
# Ubuntu / Debian
sudo apt-get install curl

# macOS
brew install curl
```

**Erro ao instalar ttkbootstrap**

```bash
pip install --upgrade pip
pip install ttkbootstrap==1.10.1
```

**Aplicação não inicia**

```bash
python3 --version        # verificar >= 3.7
pip install -r requirements.txt --force-reinstall
```

---

## Licença

MIT

