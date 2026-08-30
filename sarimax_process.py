import pandas as pd

def previsao_sarimax(modelo, data_alvo, caminho, data_inicio):
    #data de inicio no fim dos dados de treinamento
    data_inicio = pd.Timestamp(data_inicio)
    data_alvo = pd.Timestamp(data_alvo)
    datas_futuras = pd.date_range(start=data_inicio, end=data_alvo, freq='W-SUN')

    historico = pd.read_csv(caminho)[["umidmed", "tempmed"]]
    medias = historico.mean()  

    exog = pd.DataFrame(
        [medias.values] * len(datas_futuras),  
        columns=medias.index,
        index=datas_futuras
    )

    #print(f'###dataset: {exog}')
    futuro = len(exog)
    previsao = modelo.get_forecast(steps=futuro, exog=exog)
    previsoes = previsao.predicted_mean
    previsoes = pd.DataFrame(previsoes.values, columns=['previsao'], index=previsoes.index)
    previsoes["previsao"] = previsoes["previsao"].clip(lower=0)
    #print(previsoes)
    return previsoes
    


