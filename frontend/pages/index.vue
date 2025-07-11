<template>
  <div>
    <header>
      <h1>Your Daily Fortune</h1>
      <p>Enter three keywords to unveil your destiny. Your words shape your future!</p>
    </header>

    <main>
      <section class="keyword-input-section">
        <h2>Your Keywords of Fate</h2>
        <div class="keyword-inputs">
          <div v-for="(keyword, index) in keywords" :key="index" class="keyword-input-wrapper">
            <input 
              type="text"
              v-model="keyword.value" 
              :placeholder="`Keyword ${index + 1}`"
              @input="updateCharCount"
            />
            <button 
              @click="clearKeyword(index)" 
              class="clear-keyword-btn" 
              v-show="keyword.value"
            >
              ✕
            </button>
          </div>
        </div>
        <div class="char-count" :class="{ 'limit-exceeded': isCharLimitExceeded }">
          Character Count: {{ totalCharCount }} / 20
        </div>
        <div v-if="isCharLimitExceeded" class="char-limit-warning">
          ⚠️ Total character limit (20) exceeded!
        </div>
      </section>

      <section class="submission-section">
        <button 
          @click="getFortune" 
          :disabled="isLoading || isCharLimitExceeded || !allKeywordsEntered" 
          class="submit-btn"
        >
          <span v-if="!isLoading">Reveal My Fortune!</span>
          <div v-if="isLoading" class="spinner">
            <!-- <img src="loading-spinner.svg" alt="Loading..." /> -->
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid" width="200" height="200" style="shape-rendering: auto; display: block; background: transparent;" xmlns:xlink="http://www.w3.org/1999/xlink"><g>
                <circle cx="50" cy="50" r="32" stroke-width="8" stroke="#6a1b9a" stroke-dasharray="50.26548245743669 50.26548245743669" fill="none" stroke-linecap="round">
                    <animateTransform attributeName="transform" type="rotate" repeatCount="indefinite" dur="1s" keyTimes="0;1" values="0 50 50;360 50 50"></animateTransform>
                </circle>
            <g></g></g><!-- [ldio] generated by https://loading.io/ --></svg>
          </div>
        </button>
      </section>

      <section v-if="fortuneResult" class="fortune-result-section">
        <div class="fortune-card" :class="fortuneCardAnimation">
          <h3>Your Fortune:</h3>
          <p v-html="fortuneResult"></p>
        </div>
      </section>
      
      <section v-if="errorMessage" class="error-message-section">
        <div class="error-card">
          <p>{{ errorMessage }}</p>
        </div>
      </section>
    </main>

    <footer>
      <p>&copy; Fortunes are for entertainment purposes only.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  setup() {
        const keywords = ref([
            { id: 1, value: '' },
            { id: 2, value: '' },
            { id: 3, value: '' }
        ]);
        const isLoading = ref(false);
        const fortuneResult = ref('');
        const errorMessage = ref('');
        const queryCount = ref(0);
        const fortuneCardAnimation = ref('');
        
        const totalCharCount = computed(() => {
            return keywords.value.reduce((sum, kw) => sum + kw.value.length, 0);
        });

        const isCharLimitExceeded = computed(() => {
            return totalCharCount.value > 20;
        });

        const allKeywordsEntered = computed(() => {
            return keywords.value.every(kw => kw.value.trim() !== '');
        });

        const updateCharCount = () => {
            // This is mainly to trigger re-computation if needed,
            // but computed property totalCharCount already handles it.
        };

        const clearKeyword = (index) => {
            keywords.value[index].value = '';
            updateCharCount();
        };

        const mockErrors = [
            "You’ve already used your 3 fortune queries today 🛑 Try again tomorrow!",
            "The stars are a bit shy right now... 🌌 Unable to retrieve your fortune 😵‍💫 Please try later.",
            "Mystic energies are scrambled! 📡 Perhaps try different keywords? 🤔"
        ];

        const getFortune = async () => {
            fortuneResult.value = '';
            errorMessage.value = '';
            fortuneCardAnimation.value = '';

            if (!allKeywordsEntered.value) {
                errorMessage.value = "Please enter all three keywords to receive your fortune.";
                // lack keywords alert
                return;
            }

            if (isCharLimitExceeded.value) {
                errorMessage.value = "Character limit exceeded. Please shorten your keywords.";
                // exceed alert
                return;
            }

            queryCount.value++;
            if (queryCount.value > 3) { // Simulate query limit more often after 3
                errorMessage.value = mockErrors[0];
                // ask too much alert
                return;
            }
            
            isLoading.value = true;

            const keywordsArray = keywords.value.map(kw => kw.value);
            const keywordData = {
                keywords: keywordsArray,
            };
            const { data, error } = await useFetch('/api/askGork', {
                method: 'POST',
                body: keywordData,
            });
            console.log(error.value);
            try{
                fortuneResult.value = data.value ? data.value.message : '';
                fortuneCardAnimation.value = 'fortune-reveal-enter-active';
                errorMessage.value = error.value ? error.value.data.message : '';
            }
            catch (e) {
                errorMessage.value = "unexpected error occurred : " + e;
            }
            isLoading.value = false;
        };

        return {
            keywords,
            isLoading,
            fortuneResult,
            errorMessage,
            totalCharCount,
            isCharLimitExceeded,
            allKeywordsEntered,
            fortuneCardAnimation,
            updateCharCount,
            clearKeyword,
            getFortune,
        };
    }
}
</script>

