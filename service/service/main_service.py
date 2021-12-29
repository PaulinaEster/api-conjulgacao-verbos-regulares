import time
import json
from loguru import logger
from service.constants import mensagens
import pandas as pd

class ConjulgacaoVerboService():

    def __init__(self):
        logger.debug(mensagens.INICIO_LOAD_SERVICO)
        self.load_model()

    def load_model(self):
        """"
        Carrega o modelo VADER a ser usado
        """

        logger.debug(mensagens.FIM_LOAD_SERVICO)

    def executar_rest(self, texts):
        response = {}

        logger.debug(mensagens.INICIO_SERVICE)
        start_time = time.time()

        response_predicts = self.conjugar_verbo(texts['textoMensagem'])

        logger.debug(mensagens.FIM_SERVICE)
        logger.debug(f"Fim de todas as predições em {time.time()-start_time}")

        df_response = pd.DataFrame(texts, columns=['textoMensagem'])
        df_response['conjulgacao'] = response_predicts

        df_response = df_response.drop(columns=['textoMensagem'])

        response = {
                     "listaConjulgacoes": json.loads(df_response.to_json(
                                                                            orient='records', force_ascii=False))}

        return response

    def conjugar_verbo(self, texts):
        """
        Pega o modelo carregado e aplica em texts
        """
        logger.debug('Iniciando a conjulgação...')

        response = []

        for text in texts:
            pessoas = ['Eu', 'Tu', 'Ele', 'Nós', 'Vós', 'Eles']; 
            conjuga_ar = ['o', 'as', 'a', 'amos', 'ais', 'am']; 
            conjuga_er = ['o', 'es', 'e', 'emos', 'eis', 'em']; 
            conjuga_ir = ['o', 'es', 'e', 'imos', 'is', 'em']; 
            
            verbo = str(text)
            termina_em = verbo[-2:]  
            res = []
            
            if termina_em == 'ar': 
                for i in range(6):
                    res.append(pessoas[i]+' '+verbo[:-2]+conjuga_ar[i])
                response.append(res) 
            elif termina_em == 'er': 
                for i in range(6):
                    res.append(pessoas[i]+' '+verbo[:-2]+conjuga_er[i]) 
                response.append(res) 
            elif termina_em == 'ir': 
                for i in range(6):
                    res.append(pessoas[i]+' '+verbo[:-2]+conjuga_ir[i])
                response.append(res) 
            else: 
                response.append('Tem certeza que '+ verbo +' é um verbo regular?')

        return response