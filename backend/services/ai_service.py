import openai
from config import OPENAI_API_KEY

class AIService:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    def generate_activity_suggestions(self, team_data, free_slots, central_location):
        """Generate activity suggestions using OpenAI."""
        try:
            # Prepare the prompt
            prompt = self._create_prompt(team_data, free_slots, central_location)
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a team bonding activity expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse and return suggestions
            return self._parse_suggestions(response.choices[0].message.content)
        except Exception as e:
            print(f"AI suggestion error: {str(e)}")
            return self._generate_fallback_suggestions(team_data)

    def _create_prompt(self, team_data, free_slots, central_location):
        """Create a prompt for the AI model."""
        prompt = f"""
        Based on the following team information, suggest 3-5 team bonding activities:

        Team Preferences:
        - Interests: {', '.join(team_data['interests'])}
        - Budget per person: ${team_data['budget']}
        - Group size: {team_data['group_size']} people
        - Location: {central_location['formatted_address']}

        Available Time Slots:
        {self._format_time_slots(free_slots)}

        Please suggest activities that:
        1. Match the team's interests and budget
        2. Are suitable for the group size
        3. Are accessible from the central location
        4. Can be completed within the available time slots

        For each suggestion, include:
        - Activity name
        - Estimated cost per person
        - Duration
        - Why it would be a good fit for this team
        """
        return prompt

    def _format_time_slots(self, free_slots):
        """Format time slots for the prompt."""
        formatted_slots = []
        for slot in free_slots:
            start = slot['start'].strftime('%Y-%m-%d %H:%M')
            end = slot['end'].strftime('%Y-%m-%d %H:%M')
            formatted_slots.append(f"- {start} to {end}")
        return '\n'.join(formatted_slots)

    def _parse_suggestions(self, ai_response):
        """Parse the AI response into structured suggestions."""
        # This is a simplified parser - you might want to make it more robust
        suggestions = []
        current_suggestion = {}
        
        for line in ai_response.split('\n'):
            line = line.strip()
            if not line:
                if current_suggestion:
                    suggestions.append(current_suggestion)
                    current_suggestion = {}
                continue
                
            if line.startswith('- '):
                if current_suggestion:
                    suggestions.append(current_suggestion)
                current_suggestion = {'name': line[2:]}
            elif ':' in line:
                key, value = line.split(':', 1)
                current_suggestion[key.strip().lower()] = value.strip()
        
        if current_suggestion:
            suggestions.append(current_suggestion)
            
        return suggestions

    def _generate_fallback_suggestions(self, team_data):
        """Generate fallback suggestions when AI is unavailable."""
        # Simple rule-based suggestions based on interests
        suggestions = []
        interests = team_data['interests']
        
        if 'hiking' in interests:
            suggestions.append({
                'name': 'Group Hiking',
                'cost': 'Free',
                'duration': '2-3 hours',
                'description': 'A scenic hike suitable for the group size'
            })
        
        if 'games' in interests:
            suggestions.append({
                'name': 'Board Game Night',
                'cost': '$10-20 per person',
                'duration': '3-4 hours',
                'description': 'Fun team games with snacks and drinks'
            })
        
        if 'dining' in interests:
            suggestions.append({
                'name': 'Team Dinner',
                'cost': f'${team_data["budget"]} per person',
                'duration': '2 hours',
                'description': 'A casual dinner at a local restaurant'
            })
        
        return suggestions 