# 🚀 Apion - HTTP Client Pro

<div align="center">

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)

**A modern, powerful HTTP client with a beautiful dark UI**

*Test APIs like a pro with Apion - built with Python + ttkbootstrap + curl*

[Download](#-download) • [Features](#-features) • [Installation](#-installation) • [Usage](#-usage)

</div>

---

## ✨ Features

### 🎨 **Beautiful Dark Interface**
- Modern dark theme with soft colors
- Split view: Headers (left) + JSON Body (right)
- Professional layout inspired by Insomnia/Postman

### 🔥 **Powerful Functionality**
- ✅ All HTTP Methods: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- ✅ Content Types: JSON, XML, Form Data, Plain Text
- ✅ Custom Headers
- ✅ Authentication: Bearer Token, Basic Auth, API Key
- ✅ Query Parameters
- ✅ JSON Auto-formatting
- ✅ Response with syntax highlighting
- ✅ Status codes with colors (green=success, red=error)
- ✅ Response time tracking

### 🛠️ **Technical Excellence**
- Backend: curl (reliable, fast, universal)
- GUI: ttkbootstrap (stable, modern)
- Threading: Non-blocking requests
- Cross-platform: Linux, Windows, macOS

---

## 📦 Download

### **Option 1: Pre-built Executables** (Recommended for end users)

Download the latest release for your system:

| Platform | Download | Size |
|----------|----------|------|
| 🐧 **Linux** | [apion](../../releases/latest/download/apion) | ~15MB |
| 🪟 **Windows** | [apion.exe](../../releases/latest/download/apion.exe) | ~20MB |
| 🍎 **macOS** | [apion-macos](../../releases/latest/download/apion-macos) | ~18MB |

#### Installation:

**Linux/macOS:**
```bash
chmod +x apion-linux  # or apion-macos
./apion-linux
```

**Windows:**
Just double-click `apion.exe`

---

### **Option 2: From Source** (Recommended for developers)

```bash
# Clone the repository
git clone https://github.com/yourusername/apion.git
cd apion

# Install
chmod +x install-unix.sh
./install-unix.sh

# Run
./apion
```

**Windows:**
```cmd
install-windows.bat
apion.bat
```

---

## 🚀 Quick Start

### 1. **Simple GET Request**
- Method: `GET`
- URL: `https://jsonplaceholder.typicode.com/posts/1`
- Click `SEND ⚡`

### 2. **POST with JSON**
- Method: `POST`
- URL: `https://jsonplaceholder.typicode.com/posts`
- Tab **Body**:
```json
{
  "title": "Hello World",
  "body": "This is a test",
  "userId": 1
}
```
- Click `SEND ⚡`

### 3. **Authenticated Request**
- Method: `GET`
- URL: `https://api.github.com/user`
- Tab **Auth**:
  - Type: Bearer Token
  - Token: `your_github_token_here`
- Click `SEND ⚡`

---

## 📖 Usage Guide

### **Interface Overview**

```
┌─────────────────────────────────────────────────┐
│  [GET ▼] [URL________________] [SEND ⚡]        │
├─────────────────────────────────────────────────┤
│  [Headers] [Body] [Auth] [Params]               │
├─────────────────────────────────────────────────┤
│  ⚡ Response          ● 200                     │
├──────────────────────┬──────────────────────────┤
│  Headers & Status    │  Response Body (JSON)    │
│                      │                          │
│  Status: 200         │  {                       │
│  Time: 0.234s        │    "id": 1,              │
│                      │    "title": "..."        │
│  Headers:            │  }                       │
│    content-type...   │                          │
│                      │                          │
└──────────────────────┴──────────────────────────┘
```

### **Tabs Explained**

#### 📋 **Headers**
- Set Content-Type (JSON, XML, etc.)
- Add custom headers line by line:
```
Authorization: Bearer token123
X-Custom-Header: value
Accept-Language: en-US
```

#### 📝 **Body**
- Choose format: JSON, Raw, Form
- Write your payload
- Use `Format` button to prettify JSON

#### 🔐 **Auth**
- **None**: No authentication
- **Bearer Token**: For JWT/OAuth tokens
- **Basic Auth**: Username + Password
- **API Key**: Custom API key header

#### 🔗 **Params**
- Add query parameters line by line:
```
page=1
limit=10
sort=desc
```

---

## 🎨 Response Display

### **Split View Design**

**Left Panel: Headers & Status**
- HTTP status code (colored)
- Response time
- Response headers
- Request info

**Right Panel: JSON Body**
- Auto-formatted JSON
- Syntax highlighting
- Easy to read and copy

### **Status Colors**
- 🟢 **Green (200-299)**: Success
- 🟡 **Orange (300-399)**: Redirect
- 🔴 **Red (400+)**: Error

---

## 🔧 Advanced Features

### **Custom Headers**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
X-API-Key: your-api-key-here
Accept: application/json
User-Agent: Apion/1.0
```

### **Query Parameters**
Automatically appended to URL:
```
api.example.com/search?q=python&page=1&limit=20
```

### **JSON Formatting**
Click `Format` to prettify JSON:
```json
// Before
{"name":"John","age":30,"city":"NYC"}

// After
{
  "name": "John",
  "age": 30,
  "city": "NYC"
}
```

---

## 📚 Development

### **Requirements**
- Python 3.7+
- ttkbootstrap
- curl (pre-installed on most systems)

### **Building from Source**

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python http_client_stable.py

# Build executable
pip install pyinstaller
pyinstaller apion.spec
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🐛 Troubleshooting

### **curl not found**
```bash
# Ubuntu/Debian
sudo apt-get install curl

# macOS
brew install curl

# Windows
# Download from: https://curl.se/windows/
```

### **ttkbootstrap not installing**
```bash
pip install --upgrade pip
pip install ttkbootstrap==1.10.1
```

### **Application won't start**
```bash
# Check Python version
python3 --version  # Should be 3.7+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📄 License

MIT License - feel free to use in personal and commercial projects.

---

## Credits

Built using:
- **Python** - Programming language
- **ttkbootstrap** - Modern UI framework
- **curl** - HTTP client backend
- **tkinter** - GUI toolkit

---

## 🌟 Star History

If you like Apion, please give it a star! ⭐

---
