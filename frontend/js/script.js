// Script from document
document.addEventListener('DOMContentLoaded', function() {
            // API URL - using the correct localhost URL and port
            const API_URL = 'http://localhost:3000/api';
            
            // Elements
            const melachotList = document.getElementById('melachot-list');
            const contentArea = document.getElementById('content');
            const categoryFilter = document.getElementById('category-filter');
            const searchInput = document.getElementById('search-input');
            const searchButton = document.getElementById('search-button');
            const activitySearchInput = document.getElementById('activity-search-input');
            const activitySearchButton = document.getElementById('activity-search-button');
            
            // Store all melachot data
            let allMelachot = [];
            
            // Debounce function for search
            function debounce(func, delay) {
                let debounceTimer;
                return function() {
                    const context = this;
                    const args = arguments;
                    clearTimeout(debounceTimer);
                    debounceTimer = setTimeout(() => func.apply(context, args), delay);
                };
            }
           
            // Try to fetch from API first, use local data as fallback
            async function fetchMelachot() {
                try {
                    // Try the API URL first
                    const response = await fetch(`${API_URL}/melachot`);
                    if (response.ok) {
                        allMelachot = await response.json();
                        console.log("Loaded data from API successfully");
                    } else {
                        throw new Error("API request failed with status: " + response.status);
                    }
                } catch (error) {
                    console.error('Error fetching melachot:', error);
                    
                    // Use local data as fallback
                    console.log("Using local data as fallback");
                    allMelachot = localMelachotData;
                    
                    // Show warning message
                    const warningEl = document.createElement('div');
                    warningEl.style.background = "#fff3cd";
                    warningEl.style.color = "#856404";
                    warningEl.style.padding = "10px";
                    warningEl.style.marginBottom = "15px";
                    warningEl.style.borderRadius = "5px";
                    warningEl.style.border = "1px solid #ffeeba";
                    warningEl.innerHTML = `
                        <p><strong>Note:</strong> Unable to connect to the API server. Using built-in data instead.</p>
                        <p>Error: ${error.message}</p>
                        <p>To fix this, make sure your Flask server is running at http://127.0.0.1:3000</p>
                    `;
                    document.querySelector('.sidebar').prepend(warningEl);
                }
                
                // Continue with displaying the data regardless of source
                displayMelachotList(allMelachot);
                
                // Extract categories
                const uniqueCategories = [...new Set(allMelachot.map(item => item.category))];
                populateCategoryFilter(uniqueCategories);
            }
            
            // Display melachot in the list
            function displayMelachotList(melachot) {
                melachotList.innerHTML = '';
                melachot.forEach(melacha => {
                    const li = document.createElement('li');
                    li.textContent = `${melacha.name}`;
                    li.dataset.id = melacha.id;
                    li.addEventListener('click', () => showMelachaDetails(melacha));
                    melachotList.appendChild(li);
                });
            }
            
            // Populate category filter dropdown
            function populateCategoryFilter(categories) {
                categories.forEach(category => {
                    const option = document.createElement('option');
                    option.value = category;
                    option.textContent = category;
                    categoryFilter.appendChild(option);
                });
            }
            
            // Filter melachot by category
            categoryFilter.addEventListener('change', function() {
                const selectedCategory = this.value;
                if (selectedCategory === '') {
                    displayMelachotList(allMelachot);
                } else {
                    const filteredMelachot = allMelachot.filter(melacha => 
                        melacha.category === selectedCategory
                    );
                    displayMelachotList(filteredMelachot);
                }
            });
            
            // Regular Search functionality
            searchButton.addEventListener('click', performSearch);
            searchInput.addEventListener('keyup', debounce(function() {
                performSearch();
            }, 300));
            
            function performSearch() {
                const searchTerm = searchInput.value.toLowerCase().trim();
                if (searchTerm === '') {
                    displayMelachotList(allMelachot);
                    return;
                }
                
                const searchResults = allMelachot.filter(melacha => 
                    melacha.name.toLowerCase().includes(searchTerm) || 
                    melacha.description.toLowerCase().includes(searchTerm)
                );
                displayMelachotList(searchResults);
            }
            
            // Activity Search functionality
            activitySearchButton.addEventListener('click', performActivitySearch);
            activitySearchInput.addEventListener('keyup', debounce(function() {
                performActivitySearch();
            }, 300));
            
            function performActivitySearch() {
                const searchTerm = activitySearchInput.value.toLowerCase().trim();
                if (searchTerm === '') {
                    displayMelachotList(allMelachot);
                    return;
                }
                
                const searchResults = allMelachot.filter(melacha => {
                    if (!melacha.keywords) return false;
                    
                    return melacha.keywords.some(keyword => 
                        keyword.toLowerCase().includes(searchTerm)
                    );
                });
                
                displayMelachotList(searchResults);
            }
            
            // Show melacha details
            function showMelachaDetails(melacha) {
                // Update active class in list
                const listItems = melachotList.querySelectorAll('li');
                listItems.forEach(item => item.classList.remove('active'));
                const activeItem = melachotList.querySelector(`li[data-id="${melacha.id}"]`);
                if (activeItem) {
                    activeItem.classList.add('active');
                }
                
                // Determine icon based on category
                let categoryIcon = '📜';
                if (melacha.category === 'Field Work') {
                    categoryIcon = '🌾';
                } else if (melacha.category === 'Making Material Curtains') {
                    categoryIcon = '👘';
                } else if (melacha.category === 'Making Leather Curtains') {
                    categoryIcon = '🧵';
                } else if (melacha.category === 'Making the Beams') {
                    categoryIcon = '✍️';
                } else if (melacha.category === 'Putting up and Taking down') {
                    categoryIcon = '🏗️';
                } else if (melacha.category === 'Final Touches') {
                    categoryIcon = '🔨';
                }
                
                // Create examples list HTML
                const examplesHTML = melacha.examples.map(example => 
                    `<li>${example}</li>`
                ).join('');
                
                // Create keywords HTML if available
                let keywordsHTML = '';
                if (melacha.keywords && melacha.keywords.length > 0) {
                    const keywordItems = melacha.keywords.map(keyword => 
                        `<span class="keyword-item">${keyword}</span>`
                    ).join('');
                    
                    keywordsHTML = `
                        <div class="keywords-container">
                            <h3 class="keywords-title">Related Modern Activities:</h3>
                            <div class="keywords-list">
                                ${keywordItems}
                            </div>
                        </div>
                    `;
                }
                
                // Update content area
                contentArea.innerHTML = `
                    <div class="melacha-details active">
                        <div class="melacha-header">
                            <h2 class="melacha-name">${melacha.name}</h2>
                            <div class="hebrew-display">Hebrew characters: ${melacha.hebrew}</div>
                            <span class="melacha-category">${categoryIcon} ${melacha.category}</span>
                        </div>
                        
                        <p class="melacha-description">${melacha.description}</p>
                        
                        <h3 class="examples-title">Examples:</h3>
                        <ul class="examples-list">
                            ${examplesHTML}
                        </ul>
                        
                        ${keywordsHTML}
                        
                        <div class="icon-box">
                            <div class="icon"><i class="fas fa-info-circle"></i></div>
                            <div>
                                <p>This melacha is one of the 39 categories of work prohibited on Shabbat.</p>
                                <p>Understanding these categories helps in proper Shabbat observance.</p>
                            </div>
                        </div>
                    </div>
                `;
            }
            
            // Initialize
            fetchMelachot();
        });

