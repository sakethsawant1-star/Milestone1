document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('recommendation-form');

    // Views
    const viewLanding = document.getElementById('view-landing');
    const viewLoading = document.getElementById('view-loading');
    const viewResults = document.getElementById('view-results');
    const globalHeader = document.getElementById('global-header');
    const globalBg = document.getElementById('global-bg');

    const resultsGrid = document.getElementById('results-grid');

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        // Capture Static Context
        const location = document.getElementById('location').value.trim();
        const budget = document.getElementById('budget').value;
        const cuisine = document.getElementById('cuisine').value.trim();
        const rating = document.getElementById('rating').value;

        // Capture Nuance Context
        const nuance = document.getElementById('nuance').value.trim();

        if (!location || !budget) {
            alert("Please provide at least a Location and Budget.");
            return;
        }

        // Toggle to Loading View
        viewLanding.classList.add('hidden');
        globalHeader.classList.replace('bg-black/20', 'bg-white/90');
        globalHeader.classList.add('text-gray-900');
        globalHeader.classList.remove('text-white');
        globalBg.classList.add('opacity-10'); // Dim background
        viewLoading.classList.remove('hidden');

        const payload = {
            staticContext: {
                location,
                budget,
                cuisine: cuisine || "Any",
                rating: rating
            },
            nuanceContext: nuance || "None provided"
        };

        // Determine Backend URL based on environment
        const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        const backendUrl = isLocalhost
            ? 'http://localhost:5001/api/recommend'
            : 'https://web-production-9d250.up.railway.app/api/recommend';

        fetch(backendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
            .then(response => response.json())
            .then(data => {
                // Hide loading, show results
                viewLoading.classList.add('hidden');
                globalHeader.classList.replace('bg-white/90', 'bg-black/40');
                globalHeader.classList.replace('text-gray-900', 'text-white');
                globalBg.classList.replace('opacity-10', 'opacity-80');
                viewResults.classList.remove('hidden');

                resultsGrid.innerHTML = ''; // clear

                if (data.error) {
                    resultsGrid.innerHTML = `
                    <div class="md:col-span-12 glass-card rounded-xl p-8 text-center text-red-600 font-bold">
                        Error: ${data.error}
                    </div>
                `;
                    return;
                }

                // Array of reliable, premium food images to prevent broken links
                const foodImages = [
                    "https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=800&auto=format&fit=crop", // Steak/Meat
                    "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?q=80&w=800&auto=format&fit=crop", // BBQ/Grill
                    "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=800&auto=format&fit=crop", // Pizza
                    "https://images.unsplash.com/photo-1482049016688-2d3e1b311543?q=80&w=800&auto=format&fit=crop", // Sandwich/Egg
                    "https://images.unsplash.com/photo-1484723091798-dffc122598ad?q=80&w=800&auto=format&fit=crop"  // Cafe vibe
                ];

                if (data.recommendations && data.recommendations.length > 0) {
                    data.recommendations.forEach((rec, index) => {
                        // Logic to make the first card larger
                        const isFirst = index === 0;
                        const colSpan = isFirst ? 'md:col-span-12 lg:col-span-8' : 'md:col-span-6 lg:col-span-4';

                        // Cycle through the reliable images
                        const imageUrl = foodImages[index % foodImages.length];

                        const cardHtml = `
                        <article class="${colSpan} glass-card rounded-xl shadow-lg overflow-hidden flex flex-col ${isFirst ? 'md:flex-row' : ''} transform transition-transform hover:-translate-y-1 hover:shadow-xl relative bg-white/10 border border-white/20">
                            
                            <!-- Reliable Food Image -->
                            <div class="${isFirst ? 'md:w-1/2' : ''} h-48 ${isFirst ? 'md:h-auto' : ''} relative">
                                <img src="${imageUrl}" class="w-full h-full object-cover opacity-80" />
                                <div class="absolute top-4 left-4 bg-white/90 text-gray-900 font-bold px-3 py-1 rounded-full shadow-sm flex items-center gap-1 text-sm">
                                    <span class="material-symbols-outlined text-[#b7122a] text-[14px]" style="font-variation-settings: 'FILL' 1;">emoji_events</span> 
                                    Rank #${index + 1}
                                </div>
                            </div>

                            <div class="p-6 flex-grow flex flex-col justify-between ${isFirst ? 'md:w-1/2' : ''}">
                                <div>
                                    <div class="flex justify-between items-start mb-2">
                                        <h2 class="text-2xl font-bold text-gray-900 drop-shadow-sm">${rec.name}</h2>
                                    </div>
                                    
                                    <div class="bg-[#b7122a]/10 border border-[#b7122a]/20 rounded-lg p-4 mb-4 backdrop-blur-sm">
                                        <div class="flex items-center gap-2 mb-2">
                                            <span class="material-symbols-outlined text-[#b7122a] text-[18px]">psychology</span>
                                            <span class="font-bold text-[#b7122a] text-sm uppercase tracking-wide">Why it fits your vibe</span>
                                        </div>
                                        <p class="text-gray-800 text-sm leading-relaxed">${rec.rationale}</p>
                                    </div>
                                </div>
                                <button class="w-full bg-[#b7122a] text-white font-semibold py-3 rounded-lg hover:bg-[#92001c] transition-colors shadow-md active:scale-95">View Details</button>
                            </div>
                        </article>
                    `;
                        resultsGrid.insertAdjacentHTML('beforeend', cardHtml);
                    });
                } else {
                    resultsGrid.innerHTML = `
                    <div class="md:col-span-12 glass-card rounded-xl p-8 text-center text-gray-800 font-bold text-xl">
                        No recommendations found. Try adjusting your preferences.
                    </div>
                `;
                }
            })
            .catch(err => {
                viewLoading.classList.add('hidden');
                viewResults.classList.remove('hidden');
                resultsGrid.innerHTML = `
                <div class="md:col-span-12 glass-card rounded-xl p-8 text-center text-red-600 font-bold">
                    Connection Error: Could not connect to the backend server. Make sure it is running on port 5001.
                </div>
            `;
                console.error("Fetch error:", err);
            });
    });
});
