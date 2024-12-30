import yfinance as yf
import numpy as np
from scipy.stats import norm
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

# Dicionário para armazenar históricos de resultados por ticker
historico_resultados = {}

def calcular_metricas(ticker, start_date, end_date):
    try:
        # Obtendo os dados históricos do ticker
        dados = yf.download(ticker, start=start_date, end=end_date)
        
        if dados.empty:
            raise ValueError(f"Não foram encontrados dados para o ticker {ticker}.")
        
        # Obtendo os dados do benchmark
        benchmark_ticker = '^BVSP' #'^GSPC' Índice de referência (S&P 500)
        benchmark_dados = yf.download(benchmark_ticker, start=start_date, end=end_date)
        
        # Sincronizando os dados para garantir que as datas coincidem
        dados = dados[['Close']].rename(columns={'Close': 'Variações'})
        benchmark_dados = benchmark_dados[['Close']].rename(columns={'Close': 'SP500_Close'})
        
        # Juntando os dados da ação e do benchmark
        dados_combinados = dados.join(benchmark_dados, how='inner')

        # Calculando os retornos diários
        dados_combinados['Variações_Retorno'] = dados_combinados['Variações'].pct_change()
        dados_combinados['SP500_Retorno'] = dados_combinados['SP500_Close'].pct_change()

        # Calculando o beta
        cov = np.cov(dados_combinados['Variações_Retorno'].dropna(), dados_combinados['SP500_Retorno'].dropna())[0, 1]
        var = np.var(dados_combinados['SP500_Retorno'].dropna())
        beta = cov / var

        # Calculando o desvio padrão
        desvio_padrao = np.std(dados_combinados['Variações_Retorno'].dropna())

        # Filtrando apenas os retornos negativos
        retornos_negativos = dados_combinados['Variações_Retorno'][dados_combinados['Variações_Retorno'] < 0]

        # Calculando a volatilidade
        volatilidade = np.std(retornos_negativos)

        # Calculando o logaritmo da volatilidade
        log_volatilidade = np.log(volatilidade) if volatilidade > 0 else 0

        return beta, desvio_padrao, volatilidade, log_volatilidade
    except Exception as e:
        print(f"Erro ao processar o ticker {ticker}: {e}")
        return None



def adicionar_resultado_ao_historico(ticker, resultados):
    global historico_resultados

    # Verifica se há um histórico para o ticker
    if ticker not in historico_resultados:
        historico_resultados[ticker] = {'resultados': [], 'indice_resultado_atual': -1}

    # Adiciona os resultados atuais ao histórico específico do ticker
    historico_resultados[ticker]['resultados'].append(resultados)
    
    # Atualiza o índice do resultado atual
    historico_resultados[ticker]['indice_resultado_atual'] = len(historico_resultados[ticker]['resultados']) - 1

def mostrar_resultados_anteriores():
    global historico_resultados
    ticker = ticker_entry.get().split()[0]  # Pega apenas o primeiro ticker

    if ticker in historico_resultados and len(historico_resultados[ticker]['resultados']) > 1:
        # Decrementa o índice para exibir o resultado anterior
        historico_resultados[ticker]['indice_resultado_atual'] -= 1
        indice_resultado_atual = historico_resultados[ticker]['indice_resultado_atual']
        exibir_resultado(historico_resultados[ticker]['resultados'][indice_resultado_atual])
    else:
        messagebox.showinfo("Informação", "Não há mais resultados anteriores para este ticker.")

def mostrar_resultados_seguintes():
    global historico_resultados
    ticker = ticker_entry.get().split()[0]  # Pega apenas o primeiro ticker

    if ticker in historico_resultados and len(historico_resultados[ticker]['resultados']) > 1 and \
            historico_resultados[ticker]['indice_resultado_atual'] < len(historico_resultados[ticker]['resultados']) - 1:
        # Incrementa o índice para exibir o próximo resultado
        historico_resultados[ticker]['indice_resultado_atual'] += 1
        indice_resultado_atual = historico_resultados[ticker]['indice_resultado_atual']
        exibir_resultado(historico_resultados[ticker]['resultados'][indice_resultado_atual])
    else:
        messagebox.showinfo("Informação", "Não há mais resultados seguintes para este ticker.")

def exibir_resultado(resultados):
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, resultados)
    result_text.config(state="disabled")

def save_to_excel(tickers, df):
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    file_path = os.path.join(downloads_folder, 'resultados.xlsx')
    df.to_excel(file_path, index=False)
    messagebox.showinfo("Informação", f"Resultados salvos em {file_path}")

