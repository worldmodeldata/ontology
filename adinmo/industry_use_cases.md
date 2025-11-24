# Adinmo Data: Industry Use Cases & Resale Opportunities

## Executive Summary

The Adinmo dataset represents a **unique, high-value behavioral dataset** spanning in-game advertising, user behavior, monetization, and attribution. With TBs of longitudinal data linked by device ID, this dataset offers exceptional value for:

1. **AI/ML Training**: Real-world user behavior sequences for predictive modeling
2. **Market Research**: Gaming industry insights and consumer behavior patterns  
3. **Energy & Infrastructure**: Time-series usage patterns for demand forecasting
4. **Financial Services**: Consumer spending behavior and propensity modeling
5. **Advertising Technology**: Benchmarking, fraud detection, and optimization

**Key Differentiators**:
- **Longitudinal tracking**: Complete user journeys from ad exposure → install → monetization
- **Cross-game visibility**: User behavior across multiple games/apps
- **Rich context**: Device, geo, temporal, and behavioral features
- **Scale**: TBs of data, millions of users, billions of events

---

## Industry Applications & Buyers

### 1. AI & Machine Learning Training

#### Use Case 1A: Large Language Models (LLMs) & Foundation Models
**Buyer Profile**: OpenAI, Anthropic, Google, Meta, Cohere

**Dataset Value**:
- **Sequential decision-making data**: User actions in temporal order (session → ad view → click → install → purchase)
- **Reward signals**: Clear outcomes (clicks, installs, purchases) for reinforcement learning
- **Multi-modal context**: Text (device names, locations), time-series (engagement patterns), categorical (device types)

**Specific Applications**:
- **Behavior prediction models**: Next-action prediction in user flows
- **Recommendation systems**: What content/products to show based on context
- **Time-series forecasting**: Predict user actions at future timestamps
- **Contextual bandits**: Optimize which ad/content to show given user state
- **Causal inference**: Did ad exposure *cause* purchase or just correlate?

**Pricing Potential**: $50K - $500K per dataset delivery (depending on scope and exclusivity)

#### Use Case 1B: Predictive Analytics Models
**Buyer Profile**: Palantir, C3.ai, DataRobot customers

**Dataset Value**:
- **Churn prediction**: Identify users likely to stop playing
- **LTV (Lifetime Value) prediction**: Estimate future revenue per user
- **Conversion prediction**: Who will make in-app purchases?
- **Fraud detection**: Anomalous patterns indicating fraud

**Training Dataset Features**:
```
Features (from dataset):
- Session frequency, duration, recency
- Ad engagement metrics (CTR, dwell time, engagement score)
- Device characteristics
- Geo/temporal patterns
- Game progression indicators

Labels (outcomes to predict):
- Binary: Will user purchase? (from IAP table)
- Binary: Will user install advertised app? (from attributed_installs)
- Continuous: How much will user spend? (from IAP.AMOUNT_INVOICEABLE)
- Time-to-event: Days until churn/purchase
```

**Pricing Potential**: $25K - $100K per industry vertical

#### Use Case 1C: Fraud Detection Models
**Buyer Profile**: Mastercard, Visa, fraud prevention vendors (Sift, Forter)

**Dataset Value**:
- **Click fraud patterns**: Impossible click sequences, timing anomalies
- **Install fraud patterns**: Datacenter IPs, device farm signatures
- **Payment fraud patterns**: Failed IAP attempts, unusual purchase patterns
- **Bot detection**: Inhuman interaction speeds and patterns

