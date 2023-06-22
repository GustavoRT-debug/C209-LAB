import cv2
import numpy as np

# Inicialização da captura de vídeo
# VideoCapture é usada para acessar dispositivos de captura de vídeo, como câmeras, e capturar frames de vídeo em tempo real

# cap = cv2.VideoCapture("C:\\Users\\gugut\\OneDrive\\Área de Trabalho\\Inatel.mp4")
cap = cv2.VideoCapture(0)

# Criação das janelas para exibição das imagens
# namedWindow para criar uma janela na qual você pode exibir imagens ou vídeos
# WINDOW_NORMAL é uma flag utilizada na função namedWindow do OpenCV para criar uma janela redimensionável
cv2.namedWindow("Webcam", cv2.WINDOW_NORMAL)
cv2.namedWindow("Mascara", cv2.WINDOW_NORMAL)
cv2.namedWindow("Cinza", cv2.WINDOW_NORMAL)

# O valor 480 representa a altura da imagem em pixels
# O valor 640 representa a largura da imagem em pixels
# O valor 3 representa o número de canais de cores (RGB)
# Inicialização dos arrays para armazenar as imagens
# O valor 1 representa o número de canais de cores. Nesse caso, é 1
mascara = np.zeros((480, 640, 3), dtype=np.uint8)
cinza = np.zeros((480, 640, 1), dtype=np.uint8)

# Inicia um loop infinito, que será executado até que uma condição de interrupção seja atendida
while True:
    print("Por favor, tire uma foto do fundo estático do seu vídeo.")
    print("Aperte a tecla Espaço.")
    print("Aperte a tecla ESC para sair.")
    if cv2.waitKey(0) % 0x100 == 32:
        # Captura do primeiro frame para definir o fundo estático
        ret, primeiraImagem = cap.read()
        fundo = primeiraImagem.copy()
        fundo = cv2.GaussianBlur(fundo, (3, 3), 0)
        print("Tirou uma foto!")
        break

while True:
    # Captura dos frames subsequentes
    # Captura um novo frame do vídeo
    ret, imagem = cap.read()
    # Aplica um desfoque gaussiano
    imagem = cv2.GaussianBlur(imagem, (3, 3), 0)

    maiorArea = 0

    # Cálculo da diferença entre a imagem atual e o fundo estático
    mascara = cv2.absdiff(imagem, fundo)

    # Conversão da imagem para escala de cinza
    cinza = cv2.cvtColor(mascara, cv2.COLOR_BGR2GRAY)

    # Limiarização da imagem em escala de cinza para binarização
    # Pixels com valores maiores que 50 são definidos como branco (255), e pixels com valores menores ou iguais a 50 são definidos como preto (0)
    _, cinza = cv2.threshold(cinza, 50, 255, cv2.THRESH_BINARY)

    # Aplicação de operações morfológicas (dilatação e erosão) para remover ruídos
    # Cria um kernel retangular de tamanho 3x3, que será usado nas operações morfológicas de dilatação e erosão
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # Aplica uma operação de dilatação à imagem binária cinza
    cinza = cv2.dilate(cinza, kernel, iterations=1)
    # Aplica uma operação de erosão à imagem binária cinza
    cinza = cv2.erode(cinza, kernel, iterations=1)

    # Exibição das imagens nas respectivas janelas
    # Exibe as imagens
    cv2.imshow("Mascara", mascara)
    cv2.imshow("Cinza", cinza)
    cv2.imshow("Webcam", imagem)

    # Verificação de pressionamento da tecla ESC para sair do loop
    if cv2.waitKey(7) & 0xFF == 27:
        break