<style>
:root {
    --primary-bg: #f0f4f8;
    --secondary-bg: #ffffff;
    --primary-text: #333;
    --accent-color: #6a1b9a; /* Deep purple */
    --accent-color-dark: #4a148c;
    --error-color: #d32f2f;
    --success-color: #388e3c;
    --border-color: #e0e0e0;
    --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    --border-radius: 8px;
}

[v-cloak] {
    display: none;
}

body {
    font-family: var(--font-family);
    background-color: var(--primary-bg);
    color: var(--primary-text);
    margin: 0;
    padding: 20px;
    transition: background-color 0.3s, color 0.3s;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
}

#app {
    width: 100%;
    max-width: 700px;
    background-color: var(--secondary-bg);
    padding: 20px;
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
    transition: background-color 0.3s;
}

header {
    text-align: center;
    margin-bottom: 30px;
    position: relative;
}

header h1 {
    color: var(--accent-color);
    margin-bottom: 10px;
}

.keyword-input-section, .submission-section, .fortune-result-section, .error-message-section {
    margin-bottom: 25px;
    padding: 15px;
    background-color: var(--primary-bg);
    border-radius: var(--border-radius);
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
}

.keyword-inputs {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
}

.keyword-input-wrapper {
    flex-grow: 1;
    position: relative;
}

.keyword-input-wrapper input[type="text"] {
    width: calc(100% - 30px); /* Account for padding and clear button */
    padding: 10px;
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    font-size: 1em;
    background-color: var(--secondary-bg);
    color: var(--primary-text);
    transition: border-color 0.3s;
}
.keyword-input-wrapper input[type="text"]:focus {
    outline: none;
    border-color: var(--accent-color);
}


.clear-keyword-btn {
    position: absolute;
    right: 5px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    color: var(--primary-text);
    cursor: pointer;
    font-size: 1.2em;
    padding: 5px;
}
.clear-keyword-btn:hover {
    color: var(--error-color);
}

.char-count {
    font-size: 0.9em;
    color: var(--primary-text);
    opacity: 0.8;
}

.char-count.limit-exceeded {
    color: var(--error-color);
    font-weight: bold;
}

.char-limit-warning {
    color: var(--error-color);
    font-size: 0.9em;
    margin-top: 5px;
}

.submit-btn {
    display: block;
    width: 100%;
    padding: 12px 20px;
    background-color: var(--accent-color);
    color: white;
    border: none;
    border-radius: var(--border-radius);
    font-size: 1.1em;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.1s;
    position: relative; /* For spinner positioning */
    min-height: 48px; /* To prevent size change with spinner */
}

.submit-btn:hover:not(:disabled) {
    background-color: var(--accent-color-dark);
    transform: translateY(-1px);
}

.submit-btn:disabled {
    background-color: #9e9e9e;
    cursor: not-allowed;
}

.spinner {
    display: flex;
    justify-content: center;
    align-items: center;
}

.spinner img {
    width: 24px;
    height: 24px;
    animation: spin 1s linear infinite;
}

.spinner svg {
    width: 24px;
    height: 24px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.fortune-card, .error-card {
    padding: 20px;
    border-radius: var(--border-radius);
    text-align: center;
    position: relative; /* For sparkle images */
}

.fortune-card {
    background: linear-gradient(135deg, var(--accent-color), #ce93d8); /* Purple gradient */
    color: white;
    box-shadow: 0 6px 12px rgba(106, 27, 154, 0.3);
    animation: fadeInScaleUp 0.5s ease-out;
}
.fortune-card h3 {
    margin-top: 0;
}
.fortune-card p {
    font-size: 1.1em;
    line-height: 1.6;
}

.magic-orb-img {
    width: 80px;
    height: 80px;
    margin-bottom: 15px;
    animation: float 3s ease-in-out infinite;
}

.sparkle-img {
    position: absolute;
    width: 25px;
    height: 25px;
    opacity: 0.8;
    animation: sparkleShine 2s infinite alternate;
}
.sparkle-img.top-left { top: 10px; left: 10px; }
.sparkle-img.bottom-right { bottom: 10px; right: 10px; }


@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

@keyframes sparkleShine {
    0% { opacity: 0.3; transform: scale(0.8); }
    100% { opacity: 0.8; transform: scale(1.2); }
}


.error-card {
    background-color: var(--error-color);
    color: white;
    box-shadow: 0 4px 8px rgba(211, 47, 47, 0.3);
    animation: fadeIn 0.3s ease-out;
}

@keyframes fadeInScaleUp {
    from {
        opacity: 0;
        transform: scale(0.9);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Animations for fortune card appearance */
.fortune-reveal-enter-active {
    animation: fadeInScaleUp 0.5s ease-out;
}


footer {
    text-align: center;
    margin-top: 30px;
    font-size: 0.8em;
    color: var(--primary-text);
    opacity: 0.7;
}

/* Responsive adjustments */
@media (max-width: 600px) {
    body {
        padding: 10px;
    }
    #app {
        padding: 15px;
    }
    .keyword-inputs {
        flex-direction: column;
    }
    header h1 {
        font-size: 1.8em;
    }
}
</style>