**Training Features**:
- Inter-event timing (clicks too fast = bot)
- IP address patterns (datacenter detection)
- Device fingerprint analysis
- Session behavior anomalies
- Interaction depth (bots don't engage deeply)

**Pricing Potential**: $75K - $250K (fraud data commands premium pricing)

---

### 2. Energy & Infrastructure Planning

#### Use Case 2A: Electricity Demand Forecasting
**Buyer Profile**: Utility companies, grid operators, energy traders

**Key Insight**: Gaming generates **predictable, large-scale electricity demand**

**Dataset Value**:
- **Temporal usage patterns**: 
  - Peak gaming hours (evenings, weekends)
  - Seasonal variations (more gaming in winter)
  - Event-driven spikes (new game launches)
- **Geographic distribution**: 
  - City/region level gaming activity
  - Device type distribution (phones vs tablets = different power draw)
- **Demographic proxies**: 
  - Age groups (inferred from games played)
  - Behavioral patterns indicating household composition

**Specific Energy Applications**:

1. **Load Forecasting**:
```
Gaming Activity → Device Power Consumption → Aggregate Demand

Example calculation:
- 100K active users in city X
- 70% on phones (3-5W), 30% on tablets (5-8W)
- Peak gaming: 7-11 PM
- Forecast: +500-800 kW demand spike during peak
```

2. **Grid Planning**:
- Identify neighborhoods with high gaming activity (infrastructure upgrades needed)
- Predict demand growth from mobile gaming adoption
- Plan battery storage deployment for peak shaving

3. **Demand Response Programs**:
- Incentivize gaming during off-peak hours
- Targeted programs for high-consumption areas

4. **Energy Trading**:
- Predict short-term demand spikes
- Optimize trading strategies around gaming patterns

**Pricing Potential**: $100K - $500K per region/market

**Unique Advantage**: **This is hidden demand signal that utilities don't typically have access to!**

---

### 3. Market Research & Consumer Insights

#### Use Case 3A: Gaming Industry Analytics
**Buyer Profile**: Game publishers, studios, platform holders (Apple, Google, Tencent)

**Dataset Value**:
- **Competitive intelligence**: 
  - Which games monetize best?
  - What ad formats drive engagement?
  - Cross-game user migration patterns
- **Market sizing**: 
  - Genre popularity by geography
  - Device platform trends (iOS vs Android)
  - Price sensitivity analysis
- **User acquisition strategies**:
  - Which campaigns drive highest-quality users?
  - Creative strategies that work
  - Attribution model effectiveness

**Specific Applications**:
- **Benchmarking**: How does my game's monetization compare to market?
- **User persona development**: What types of players exist? How do they behave?
- **Market entry analysis**: Should I launch in market X? What monetization to expect?
- **Competitive positioning**: Where are gaps in the market?

**Pricing Potential**: $30K - $150K per report/dataset

#### Use Case 3B: Advertising Effectiveness Research
**Buyer Profile**: Ad agencies, brand marketers, ad tech platforms

**Dataset Value**:
- **In-game advertising effectiveness**:
  - Engagement metrics by creative type
  - Optimal ad frequency and timing
  - Format performance (banner vs video vs rewarded)
- **Attribution insights**:
  - Click-through rates by vertical
  - Install rates by campaign type
  - View-through vs click-through effectiveness
- **Creative analysis**:
  - Which creative elements drive engagement?
  - Ad fatigue patterns
  - Contextual relevance impact

**Pricing Potential**: $50K - $200K per study

---

### 4. Financial Services & Consumer Analytics

#### Use Case 4A: Consumer Spending Behavior Models
**Buyer Profile**: Banks, credit card companies, fintech startups

**Dataset Value**:
- **Micro-transaction behavior**: 
  - IAP table shows real purchase decisions and failures
  - Price sensitivity (what prices do people accept/reject?)
  - Payment failure patterns
- **Spending propensity**:
  - Who makes purchases vs who doesn't?
  - Early indicators of purchasing behavior
  - Impulse buying vs planned purchases
- **Financial health signals**:
  - Failed purchases → potential financial stress
  - Purchase abandonment patterns
  - Currency/region-specific behaviors

**Specific Applications**:

1. **Credit Risk Modeling**:
- Frequent IAP failures → potential financial stress indicator
- Spending patterns correlated with creditworthiness
- Predictive signal for loan default risk

2. **Targeted Product Recommendations**:
- High IAP users → target for credit cards with rewards
- Failed purchase users → target for buy-now-pay-later (BNPL) products
- Geographic spending patterns → regional product optimization

3. **Fraud Detection**:
- Unusual purchase patterns
- Cross-device payment behavior
- Geographic anomalies

**Pricing Potential**: $50K - $300K per application

#### Use Case 4B: Propensity-to-Purchase Modeling
**Buyer Profile**: E-commerce platforms, retail analytics firms

**Dataset Value**:
- **Conversion funnel insights**: What leads to purchase?
- **Abandonment analysis**: Why do 95% of IAP attempts fail?
- **Re-engagement strategies**: Can failed purchasers be recovered?

**Training Labels**:
- Binary: Purchase made vs abandoned
- Time-to-conversion
- Purchase amount
- Repeat purchase likelihood

**Pricing Potential**: $40K - $150K per model/industry

---

### 5. Telecommunications & Network Planning

#### Use Case 5A: Network Capacity Planning
**Buyer Profile**: Mobile carriers (Verizon, AT&T, T-Mobile, Vodafone)

**Dataset Value**:
- **Data usage patterns**:
  - Gaming generates significant mobile data traffic
  - Predictable temporal patterns (peak hours)
  - Geographic hotspots (where users game most)
- **Device capabilities**:
  - What devices are popular? (network requirements differ)
  - OS distribution (affects network protocols)
- **Connection type preferences**:
  - WiFi vs cellular usage patterns
  - Quality requirements for gaming

**Specific Applications**:

1. **Cell Tower Capacity Planning**:
- Identify high-gaming areas (need more capacity)
- Predict future demand from device adoption trends
- Optimize tower placement for gaming traffic

2. **Network Optimization**:
- Prioritize gaming traffic during peak hours
- QoS policies informed by usage patterns
- Latency-sensitive application detection

3. **5G Rollout Strategy**:
- Target gamers first (high-value users)
- Identify markets with most gaming demand
- Calculate ROI of 5G deployment by area

**Pricing Potential**: $75K - $400K per network operator

---

### 6. Advertising Technology (AdTech) Industry

#### Use Case 6A: AdTech Platform Benchmarking
**Buyer Profile**: DSPs, SSPs, ad exchanges, MMPs (Adjust, AppsFlyer, Branch)

**Dataset Value**:
- **Fill rate benchmarks**: What's a good fill rate by geo/device/game?
- **CPM benchmarks**: Am I paying competitive prices?
- **Exchange performance**: Which exchanges fill best?
- **Attribution performance**: How do different MMPs perform?

**Specific Applications**:
- Competitive positioning ("Our fill rates are top quartile")
- Sales enablement (show prospects industry benchmarks)
- Product optimization (improve to match/beat benchmarks)
- Pricing strategies (informed by market rates)

**Pricing Potential**: $30K - $100K per platform (recurring annual subscriptions)

#### Use Case 6B: Fraud Detection & Prevention
**Buyer Profile**: Fraud detection vendors (Pixalate, Integral Ad Science, DoubleVerify)

**Dataset Value**:
- **Fraud patterns**:
  - Click fraud signatures
  - Install fraud patterns (datacenter IPs, device farms)
  - Ad stacking/hiding patterns
  - Bot behavior signatures
- **Clean vs fraudulent traffic**:
  - Labeled examples for training
  - Geographic fraud hotspots
  - Device fraud patterns

**Pricing Potential**: $100K - $500K (fraud data is premium-priced due to scarcity)

---

### 7. Academic & Research Institutions

#### Use Case 7A: Behavioral Economics Research
**Buyer Profile**: Universities, research labs, think tanks

**Research Questions**:
- How do digital natives make purchase decisions?
- What drives micro-transaction behavior?
- Attention economics in gaming environments
- Privacy attitudes (consent patterns in GDPR fields)
- Cross-cultural differences in gaming behavior

**Dataset Value**:
- Large-scale behavioral data (can't be replicated in lab)
- Real-world decisions with real money
- Longitudinal tracking (see behavior change over time)
- Cross-cultural representation

**Pricing Potential**: $10K - $50K per research project (lower prices but high volume potential)

---

### 8. Government & Policy Applications

#### Use Case 8A: Economic Indicators & Consumer Confidence
**Buyer Profile**: Central banks, economic research departments, Treasury departments

**Dataset Value**:
- **Real-time economic indicators**:
  - Micro-transaction velocity → consumer spending health
  - Failed purchase rate → financial stress indicator
  - Gaming engagement → leisure time availability
- **Geographic economic health**:
  - Spending patterns by region
  - Early warning signals for economic downturns
- **Digital economy measurement**:
  - Mobile gaming as GDP component
  - Cross-border digital transactions

**Pricing Potential**: $50K - $300K per government agency

#### Use Case 8B: Youth & Screen Time Policy Research
**Buyer Profile**: Health departments, education ministries, child welfare agencies

**Dataset Value**:
- Gaming engagement patterns by age group (inferred from games)
- Ad exposure intensity for different demographics
- In-app purchase behavior (child spending concerns)
- Time-of-day usage patterns (late-night gaming)

**Pricing Potential**: $20K - $100K per policy study

---

## Unique Dataset Advantages for AI/ML Training

### 1. **Sequential Behavioral Data**
Most datasets are cross-sectional. This dataset captures **user journeys over time**:
- Session → ad exposure → click → install → engagement → purchase
- Multiple sessions per user (repeat behavior patterns)
- Attribution chains (cause → effect with time lag)

**Value for ML**: Train sequence models (LSTMs, Transformers) that understand temporal patterns.

### 2. **Natural Experiment Structure**
Users are randomly exposed to different ads/campaigns → **natural A/B test at scale**:
- Treatment group: Saw ad
- Control group: Didn't see ad
- Outcome: Install, purchase, engagement

**Value for ML**: Causal inference, uplift modeling, treatment effect estimation.

### 3. **Multi-Table Relational Structure**
Not flat CSV - **rich relational data** across 6 tables:
- Train models to do JOIN predictions (which impression leads to purchase?)
- Graph neural networks (users → games → campaigns → purchases)
- Multi-task learning (predict clicks AND installs AND purchases simultaneously)

**Value for ML**: More sophisticated model architectures, better transfer learning.

### 4. **Failure Data**
95% of IAP attempts fail! Most datasets only show successes. This shows **both success and failure**:
- What leads to purchase failure?
- Can we recover failed purchasers?
- What differentiates success from failure?

**Value for ML**: Imbalanced learning, failure mode analysis, recovery strategies.

### 5. **Privacy-Compliant Yet Rich**
**ANON_DEVICE_ID** enables longitudinal tracking WITHOUT exposing PII:
- Track users over time
- Link behavior across sessions/games
- No GDPR/CCPA violations

**Value for ML**: Can train on real user journeys without privacy concerns.

---

## Pricing Strategy Recommendations

### Tier 1: Raw Data Access
- **Target**: Large tech companies, research institutions
- **Product**: Full dataset access (all 6 tables, historical + ongoing)
- **Pricing**: $200K - $1M per year
- **Volume**: 5-10 buyers globally

### Tier 2: Aggregated Insights & Benchmarks
- **Target**: Mid-sized companies, ad tech platforms
- **Product**: Pre-aggregated reports, benchmarks, anonymized cohort analysis
- **Pricing**: $50K - $200K per year
- **Volume**: 50-100 buyers globally

### Tier 3: Specific Use Case Datasets
- **Target**: Specialized buyers (energy companies, financial services)
- **Product**: Custom extracts tailored to use case
- **Pricing**: $30K - $150K per delivery
- **Volume**: 100-500 buyers globally

### Tier 4: API Access for Real-Time Insights
- **Target**: Ad tech platforms, fraud detection services
- **Product**: API queries against dataset
- **Pricing**: $10K - $50K per year + usage fees
- **Volume**: 200-1000 buyers globally

---

## Competitive Positioning

### What Makes This Dataset Unique?

1. **In-Game Advertising**: Most datasets focus on web/mobile ads, not in-game
2. **Complete Attribution Chain**: Impression → click → install → purchase (rare to have all links)
3. **Cross-Game Visibility**: See users across multiple games (network effects)
4. **IAP + Ad Revenue**: Both monetization streams (most datasets show only one)
5. **Failed Transactions**: Shows attempts, not just successes (behavioral insights)
6. **Device-Level Longitudinal**: Track same user over months/years

### Competitive Datasets (and how Adinmo data is better)

| Dataset | What They Have | What Adinmo Adds |
|---------|----------------|------------------|
| **AdTech Click Logs** | Impressions, clicks | In-game context, attribution to purchases |
| **Mobile App Analytics** | App usage, sessions | Ad exposure, cross-app visibility |
| **Attribution Platforms** | Install attribution | Pre-install behavior, organic monetization |
| **IAP Transaction Logs** | Purchase data | Ad influence, failed purchases, full user journey |
| **Energy Consumption Data** | Aggregate usage | Behavioral drivers of usage |

---

## Risk Mitigation & Compliance

### Privacy Considerations
- **ANON_DEVICE_ID**: Already anonymized (not raw IDFA/GAID)
- **Redacted PII**: IP, email, precise geo already removed in sample
- **GDPR Compliance**: Consent flags present, can filter to consented users only
- **COPPA Compliance**: Child flags present, can exclude child-directed traffic

### Data Security
- **Encryption**: At rest and in transit
- **Access Controls**: Buyer-specific credentials, audit logs
- **Data Retention**: Clear policies on how long buyers can store
- **Usage Restrictions**: Contractual limits on data use (no re-identification)

### Competitive Sensitivity
- **Anonymize Game IDs**: Don't reveal specific game performance
- **Aggregate Small Segments**: Prevent identification of specific games
- **Delay Real-Time Data**: Historical data only (30-90 day lag)

---

## Go-To-Market Strategy

### Phase 1: Pilot Customers (Months 1-6)
- **Target**: 3-5 friendly customers from different verticals
- **Pricing**: 50% discount for early adopters
- **Goal**: Validate use cases, gather testimonials, refine product
- **Industries**: Energy (1), ML platform (1), AdTech (1), Gaming (1), Finance (1)

### Phase 2: Industry Expansion (Months 7-12)
- **Target**: 20-30 customers across 8 industries
- **Pricing**: Standard pricing
- **Goal**: Establish market presence, generate case studies
- **Focus**: High-value use cases with clear ROI

### Phase 3: Scale (Year 2+)
- **Target**: 100+ customers globally
- **Product**: Tiered offerings (raw data, insights, API)
- **Goal**: Become industry-standard gaming behavioral dataset
- **Channels**: Direct sales, partnerships, data marketplaces (AWS, Snowflake)

---

## Conclusion

The Adinmo dataset represents a **rare combination of scale, richness, and longitudinal depth** that commands premium pricing in data markets. The key to maximizing value is:

1. **Position as ML training data** (highest willingness-to-pay)
2. **Target non-obvious buyers** (energy companies, financial services - less competition)
3. **Emphasize unique advantages** (longitudinal, cross-game, attribution chain)
4. **Package creatively** (raw data + aggregated insights + API)
5. **Build recurring revenue** (annual subscriptions, not one-time sales)

**Revenue Potential**: $5M - $25M annually at scale (100-200 customers × $50K-$200K average)

