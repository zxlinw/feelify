<template>
  <div id="app" class="max-w-md mx-auto mt-16 text-center font-sans p-4">
    <h1 class="text-3xl font-bold mb-6 text-blue-600">Feelify 🎵</h1>

    <form @submit.prevent="fetchPlaylist" class="flex flex-col sm:flex-row items-center justify-center gap-3 mb-6">
      <input
        v-model="emotion"
        placeholder="How are you feeling?"
        class="w-full sm:w-2/3 px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
      <button
        type="submit"
        class="bg-blue-500 hover:bg-blue-600 text-white font-medium px-4 py-2 rounded-lg transition"
      >
        Get Playlist
      </button>
    </form>

    <div v-if="playlistUrl" class="mb-4">
      <p class="font-semibold text-gray-700 mb-1">Spotify Playlist:</p>
      <a :href="playlistUrl" target="_blank" class="text-blue-500 underline break-all">{{ playlistUrl }}</a>
    </div>

    <p v-if="error" class="text-red-500 font-medium">{{ error }}</p>
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
        const res = await fetch(`http://127.0.0.1:8000/api/get-playlist/?emotion=${emotion.value}`)
        const data = await res.json()

        if (data && data.playlist_url) {
          playlistUrl.value = data.playlist_url
        } else {
          error.value = 'No playlist found.'
        }
      } catch (err) {
        error.value = 'Error fetching playlist.'
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
/* No custom styles needed since Tailwind CSS handles everything */
</style>
