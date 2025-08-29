# report_generator.py - Generate comprehensive GameFi analysis reports
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pandas as pd

class GameFiReportGenerator:
    def __init__(self, analyzer, simulator):
        self.analyzer = analyzer
        self.simulator = simulator
        
    def generate_full_report(self, token_data: Dict, output_path: str = None) -> str:
        """Generate comprehensive GameFi token analysis report"""
        
        # Get AI analysis
        ai_analysis = self.analyzer.analyze_token_sustainability(token_data)
        
        # Run economics simulation
        simulation_results = self.simulator.simulate_earnings_distribution()
        sustainability_analysis = self.simulator.analyze_economic_sustainability(
            token_data['supply_metrics']['treasury_balance'], 
            simulation_results
        )
        
        # Generate report sections
        report_sections = {
            'executive_summary': self._create_executive_summary(ai_analysis, sustainability_analysis),
            'token_metrics': self._analyze_token_metrics(token_data),
            'economic_model': self._analyze_economic_model(simulation_results, sustainability_analysis),
            'risk_assessment': self._create_risk_assessment(ai_analysis['risk_factors']),
            'recommendations': self._compile_recommendations(ai_analysis, sustainability_analysis),
            'monitoring_dashboard': self._create_monitoring_metrics(token_data)
        }
        
        # Combine into full report
        full_report = self._format_report(report_sections)
        
        # Save report if path provided
        if output_path:
            with open(output_path, 'w') as f:
                f.write(full_report)
        
        return full_report
    
    def _create_executive_summary(self, ai_analysis: Dict, sustainability: Dict) -> str:
        """Create executive summary with key findings"""
        
        sustainability_score = ai_analysis['sustainability_score']
        runway_days = sustainability['treasury_runway_days']
        status = sustainability['sustainability_status']
        
        summary = f"""
## Executive Summary

**Sustainability Score: {sustainability_score:.1f}/100**
**Treasury Runway: {runway_days:.0f} days**
**Overall Status: {status}**

### Key Findings:

**Economic Health:**
- The token shows a sustainability score of {sustainability_score:.1f}/100
- Treasury runway provides {runway_days:.0f} days of current emission rates
- Daily emission cost: ${sustainability['daily_emission_cost_usd']:,.2f}

**Critical Insights:**
{ai_analysis['sustainability_outlook']}

**Immediate Actions Required:**
"""
        
        # Add top 3 recommendations
        top_recommendations = sustainability['recommended_actions'][:3]
        for i, rec in enumerate(top_recommendations, 1):
            summary += f"\n{i}. {rec}"
        
        return summary
    
    def _analyze_token_metrics(self, token_data: Dict) -> str:
        """Analyze core token metrics"""
        
        supply_data = token_data['supply_metrics']
        gaming_data = token_data['gaming_metrics']
        price_data = token_data['price_history']
        
        # Calculate key ratios
        circulation_ratio = supply_data['circulating_supply'] / supply_data['total_supply']
        staking_ratio = supply_data['staked_tokens'] / supply_data['circulating_supply']
        inflation_rate = (supply_data['daily_emissions'] * 365) / supply_data['circulating_supply']
        
        metrics_analysis = f"""
## Token Metrics Analysis

### Supply Dynamics
- **Total Supply:** {supply_data['total_supply']:,} tokens
- **Circulating Supply:** {supply_data['circulating_supply']:,} tokens ({circulation_ratio:.1%})
- **Staked Tokens:** {supply_data['staked_tokens']:,} tokens ({staking_ratio:.1%})
- **Daily Emissions:** {supply_data['daily_emissions']:,} tokens
- **Annual Inflation Rate:** {inflation_rate:.1%}

### Price Performance
- **Current Price:** ${price_data['price'].iloc[-1]:.4f}
- **30-Day Change:** {((price_data['price'].iloc[-1] / price_data['price'].iloc[0]) - 1) * 100:.2f}%
- **Average Daily Volume:** ${price_data['volume'].mean():,.2f}
- **Price Volatility:** {(price_data['price'].std() / price_data['price'].mean()) * 100:.1f}%

### Gaming Metrics
- **Daily Active Users:** {gaming_data['daily_active_users']:,}
- **7-Day Retention:** {gaming_data['user_retention_7d']*100:.1f}%
- **30-Day Retention:** {gaming_data['user_retention_30d']*100:.1f}%
- **Tokens Earned Per Hour:** {gaming_data['tokens_earned_per_hour']}
"""
        
        return metrics_analysis
    
    def _analyze_economic_model(self, simulation_results: Dict, sustainability: Dict) -> str:
        """Analyze the play-to-earn economic model"""
        
        avg_emissions = simulation_results['average_daily_emissions']
        peak_emissions = simulation_results['peak_daily_emissions']
        retention_rate = simulation_results['player_retention_rate']
        
        economic_analysis = f"""
## Economic Model Analysis

### Emission Dynamics
- **Average Daily Emissions:** {avg_emissions:,.0f} tokens
- **Peak Daily Emissions:** {peak_emissions:,.0f} tokens
- **Total Tokens Earned (30d):** {simulation_results['total_tokens_earned']:,.0f}
- **Player Retention Rate:** {retention_rate:.1%}

### Sustainability Metrics
- **Treasury Runway:** {sustainability['treasury_runway_days']:.0f} days
- **Daily Cost (USD):** ${sustainability['daily_emission_cost_usd']:,.2f}
- **Required Revenue per User:** ${sustainability['required_revenue_per_user_daily']:.2f}/day

### Economic Balance Assessment
The current economic model shows {'sustainable' if sustainability['treasury_runway_days'] > 365 else 'unsustainable'} characteristics.
Key factors influencing sustainability:

1. **Token Emission Rate:** {'High' if avg_emissions > 1000000 else 'Moderate' if avg_emissions > 100000 else 'Low'} daily emissions
2. **Player Retention:** {'Strong' if retention_rate > 0.7 else 'Moderate' if retention_rate > 0.4 else 'Weak'} retention rates
3. **Treasury Management:** {'Healthy' if sustainability['treasury_runway_days'] > 365 else 'Critical'} runway duration
"""
        
        return economic_analysis
    
    def _create_risk_assessment(self, risk_factors: List[Dict]) -> str:
        """Create detailed risk assessment section"""
        
        risk_section = """
## Risk Assessment

### Identified Risk Factors
"""
        
        for risk in risk_factors:
            risk_section += f"""
**{risk['factor']}** - {risk['severity']} Risk
- {risk['description']}
"""
        
        # Add general risk categories
        risk_section += """
### Risk Mitigation Strategies

**Economic Risks:**
- Monitor token emission rates weekly
- Implement dynamic reward adjustments
- Maintain 6+ month treasury runway

**User Engagement Risks:**
- Track retention metrics daily
- Implement player feedback systems
- Regular gameplay balance updates

**Market Risks:**
- Diversify treasury holdings
- Implement token burning mechanisms
- Monitor competitor strategies
"""
        
        return risk_section
    
    def _compile_recommendations(self, ai_analysis: Dict, sustainability: Dict) -> str:
        """Compile actionable recommendations"""
        
        recommendations_section = """
## Strategic Recommendations

### Immediate Actions (0-30 days)
"""
        
        # Add immediate recommendations
        immediate_actions = sustainability['recommended_actions'][:3]
        for action in immediate_actions:
            recommendations_section += f"- {action}\n"
        
        recommendations_section += """
### Medium-term Strategies (1-6 months)
"""
        
        # Add AI recommendations
        ai_recommendations = ai_analysis.get('recommendations', [])
        for rec in ai_recommendations[:3]:
            recommendations_section += f"- {rec}\n"
        
        recommendations_section += """
### Long-term Development (6+ months)
- Develop additional revenue streams beyond token sales
- Expand gaming ecosystem with new features
- Build strategic partnerships with other GameFi projects
- Implement governance mechanisms for community input
"""
        
        return recommendations_section
    
    def _create_monitoring_metrics(self, token_data: Dict) -> str:
        """Create monitoring dashboard specifications"""
        
        monitoring_section = """
## Monitoring Dashboard Metrics

### Daily Tracking Metrics
- Active user count and retention rates
- Token emission volumes and treasury balance
- Price performance and trading volumes
- Player engagement and session duration

### Weekly Analysis Metrics  
- User acquisition and churn rates
- Token distribution and staking ratios
- Revenue per user and lifetime value
- Competitor performance benchmarks

### Monthly Strategic Reviews
- Economic model sustainability assessment
- Risk factor evaluation and mitigation
- Strategic initiative performance
- Market positioning and opportunity analysis

### Alert Thresholds
- Treasury runway < 180 days: **Critical Alert**
- 7-day retention < 25%: **High Priority**
- Daily active users decline > 20%: **Medium Priority**
- Token price volatility > 50%: **Monitor Closely**
"""
        
        return monitoring_section
    
    def _format_report(self, sections: Dict) -> str:
        """Format all sections into final report"""
        
        report_header = f"""
# GameFi Token Analysis Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Analysis Framework:** Ollama AI + Economic Simulation

---
"""
        
        full_report = report_header
        
        # Add each section
        for section_name, section_content in sections.items():
            full_report += section_content + "\n\n---\n\n"
        
        # Add footer
        full_report += """
## Disclaimer
This analysis is for informational purposes only and should not be considered financial advice. 
GameFi investments carry significant risks. Always conduct your own research and consult with 
financial professionals before making investment decisions.

**Report generated using Ollama AI and proprietary GameFi analysis algorithms.**
"""
        
        return full_report

# Generate comprehensive report
report_generator = GameFiReportGenerator(analyzer, simulator)
full_report = report_generator.generate_full_report(token_data, 'gamefi_analysis_report.md')
print("Report generated successfully!")