def show_results():
    global historico_resultados

    tickers = ticker_entry.get().split()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    portfolio_value = float(portfolio_value_entry.get())

    if not tickers or not start_date or not end_date:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    try:
        start_date = datetime.strptime(start_date, "%d/%m/%Y")
        end_date = datetime.strptime(end_date, "%d/%m/%Y")
    except ValueError:
        messagebox.showerror("Erro", "As datas devem estar no formato DD/MM/AAAA.")
        return

    resultados_df = pd.DataFrame()

    for ticker in tickers:
        metricas = calcular_metricas(ticker, start_date, end_date)
        
        if metricas:
            beta, desvio_padrao, volatilidade, log_volatilidade = metricas
            returns = yf.download(ticker, start=start_date, end=end_date)['Adj Close'].pct_change().dropna()
            confidence_level = 0.95  # Define o nível de confiança
            
            def calculate_var(returns, portfolio_value, confidence_level):
                expected_returns = returns.mean()
                volatility = returns[returns < 0].std()
                var = portfolio_value * (expected_returns - volatility * norm.ppf(1 - confidence_level))
                return var
            
            var = calculate_var(returns, portfolio_value, confidence_level)
            var_percentage = (var / portfolio_value) * 100

            # Usar iloc[0] para acessar o valor se for um pd.Series
            var = float(var.iloc[0]) if isinstance(var, pd.Series) else var
            var_percentage = float(var_percentage.iloc[0]) if isinstance(var_percentage, pd.Series) else var_percentage

            resultado_texto = (
                f"Ticker: {ticker}\n"
                f"Beta: {beta:.2f}\n"
                f"Desvio Padrão: {desvio_padrao*100:.3f}\n"
                f"Volatilidade: {volatilidade*100:.3f}\n"
                f"Log da Volatilidade Negativa: {log_volatilidade:.2f}\n"
                f"Value at Risk (95% confidence): ${var:,.2f}\n"
                f"Porcentagem de perda máxima esperada: {var_percentage:.2f}%\n"
            )

            adicionar_resultado_ao_historico(ticker, resultado_texto)
            exibir_resultado(resultado_texto)

            # Adicionar resultados ao DataFrame
            dados_dict = {
                "Ticker": ticker,
                "Beta": beta,
                "Desvio Padrão (%)": desvio_padrao*100,
                "Volatilidade (%)": volatilidade*100,
                "Log da Volatilidade Negativa": log_volatilidade,
                "Value at Risk (95% confidence)": var,
                "Porcentagem de perda máxima esperada (%)": var_percentage
            }
            resultados_df = pd.concat([resultados_df, pd.DataFrame([dados_dict])], ignore_index=True)
        else:
            messagebox.showerror("Erro", f"Erro ao processar {ticker}. O ticker pode não estar disponível ou ocorreu outro erro.")

    # Garantir que os dados no DataFrame sejam numéricos
    resultados_df = resultados_df.apply(pd.to_numeric, errors='ignore')

    save_to_excel(tickers, resultados_df)  # Salva os resultados no Excel




# Configuração da janela
window = tk.Tk()
window.title("Análise de Ações")
window.geometry("450x500")

# Rótulos e entradas de dados
tk.Label(window, text="Ticker da Ação:").pack()
ticker_entry = tk.Entry(window)
ticker_entry.pack()

tk.Label(window, text="Data de Início (DD/MM/AAAA):").pack()
start_date_entry = tk.Entry(window)
start_date_entry.pack()

tk.Label(window, text="Data de Fim (DD/MM/AAAA):").pack()
end_date_entry = tk.Entry(window)
end_date_entry.pack()

tk.Label(window, text="Valor do Portfólio:").pack()  # Adicione um rótulo para o valor do portfólio
portfolio_value_entry = tk.Entry(window)
portfolio_value_entry.pack()

# Botão para calcular métricas
calculate_button = tk.Button(window, text="Calcular Métricas", command=show_results)
calculate_button.pack()

# Texto para exibir resultados
result_text = tk.Text(window, height=10, width=50)
result_text.pack()
result_text.config(state="disabled")

# Adicionar botões para navegar pelos resultados anteriores e seguintes
anterior_button = tk.Button(window, text="Anterior", command=mostrar_resultados_anteriores)
anterior_button.pack()

seguinte_button = tk.Button(window, text="Seguinte", command=mostrar_resultados_seguintes)
seguinte_button.pack()

# Iniciar a janela
window.mainloop()
