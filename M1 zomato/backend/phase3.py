import json
import os

def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, '..', 'phase1', 'zomato_cleaned_full.json')
    try:
        with open(data_path, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

def filter_restaurants(restaurants, location, budget, cuisine=None, rating=None):
    filtered = []
    location_lower = location.lower()
    cuisine_lower = cuisine.lower() if cuisine and cuisine != "Any" else None
    
    for r in restaurants:
        if location_lower not in r.get('location', '').lower():
            continue
            
        cost = r.get('costForTwo', 0)
        if budget == 'low' and cost > 500:
            continue
        elif budget == 'medium' and (cost <= 500 or cost > 1500):
            continue
        elif budget == 'high' and cost <= 1500:
            continue
            
        if cuisine_lower:
            r_cuisines = r.get('cuisines', '').lower()
            if cuisine_lower not in r_cuisines:
                continue
                
        if rating and rating.lower() != "any":
            try:
                # rating could be '3.5', '4.0', '4.5' etc.
                min_rating = float(rating.replace('+', ''))
                if r.get('rating', 0) < min_rating:
                    continue
            except ValueError:
                pass
                
                
        filtered.append(r)
        
    # If filters were too strict and nothing matched, fallback to just location
    if not filtered:
        for r in restaurants:
            if location_lower in r.get('location', '').lower():
                filtered.append(r)
        
    # Sort by rating descending
    filtered.sort(key=lambda x: x.get('rating', 0), reverse=True)
    return filtered[:20]

def assemble_context(candidates):
    context_lines = []
    for i, c in enumerate(candidates):
        line = f"{i+1}. {c['name']} (Location: {c['location']}, Cuisines: {c['cuisines']}, Cost for Two: INR {c['costForTwo']}, Rating: {c['rating']})"
        context_lines.append(line)
    return "\n".join(context_lines)

def build_prompt(payload):
    static_ctx = payload.get('staticContext', {})
    nuance = payload.get('nuanceContext', '')
    
    location = static_ctx.get('location', '')
    budget = static_ctx.get('budget', '')
    cuisine = static_ctx.get('cuisine', '')
    rating = static_ctx.get('rating', 'Any')
    
    restaurants = load_data()
    candidates = filter_restaurants(restaurants, location, budget, cuisine, rating)
    
    if not candidates:
        return None, "No restaurants found matching the strict location and budget criteria."
        
    context_str = assemble_context(candidates)
    
    prompt = f"""You are an expert AI restaurant recommender. 

The user has the following specific preferences:
- Location: {location}
- Budget: {budget}
- Cuisine Preference: {cuisine}
- Minimum Rating: {rating}
- Specific Nuance/Vibe: "{nuance}"

Here are the top candidate restaurants that match the basic criteria:
{context_str}

Task:
From the candidate list above, select the top 3 to 5 restaurants that BEST match the user's specific nuance/vibe. 

Provide your response in valid JSON format with the following structure:
{{
  "recommendations": [
    {{
      "name": "Restaurant Name",
      "rationale": "A concise, human-readable explanation of why this restaurant perfectly fits the user's vibe."
    }}
  ]
}}
Do NOT output any markdown, only raw JSON.
"""
    return prompt, None
