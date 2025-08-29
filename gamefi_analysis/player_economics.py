# player_economics.py - Play-to-earn economics modeling
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class PlayerProfile:
    skill_level: float  # 0.0 to 1.0
    time_investment: float  # hours per day
    risk_tolerance: float  # 0.0 to 1.0
    retention_probability: float  # 0.0 to 1.0

class PlayToEarnSimulator:
    def __init__(self, token_price: float, base_earning_rate: float):
        self.token_price = token_price
        self.base_earning_rate = base_earning_rate  # tokens per hour
        self.player_profiles = []
        
    def add_player_cohort(self, profile: PlayerProfile, count: int):
        """Add a cohort of players with similar characteristics"""
        for _ in range(count):
            # Add some variance to the profile
            varied_profile = PlayerProfile(
                skill_level=max(0, min(1, profile.skill_level + np.random.normal(0, 0.1))),
                time_investment=max(0.5, profile.time_investment + np.random.normal(0, 0.5)),
                risk_tolerance=max(0, min(1, profile.risk_tolerance + np.random.normal(0, 0.1))),
                retention_probability=max(0, min(1, profile.retention_probability + np.random.normal(0, 0.05)))
            )
            self.player_profiles.append(varied_profile)
    
    def simulate_earnings_distribution(self, days: int = 30) -> Dict:
        """Simulate token earnings across player base"""
        
        daily_earnings = []
        active_players = []
        total_tokens_earned = 0
        
        for day in range(days):
            day_earnings = 0
            day_active = 0
            
            for player in self.player_profiles:
                # Check if player is still active (simplified retention model)
                if np.random.random() < player.retention_probability:
                    # Calculate daily earnings for this player
                    skill_multiplier = 0.5 + (player.skill_level * 1.5)  # 0.5x to 2.0x multiplier
                    time_factor = player.time_investment
                    
                    player_daily_tokens = (
                        self.base_earning_rate * 
                        skill_multiplier * 
                        time_factor *
                        np.random.uniform(0.8, 1.2)  # Daily variance
                    )
                    
                    day_earnings += player_daily_tokens
                    day_active += 1
                    total_tokens_earned += player_daily_tokens
            
            daily_earnings.append(day_earnings)
            active_players.append(day_active)
        
        return {
            'daily_token_emissions': daily_earnings,
            'active_players': active_players,
            'total_tokens_earned': total_tokens_earned,
            'average_daily_emissions': np.mean(daily_earnings),
            'peak_daily_emissions': max(daily_earnings),
            'player_retention_rate': np.mean(active_players) / len(self.player_profiles)
        }
    
    def analyze_economic_sustainability(self, treasury_tokens: float, simulation_results: Dict) -> Dict:
        """Analyze if the economic model is sustainable"""
        
        daily_emissions = simulation_results['average_daily_emissions']
        treasury_runway_days = treasury_tokens / daily_emissions if daily_emissions > 0 else float('inf')
        
        # Calculate required token price appreciation to maintain sustainability
        current_daily_cost_usd = daily_emissions * self.token_price
        
        # Estimate required revenue per user to break even
        active_players = simulation_results['player_retention_rate'] * len(self.player_profiles)
        required_revenue_per_user = current_daily_cost_usd / active_players if active_players > 0 else 0
        
        sustainability_analysis = {
            'treasury_runway_days': treasury_runway_days,
            'daily_emission_cost_usd': current_daily_cost_usd,
            'required_revenue_per_user_daily': required_revenue_per_user,
            'sustainability_status': self._assess_sustainability(treasury_runway_days, required_revenue_per_user),
            'recommended_actions': self._generate_recommendations(treasury_runway_days, required_revenue_per_user)
        }
        
        return sustainability_analysis
    
    def _assess_sustainability(self, runway_days: float, revenue_per_user: float) -> str:
        """Assess overall sustainability status"""
        
        if runway_days < 90:
            return "Critical - Immediate action required"
        elif runway_days < 180:
            return "High Risk - Monitor closely"
        elif revenue_per_user > 5.0:  # $5+ per user per day
            return "Unsustainable - Revenue model needed"
        elif runway_days > 365:
            return "Healthy - Long-term sustainable"
        else:
            return "Moderate Risk - Optimization needed"
    
    def _generate_recommendations(self, runway_days: float, revenue_per_user: float) -> List[str]:
        """Generate specific recommendations based on analysis"""
        
        recommendations = []
        
        if runway_days < 180:
            recommendations.append("Reduce token emission rates by 20-30%")
            recommendations.append("Implement token burning mechanisms")
            recommendations.append("Seek additional treasury funding")
        
        if revenue_per_user > 3.0:
            recommendations.append("Introduce premium features or NFT sales")
            recommendations.append("Implement tournament entry fees")
            recommendations.append("Add advertising revenue streams")
        
        if runway_days > 365 and revenue_per_user < 1.0:
            recommendations.append("Consider increasing reward rates to attract players")
            recommendations.append("Expand marketing to grow player base")
        
        return recommendations

# Example usage with different player types
simulator = PlayToEarnSimulator(token_price=0.15, base_earning_rate=25)

# Add different player cohorts
casual_players = PlayerProfile(skill_level=0.3, time_investment=1.5, risk_tolerance=0.4, retention_probability=0.6)
simulator.add_player_cohort(casual_players, 5000)

hardcore_players = PlayerProfile(skill_level=0.8, time_investment=6.0, risk_tolerance=0.7, retention_probability=0.85)
simulator.add_player_cohort(hardcore_players, 1000)

intermediate_players = PlayerProfile(skill_level=0.5, time_investment=3.0, risk_tolerance=0.5, retention_probability=0.7)
simulator.add_player_cohort(intermediate_players, 3000)

# Run simulation
results = simulator.simulate_earnings_distribution(30)
sustainability = simulator.analyze_economic_sustainability(50000000, results)

print(f"Treasury runway: {sustainability['treasury_runway_days']:.0f} days")
print(f"Daily cost: ${sustainability['daily_emission_cost_usd']:,.2f}")
print(f"Status: {sustainability['sustainability_status']}")


