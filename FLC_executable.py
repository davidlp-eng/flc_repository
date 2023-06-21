import gi
from sympy import *
from coeficientes_marin import coef_mar
from diagrama_ciclos import ciclos_plot
from sympy import Float
import pandas as pd
import os
import re

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gio
from gi.repository import Gdk

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
import numpy as np

class Handler(object):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("user_interface.glade")
        self.builder.connect_signals(self)

        self.stack = self.builder.get_object("stack_n1")
        self.stack.connect("notify::visible-child", self.on_stack_n1_notify)

        # Dados de entrada
        self.ka_b = 1
        self.kb_b = 1
        self.kc_b = 1
        self.kd_b = 1
        self.plots_budynas = 1
        self.kt_flexao = 1.0
        self.kt_tracao = 1.0
        self.kt_torcao = 1.0
        self.kt_cis = 1.0
        self.h_r_secao = 0.0
        self.d_secao = 0.0
        self.b_w_secao = 0.0
        self.met_simple = 1
        self.neuber_puro = 0
        self.nh_modificado = 0
        self.Sut = 1.0
        self.Sy = 1.0
        self.temp = 1.0
        self.conf_1 = 1
        self.conf_2 = 0
        self.conf_3 = 0
        self.conf_4 = 0
        self.conf_5 = 0
        self.conf_6 = 0
        self.conf_7 = 0
        self.conf_8 = 0
        self.flexo_rot_nao = 0
        self.flexao_ou_flexo = 1
        self.axial_puro = 0
        self.torcao_pura = 0
        self.retificado = 1
        self.forjado = 0
        self.usinado_laminado = 0
        self.laminado_quente = 0
        self.flexao_max = 0
        self.flexao_min = 0
        self.tracao_max = 0
        self.tracao_min = 0
        self.torcao_max = 0
        self.torcao_min = 0
        self.cisalhamento_max = 0 
        self.cisalhamento_min = 0 
        # 
        self.Se = 1.0
        self.Sm = 1.0
        self.sigma_a = float
        self.sigma_m = float
        self.page_name = int
        self.flag_creat_button = 0
        self.flag_creat_save = 0
        self.flag_page_menu = 0


    def on_main_window_2_destroy(self, dialog):
        Gtk.main_quit()

    def on_about_activate(self, Window):

        about_window = Builder.get_object("about_dialog")
        about_window.run()
        about_window.hide()

    
    def on_open_activate(self, dialog):

        aviso: Gtk.FileChooserDialog(action=Gtk.FileChooserAction.OPEN) = Builder.get_object("file_chooser")

        if self.flag_creat_button == 0:
            aviso.add_buttons(
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN,
                Gtk.ResponseType.OK,
            )
            self.flag_creat_button = 1
            self.add_filters(aviso)

        response = aviso.run()
        aviso.hide()

        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + aviso.get_filename())
            self.preencher = aviso.get_filename()
            self.open_aux()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Arquvios de texto (.txt)")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Qualquer arquivo")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)


    def on_save_activate(self, event):
        print('save')
        
        if self.flag_creat_save == 1:
            self.template()

        else:

            flag = 1

            while flag == 1:
                dialog = Gtk.FileChooserDialog("Selecione uma pasta",
                                        None, Gtk.FileChooserAction.SELECT_FOLDER,
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
                
                self.add_filters(dialog)

                nome_arquivo = Gtk.Entry()
                nome_arquivo.set_placeholder_text("Nome do arquivo")
                dialog.set_extra_widget(nome_arquivo)

                # Define o ícone de pasta
                dialog.set_icon_name("folder")

                response = dialog.run()

                if response == Gtk.ResponseType.OK:

                    self.folder_path = dialog.get_current_folder()
                    print(dialog)
                    print("Save clicked")

                    if self.folder_path is not None:
                        print("File selected: {}".format(self.folder_path))
                        self.file_name = nome_arquivo.get_text()

                        if self.file_name == '':
                            self.file_name = 'Novo_arquivo'

                        print("Nome do arquivo: {}".format(self.file_name))
                        self.flag_creat_save = 1

                        # Caminho completo (caminho + nome do arquivo)
                        self.caminho_completo = os.path.join(self.folder_path, self.file_name)

                        # Adicionar código para salvamento

                        flag = 0
                        self.template()
                        dialog.hide()
                    
                    else:
                        self.aviso_mensagem('Pasta inválida','Selecione de forma adequada o local de salvamento','dialog-warning')
                        dialog.hide()

                elif response == Gtk.ResponseType.CANCEL:
                    print("Cancel clicked")
                    dialog.hide()
                    break
                flag = 0

    def on_save_as_activate(self, event):
        self.flag_creat_save = 0
        self.on_save_activate(self)

    def open_aux(self):

        texto = self.preencher

        with open(texto, 'r') as arquivo:
            texto_convertido = arquivo.read()

        # Expressão regular para extrair os valores após os ":" (excluindo espaços em branco)
        padrao = r":([^\n]+)"

        # Extrair os valores usando a expressão regular
        valores = re.findall(padrao, texto_convertido)
        
        if valores:
            # Armazenar os valores em variáveis separadas
            ka_b = int(valores[0])
            ka_n = int(valores[1])
            kb_b = int(valores[2])
            kb_n = int(valores[3])
            kc_b = int(valores[4])
            kc_n = int(valores[5])
            kd_b = int(valores[6])
            kd_n = int(valores[7])
            plots_budynas = int(valores[8])
            plots_norton = int(valores[9])

            if ka_b == 1:
                Builder.get_object("ka_b").set_active(True)
                Builder.get_object("ka_n").set_active(False)
            elif ka_n == 1:
                Builder.get_object("ka_n").set_active(True)
                Builder.get_object("ka_b").set_active(False)
            if kb_b == 1:
                Builder.get_object("kb_b").set_active(True)
                Builder.get_object("kb_n").set_active(False)
            elif kb_n == 1:
                Builder.get_object("kb_n").set_active(True)
                Builder.get_object("kb_b").set_active(False)
            if kc_b == 1:
                Builder.get_object("kc_b").set_active(True)
                Builder.get_object("kc_n").set_active(False)
            elif kc_n == 1:
                Builder.get_object("kc_n").set_active(True)
                Builder.get_object("kc_b").set_active(False)
            if kd_b == 1:
                Builder.get_object("kd_b").set_active(True)
                Builder.get_object("kd_n").set_active(False)
            elif kd_n == 1:
                Builder.get_object("kd_n").set_active(True)
                Builder.get_object("kd_b").set_active(False)
            if plots_budynas == 1:
                Builder.get_object("plots_budynas").set_active(True)
                Builder.get_object("plots_norton").set_active(False)
            elif plots_norton == 1:
                Builder.get_object("plots_norton").set_active(True)
                Builder.get_object("plots_budynas").set_active(False)

            kt_flexao = (valores[10])
            Builder.get_object("kt_flexao").set_text(kt_flexao)
            kt_tracao = (valores[11])
            Builder.get_object("kt_tracao").set_text(kt_tracao)
            kt_torcao = (valores[12])
            Builder.get_object("kt_torcao").set_text(kt_torcao)
            kt_cis = (valores[13])
            Builder.get_object("kt_cis").set_text(kt_cis)
            h_r_secao = (valores[14])
            Builder.get_object("h_r_secao").set_text(h_r_secao)
            d_secao = (valores[15])
            Builder.get_object("d_secao").set_text(d_secao)
            b_w_secao = (valores[16])
            Builder.get_object("b_w_secao").set_text(b_w_secao)
            metodo_simplificado = int(valores[17])
            neuber_puro = int(valores[18])
            neuber_heywood_modificado = int(valores[19])
            if metodo_simplificado == 1:
                Builder.get_object("part_neuber_1").set_active(True)
            else:
                Builder.get_object("part_neuber_1").set_active(False)
            if neuber_puro == 1:
                Builder.get_object("part_neuber_2").set_active(True)
            else:
                Builder.get_object("part_neuber_2").set_active(False)
            if neuber_heywood_modificado == 1:
                Builder.get_object("part_neuber_3").set_active(True)
            else:
                Builder.get_object("part_neuber_3").set_active(False)

            Sut = (valores[20])
            Builder.get_object("sut").set_text(Sut)
            Sy = (valores[21])
            Builder.get_object("sy").set_text(Sy)
            temperatura = (valores[22])
            Builder.get_object("temp").set_text(temperatura)
            confiabilidade_0_5 = int(valores[23])
            confiabilidade_0_9 = int(valores[24])
            confiabilidade_0_95 = int(valores[25])
            confiabilidade_0_99 = int(valores[26])
            confiabilidade_0_999 = int(valores[27])
            confiabilidade_0_9999 = int(valores[28])
            confiabilidade_0_99999 = int(valores[29])
            confiabilidade_0_999999 = int(valores[30])
            if confiabilidade_0_5 == 1:
                Builder.get_object("conf_1").set_active(True)
            else:
                Builder.get_object("conf_1").set_active(False)
            if confiabilidade_0_9 == 1:
                Builder.get_object("conf_2").set_active(True)
            else:
                Builder.get_object("conf_2").set_active(False)
            if confiabilidade_0_95 == 1:
                Builder.get_object("conf_3").set_active(True)
            else:
                Builder.get_object("conf_3").set_active(False)
            if confiabilidade_0_99 == 1:
                Builder.get_object("conf_4").set_active(True)
            else:
                Builder.get_object("conf_4").set_active(False)
            if confiabilidade_0_999 == 1:
                Builder.get_object("conf_5").set_active(True)
            else:
                Builder.get_object("conf_5").set_active(False)
            if confiabilidade_0_9999 == 1:
                Builder.get_object("conf_6").set_active(True)
            else:
                Builder.get_object("conf_6").set_active(False)
            if confiabilidade_0_99999 == 1:
                Builder.get_object("conf_7").set_active(True)
            else:
                Builder.get_object("conf_7").set_active(False)
            if confiabilidade_0_999999 == 1:
                Builder.get_object("conf_8").set_active(True)
            else:
                Builder.get_object("conf_8").set_active(False)

            flexo_roatacao_sim = int(valores[31])
            flexo_roatacao_nao = int(valores[32])
            if flexo_roatacao_sim == 1:
                Builder.get_object("flexo_rot_sim").set_active(True)
            else:
                Builder.get_object("flexo_rot_sim").set_active(False)
            if flexo_roatacao_nao == 1:
                Builder.get_object("flexo_rot_nao").set_active(True)
            else:
                Builder.get_object("flexo_rot_nao").set_active(False)

            flexao_pura_flexo_torcao = int(valores[33])
            axial_puro = int(valores[34])
            torcao_pura = int(valores[35])

            if flexao_pura_flexo_torcao == 1:
                Builder.get_object("flexao_ou_flexo").set_active(True)
            else:
                Builder.get_object("flexao_ou_flexo").set_active(False)
            if axial_puro == 1:
                Builder.get_object("axial_puro").set_active(True)
            else:
                Builder.get_object("axial_puro").set_active(False)
            if torcao_pura == 1:
                Builder.get_object("torcao_pura").set_active(True)
            else:
                Builder.get_object("torcao_pura").set_active(False)
            
            retificado = int(valores[36])
            forjado = int(valores[37])
            usinado_laminado = int(valores[38])
            laminado_quente = int(valores[39])

            if retificado == 1:
                Builder.get_object("retificado").set_active(True)
            else:
                Builder.get_object("retificado").set_active(False)
            if forjado == 1:
                Builder.get_object("forjado").set_active(True)
            else:
                Builder.get_object("forjado").set_active(False)
            if usinado_laminado == 1:
                Builder.get_object("usinado_laminado").set_active(True)
            else:
                Builder.get_object("usinado_laminado").set_active(False)
            if laminado_quente == 1:
                Builder.get_object("laminado_quente").set_active(True)
            else:
                Builder.get_object("laminado_quente").set_active(False)

            flexao_maxima = (valores[40])
            Builder.get_object("flexao_max").set_text(flexao_maxima)
            flexao_minima = (valores[41])
            Builder.get_object("flexao_min").set_text(flexao_minima)
            tracao_maxima = (valores[42])
            Builder.get_object("tracao_max").set_text(tracao_maxima)
            tracao_minima = (valores[43])
            Builder.get_object("tracao_min").set_text(tracao_minima)
            torcao_maxima = (valores[44])
            Builder.get_object("torcao_max").set_text(torcao_maxima)
            torcao_minima = (valores[45])
            Builder.get_object("torcao_min").set_text(torcao_minima)
            cisalhamento_maxima = (valores[46])
            Builder.get_object("cisalhamento_max").set_text(cisalhamento_maxima)
            cisalhamento_minima = (valores[47])
            Builder.get_object("cisalhamento_min").set_text(cisalhamento_minima)
    
        else:
            self.aviso_mensagem('Arquivo selecionado fora do template','O arquivo que você selecionou está fora do template, se deseja ter esse template use o Software normalmente e no final use a opção "salvar", isso irá gerar um modelo pronto na pasta selecionada','dialog-error')

    def template(self):
        self.model_content = """
Variáveis do Software

Metodologias
1. Variável ka_b:{var1}
2. Variável ka_n:{var2}
3. Variável kb_b:{var3}
4. Variável kb_n:{var4}
5. Variável kc_b:{var5}
6. Variável kc_n:{var6}
7. Variável kd_b:{var7}
8. Variável kd_n:{var8}
9. Variável plots_budynas:{var9}
10. Variável plots_norton:{var10}

Fator geométrico (quando for calcular, sempre deixar no menu da seção transversal desejada)
11. Variável kt_flexao:{var11}
12. Variável kt_tracao:{var12}
13. Variável kt_torcao:{var13}
14. Variável kt_cisalhamento:{var14}
15. Variável h ou r da secao:{var15}
16. Variável d da secao:{var16}
17. Variável b ou w secao:{var17}
18. Variável método simplificado:{var18}
19. Variável neuber puro:{var19}
20. Variável neuber-heywood modificado:{var20}

Material
21. Variável Sut:{var21}
22. Variável Sy:{var22}
23. Variável temperatura:{var23}
24. Variável confiabilidade 0.5:{var24}
25. Variável confiabilidade 0.9:{var25}
26. Variável confiabilidade 0.95:{var26}
27. Variável confiabilidade 0.99:{var27}
28. Variável confiabilidade 0.999:{var28}
29. Variável confiabilidade 0.9999:{var29}
30. Variável confiabilidade 0.99999:{var30}
31. Variável confiabilidade 0.999999:{var31}
32. Variável flexo roatacao sim:{var32}
33. Variável flexo roatacao não:{var33}
34. Variável flexao pura e/ou flexo torcao:{var34}
35. Variável axial puro:{var35}
36. Variável torcao pura:{var36}
37. Variável retificado:{var37}
38. Variável forjado:{var38}
39. Variável usinado ou laminado a frio:{var39}
40. Variável laminado a quente:{var40}
41. Variável flexao maxima:{var41}
42. Variável flexao minima:{var42}
43. Variável tracao maxima:{var43}
44. Variável tracao minima:{var44}
45. Variável torcao maxima:{var45}
46. Variável torcao minima:{var46}
47. Variável cisalhamento maxima:{var47}
48. Variável cisalhamento minima:{var48}
"""
        if self.ka_b == 0:
            self.ka_n = 1
        else:
            self.ka_n = 0
        if self.kb_b == 0:
            self.kb_n = 1
        else:
            self.kb_n = 0
        if self.kc_b == 0:
            self.kc_n = 1
        else:
            self.kc_n = 0
        if self.kd_b == 0:
            self.kd_n = 1
        else:
            self.kd_n = 0
        if self.flexo_rot_nao == 0:
            self.flexo_rot_sim = 1
        else:
            self.flexo_rot_sim = 0
        if self.plots_budynas == 1:
            self.plots_norton = 0

        # Substituindo as variáveis no modelo/template
        self.model_content = self.model_content.format(
            var1=self.ka_b, var2=self.ka_n, var3=self.kb_b, var4=self.kb_n, var5=self.kc_b , var6=self.kc_n, var7=self.kd_b, var8=self.kd_n,
            var9=self.plots_budynas, var10=self.plots_norton, var11=self.kt_flexao, var12=self.kt_tracao, var13=self.kt_torcao, var14=self.kt_cis, var15=self.h_r_secao,
            var16=self.d_secao, var17=self.b_w_secao, var18=self.met_simple, var19=self.neuber_puro, var20=self.nh_modificado, var21=self.Sut, var22=self.Sy,
            var23=self.temp, var24=self.conf_1, var25=self.conf_2, var26=self.conf_3, var27=self.conf_4, var28=self.conf_5, var29=self.conf_6,
            var30=self.conf_7, var31=self.conf_8, var32=self.flexo_rot_sim, var33=self.flexo_rot_nao, 
            var34=self.flexao_ou_flexo, var35=self.axial_puro, var36=self.torcao_pura,var37=self.retificado, 
            var38=self.forjado, var39=self.usinado_laminado, var40=self.laminado_quente, 
            var41=self.flexao_max, var42=self.flexao_min, var43=self.tracao_max, var44=self.tracao_min, 
            var45=self.torcao_max, var46=self.torcao_min, var47=self.cisalhamento_max, var48=self.cisalhamento_min,
        )

        # Salvando o modelo definitivo
        self.caminho_completo_ext = self.caminho_completo+'.txt'
        df = pd.DataFrame({'': [self.model_content]})
        df.to_csv(self.caminho_completo_ext, sep='\t', index=False)


    def on_exit_activate(self, Window):
        Gtk.main_quit()

    def on_coefs_clicked(self, Button):
        coefs_window = Builder.get_object("marin_coefs_window")

        coefs_window.show_all()
    
    def on_stack_n1_notify(self, stack_n1, gparamstring):

        self.page_name = stack_n1.get_visible_child_name()
        print("A página atual é:", self.page_name)

        self.title = Builder.get_object("title_select")
        self.r_or_h = Builder.get_object("r_or_h")
        self.D_or_W = Builder.get_object("D_or_W")
        self.r_box = Builder.get_object("r_box")

        if self.page_name == "op3":
            self.title.set_text("Inserir, nesse caso, somente d e D")
            self.r_box.hide()

        elif self.page_name == "op6":
            self.title.set_text("Inserir, nesse caso, somente h, d e W")
            self.r_box.show()
            self.r_or_h.set_text("Valor de h [mm] = ")
            self.D_or_W.set_text("Valor de W [mm] = ")
        else:
            self.title.set_text("Inserir, nesse caso, somente r, d e D")
            self.r_box.show()
            self.r_or_h.set_text("Valor de r [mm] = ")
            self.D_or_W.set_text("Valor de D [mm] = ")

    def on_stack1_notify(self, stack1, gparamstring):

        if self.flag_page_menu == 0:
            self.menu_name = stack1.get_visible_child_name()
            print("A página atual é:", self.menu_name)

            if self.menu_name == "page2":
                self.result_box_marin = Builder.get_object("result_box_marin")
                self.result_box_marin.hide()
                self.flag_page_menu = 1


    def aviso_mensagem(self, titulo, texto, icone):
        aviso: Gtk.MessageDialog = Builder.get_object("mensagem")
        aviso.props.text = titulo
        aviso.props.secondary_text = texto
        aviso.props.icon_name = icone
        aviso.show_all()
        aviso.run()
        aviso.hide()

    def on_export_criterios_clicked(self, button):
        if self.flag_creat_save == 0:
            self.aviso_mensagem('Salve primeiro','Salve pelo menos uma vez, para ser possível a exportação dos dados de critérios','dialog-warning')
        
        else:

            df_final = pd.DataFrame()

            if self.sodeberg == true:
                titulo = 'Critério de Soderberg'
                df_soder = pd.DataFrame({'Tensão média': self.x_soder, 'Tensão alternada': self.y_soder})
                df_final = df_final.append([pd.DataFrame([titulo]), df_soder], ignore_index=True)

            if self.goodman == true:
                titulo = 'Critério de Goodman modificado'
                df_goodman = pd.DataFrame({'Tensão média': self.x_good, 'Tensão alternada': self.y_good})
                df_final = df_final.append([pd.DataFrame([titulo]), df_goodman], ignore_index=True)

            if self.gerber == true:
                titulo = 'Critério de Gerber'
                df_gerber = pd.DataFrame({'Tensão média': self.x_gerber, 'Tensão alternada': self.y_gerber})
                df_final = df_final.append([pd.DataFrame([titulo]), df_gerber], ignore_index=True)

            if self.asme == true:
                titulo = 'Critério elíptico da ASME'
                df_asme = pd.DataFrame({'Tensão média': self.x_asme, 'Tensão alternada': self.y_asme})
                df_final = df_final.append([pd.DataFrame([titulo]), df_asme], ignore_index=True)

            if self.langer == true:
                titulo = 'Critério de escoamento (Langer)'
                df_langer = pd.DataFrame({'Tensão média': self.x_langer, 'Tensão alternada': self.y_langer})
                df_final = df_final.append([pd.DataFrame([titulo]), df_langer], ignore_index=True)

            titulo = 'Linha de carregmento'
            df_r = pd.DataFrame({'Tensão média': self.x_linha_r, 'Tensão alternada': self.y_linha_r})
            df_final = df_final.append([pd.DataFrame([titulo]), df_r], ignore_index=True)

            # Salvar o DataFrame em um arquivo CSV
            df_final.to_csv(self.caminho_completo, index=False)
            #emblem-default
            self.aviso_mensagem('Sucesso !!!','Salvamento realizado com sucesso','emblem-default')


    def on_calc_coefs_clicked(self, Button):

        # Concentrador de tensão

        ## Coletando valores de tensão

        self.flexao_max = sympify(Builder.get_object("flexao_max").get_text())
        self.flexao_min = sympify(Builder.get_object("flexao_min").get_text())
        self.tracao_max = sympify(Builder.get_object("tracao_max").get_text())
        self.tracao_min = sympify(Builder.get_object("tracao_min").get_text())
        self.torcao_max = sympify(Builder.get_object("torcao_max").get_text())
        self.torcao_min = sympify(Builder.get_object("torcao_min").get_text())
        self.cisalhamento_max = sympify(Builder.get_object("cisalhamento_max").get_text())    
        self.cisalhamento_min = sympify(Builder.get_object("cisalhamento_min").get_text())

        ### Teste falha estática

        somatorio_carregamentos = self.flexao_max + self.tracao_max + self.torcao_max + self.cisalhamento_max
        print('O valor do somatorio: ',somatorio_carregamentos)

        self.Sy = sympify(Builder.get_object("sy").get_text())

        N_estatico = 0

        if somatorio_carregamentos > 0:
            N_estatico = self.Sy/somatorio_carregamentos

            if N_estatico < 1:
                self.aviso_mensagem('Falha estática detectada','Verifique o seu cálculo para prosseguir','dialog-error')
                print('Falha estática')
        
            elif N_estatico > 1:
                print('Entrei nos coeficientes')
                self.result_box_marin.show()

                # Coeficientes de marin

                self.Sut = sympify(Builder.get_object("sut").get_text())

                Se_lin = coef_mar().s_e(self.Sut)
                Builder.get_object("se_lin").set_text(str(Se_lin))

                if Builder.get_object("ka_b").get_active() == True:
                    self.ka_b = 1
                else:
                    self.ka_b = 0

                self.retificado = 0
                if Builder.get_object("retificado").get_active() == True:
                    self.retificado = 1
                
                if Builder.get_object("usinado_laminado").get_active() == True:
                    self.usinado_laminado = 1

                if Builder.get_object("laminado_quente").get_active() == True:
                    self.laminado_quente = 1

                if Builder.get_object("forjado").get_active() == True:
                    self.forjado = 1

                k_a = coef_mar().k_a(self.Sut,self.retificado,self.usinado_laminado,self.laminado_quente,self.forjado,self.ka_b)
                Builder.get_object("ka").set_text(str(k_a))
                print(k_a)

                if Builder.get_object("kb_b").get_active() == True:
                    self.kb_b = 1
                else:
                    self.kb_b = 0
                
                if Builder.get_object("flexo_rot_nao").get_active() == True:
                    self.flexo_rot_nao = 1
                
                # d = sympify(Builder.get_object("d_secao").get_text())
                # h = sympify(Builder.get_object("h_r_secao").get_text())
                # b = sympify(Builder.get_object("b_w_secao").get_text())
                self.d_secao = sympify(Builder.get_object("d_secao").get_text())
                self.h_r_secao = sympify(Builder.get_object("h_r_secao").get_text())
                self.b_w_secao = sympify(Builder.get_object("b_w_secao").get_text())

                if self.page_name == 'op1' or self.page_name == 'op2' or self.page_name == 'op3':
                    tipo_secao = 1
                else:
                    tipo_secao = 0


                self.flexao_ou_flexo, self.ax_puro, self.torcao_pura = 0,0,0

                if Builder.get_object("kc_b").get_active() == True:
                    self.kc_b = 1
                else:
                    self.kc_b = 0

                if Builder.get_object("flexao_ou_flexo").get_active() == True:
                    self.flexao_ou_flexo = 1
                
                if Builder.get_object("axial_puro").get_active() == True:
                    self.axial_puro = 1
                
                if Builder.get_object("torcao_pura").get_active() == True:
                    self.torcao_pura = 1

                if self.axial_puro == 1:
                    k_b = 1
                    Builder.get_object("kb").set_text(str(k_b))
                else:
                    k_b = coef_mar().k_b(self.d_secao,tipo_secao,self.flexo_rot_nao,self.b_w_secao,self.h_r_secao,self.kb_b)
                    Builder.get_object("kb").set_text(str(k_b))
                    print(k_b)

                k_c = coef_mar().k_c(self.flexao_ou_flexo,self.axial_puro,self.torcao_pura,self.kc_b)
                Builder.get_object("kc").set_text(str(k_c))
                print(k_c)


                if Builder.get_object("kd_b").get_active() == True:
                    self.kd_b = 1
                else:
                    self.kd_b = 0

                self.temp = sympify(Builder.get_object("temp").get_text())
                k_d = coef_mar().k_d(self.temp, self.kd_b)
                Builder.get_object("kd").set_text(str(k_d))
                print(k_d)
                self.conf_1 = 0

                if Builder.get_object("conf_1").get_active() == True:
                    porcent = 0.5
                    self.conf_1 = 1
                elif Builder.get_object("conf_2").get_active() == True:
                    porcent = 0.9
                    self.conf_2 = 1
                elif Builder.get_object("conf_3").get_active() == True:
                    porcent = 0.95
                    self.conf_3 = 1
                elif Builder.get_object("conf_4").get_active() == True:
                    porcent = 0.99
                    self.conf_4 = 1
                elif Builder.get_object("conf_5").get_active() == True:
                    porcent = 0.999
                    self.conf_5 = 1
                elif Builder.get_object("conf_6").get_active() == True:
                    porcent = 0.9999
                    self.conf_6 = 1
                elif Builder.get_object("conf_7").get_active() == True:
                    porcent = 0.99999
                    self.conf_7 = 1
                elif Builder.get_object("conf_8").get_active() == True:
                    porcent = 0.999999
                    self.conf_8 = 1

                k_e = coef_mar().k_e(porcent)
                Builder.get_object("ke").set_text(str(k_e))
                print(k_e)

                k_f = sympify(Builder.get_object("kf").get_text())

                # Fim

                ### Valor dos concentradores de tensão
                self.met_simple = 0
                self.neuber_puro = 0
                self.nh_modificado = 0

                if Builder.get_object("part_neuber_1").get_active() == True:
                    self.met_simple = 1
                elif Builder.get_object("part_neuber_2").get_active() == True:
                    self.neuber_puro = 1
                elif Builder.get_object("part_neuber_3").get_active() == True:
                    self.nh_modificado = 1

                furo_transversal = 0
                ombro_rebaixo = 0
                fenda_sulco_entalhe = 0

                if self.page_name == 'op3' or self.page_name == 'op6':
                    furo_transversal = 1
                elif self.page_name == 'op1' or self.page_name == 'op4':
                    ombro_rebaixo = 1
                elif self.page_name == 'op2' or self.page_name == 'op5':
                    fenda_sulco_entalhe = 1

                self.kt_flexao = sympify(Builder.get_object("kt_flexao").get_text())
                self.kt_torcao = sympify(Builder.get_object("kt_torcao").get_text())
                self.kt_cis = sympify(Builder.get_object("kt_cis").get_text())
                self.kt_tracao = sympify(Builder.get_object("kt_tracao").get_text())
                
                if Builder.get_object("plots_budynas").get_active() == True:
                    self.plots_budynas = 1
                else:
                    self.plots_budynas = 0

                ### Fim

                ### Plot

                plot_var = list(ciclos_plot().plot_values(self.kt_flexao, self.kt_torcao, self.kt_tracao, self.kt_cis, self.h_r_secao, self.Sut,
                            furo_transversal,ombro_rebaixo,fenda_sulco_entalhe,
                            self.met_simple, self.neuber_puro, self.nh_modificado,
                            self.flexao_max,self.flexao_min, self.tracao_max, self.tracao_min, self.torcao_max,self.torcao_min, self.cisalhamento_max, self.cisalhamento_min,
                            k_a, k_b, k_c, k_d, k_e, k_f, Se_lin, self.plots_budynas))
                
                self.Se = plot_var[0]
                self.sigma_a = plot_var[1]
                self.sigma_m = plot_var[2]
                self.Sm = plot_var[3]
                self.kf_flexao = plot_var[4]
                self.kf_tracao = plot_var[5]
                self.kfs_torcao = plot_var[6]
                self.kfs_cis = plot_var[7]
                
                print(plot_var)

                ### Fim

                ## Fim
        
        else:
            self.aviso_mensagem('Carregamentos não preenchidos','Verifique se os carregamentos foram preenchidos de forma correta','dialog-error')


    def on_plotar_diagrama_clicked(self, Button):

        Builder.get_object("sigma_m").set_text(str(self.sigma_m))
        Builder.get_object("sigma_a").set_text(str(self.sigma_a))
        Builder.get_object("sut_print").set_text(str(self.Sut))
        Builder.get_object("Se").set_text(str(self.Se))
        Builder.get_object("Kf_flexao").set_text(str(self.kf_flexao))
        Builder.get_object("Kf_tracao").set_text(str(self.kf_tracao))
        Builder.get_object("Kfs_torcao").set_text(str(self.kfs_torcao))
        Builder.get_object("Kfs_cis").set_text(str(self.kfs_cis))
        
        sw = Builder.get_object("diagrama_plot")

        figure = Figure(figsize=(10, 8), dpi = 150)
        axis = figure.add_subplot()

        # Definindo os valores de y
        #y1 = np.linspace(np.float64(Float(self.Sut).evalf()), np.float64(Float(self.sigma_m).evalf()), num=100)
        #y2 = np.linspace(np.float64(Float(self.sigma_m).evalf()), np.float64(Float(self.Se).evalf()), num=100)
        y3 = np.linspace(np.float64(Float(self.Se).evalf()), np.float64(Float(self.Se).evalf()), num=100)
        y4 = np.linspace(np.float64(Float(self.sigma_a).evalf()), np.float64(Float(self.sigma_a).evalf()), num=100)

        # Definindo os valores de x no eixo logarítmico
        #x1 = np.logspace(0, 3, num=100)
        #x2 = np.logspace(3, 6, num=100)
        x3 = np.logspace(6, 9, num=100)
        x4 = np.logspace(0, 9, num=100)

        # Plotando o gráfico
        #axis.plot(x1, y1,'b-', label='Diagrama de Wöhler \nusando carregamentos')
        #axis.plot(x2, y2, 'b-')
        axis.plot(x3, y3, 'b-')
        axis.plot(x4, y4, 'r-', label='Ponto $\sigma_a$ calculado')

        if self.Sm > 0:
            Builder.get_object("Sm").set_text(str(self.Sm))
            y1b = np.linspace(np.float64(Float(self.Sut).evalf()), np.float64(Float(self.Sm).evalf()), num=100)
            y2b = np.linspace(np.float64(Float(self.Sm).evalf()), np.float64(Float(self.Se).evalf()), num=100)
            x1b = np.logspace(0, 3, num=100)
            x2b = np.logspace(3, 6, num=100)
            axis.plot(x1b, y1b, 'b-', label='Diagrama de Wöhler usando \naproximações de $S_{ut}$ Budynas 2019')
            axis.plot(x2b, y2b, 'b-')

        elif self.Sm == -1:

            if Builder.get_object("flexao_ou_flexo").get_active() == True:
                self.Sm = 0.9*self.Sut
                
            if Builder.get_object("axial_puro").get_active() == True:
                self.Sm = 0.75*self.Sut
                
            if Builder.get_object("torcao_pura").get_active() == True:
                self.Sm = 1*self.Sut

            y1b = np.linspace(np.float64(Float(self.Sut).evalf()), np.float64(Float(self.Sm).evalf()), num=100)
            y2b = np.linspace(np.float64(Float(self.Sm).evalf()), np.float64(Float(self.Se).evalf()), num=100)
            x1b = np.logspace(0, 3, num=100)
            x2b = np.logspace(3, 6, num=100)
            axis.plot(x1b, y1b, 'b-', label='Diagrama de Wöhler usando \naproximações de $S_{ut}$ Norton 2013')
            axis.plot(x2b, y2b, 'b-')

            Builder.get_object("Sm").set_text(str(self.Sm))

        axis.set_yscale('linear')  # Configurando escala linear para o eixo y
        axis.set_xscale('log')     # Configurando escala logarítmica para o eixo x
        axis.set_xlabel('Número de ciclos (N)')
        axis.set_ylabel('$\sigma$ (MPa)')
        axis.grid(True)

        if self.Se < self.sigma_a:
            limite = self.Se*0.7
        else:
            limite = self.sigma_a*0.7

        # Conferir erro
        #axis.set_ylim(limite, np.float64(Float(self.Sut).evalf())*1.05)
        #axis.set_xlim(1, 1*10**9)
        # Adicionando a legenda ao lado do nome da linha do plot
        axis.legend(loc='upper right')

        canvas = FigureCanvas(figure)  
        canvas.set_size_request(1000, 800)
        sw.add(canvas)
        sw.show_all()

    def on_plotar_criterios_clicked(self, button):

        self.sodeberg = Builder.get_object("sodeberg").get_active()
        self.goodman = Builder.get_object("goodman").get_active()
        self.gerber = Builder.get_object("gerber").get_active()
        self.asme = Builder.get_object("asme").get_active()
        self.langer = Builder.get_object("langer").get_active()

        r_inclinacao = np.float64(Float(self.sigma_a).evalf())/np.float64(Float(self.sigma_m).evalf()) 

        sw = Builder.get_object("criterios_plot")

        figure = Figure(figsize=(10, 8), dpi = 150)
        axis = figure.add_subplot()

        # Definindo os valores de x
        self.x_soder = np.linspace(0, np.float64(Float(self.Sy).evalf()), num=100)
        self.x_linha_r = np.linspace(0, 1.1*np.float64(Float(self.Sut).evalf()), num=100)
        self.x_good = np.linspace(0, np.float64(Float(self.Sut).evalf()), num=100)
        self.x_langer = np.linspace(0, np.float64(Float(self.Sy).evalf()), num=100)
        self.x_gerber = np.linspace(0, np.float64(Float(self.Sut).evalf()), num=100)
        self.x_asme = np.linspace(0, np.float64(Float(self.Sy).evalf()), num=100)

        # Definindo os valores de y
        self.y_soder = np.linspace(np.float64(Float(self.Se).evalf()), 0, num=100)
        self.y_linha_r = r_inclinacao*self.x_linha_r
        self.y_good = np.linspace(np.float64(Float(self.Se).evalf()), 0, num=100)
        self.y_langer = np.linspace(np.float64(Float(self.Sy).evalf()), 0, num=100)
        self.y_gerber = np.float64(Float(self.Se).evalf())*(1-(self.x_gerber**2/np.float64(Float(self.Sut).evalf())**2))
        self.y_asme = np.sqrt(np.float64(Float(self.Se).evalf())**2*(1-(self.x_asme**2/np.float64(Float(self.Sy).evalf())**2)))

        # Coefecientes de segurança
        N_soder = 1/((np.float64(Float(self.sigma_a).evalf())/np.float64(Float(self.Se).evalf()))+(np.float64(Float(self.sigma_m).evalf())/np.float64(Float(self.Sy).evalf())))
        N_good = 1/((np.float64(Float(self.sigma_a).evalf())/np.float64(Float(self.Se).evalf()))+(np.float64(Float(self.sigma_m).evalf())/np.float64(Float(self.Sut).evalf())))
        N_gerber = (-np.float64(Float(self.sigma_a).evalf())*(np.float64(Float(self.Sut).evalf())**2)+
                    np.float64(Float(self.Sut).evalf())*sqrt((np.float64(Float(self.sigma_a).evalf())**2)*
                    (np.float64(Float(self.Sut).evalf())**2)+4*(np.float64(Float(self.Se).evalf())**2)*
                    (np.float64(Float(self.sigma_m).evalf())**2)))/(2*np.float64(Float(self.Se).evalf())*
                    (np.float64(Float(self.sigma_m).evalf())**2))
        N_asme = (np.float64(Float(self.Se).evalf())*np.float64(Float(self.Sy).evalf())*
                  sqrt((np.float64(Float(self.sigma_a).evalf())**2)*(np.float64(Float(self.Sy).evalf())**2)+
                       (np.float64(Float(self.Se).evalf())**2)*(np.float64(Float(self.sigma_m).evalf())**2)))/((np.float64(Float(self.sigma_a).evalf())**2)*
                        (np.float64(Float(self.Sy).evalf())**2)+ (np.float64(Float(self.Se).evalf())**2)*(np.float64(Float(self.sigma_m).evalf())**2))
        N_langer = np.float64(Float(self.Sy).evalf())/(np.float64(Float(self.sigma_a).evalf())+np.float64(Float(self.sigma_m).evalf()))

        # Mostrando valores calculados para o usuário e plotando critérios

        if self.sodeberg == true:
            Builder.get_object("n_soderberg").set_text(str(N_soder))
            axis.plot(self.x_soder, self.y_soder, label='Critério de Soderberg')
        else:
            Builder.get_object("n_soderberg").set_text('Coeficiente de segurança')

        if self.goodman == true:
            Builder.get_object("n_goodman").set_text(str(N_good))
            axis.plot(self.x_good, self.y_good, label='Critério de Goodman modificado')
        else:
            Builder.get_object("n_goodman").set_text('Coeficiente de segurança')
        
        if self.gerber == true:
            Builder.get_object("n_gerber").set_text(str(N_gerber))
            axis.plot(self.x_gerber, self.y_gerber, label='Critério de Gerber')
        else:
            Builder.get_object("n_gerber").set_text('Coeficiente de segurança')

        if self.asme == true:
            Builder.get_object("n_asme").set_text(str(N_asme))
            axis.plot(self.x_asme, self.y_asme, label='Critério elíptico da ASME')
        else:
            Builder.get_object("n_asme").set_text('Coeficiente de segurança')

        if self.langer == true:
            Builder.get_object("n_langer").set_text(str(N_langer))
            axis.plot(self.x_langer, self.y_langer, label='Critério de escoamento (Langer)')
        else:
            Builder.get_object("n_langer").set_text('Coeficiente de segurança')

        axis.plot(self.x_linha_r, self.y_linha_r, label='Linha de carga')

        # Traçar a linha tracejada até o ponto
        axis.plot([np.float64(Float(self.sigma_m).evalf()), np.float64(Float(self.sigma_m).evalf())], [0, np.float64(Float(self.sigma_a).evalf())], 'r--')
        axis.plot([0, np.float64(Float(self.sigma_m).evalf())], [np.float64(Float(self.sigma_a).evalf()), np.float64(Float(self.sigma_a).evalf())], 'r--')

        # Adicionar o círculo vermelho ao redor do ponto
        axis.scatter(np.float64(Float(self.sigma_m).evalf()), np.float64(Float(self.sigma_a).evalf()), color='red', zorder=10)

        axis.set_yscale('linear')  # Configurando escala linear para o eixo y
        axis.set_xscale('linear')     # Configurando escala logarítmica para o eixo x
        axis.set_xlabel('Tensão média $\sigma_m$ (MPa)')
        axis.set_ylabel('Tensão alternada $\sigma_a$ (MPa)')
        axis.grid(True)
        #axis.tight_layout()     # Ajustando o espaçamento do gráfico

        axis.set_xlim(0, np.float64(Float(self.Sut).evalf())*1.1)
        axis.set_ylim(0, np.float64(Float(self.Sy).evalf())*1.1)

        # Adicionando a legenda ao lado do nome da linha do plot
        axis.legend(loc='upper right')

        canvas = FigureCanvas(figure)  
        canvas.set_size_request(1000, 800)
        sw.add(canvas)
        sw.show_all()
    

Builder = Gtk.Builder()
Builder.add_from_file("user_interface.glade")
Builder.connect_signals(Handler())
Window: Gtk.Window = Builder.get_object("main_window_2")

Window.show_all()
Gtk.main()
