# Quick analysis script for any GameFi token
def quick_gamefi_analysis(token_symbol: str):
    """Perform rapid GameFi token assessment"""
    
    # Collect data
    token_data = collector.fetch_token_metrics(token_symbol)
    
    # AI analysis
    analysis = analyzer.analyze_token_sustainability(token_data)
    
    # Economic simulation
    sim_results = simulator.simulate_earnings_distribution()
    sustainability = simulator.analyze_economic_sustainability(
        token_data['supply_metrics']['treasury_balance'], sim_results
    )
    
    # Quick assessment
    print(f"\n=== {token_symbol.upper()} Quick Analysis ===")
    print(f"Sustainability Score: {analysis['sustainability_score']:.1f}/100")
    print(f"Treasury Runway: {sustainability['treasury_runway_days']:.0f} days")
    print(f"Status: {sustainability['sustainability_status']}")
    print(f"Top Risk: {analysis['risk_factors'][0]['factor'] if analysis['risk_factors'] else 'None identified'}")
    
    return {
        'score': analysis['sustainability_score'],
        'runway': sustainability['treasury_runway_days'],
        'status': sustainability['sustainability_status']
    }

# Analyze multiple projects
projects = ['axie-infinity', 'the-sandbox', 'decentraland', 'gala']
results = {}

for project in projects:
    try:
        results[project] = quick_gamefi_analysis(project)
    except Exception as e:
        print(f"Error analyzing {project}: {e}")


