import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from config import AI_CONFIG

@dataclass
class ModelPerformance:
    """Data class for tracking model performance metrics."""
    provider: str
    model: str
    response_time: float
    success: bool
    error_message: str = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class AIModelManager:
    """Manages AI model selection, performance tracking, and advanced features."""
    
    def __init__(self):
        self.performance_history: List[ModelPerformance] = []
        self.model_preferences: Dict[str, Dict] = {}
        self.ab_test_config: Dict[str, Any] = {}
        self.load_preferences()
    
    def load_preferences(self):
        """Load model preferences from file."""
        try:
            with open('model_preferences.json', 'r') as f:
                self.model_preferences = json.load(f)
        except FileNotFoundError:
            self.model_preferences = {
                'default': AI_CONFIG['default_provider'],
                'fallback': AI_CONFIG['fallback_provider'],
                'performance_based': True,
                'cost_optimization': False
            }
    
    def save_preferences(self):
        """Save model preferences to file."""
        with open('model_preferences.json', 'w') as f:
            json.dump(self.model_preferences, f, indent=2)
    
    def record_performance(self, provider: str, model: str, response_time: float, 
                          success: bool, error_message: str = None):
        """Record performance metrics for a model."""
        performance = ModelPerformance(
            provider=provider,
            model=model,
            response_time=response_time,
            success=success,
            error_message=error_message
        )
        self.performance_history.append(performance)
        
        # Keep only last 1000 records to prevent memory issues
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]
    
    def get_best_performing_model(self, time_window_hours: int = 24) -> Optional[str]:
        """Get the best performing model based on recent performance."""
        if not self.performance_history:
            return None
        
        cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
        recent_performance = [
            p for p in self.performance_history 
            if p.timestamp > cutoff_time and p.success
        ]
        
        if not recent_performance:
            return None
        
        # Calculate average response time by provider
        provider_stats = {}
        for perf in recent_performance:
            if perf.provider not in provider_stats:
                provider_stats[perf.provider] = {'total_time': 0, 'count': 0}
            provider_stats[perf.provider]['total_time'] += perf.response_time
            provider_stats[perf.provider]['count'] += 1
        
        # Find provider with lowest average response time
        best_provider = min(
            provider_stats.keys(),
            key=lambda p: provider_stats[p]['total_time'] / provider_stats[p]['count']
        )
        
        return best_provider
    
    def get_performance_stats(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Get performance statistics for all providers."""
        if not self.performance_history:
            return {}
        
        cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
        recent_performance = [
            p for p in self.performance_history 
            if p.timestamp > cutoff_time
        ]
        
        stats = {}
        for perf in recent_performance:
            if perf.provider not in stats:
                stats[perf.provider] = {
                    'total_requests': 0,
                    'successful_requests': 0,
                    'total_response_time': 0,
                    'errors': []
                }
            
            stats[perf.provider]['total_requests'] += 1
            stats[perf.provider]['total_response_time'] += perf.response_time
            
            if perf.success:
                stats[perf.provider]['successful_requests'] += 1
            else:
                stats[perf.provider]['errors'].append(perf.error_message)
        
        # Calculate averages and success rates
        for provider in stats:
            total = stats[provider]['total_requests']
            if total > 0:
                stats[provider]['success_rate'] = stats[provider]['successful_requests'] / total
                stats[provider]['avg_response_time'] = stats[provider]['total_response_time'] / total
            else:
                stats[provider]['success_rate'] = 0
                stats[provider]['avg_response_time'] = 0
        
        return stats
    
    def setup_ab_test(self, test_name: str, providers: List[str], 
                     traffic_split: Dict[str, float] = None):
        """Setup A/B testing configuration."""
        if not traffic_split:
            # Equal split if not specified
            traffic_split = {provider: 1.0/len(providers) for provider in providers}
        
        self.ab_test_config[test_name] = {
            'providers': providers,
            'traffic_split': traffic_split,
            'start_time': datetime.now(),
            'results': {provider: {'requests': 0, 'successes': 0} for provider in providers}
        }
    
    def get_ab_test_provider(self, test_name: str) -> Optional[str]:
        """Get provider for A/B testing based on traffic split."""
        if test_name not in self.ab_test_config:
            return None
        
        config = self.ab_test_config[test_name]
        import random
        
        # Simple random selection based on traffic split
        rand = random.random()
        cumulative = 0
        
        for provider, split in config['traffic_split'].items():
            cumulative += split
            if rand <= cumulative:
                return provider
        
        return config['providers'][0]  # Fallback
    
    def record_ab_test_result(self, test_name: str, provider: str, success: bool):
        """Record A/B test result."""
        if test_name in self.ab_test_config:
            self.ab_test_config[test_name]['results'][provider]['requests'] += 1
            if success:
                self.ab_test_config[test_name]['results'][provider]['successes'] += 1
    
    def get_ab_test_results(self, test_name: str) -> Optional[Dict[str, Any]]:
        """Get A/B test results."""
        if test_name not in self.ab_test_config:
            return None
        
        config = self.ab_test_config[test_name]
        results = config['results']
        
        # Calculate success rates
        for provider in results:
            requests = results[provider]['requests']
            if requests > 0:
                results[provider]['success_rate'] = results[provider]['successes'] / requests
            else:
                results[provider]['success_rate'] = 0
        
        return {
            'test_name': test_name,
            'start_time': config['start_time'].isoformat(),
            'traffic_split': config['traffic_split'],
            'results': results
        }
    
    def get_model_recommendations(self, use_case: str = 'general') -> Dict[str, Any]:
        """Get model recommendations based on use case and performance."""
        recommendations = {
            'fastest': self.get_best_performing_model(),
            'most_reliable': self._get_most_reliable_model(),
            'cost_effective': self._get_cost_effective_model(),
            'best_for_use_case': self._get_best_for_use_case(use_case)
        }
        
        return recommendations
    
    def _get_most_reliable_model(self) -> Optional[str]:
        """Get the most reliable model based on success rate."""
        stats = self.get_performance_stats()
        if not stats:
            return None
        
        most_reliable = max(stats.keys(), key=lambda p: stats[p]['success_rate'])
        return most_reliable if stats[most_reliable]['success_rate'] > 0.8 else None
    
    def _get_cost_effective_model(self) -> Optional[str]:
        """Get the most cost-effective model (simplified implementation)."""
        # This is a simplified implementation
        # In a real scenario, you'd track actual costs per request
        cost_estimates = {
            'openai': {'gpt-4': 0.03, 'gpt-3.5-turbo': 0.002},
            'anthropic': {'claude-3-sonnet-20240229': 0.015, 'claude-3-haiku-20240307': 0.00025},
            'google': {'gemini-1.5-pro': 0.0075, 'gemini-1.5-flash': 0.00075}
        }
        
        # Return the cheapest available model
        cheapest = None
        min_cost = float('inf')
        
        for provider, models in cost_estimates.items():
            for model, cost in models.items():
                if cost < min_cost:
                    min_cost = cost
                    cheapest = provider
        
        return cheapest
    
    def _get_best_for_use_case(self, use_case: str) -> Optional[str]:
        """Get the best model for a specific use case."""
        use_case_recommendations = {
            'creative': 'openai',  # GPT models are good for creative tasks
            'analytical': 'anthropic',  # Claude is good for analysis
            'multimodal': 'google',  # Gemini has strong multimodal capabilities
            'general': 'openai'  # Default recommendation
        }
        
        return use_case_recommendations.get(use_case, 'openai')
    
    def export_performance_data(self, filename: str = None) -> str:
        """Export performance data to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'performance_data_{timestamp}.json'
        
        data = {
            'performance_history': [asdict(p) for p in self.performance_history],
            'model_preferences': self.model_preferences,
            'ab_test_config': self.ab_test_config,
            'export_timestamp': datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return filename 