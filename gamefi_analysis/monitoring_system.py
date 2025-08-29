# monitoring_system.py - Real-time GameFi monitoring
import schedule
import time
import smtplib
from email.mime.text import MimeText
from datetime import datetime, timedelta

class GameFiMonitoringSystem:
    def __init__(self, config):
        self.config = config
        self.alert_thresholds = {
            'treasury_runway_critical': 90,  # days
            'treasury_runway_warning': 180,  # days
            'retention_rate_critical': 0.2,  # 20%
            'sustainability_score_warning': 40,  # out of 100
            'price_drop_alert': 0.2  # 20% in 24h
        }
        
    def setup_monitoring_schedule(self):
        """Setup automated monitoring schedule"""
        
        # Daily monitoring
        schedule.every().day.at("09:00").do(self.daily_health_check)
        schedule.every().day.at("18:00").do(self.daily_summary_report)
        
        # Weekly deep analysis
        schedule.every().monday.at("10:00").do(self.weekly_analysis)
        
        # Real-time price monitoring (every 15 minutes during trading hours)
        schedule.every(15).minutes.do(self.price_monitoring)
        
        print("Monitoring system initialized. Starting continuous monitoring...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def daily_health_check(self):
        """Perform daily health assessment"""
        
        projects_to_monitor = self.config.get('monitored_projects', [])
        alerts = []
        
        for project in projects_to_monitor:
            try:
                # Collect latest data
                token_data = collector.fetch_token_metrics(project)
                analysis = analyzer.analyze_token_sustainability(token_data)
                
                # Check alert conditions
                project_alerts = self.check_alert_conditions(project, analysis, token_data)
                alerts.extend(project_alerts)
                
            except Exception as e:
                alerts.append({
                    'project': project,
                    'type': 'data_error',
                    'message': f"Failed to analyze {project}: {e}",
                    'severity': 'medium'
                })
        
        # Send alerts if any critical issues found
        if alerts:
            self.send_alert_notification(alerts)
        
        # Log daily status
        self.log_daily_status(alerts)
    
    def check_alert_conditions(self, project: str, analysis: Dict, token_data: Dict) -> List[Dict]:
        """Check various alert conditions for a project"""
        
        alerts = []
        
        # Treasury runway alerts
        runway_days = self.calculate_treasury_runway(token_data)
        if runway_days < self.alert_thresholds['treasury_runway_critical']:
            alerts.append({
                'project': project,
                'type': 'treasury_critical',
                'message': f"Treasury runway critically low: {runway_days:.0f} days remaining",
                'severity': 'critical',
                'value': runway_days
            })
        elif runway_days < self.alert_thresholds['treasury_runway_warning']:
            alerts.append({
                'project': project,
                'type': 'treasury_warning',
                'message': f"Treasury runway warning: {runway_days:.0f} days remaining",
                'severity': 'warning',
                'value': runway_days
            })
        
        # Sustainability score alerts
        score = analysis['sustainability_score']
        if score < self.alert_thresholds['sustainability_score_warning']:
            alerts.append({
                'project': project,
                'type': 'sustainability_low',
                'message': f"Sustainability score low: {score:.1f}/100",
                'severity': 'warning',
                'value': score
            })
        
        # User retention alerts
        retention = token_data['gaming_metrics']['user_retention_7d']
        if retention < self.alert_thresholds['retention_rate_critical']:
            alerts.append({
                'project': project,
                'type': 'retention_critical',
                'message': f"User retention critically low: {retention*100:.1f}%",
                'severity': 'high',
                'value': retention
            })
        
        return alerts
    
    def price_monitoring(self):
        """Monitor price movements for alerts"""
        
        current_time = datetime.now().hour
        
        # Only monitor during active trading hours (0-23 UTC)
        if 0 <= current_time <= 23:
            projects = self.config.get('monitored_projects', [])
            
            for project in projects:
                try:
                    # Get 24-hour price data
                    price_data = collector.fetch_token_metrics(project, days=1)
                    
                    if price_data and len(price_data['price_history']) >= 2:
                        current_price = price_data['price_history']['price'].iloc[-1]
                        previous_price = price_data['price_history']['price'].iloc[0]
                        price_change = (current_price - previous_price) / previous_price
                        
                        # Check for significant price movements
                        if abs(price_change) > self.alert_thresholds['price_drop_alert']:
                            direction = "increased" if price_change > 0 else "decreased"
                            self.send_price_alert(project, current_price, price_change, direction)
                
                except Exception as e:
                    print(f"Price monitoring error for {project}: {e}")
    
    def send_alert_notification(self, alerts: List[Dict]):
        """Send alert notifications via email/webhook"""
        
        critical_alerts = [a for a in alerts if a['severity'] == 'critical']
        high_alerts = [a for a in alerts if a['severity'] == 'high']
        warning_alerts = [a for a in alerts if a['severity'] == 'warning']
        
        if critical_alerts or high_alerts:
            # Send immediate notification for critical/high alerts
            self.send_email_alert(critical_alerts + high_alerts, urgent=True)
        
        if warning_alerts:
            # Send daily digest for warnings
            self.send_email_alert(warning_alerts, urgent=False)
    
    def send_email_alert(self, alerts: List[Dict], urgent: bool = False):
        """Send email alert notification"""
        
        subject = "🚨 Critical GameFi Alert" if urgent else "⚠️ GameFi Warning Notification"
        
        body = f"""
GameFi Monitoring Alert - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{"URGENT ACTION REQUIRED" if urgent else "MONITORING ALERT"}

Detected Issues:
"""
        
        for alert in alerts:
            body += f"""
• {alert['project'].upper()}: {alert['message']}
  Severity: {alert['severity'].upper()}
  Type: {alert['type']}
"""
        
        body += """

This is an automated alert from your GameFi monitoring system.
Review the full dashboard for detailed analysis and recommendations.
"""
        
        # Send email (configure with your SMTP settings)
        try:
            msg = MimeText(body)
            msg['Subject'] = subject
            msg['From'] = self.config['email_from']
            msg['To'] = self.config['email_to']
            
            # Configure SMTP server
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['email_username'], self.config['email_password'])
            server.send_message(msg)
            server.quit()
            
            print(f"Alert email sent: {subject}")
            
        except Exception as e:
            print(f"Failed to send email alert: {e}")

# Setup monitoring
monitoring_config = {
    'monitored_projects': ['axie-infinity', 'the-sandbox', 'decentraland'],
    'email_from': 'gamefi-monitor@yours.com',
    'email_to': 'alerts@yourdomain.com',
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email_username': 'your-email@gmail.com',
    'email_password': 'your-app-password'
}

monitor = GameFiMonitoringSystem(monitoring_config)
# monitor.setup_monitoring_schedule()  # Uncomment to start monitoring


