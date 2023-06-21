import math
from tkinter import END

class ciclos_plot():
    def _init_(self):
        self.funcoes = {
            "plot_values": self.plot_values,

        }

    def plot_values(self, Kt_flexao, Kt_torcao, Kt_tracao, Kt_cis, r_sec, Sut,
                    furo_transversal,ombro_rebaixo,fenda_sulco_entalhe,
                    met_simple, neuber_puro, nh_modificado,
                    flexao_max,flexao_min, tracao_max, tracao_min, torcao_max,torcao_min, cis_max, cis_min,
                    ka, kb, kc, kd, ke, kf, Se_lin, plots_budynas):
        
        #if furo_transversal == 1:
        #    raiz_a = 174/Sut
        #elif ombro_rebaixo == 1:
        #    raiz_a = 139/Sut
        #elif fenda_sulco_entalhe == 1:
        #    raiz_a = 104/Sut

        raiz_a = 1.24 - 2.25*(10**-3)*Sut + 1.6*(10**-6)*Sut**2 - 4.11*(10**-10)*Sut**3

        raiz_a_torcao = 0.958 - 1.83*(10**-3)*Sut + 1.43*(10**-6)*Sut**2 -4.11*(10**-10)*Sut**3
        
        # (bending or axial) raiz_a = 1.24 - 2.25*(10**-3)*Sut + 1,6*(10**-6)*Sut**2 - 4.11*(10**-10)*Sut**3    340 <= Sut <= 1700
        # (Torsion) raiz_a = 0.958 - 1.83*(10**-3)*Sut + 1.43*(10**-6)*Sut**2 -4.11*(10**-11)*Sut**3    340 <= Sut <= 1500
        # Implementar mensagem de erro fora do intervalo

        q = 1/(1 + (raiz_a/math.sqrt(r_sec)))
        qs = 1/(1 + (raiz_a_torcao/math.sqrt(r_sec)))

        kfs_cis = 1

        kfs_torcao = 1 + qs*(Kt_torcao-1)

        if met_simple == 1:
            
            kf_tracao = 1 + q*(Kt_tracao-1);
                    
            kf_flexao = 1 + q*(Kt_flexao-1);

        elif neuber_puro == 1:
            
            kf_tracao = 1 + ((Kt_tracao-1)/(1+(raiz_a/math.sqrt(r_sec))))
                   
            kf_flexao = 1 + ((Kt_flexao-1)/(1+(raiz_a/math.sqrt(r_sec))))

        elif nh_modificado == 1:

            kf_tracao = (Kt_tracao)/(1+2*((Kt_tracao-1)/Kt_tracao)*(raiz_a/math.sqrt(r_sec)));
                    
            kf_flexao = (Kt_flexao)/(1+2*((Kt_flexao-1)/Kt_flexao)*(raiz_a/math.sqrt(r_sec)));
        
        sigma_a_flexao = abs(flexao_max-flexao_min)/2
        sigma_m_flexao = abs(flexao_max+flexao_min)/2

        sigma_a_tracao = abs(tracao_max-tracao_min)/2
        sigma_m_tracao = abs(tracao_max+tracao_min)/2
        
        sigma_a_torcao = abs(torcao_max-torcao_min)/2
        sigma_m_torcao = abs(torcao_max+torcao_min)/2
        
        sigma_a_cis = abs(cis_max-cis_min)/2
        sigma_m_cis = abs(cis_max+cis_min)/2

        sigma_a = math.sqrt((kf_flexao*sigma_a_flexao + kf_tracao*sigma_a_tracao)**2 + 3*(kfs_torcao*sigma_a_torcao+kfs_cis*sigma_a_cis)**2)
        sigma_m = math.sqrt((kf_flexao*sigma_m_flexao + kf_tracao*sigma_m_tracao)**2 + 3*(kfs_torcao*sigma_m_torcao+kfs_cis*sigma_m_cis)**2)

        print('Sigma a = ',sigma_a)
        print('Sigma m = ',sigma_m)

        Se = Se_lin*ka*kb*kc*kd*ke*kf

        if plots_budynas == 1:

            if Sut > 500 and Sut <= 1400:
                f = 1.06 - (4.1*10**(-4))*Sut + (1.5*10**(-7))*Sut**2
                Sm = f*Sut

            else:
                Sm = 1*Sut
        else:
            Sm = -1

        return Se, sigma_a, sigma_m, Sm, kf_flexao, kf_tracao, kfs_torcao, kfs_cis


if __name__ == '_main_':
    ciclos_plot = ciclos_plot()
    resultado = ciclos_plot.funcoes['plot_values'](0.999999)
    print("Resultado: ", resultado)