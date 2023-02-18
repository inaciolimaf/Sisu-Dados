import time
from tqdm import tqdm
import pandas as pd
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import selenium.common


class SISUApi:
    def __init__(self) -> None:
        self.codigoSISU = []
        self.universidade = []
        self.campus = []
        self.nomeEstado = []
        self.nomeMunicipio = []
        self.nomeCurso = []
        self.grau = []
        self.turno = []
        self.codigoIES = []
        self.MinimaNotaCN = []
        self.pesoNotaCN = []
        self.minimoNotaMT = []
        self.pesoNotaMT = []
        self.minimoNotaL = []
        self.pesoNotaL = []
        self.minimoNotaCH = []
        self.pesoNotaCH = []
        self.minimoNotaREDACAO = []
        self.pesoNotaREDACAO = []
        self.mediaMinima = []
        self.cota = []
        self.bonus_percentual = []
        self.vagasCota = []
        self.notaCorteAtual = []
        self.notasCorteAnteriores = []
        self.num_dia = int(input("Digite o dia: "))
        # Declara as colunas que vão ser preenchidas
        servico = Service(ChromeDriverManager().install())
        # Para instalar o webdriver automaticamente
        self.navegador = webdriver.Chrome(service=servico)

    def preencher_dados(self):
        linkUniversidades = "https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/instituicoes/uf"
        self._get_url(linkUniversidades)
        self.resultado = dict(self.resultado)
        for estado, universidades in self.resultado.items():
            for universidade in universidades:
                print(f"Para a universidade: {universidade['no_ies']}")
                linkUniversidade = f"https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/instituicao/{universidade['co_ies']}"
                self._get_url(linkUniversidade)
                cursos = dict(self.resultado)
                for i in range(0, len(cursos)-1):
                    # -1 porque a primeira chave é do json é "search_rule"
                    codigo = cursos[str(i)]["co_oferta"]
                    print(codigo)
                    linkcurso = f"https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/{codigo}/modalidades"
                    # Nesse link retorna um json com várias informações sobre os cursos
                    self._get_url(linkcurso)
                    # Lê o link
                    if self.resultado == "":
                        continue
                        # Se não existir nenhuma vaga com o código digitado o retorno é vazio e só pula para a próxima interação
                    else:
                        arquivoJson = self.resultado
                        self.dados = dict(arquivoJson)
                        # Pega o Json e converte em dicionário por garantia
                        self._preencher_dado()
                        # Preenche as listas com os valores do json

    def _get_url(self, link):
        self.navegador.delete_all_cookies()
        self.navegador.get(link)
        # Não será possível usar requests porque as vezes retorna 403 forbidden
        if self.navegador.current_url == link:
            # Como quando o código não existe ele não muda o link da página,
            # Se mudar significa que existe o código, senão, não existe
            try:
                texto = self.navegador.find_element(By.TAG_NAME, "pre").text
                self.resultado = json.loads(texto)
                # Pega o texto da página e gera o Json
            except selenium.common.exceptions.NoSuchElementException as e:
                self.resultado = ""
                #  Caso o resultado não seja encontrado, o código não existe, o resultado é vazio
            except selenium.common.exceptions.WebDriverException as e:
                time.sleep(1)
                self._get_url(link)
            except json.decoder.JSONDecodeError as e:
                print("DEU MUITO ERRADO")
                print("="*30)
                time.sleep(1)
                self._get_url(link)
            # Caso der algum desses erros essa função é executada novamente
        else:
            self.resultado = ""
            #  Caso o resultado não seja encontrado, o código não existe, o resultado é vazio

    def _preencher_dado(self):
        modalidades = self.dados['modalidades']
        oferta = self.dados['oferta']
        # O arquivo Json é dividido nessas duas partes
        # A oferta com as informações do curso no geral valido para todas as cotas
        # e a modalidade que são as cotas e as informações específicas
        for modalidade in modalidades:
            self.codigoSISU.append(oferta['co_oferta'])
            self.codigoIES.append(oferta['co_ies'])
            self.universidade.append(oferta['no_ies'])
            self.nomeEstado.append(oferta['sg_uf_ies'])
            self.nomeMunicipio.append(oferta['no_municipio_campus'])
            self.campus.append(oferta['no_campus'])
            self.nomeCurso.append(oferta['no_curso'])
            self.grau.append(oferta['no_grau'])
            self.turno.append(oferta['no_turno'])
            self.MinimaNotaCN.append(oferta['nu_nmin_cn'])
            self.pesoNotaCN.append(oferta['nu_peso_cn'])
            self.minimoNotaMT.append(oferta['nu_nmin_m'])
            self.pesoNotaMT.append(oferta['nu_peso_m'])
            self.minimoNotaL.append(oferta['nu_nmin_l'])
            self.pesoNotaL.append(oferta['nu_peso_l'])
            self.minimoNotaCH.append(oferta['nu_nmin_ch'])
            self.pesoNotaCH.append(oferta['nu_peso_ch'])
            self.minimoNotaREDACAO.append(oferta['nu_nmin_r'])
            self.pesoNotaREDACAO.append(oferta['nu_peso_r'])
            self.mediaMinima.append(oferta['nu_media_minima'])
            self.cota.append(modalidade['no_concorrencia'])
            self.vagasCota.append(modalidade['qt_vagas'])
            self.bonus_percentual.append(modalidade['qt_bonus_perc'])
            self.notaCorteAtual.append(modalidade['nu_nota_corte'])

    def exportar_dados(self):
        self.pegar_dados_anteriores()
        valores = {'CodigoSISU': self.codigoSISU,
                   'CodigoIES': self.codigoIES,
                   'Universidade': self.universidade,
                   'Nome_Estado': self.nomeEstado,
                   'Nome_Municipio_Campus': self.nomeMunicipio,
                   'Campus': self.campus,
                   'Nome_Curso': self.nomeCurso,
                   'Grau': self.grau,
                   'Turno': self.turno,
                   'Cota': self.cota,
                   'Quant_Vagas_Cota': self.vagasCota,
                   'Minimo_Nota_CN': self.MinimaNotaCN,
                   'Peso_Nota_CN': self.pesoNotaCN,
                   'Minimo_Nota_MT': self.minimoNotaMT,
                   'Peso_Nota_MT': self.pesoNotaMT,
                   'Minimo_Nota_L': self.minimoNotaL,
                   'Peso_Nota_L': self.pesoNotaL,
                   'Minimo_Nota_CH': self.minimoNotaCH,
                   'Peso_Nota_CH': self.pesoNotaCH,
                   'Minimo_Nota_REDACAO': self.minimoNotaREDACAO,
                   'Peso_Nota_REDACAO': self.pesoNotaREDACAO,
                   'Media_Minima': self.mediaMinima,
                   'Bonus_Percentual': self.bonus_percentual
                   }
        for notaAnterior in self.notasCorteAnteriores:
            valores.update(notaAnterior)

        valores.update({f'Nota_Corte_{self.num_dia}_Dia': self.notaCorteAtual})
        df = pd.DataFrame(valores)
        df.to_excel(f'ResultadoDia{self.num_dia}.xlsx', index=False)

    def pegar_dados_anteriores(self):
        for dia_anterior in range(1, self.num_dia):
            df = pd.read_excel(f"ResultadoDia{self.num_dia-1}.xlsx")
            if dia_anterior == self.num_dia - 1:
                nota_de_corte_dia = df[f'Nota_Corte_{dia_anterior}_Dia']
                diferenca_nota_corte = []
                for i, nota in enumerate(list(nota_de_corte_dia)):
                    diferenca_nota_corte.append(
                        float(self.notaCorteAtual[i])-float(nota))
                self.notasCorteAnteriores.append(
                    {f'Nota_Corte_{dia_anterior}_Dia': nota_de_corte_dia})
                self.notasCorteAnteriores.append(
                    {f'Diferenca_Corte_{dia_anterior}_Para_{dia_anterior+1}_Dia': diferenca_nota_corte})
            else:
                self.notasCorteAnteriores.append({f'Nota_Corte_{dia_anterior}_Dia':
                                                  df[f'Nota_Corte_{dia_anterior}_Dia']})
                self.notasCorteAnteriores.append({f'Diferenca_Corte_{dia_anterior}_Para_{dia_anterior+1}_Dia':
                                                  df[f'Diferenca_Corte_{dia_anterior}_Para_{dia_anterior+1}_Dia']})


if __name__ == "__main__":
    sisu = SISUApi()
    sisu.preencher_dados()
    sisu.exportar_dados()