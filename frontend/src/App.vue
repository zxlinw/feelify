<template>
  <div id="app">
    <!-- Title Row -->
    <header>
      <h1>Feelify 🎵</h1>
    </header>

    <!-- Form Row -->
    <section class="input-section">
      <form @submit.prevent="fetchPlaylist">
        <input v-model="emotion" placeholder="How are you feeling?" />
        <button type="submit">Get Playlist</button>
      </form>
    </section>

    <!-- Result Row -->
    <section class="result-section">
      <div v-if="playlistUrl">
        <p><strong>Spotify Playlist:</strong></p>
        <a :href="playlistUrl" target="_blank">{{ playlistUrl }}</a>
      </div>
      <p v-else-if="error" class="error">{{ error }}</p>
    </section>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue'

export default {
  setup() {
    const emotion = ref('')
    const playlistUrl = ref('')
    const error = ref('')

    const fetchPlaylist = async () => {
      try {
        error.value = ''
        playlistUrl.value = ''
        const res = await fetch(`http://127.0.0.1:8000/api/get-playlist/?emotion=${emotion.value}`)
        const data = await res.json()

        if (data && data.playlist_url) {
          playlistUrl.value = data.playlist_url
        } else {
          error.value = 'No playlist found.'
        }
      } catch (err) {
        error.value = 'Error fetching playlist.'
        playlistUrl.value = ''
        console.error(err)
      }
    }

    return {
      emotion,
      playlistUrl,
      error,
      fetchPlaylist
    }
  }
}
</script>

<style>
/* Reset and base styling */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
body {
  background-color: #1e1e2f;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #ffffff;
  min-height: 100vh;
}

/* Main container layout */
#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  padding: 2rem;
  justify-content: center;
  position: relative;
}

/* Title styling */
header h1 {
  color: #4ea8de;
  font-size: 3rem;
  margin-bottom: 2rem;
  text-align: center;
}

/* Form section */
.input-section {
  width: 100%;
  display: flex;
  justify-content: center;
}
form {
  display: flex;
  gap: 10px;
  width: 100%;
  max-width: 500px;
}
input {
  padding: 10px;
  border-radius: 8px;
  border: none;
  flex: 1;
  font-size: 1rem;
}
button {
  padding: 10px 16px;
  background-color: #4ea8de;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
button:hover {
  background-color: #3a88b8;
}

/* Result section always takes up space to avoid layout shift */
.result-section {
  text-align: center;
  margin-top: 2rem;
  min-height: 3rem;
}
.result-section a {
  color: #93c5fd;
  word-break: break-word;
}
.error {
  color: #ff6b6b;
  font-weight: bold;
}
</style>
