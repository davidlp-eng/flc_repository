import numpy as np
import matplotlib.pyplot as plt
import math

Sut = 500
Sm = 450
Se = 100
sigma_a = 70
Sy = 300
r_inclinacao = sigma_a/Sm  # Sm deveria ser sigma_m

# Definindo os valores de x
x_soder = np.linspace(0, Sy, num=100)
x_linha_r = np.linspace(0, 1.1*Sut, num=100)
x_good = np.linspace(0, Sut, num=100)
x_langer = np.linspace(0, Sy, num=100)
x_gerber = np.linspace(0, Sut, num=100)
x_asme = np.linspace(0, Sy, num=100)

# Definindo os valores de y
y_soder = np.linspace(Se, 0, num=100)
y_linha_r = r_inclinacao*x_linha_r
y_good = np.linspace(Se, 0, num=100)
y_langer = np.linspace(Sy, 0, num=100)
y_gerber = Se*(1-(x_gerber**2/Sut**2))
y_asme = np.sqrt(Se**2*(1-(x_asme**2/Sy**2)))

# Coefecientes de segurança
N_soder = 1/((sigma_a/Se)+(Sm/Sy))
N_good = 1/((sigma_a/Se)+(Sm/Sut))
#N_gerber = (-Sigma_a_val*(Sut_val^2)+Sut_val*sqrt((Sigma_a_val^2)*(Sut_val^2)+4*(Se_val^2)*(sigma_m^2)))/(2*Se_val*(sigma_m^2))
#N_asme = (Se_val*Syt_val*sqrt((Sigma_a_val^2)*(Syt_val^2)+(Se_val^2)*(sigma_m^2)))/((Sigma_a_val^2)*(Syt_val^2)+(Se_val^2)*(sigma_m^2))

# Plotando o gráfico
plt.plot(x_linha_r, y_linha_r, label='Linha de carga')
plt.plot(x_soder, y_soder, label='Critério de Soderberg')
plt.plot(x_good, y_good, label='Critério de Goodman modificado')
plt.plot(x_langer, y_langer, label='Critério de escoamento (Langer)')
plt.plot(x_gerber, y_gerber, label='Critério de Gerber')
plt.plot(x_asme, y_asme, label='Critério de elíptico da ASME')

# Traçar a linha tracejada até o ponto
plt.plot([Sm, Sm], [0, sigma_a], 'r--')
plt.plot([0, Sm], [sigma_a, sigma_a], 'r--')

# Adicionar o círculo vermelho ao redor do ponto
plt.scatter(Sm, sigma_a, color='red', zorder=10)

plt.yscale('linear')  # Configurando escala linear para o eixo y
plt.xscale('linear')     # Configurando escala logarítmica para o eixo x
plt.xlabel('Tensão média $\sigma_m$')
plt.ylabel('Tensão alternada $\sigma_a$')
plt.grid(True)
plt.tight_layout()     # Ajustando o espaçamento do gráfico

plt.xlim(0, Sut*1.1)
plt.ylim(0, Sy*1.1)

# Adicionando a legenda ao lado do nome da linha do plot
plt.legend(loc='upper right')

plt.show()