import math

class coef_mar():
    def __init__(self):
        self.funcoes = {
            "s_e": self.s_e,
            "k_a": self.k_a,
            "k_b": self.k_b,
            "k_c": self.k_c,
            "k_d": self.k_d,
            "k_e": self.k_e,
        }

    def s_e(self, Sut):

        if(Sut <= 1400):
            Limite_enduranca = 0.5 * Sut
        else:
            Limite_enduranca = 700

        return Limite_enduranca

    def k_a(self, Sut, retificado_button, usinado_laminado_button,
                          laminado_quente_button, forjado_button, ka_b):
        
        if(ka_b == 1):

            if retificado_button == 1:
                a = 1.38
                b = -0.067
                    
            elif usinado_laminado_button == 1:
                a = 3.04
                b = -0.217
                    
            elif laminado_quente_button == 1:
                a = 38.6
                b = -0.650
                
            elif forjado_button == 1:
                a = 54.9
                b = -0.758
        
        else:

            if retificado_button == 1:
                a = 1.58
                b = -0.085
                    
            elif usinado_laminado_button == 1:
                a = 4.51
                b = -0.265
                    
            elif laminado_quente_button == 1:
                a = 57.7
                b = -0.718
                    
            elif forjado_button == 1:
                a = 272
                b = -0.995

        return a * (Sut**b)

    def k_b(self, d_secao, sec_circ_button, flex_rot_no, b_secao, h_secao, kb_b):
     
        if(kb_b == 1):

            if sec_circ_button == 1:

                if flex_rot_no == 1:
                    d_e = 0.370 * d_secao
                    d_secao = d_e
                
                if d_secao <= 7.62 and d_secao > 0:
                    k_b = 1
                        
                elif d_secao > 7.62 and d_secao <= 51:
                    k_b = (d_secao/7.62)**(-0.107)
                        
                elif d_secao > 51 and d_secao <= 254:
                    k_b = 1.51 * (d_secao**(-0.157))
                
                elif d_secao > 254:
                    k_b = 1

            else:
                    
                d_e = 0.808*math.sqrt(b_secao*h_secao)
                d_secao = d_e
                    
                if d_secao <= 7.62 and d_secao > 0:
                    k_b = 1
                        
                elif d_secao > 7.62 and d_secao <= 51:
                    k_b = 1.24 * (d_secao**(-0.107))
                        
                elif d_secao > 51 and d_secao < 254:
                    k_b = 1.51 * (d_secao**(-0.157))

                elif d_secao > 254:
                    k_b = 1
                    
        else:
            
            if sec_circ_button == 1:

                if flex_rot_no == 1:
                    d_e = 0.370 * d_secao
                    d_secao = d_e
                
                if d_secao <= 8 and d_secao > 0:
                    k_b = 1
                        
                elif d_secao > 8 and d_secao <= 250:
                    k_b = 1.189 * (d_secao**(-0.097))
                
                elif d_secao > 250:
                    k_b = 0.6

            else:
                    
                d_e = math.sqrt((0.05*b_secao*h_secao)/0.0766)
                    
                d_secao = d_e
                    
                if d_secao <= 8:
                    k_b = 1
                        
                elif d_secao > 8 and d_secao <= 250:
                    k_b = 1.189 * (d_secao**(-0.097))
                        
                elif d_secao > 250:
                    k_b = 0.6
                        
        return k_b

    def k_c(self, flex_pura_e_flexo_tor, ax_puro, torc_pura,kc_b):

        print(kc_b)
        
        if(kc_b == 1):
            if flex_pura_e_flexo_tor == 1:
                k_c = 1
                    
            elif ax_puro == 1:
                k_c = 0.85
                    
            elif torc_pura == 1:
                k_c = 0.59

        else:
            if flex_pura_e_flexo_tor == 1:
                k_c = 1
                    
            elif ax_puro == 1:
                k_c = 0.85
                
            elif torc_pura == 1: 
                k_c = 1 # Caso especial, olhar página 330 do Norton 2013
        
        return k_c

    def k_d(self, temperatura,kd_b):

        if(kd_b == 1):
            k_d = 0.99 + 5.9*(10**-4)*temperatura - 2.1*(10**-6)*(temperatura**2)

        else:
            if temperatura <= 450:
                k_d = 1
                    
            elif temperatura > 450 or temperatura <= 550: 
                k_d = 1 - 0.0058 * (temperatura - 450)

        return k_d

    def k_e(self, porcent):

        if porcent == 0.5:
            z_a = 0
                
        elif porcent == 0.9: 
            z_a = 1.288
                
        elif porcent == 0.95:
            z_a = 1.645
                
        elif porcent == 0.99:
            z_a = 2.326
                
        elif porcent == 0.999:
            z_a = 3.091
                
        elif porcent == 0.9999:
            z_a = 3.719
                
        elif porcent == 0.99999:
            z_a = 4.265
                
        elif porcent == 0.999999:
            z_a = 4.753
                
        k_e = 1 - 0.08 * z_a

        return k_e

if __name__ == '__main__':
    coef_mar = coef_mar()
    resultado = coef_mar.funcoes['k_d'](500)
    print("Resultado: ", resultado)