# Risco
Este código gera indicadores com função de ajudar na gestão de risco de uma carteira de investimentos, realizando análises financeiras de ações com base em um intervalo de datas fornecido, ele utiliza uma interface gráfica para coletar os parâmetros e retorna as seguintes métricas para cada ação (ticker).

Usanado a biblioteca Tkinter como interface para exibir os resultados, botões para calcular métricas e navegar entre resultados anteriores e seguintes, Salvar os dados calculados no arquivo resultados.xlsx na pasta de downloads.

Valores Calculados: 

-Beta: Relação entre o retorno de ações Brasileira e o benchmark Ibovespa (^BVSP, que pode ser subtituido pelo indexador desejado para calculo do Beta)

-Desvio Padrão (%): Volatilidade geral dos retornos diários

-Volatilidade (%): Apenas para retornos negativos

-Log da Volatilidade Negativa: Logaritmo da volatilidade negativa (usado em modelos financeiros)

-Value at Risk (VaR)*: Perda máxima esperada com 95% de confiança, em valor monetário

-Porcentagem de Perda Máxima: VaR como percentual do valor do portfólio 

-Histórico de Resultados: Permite navegar pelos resultados calculados anteriormente

Entradas do Usuário: 

-Tickers (código das ações, como "PETR4.SA")

-Datas de início e fim (formato: DD/MM/AAAA)

-Valor do portfólio (em reais ou dólares, conforme mercado).

*O Value at Risk (VaR) é uma medida usada para estimar o risco financeiro de uma carteira de investimentos ou de um ativo em um determinado período de tempo. Ele quantifica a perda potencial máxima em um investimento sob condições normais de mercado, com um determinado nível de confiança.
