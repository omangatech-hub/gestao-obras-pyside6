# Tela de Splash (Abertura)

## Como adicionar uma imagem personalizada

1. **Prepare sua imagem**
   - Formato: PNG ou JPG
   - Tamanho recomendado: 800x600 pixels ou similar

2. **Adicione ao projeto**
   - Copie o arquivo de imagem para a pasta `assets/`
   - Renomeie para `splash.png` (ou altere no código `tela_splash.py`)

3. **Resultado**
   - A tela de splash aparecerá por 3 segundos ao iniciar o programa
   - Você pode alterar o tempo em `main.py` na linha: `TelaSplash.fechar_splash(splash, 3000)`
   - O tempo está em milissegundos (3000 = 3 segundos)

## Estrutura de pastas

```
gestao_obras_pyside6/
├── assets/
│   └── splash.png          <-- Coloque sua imagem aqui
├── ui/
│   └── tela_splash.py      <-- Configuração da splash
├── main.py                 <-- Arquivo principal
└── ...
```

## Personalizações

No arquivo `tela_splash.py`, você pode:
- Alterar a cor de fundo padrão (linha com `QColor(41, 128, 185)`)
- Mudar o texto (linha com "Gestão de Obras PySide6")
- Ajustar o tamanho da fonte
