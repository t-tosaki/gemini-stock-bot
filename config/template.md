# {ticker} {company_name}（{current_price.date}）

## 💰 株価情報

- 株価: {current_price.close}円（前日終値: {current_price.prev_close}円 / 始値: {current_price.open}円 / 高値: {current_price.high}円 / 安値: {current_price.low}円）（{状況コメント}）
- 出来高: {current_price.volume} / 平均: {risk_metrics.avg_volume}（{状況コメント}）
- 52週レンジ: {52_week.high}円 ~ {52_week.low}円（{状況コメント}）
- Beta: {risk_metrics.beta}（{状況コメント}）

## 📈 バリュエーション

- PER: {valuation.per}倍（{状況コメント}）
- PBR: {valuation.pbr}倍（{状況コメント}）
- 配当利回り: {dividend.yield_percent}%
- 決算日: {risk_metrics.earnings_date}

## 📊 テクニカル指標

- Stochastic RSI: %K: {technical_indicators.stochastic_rsi.stochastic_k} / %D {technical_indicators.stochastic_rsi.stochastic_d}（{状況コメント}）
- MACD: {technical_indicators.macd.macd}（{状況コメント}）
- ADX: {technical_indicators.adx.adx}（{状況コメント}）
- Supertrend: {technical_indicators.supertrend.supertrend}円（{状況コメント}）
- 一目均衡表: 転換戦: {technical_indicators.ichimoku.tenkan_sen} / 基準線: {technical_indicators.ichimoku.kijun_sen} / 遅行線: {technical_indicators.ichimoku.chikou_span}（{状況コメント}）
- 雲: A: {technical_indicators.ichimoku.cloud.senkou_span_b}円 / B: {technical_indicators.ichimoku.cloud.senkou_span_a}円（{状況コメント}）

### テクニカル分析結果

{各テクニカル指標を踏まえた総合的な分析・判断}

## 📰 関連ニュース

### 銘柄関連ニュース

{銘柄関連ニュースの要約と株価への影響分析}

### マクロ経済ニュース

{関連性のあるマクロ経済ニュースの要約と株価への影響分析}

## 🎯 総合判断

- {買い/売り/様子見}

### 根拠

{根拠の要約}

### 注目

{次に見るべきポイント}
