# -*- coding: utf-8 -*-
"""
Option Delta查询工具
查询实时期权 Delta 值

运行: streamlit run option_delta_app.py
"""

import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Black-Scholes 模型计算 Delta
def black_scholes_delta(S, K, T, r, sigma, option_type='call'):
    """计算期权 Delta"""
    from scipy.stats import norm
    
    if T <= 0:
        return 1.0 if option_type == 'call' and S > K else 0.0 if option_type == 'put' and S < K else 0.5
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    if option_type.lower() == 'call':
        return norm.cdf(d1)
    else:
        return norm.cdf(d1) - 1

def get_option_delta(ticker, expiration_date, strike, option_type, volatility=None):
    """获取期权 Delta"""
    stock = yf.Ticker(ticker)
    
    # 获取当前股价
    current_price = stock.history(period='1d')['Close'].iloc[-1]
    
    # 计算到期天数
    exp_date = datetime.strptime(expiration_date, '%Y-%m-%d')
    today = datetime.now()
    T = (exp_date - today).days / 365.0
    
    if T <= 0:
        return None, "到期日期已过"
    
    # 如果没有提供波动率，使用历史波动率
    if volatility is None:
        # 估算隐含波动率（使用30天历史波动率）
        hist_vol = stock.history(period='30d')['Close'].pct_change().std() * np.sqrt(252)
        volatility = max(hist_vol, 0.1)  # 最低10%波动率
    
    # 假设无风险利率为 5%
    r = 0.05
    
    # 计算 Delta
    delta = black_scholes_delta(current_price, float(strike), T, r, volatility, option_type)
    
    return delta, current_price

# Streamlit 界面
st.set_page_config(page_title="期权 Delta 查询", page_icon="📈", layout="centered")

st.title("📈 期权 Delta 查询工具")

st.markdown("""
输入股票代码和期权参数，查询实时 Delta 值
""")

# 输入区域
col1, col2 = st.columns(2)

with col1:
    ticker = st.text_input("股票代码", value="AAPL").upper()

with col2:
    option_type = st.selectbox("期权类型", ["Call", "Put"])

st.markdown("---")

# 获取期权链
try:
    stock = yf.Ticker(ticker)
    expirations = stock.options
    
    if len(expirations) == 0:
        st.error(f"❌ {ticker} 没有可用的期权数据")
    else:
        # 显示可用到期日
        st.write("📅 可选到期日:")
        cols = st.columns(4)
        selected_exp = None
        
        for i, exp in enumerate(expirations[:12]):  # 最多显示12个
            with cols[i % 4]:
                if st.button(exp, key=f"exp_{i}"):
                    selected_exp = exp
        
        st.markdown("---")
        
        if selected_exp:
            st.success(f"选择到期日: {selected_exp}")
            
            # 获取该到期日的期权链
            opt = stock.option_chain(selected_exp)
            
            if option_type == "Call":
                options = opt.calls
            else:
                options = opt.puts
            
            # 输入行权价
            strike = st.number_input("行权价 (Strike Price)", min_value=0.0, step=0.5, value=float(options['strike'].iloc[len(options)//2] if len(options) > 0 else 100.0))
            
            # 搜索最接近的期权
            closest = options.iloc[(options['strike'] - strike).abs().argsort()[:1]]
            
            if len(closest) > 0:
                row = closest.iloc[0]
                
                st.markdown("### 📊 期权信息")
                
                # 显示当前股价
                current_price = stock.history(period='1d')['Close'].iloc[-1]
                st.write(f"**当前股价:** ${current_price:.2f}")
                st.write(f"**行权价:** ${row['strike']:.2f}")
                st.write(f"**到期日:** {selected_exp}")
                
                # 计算 Delta
                delta, price = get_option_delta(ticker, selected_exp, row['strike'], option_type)
                
                if delta is not None:
                    st.markdown("### 🎯 Delta 值")
                    st.markdown(f"## {delta:.4f}")
                    
                    # Delta 解释
                    if option_type == "Call":
                        if delta > 0.7:
                            st.info("💚 深度实值期权 (ITM)")
                        elif delta > 0.3:
                            st.info("🧡 平值期权 (ATM)")
                        else:
                            st.info("❤️ 深度虚值期权 (OTM)")
                    else:
                        if delta < -0.7:
                            st.info("💚 深度实值期权 (ITM)")
                        elif delta > -0.3:
                            st.info("🧡 平值期权 (ATM)")
                        else:
                            st.info("❤️ 深度虚值期权 (OTM)")
                    
                    # 其他信息
                    st.write(f"**隐含波动率:** {row.get('impliedVolatility', 'N/A'):.2%}" if row.get('impliedVolatility') else "**隐含波动率:** N/A")
                    st.write(f"**理论价格:** ${row.get('lastPrice', 0):.2f}" if row.get('lastPrice') else "**最新价格:** N/A")
                    st.write(f"**未平仓合约:** {row.get('openInterest', 'N/A'):,}" if row.get('openInterest') else "**未平仓合约:** N/A")
                    
                else:
                    st.error(price)  # 错误信息
                    
except Exception as e:
    st.error(f"❌ 错误: {str(e)}")

# 底部说明
st.markdown("---")
st.caption("📌 Delta 值表示标的资产价格变动1美元时期权价格的变动量")

