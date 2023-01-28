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
        servico = Service(ChromeDriverManager().install())
        # Para instalar o webdriver automaticamente
        self.navegador = webdriver.Chrome(service=servico)
        self.corteAnteior = []
        self.novoCorte = []
        self.diferençaCorte = []
        self.dia = input('Ler para o dia: ')

    def preencher_dados(self):
        codigos = self._pega_codigos()
        for codigo in codigos:
            # Pelas minhas observações os códigos variam entre esses dois valores
            # O tqdm é para criar uma barra de progresso
            link = f"https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/{codigo}/modalidades"
            # Nesse link retorna um json com várias informações sobre os cursos
            self._get_url(link)
            # Lê o link
            if self.resultado == "":
                continue
                # Se não existir nenhuma vaga com o código digitado o retorno é vazio e só pula para a próxima interação
            else:
                arquivoJson = self.resultado
                print(
                    f"\nEncontrado Json. Já encontrados: {len(self.codigoSISU)}")
                arquivoJson = dict(arquivoJson)
                # Pega o Json e converte em dicionário por garantia
                self._preencher_dado(arquivoJson)
                # Preenche as listas com os valores do json
        self.corteAnteior = self._pega_ultimo_corte()
        if len(self.corteAnteior) == len(self.novoCorte):
            for i, anterior in enumerate(self.corteAnteior):
                novo = self.novoCorte[i]
                self.diferençaCorte.append(novo-anterior)
        else:
            print("ERRO: O corte anterior e o novo corte não tem o mesmo tamanho")
            quit()

    def _pega_ultimo_corte(self):
        return list(set(pd.read_excel(f"ResultadoDia{self.dia}.xlsx")[f'Nota_Corte_{self.dia}_Dia']))

    def _pega_codigos(self) -> list:
        return list(set(pd.read_excel(f"ResultadoDia{self.dia}.xlsx")['CodigoSISU']))
        # Uso do set() para não ter valores repetidos

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

    def _preencher_dado(self, arquivoJson):
        modalidades = arquivoJson['modalidades']
        oferta = arquivoJson['oferta']
        # O arquivo Json é dividido nessas duas partes
        # A oferta com as informações do curso no geral valido para todas as cotas
        # e a modalidade que são as cotas e as informações específicas
        for modalidade in modalidades:
            self.novoCorte.append(modalidades['nu_nota_corte'])

    def exportar_dados(self):
        df = pd.read_excel(f"ResultadoDia{self.dia}.xlsx")
        df[f'Nota_Corte_{self.dia+1}_Dia'] = self.novoCorte
        df[f'Diferenca_Corte_{self.dia}_e_{self.dia+1}_dia'] = self.diferençaCorte
        df.to_excel(f'ResultadoDia{self.num_dia+1}.xlsx', index = False)

if __name__ == "__main__":
    sisu = SISUApi()
    sisu.preencher_dados()
    sisu.exportar_dados()
