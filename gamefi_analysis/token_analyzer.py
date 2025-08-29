# token_analyzer.py - AI-powered GameFi token analysis
import ollama
import json
from typing import Dict, List

class GameFiTokenAnalyzer:
    def __init__(self, ollama_host, model_name):
        self.client = ollama.Client(host=ollama_host)
        self.model = model_name
        
    def analyze_token_sustainability(self, token_data: Dict) -> Dict:
        """
        Analyze GameFi token sustainability using Ollama AI
        Returns: Comprehensive sustainability assessment
        """
        
        # Prepare data for AI analysis
        analysis_prompt = self._create_analysis_prompt(token_data)
        
        # Get AI analysis
        response = self.client.chat(
            model=self.model,
            messages=[{
                'role': 'user',
                'content': analysis_prompt
            }]
        )
        
        # Parse and structure the response
        analysis_result = self._parse_ai_response(response['message']['content'])
        
        # Add quantitative scoring
        analysis_result['sustainability_score'] = self._calculate_sustainability_score(token_data)
        analysis_result['risk_factors'] = self._identify_risk_factors(token_data)
        
        return analysis_result
    
    def _create_analysis_prompt(self, token_data: Dict) -> str:
        """Create detailed prompt for AI analysis"""
        
        price_data = token_data['price_history']
        supply_data = token_data['supply_metrics']
        gaming_data = token_data['gaming_metrics']
        
        prompt = f"""
        Analyze this GameFi token's economic sustainability:

        PRICE METRICS:
        - Current price: ${price_data['price'].iloc[-1]:.4f}
        - 30-day change: {((price_data['price'].iloc[-1] / price_data['price'].iloc[0]) - 1) * 100:.2f}%
        - Average daily volume: ${price_data['volume'].mean():,.2f}
        - Price volatility: {price_data['price'].std():.4f}

        SUPPLY METRICS:
        - Total supply: {supply_data['total_supply']:,}
        - Circulating supply: {supply_data['circulating_supply']:,}
        - Daily emissions: {supply_data['daily_emissions']:,}
        - Staked tokens: {supply_data['staked_tokens']:,}
        - Treasury balance: {supply_data['treasury_balance']:,}

        GAMING METRICS:
        - Daily active users: {gaming_data['daily_active_users']:,}
        - Monthly active users: {gaming_data['monthly_active_users']:,}
        - 7-day retention: {gaming_data['user_retention_7d']*100:.1f}%
        - 30-day retention: {gaming_data['user_retention_30d']*100:.1f}%
        - Tokens earned per hour: {gaming_data['tokens_earned_per_hour']}

        Provide analysis covering:
        1. Economic sustainability outlook (1-5 score)
        2. Key strengths and weaknesses
        3. Inflationary/deflationary balance
        4. Player retention impact on token demand
        5. Treasury runway assessment
        6. Recommended monitoring metrics
        7. Risk mitigation suggestions

        Format response as structured analysis with clear sections.
        """
        
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> Dict:
        """Parse AI response into structured data"""
        
        # This is a simplified parser - in production, you'd want more robust parsing
        sections = response_text.split('\n\n')
        
        parsed_response = {
            'overall_assessment': '',
            'sustainability_outlook': '',
            'key_strengths': [],
            'key_weaknesses': [],
            'recommendations': [],
            'raw_analysis': response_text
        }
        
        # Extract structured information from AI response
        for section in sections:
            if 'sustainability' in section.lower():
                parsed_response['sustainability_outlook'] = section
            elif 'strength' in section.lower():
                parsed_response['key_strengths'] = self._extract_bullet_points(section)
            elif 'weakness' in section.lower() or 'risk' in section.lower():
                parsed_response['key_weaknesses'] = self._extract_bullet_points(section)
            elif 'recommend' in section.lower():
                parsed_response['recommendations'] = self._extract_bullet_points(section)
        
        return parsed_response
    
    def _extract_bullet_points(self, text: str) -> List[str]:
        """Extract bullet points from text"""
        lines = text.split('\n')
        bullet_points = []
        
        for line in lines:
            line = line.strip()
            if line.startswith(('-', '•', '*', '1.', '2.', '3.', '4.', '5.')):
                bullet_points.append(line[2:].strip())
        
        return bullet_points
    
    def _calculate_sustainability_score(self, token_data: Dict) -> float:
        """Calculate quantitative sustainability score (0-100)"""
        
        supply_data = token_data['supply_metrics']
        gaming_data = token_data['gaming_metrics']
        price_data = token_data['price_history']
        
        # Supply health score (0-25)
        supply_ratio = supply_data['circulating_supply'] / supply_data['total_supply']
        supply_score = min(25, (1 - supply_ratio) * 50)
        
        # User engagement score (0-25)
        retention_score = (gaming_data['user_retention_7d'] + gaming_data['user_retention_30d']) * 50
        
        # Treasury sustainability score (0-25)
        daily_cost = supply_data['daily_emissions'] * price_data['price'].iloc[-1]
        treasury_value = supply_data['treasury_balance'] * price_data['price'].iloc[-1]
        runway_days = treasury_value / daily_cost if daily_cost > 0 else 365
        treasury_score = min(25, (runway_days / 365) * 25)
        
        # Price stability score (0-25)
        volatility = price_data['price'].std() / price_data['price'].mean()
        stability_score = max(0, 25 - (volatility * 100))
        
        total_score = supply_score + retention_score + treasury_score + stability_score
        
        return min(100, max(0, total_score))
    
    def _identify_risk_factors(self, token_data: Dict) -> List[Dict]:
        """Identify specific risk factors with severity ratings"""
        
        risks = []
        supply_data = token_data['supply_metrics']
        gaming_data = token_data['gaming_metrics']
        
        # High inflation risk
        inflation_rate = (supply_data['daily_emissions'] * 365) / supply_data['circulating_supply']
        if inflation_rate > 0.5:  # 50% annual inflation
            risks.append({
                'factor': 'High Token Inflation',
                'severity': 'High',
                'description': f'Annual inflation rate of {inflation_rate*100:.1f}% may devalue tokens'
            })
        
        # Low user retention risk
        if gaming_data['user_retention_30d'] < 0.2:  # Less than 20% retention
            risks.append({
                'factor': 'Poor User Retention',
                'severity': 'Medium',
                'description': f'30-day retention of {gaming_data["user_retention_30d"]*100:.1f}% indicates engagement issues'
            })
        
        # Treasury depletion risk
        daily_cost = supply_data['daily_emissions'] * token_data['price_history']['price'].iloc[-1]
        treasury_value = supply_data['treasury_balance'] * token_data['price_history']['price'].iloc[-1]
        runway_days = treasury_value / daily_cost if daily_cost > 0 else 365
        
        if runway_days < 180:  # Less than 6 months runway
            risks.append({
                'factor': 'Treasury Depletion',
                'severity': 'Critical',
                'description': f'Treasury runway of {runway_days:.0f} days requires immediate attention'
            })
        
        return risks

# Usage example
analyzer = GameFiTokenAnalyzer(OLLAMA_HOST, OLLAMA_MODEL)
analysis_result = analyzer.analyze_token_sustainability(token_data)


