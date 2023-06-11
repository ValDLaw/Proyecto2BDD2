<template>
  <div class="scrollable-content">
    <div class="background-image"></div>
    <div class="search-container">
      <div class="search-input">
        <input type="text" v-model="searchTerm" placeholder="Buscar" />
        <input type="number" v-model.number="topK" placeholder="Cantidad K" />
        <button @click="search" class="search-button">Buscar</button>
      </div>

      <ul v-if="searchResults.length > 0" class="search-results">
        <li v-for="(item, index) in searchResults" :key="index">{{ item }}</li>
      </ul>

      <p v-else class="no-results" v-if="searched && searchResults.length === 0">
        No se encontraron resultados.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchTerm: '',
      topK: 5, // Valor predeterminado para el top K
      dictionary: {
        // Diccionario ejemplo de prueba
        apple: 'manzana',
        banana: 'plátano',
        cherry: 'cereza',
        orange: 'naranja',
        peach: 'durazno',
        pineapple: 'piña',
      },
      searchResults: [],
    };
  },
  methods: {
    search() {
      const results = [];
      const searchTerm = this.searchTerm.toLowerCase();
      let count = 0;

      // Logica para coincidencias

      this.searchResults = results;
    },
  },
};
</script>

<style scoped>
.scrollable-content {
  position: relative;
  overflow-y: scroll;
  height: 100vh;
}

.background-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background-image: url('./assets/cornell_university.avif');
  opacity: 0.8;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  transition: opacity 0.2s ease;
}

.fixed-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100px;
  background-color: #ffffff;
  z-index: 1;
}

.logo-image {
  display: block;
  width: 100px;
  height: 100px;
  margin: 20px;
}

.search-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  margin: 0 auto;
  background-color: white;
  padding: 20px;
}

.search-input {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.search-input input[type="text"],
.search-input input[type="number"] {
  padding: 8px;
  font-size: 14px;
  border-radius: 4px;
  border: 1px solid #ccc;
  outline: none;
}

.search-input button {
  padding: 8px 12px;
  font-size: 14px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-results {
  list-style: none;
  padding: 0;
}

.search-results li {
  margin-bottom: 4px;
}

.no-results {
  color: #ff0000;
  font-style: italic;
}
</style>
