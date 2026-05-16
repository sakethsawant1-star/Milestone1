"use client";

import { useState } from "react";
import { RecommendationCard } from "../components/RecommendationCard";
import { getRecommendApiUrl } from "../lib/api";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [recommendations, setRecommendations] = useState<any[] | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setRecommendations(null);

    const formData = new FormData(e.currentTarget);
    const payload = {
      staticContext: {
        location: formData.get("location"),
        budget: formData.get("budget"),
        cuisine: formData.get("cuisine") || "Any",
        rating: formData.get("rating") || "Any",
      },
      nuanceContext: formData.get("nuance") || "None provided",
    };

    try {
      const response = await fetch(getRecommendApiUrl(), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      
      if (data.error) {
        setError(data.error);
      } else if (data.recommendations) {
        setRecommendations(data.recommendations);
      } else {
        setError("Unexpected response from the server.");
      }
    } catch (err) {
      setError("Connection Error: Could not connect to the backend server. Make sure it is running on port 5001.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid md:grid-cols-[1fr_1.5fr] gap-8 items-start">
      {/* Input Section */}
      <section className="glass-card p-8">
        <h2 className="text-xl font-bold text-white mb-6 border-b border-slate-700 pb-2">Your Preferences</h2>
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label htmlFor="location" className="block text-sm font-medium text-slate-300 mb-1">Location</label>
            <select id="location" name="location" required className="glass-input appearance-none bg-slate-900/80">
              <option value="" disabled selected>Select a location...</option>
              <option value="BTM">BTM</option>
              <option value="Banashankari">Banashankari</option>
              <option value="Bannerghatta Road">Bannerghatta Road</option>
              <option value="Basavanagudi">Basavanagudi</option>
              <option value="Bellandur">Bellandur</option>
              <option value="Bommanahalli">Bommanahalli</option>
              <option value="Brigade Road">Brigade Road</option>
              <option value="Brookefield">Brookefield</option>
              <option value="CV Raman Nagar">CV Raman Nagar</option>
              <option value="Central Bangalore">Central Bangalore</option>
              <option value="Church Street">Church Street</option>
              <option value="City Market">City Market</option>
              <option value="Commercial Street">Commercial Street</option>
              <option value="Cunningham Road">Cunningham Road</option>
              <option value="Domlur">Domlur</option>
              <option value="East Bangalore">East Bangalore</option>
              <option value="Ejipura">Ejipura</option>
              <option value="Electronic City">Electronic City</option>
              <option value="Frazer Town">Frazer Town</option>
              <option value="HBR Layout">HBR Layout</option>
              <option value="HSR">HSR</option>
              <option value="Hosur Road">Hosur Road</option>
              <option value="ITPL Main Road, Whitefield">ITPL Main Road, Whitefield</option>
              <option value="Indiranagar">Indiranagar</option>
              <option value="Infantry Road">Infantry Road</option>
              <option value="JP Nagar">JP Nagar</option>
              <option value="Jalahalli">Jalahalli</option>
              <option value="Jayanagar">Jayanagar</option>
              <option value="Jeevan Bhima Nagar">Jeevan Bhima Nagar</option>
              <option value="KR Puram">KR Puram</option>
              <option value="Kammanahalli">Kammanahalli</option>
              <option value="Kanakapura Road">Kanakapura Road</option>
              <option value="Koramangala">Koramangala</option>
              <option value="Kumaraswamy Layout">Kumaraswamy Layout</option>
              <option value="Langford Town">Langford Town</option>
              <option value="Lavelle Road">Lavelle Road</option>
              <option value="MG Road">MG Road</option>
              <option value="Majestic">Majestic</option>
              <option value="Malleshwaram">Malleshwaram</option>
              <option value="Marathahalli">Marathahalli</option>
              <option value="Mysore Road">Mysore Road</option>
              <option value="Nagarbhavi">Nagarbhavi</option>
              <option value="Old Airport Road">Old Airport Road</option>
              <option value="Old Madras Road">Old Madras Road</option>
              <option value="RT Nagar">RT Nagar</option>
              <option value="Race Course Road">Race Course Road</option>
              <option value="Rajajinagar">Rajajinagar</option>
              <option value="Rajarajeshwari Nagar">Rajarajeshwari Nagar</option>
              <option value="Residency Road">Residency Road</option>
              <option value="Richmond Road">Richmond Road</option>
              <option value="Sanjay Nagar">Sanjay Nagar</option>
              <option value="Sarjapur Road">Sarjapur Road</option>
              <option value="Seshadripuram">Seshadripuram</option>
              <option value="Shanti Nagar">Shanti Nagar</option>
              <option value="Shivajinagar">Shivajinagar</option>
              <option value="South Bangalore">South Bangalore</option>
              <option value="St. Marks Road">St. Marks Road</option>
              <option value="Ulsoor">Ulsoor</option>
              <option value="Uttarahalli">Uttarahalli</option>
              <option value="Vasanth Nagar">Vasanth Nagar</option>
              <option value="Vijay Nagar">Vijay Nagar</option>
              <option value="Whitefield">Whitefield</option>
              <option value="Wilson Garden">Wilson Garden</option>
            </select>
          </div>

          <div>
            <label htmlFor="budget" className="block text-sm font-medium text-slate-300 mb-1">Budget (for two)</label>
            <select id="budget" name="budget" required className="glass-input appearance-none bg-slate-900/80">
              <option value="" disabled selected>Select your budget...</option>
              <option value="low">₹ (Under ₹500)</option>
              <option value="medium">₹₹ (₹500 - ₹1500)</option>
              <option value="high">₹₹₹ (Above ₹1500)</option>
            </select>
          </div>

          <div>
            <label htmlFor="cuisine" className="block text-sm font-medium text-slate-300 mb-1">Cuisine (Optional)</label>
            <input type="text" id="cuisine" name="cuisine" placeholder="e.g., Italian, Sushi..." className="glass-input" />
          </div>

          <div>
            <label htmlFor="rating" className="block text-sm font-medium text-slate-300 mb-1">Minimum Rating</label>
            <select id="rating" name="rating" className="glass-input appearance-none bg-slate-900/80">
              <option value="Any" selected>Any Rating</option>
              <option value="3.5+">3.5 & Above</option>
              <option value="4.0+">4.0 & Above</option>
              <option value="4.5+">4.5 & Above</option>
            </select>
          </div>

          <div>
            <label htmlFor="nuance" className="block text-sm font-medium text-primary mb-1">What's the vibe?</label>
            <textarea id="nuance" name="nuance" rows={3} placeholder="A quiet romantic place with great lighting..." className="glass-input resize-none" />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className={`w-full py-4 px-6 rounded-xl font-bold text-white shadow-lg transition-all 
              ${loading ? 'bg-slate-700 cursor-not-allowed' : 'bg-gradient-to-r from-primary to-accent hover:opacity-90 hover:shadow-primary/30 active:scale-[0.98]'}`}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </span>
            ) : 'Find Recommendations'}
          </button>
        </form>
      </section>

      {/* Results Section */}
      <section className="min-h-[400px]">
        {error && (
          <div className="glass-card p-6 bg-red-500/10 border-red-500/30 text-red-200">
            <p className="font-semibold text-red-400 mb-1">Oops, something went wrong</p>
            <p className="text-sm">{error}</p>
          </div>
        )}

        {loading && !error && (
          <div className="h-full flex flex-col items-center justify-center text-slate-400 space-y-6 animate-pulse">
            <div className="relative">
              <div className="w-16 h-16 rounded-full border-4 border-slate-700"></div>
              <div className="w-16 h-16 rounded-full border-4 border-primary border-t-transparent animate-spin absolute inset-0"></div>
            </div>
            <p className="text-lg">Consulting the AI Engine...</p>
          </div>
        )}

        {!loading && !error && !recommendations && (
          <div className="h-full flex items-center justify-center text-slate-500 border-2 border-dashed border-slate-700/50 rounded-2xl p-8 text-center">
            <p>Tell us what you're craving on the left, and our AI will hand-pick the perfect spots for you.</p>
          </div>
        )}

        {!loading && recommendations && (
          <div className="space-y-2">
            <h2 className="text-2xl font-bold text-white mb-6">Top Picks For You</h2>
            {recommendations.length > 0 ? (
              recommendations.map((rec, idx) => (
                <RecommendationCard
                  key={idx}
                  name={rec.name}
                  rationale={rec.rationale}
                  rank={idx + 1}
                  cuisines={rec.cuisines}
                  costForTwo={rec.costForTwo}
                  rating={rec.rating}
                  location={rec.location}
                />
              ))
            ) : (
              <p className="text-slate-400">No matching restaurants found.</p>
            )}
          </div>
        )}
      </section>
    </div>
  );
}
