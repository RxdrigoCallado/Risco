# Risco
 Código gera indicadores com função de ajudar na gestão de risco de uma carteira de investimentos, realizando análises financeiras de ações com base em um intervalo de datas fornecido. 

Ele utiliza uma interface gráfica para coletar os parâmetros e retorna as seguintes métricas para cada ação (ticker):

Valores Calculados- 
Beta: Relação entre o retorno da ação e o benchmark (exemplo: ^BVSP), Desvio Padrão (%): Volatilidade geral dos retornos diários, Volatilidade (%): Apenas para retornos negativos, Log da Volatilidade Negativa: Logaritmo da volatilidade negativa (usado em modelos financeiros), Value at Risk (VaR): Perda máxima esperada com 95% de confiança, em valor monetário, Porcentagem de Perda Máxima: VaR como percentual do valor do portfólio, Recursos Adicionais, Histórico de Resultados: Permite navegar pelos resultados calculados anteriormente.

Entradas do Usuário- Tickers (código das ações, como "PETR4.SA"), Datas de início e fim (formato: DD/MM/AAAA), Valor do portfólio (em reais ou dólares, conforme mercado).

Interface- Área para exibir os resultados, botões para calcular métricas e navegar entre resultados anteriores e seguintes, Salvar os dados calculados no arquivo resultados.xlsx na pasta de downloads.
