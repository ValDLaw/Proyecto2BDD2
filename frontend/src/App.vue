

<template>
  <div class="scrollable-content">
    <div class="background-image"></div>
    <header v-fadeout="{ scrollThreshold: 100 }">
      <!-- Aquí va tu logo -->
      <img src="./assets/arxiv_logo.png" alt="Logo" />
    </header>
    <div class="search-container">
      <div class="search-input">
        <input type="text" v-model="searchTerm" placeholder="Search scholarly articles" />
        <input type="number" v-model.number="topK" placeholder="Cantidad K" />
        <button @click="search" class="search-button">Search</button>
      </div>
    </div>

    <div class="container">
      <div class="button-container">
        <button @click="seleccionarTabla('tablaA')" class="selection-button">Tabla A</button>
        <button @click="seleccionarTabla('tablaB')" class="selection-button">Tabla B</button>
        <button @click="seleccionarTabla('tablaC')" class="selection-button">Tabla C</button>
      </div>
      
      <!-- Aquí se mostrará la tabla seleccionada -->
      <div v-if="tablaSeleccionada === 'tablaA'" class="tabla-container">
        <table class="my-table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Edad</th>
              <th>País</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(persona, index) in listaPersonas" :key="index">
              <td>{{ persona.nombre }}</td>
              <td>{{ persona.edad }}</td>
              <td>{{ persona.pais }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="tablaSeleccionada === 'tablaB'" class="tabla-container">
        <!-- Código HTML de la tabla B -->
      </div>
      <div v-if="tablaSeleccionada === 'tablaC'" class="tabla-container">
        <!-- Código HTML de la tabla C -->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  directives: {
    fadeout: {
      inserted: function(el, binding) {
        const scrollThreshold = binding.value.scrollThreshold || 100;
        let lastScrollTop = window.pageYOffset || document.documentElement.scrollTop;

        window.addEventListener('scroll', function() {
          const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
          const isScrolled = scrollTop > lastScrollTop;

          if (isScrolled && scrollTop > scrollThreshold) {
            el.style.opacity = '0';
          } else {
            el.style.opacity = '1';
          }

          lastScrollTop = scrollTop;
        });
      },
    },
  },
  data() {
    return {
      isScrolled: false,
      searchTerm: '',
      tablaSeleccionada: 'tablaA',
      topK: 5, // Valor predeterminado para el top K
      listaPersonas: [
        { nombre: "Juan", edad: 25, pais: "Argentina" },
        { nombre: "María", edad: 30, pais: "España" },
        { nombre: "Carlos", edad: 40, pais: "México" },
        { nombre: "Juan", edad: 25, pais: "Argentina" },
        { nombre: "María", edad: 30, pais: "España" },
        { nombre: "Carlos", edad: 40, pais: "México" },
        
      ],
      searchResultsColumn1: [],
      searchResultsColumn2: [],
    };
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    search() {
      const resultsColumn1 = [];
      const resultsColumn2 = [];
      const searchTerm = this.searchTerm.toLowerCase();
      let count = 0;

      // Lógica para coincidencias y distribución en columnas
      for (const key in this.dictionary) {
        if (key.includes(searchTerm)) {
          if (count < this.topK) {
            if (count % 2 === 0) {
              resultsColumn1.push(this.dictionary[key]);
            } else {
              resultsColumn2.push(this.dictionary[key]);
            }
            count++;
          } else {
            break;
          }
        }
      }

      this.searchResultsColumn1 = resultsColumn1;
      this.searchResultsColumn2 = resultsColumn2;
    },
    seleccionarTabla(tabla) {
      this.tablaSeleccionada = tabla;
    },
    handleScroll() {
      this.isScrolled = window.pageYOffset > 0;
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
.scrollable-content {
  position: relative;
  overflow-y: scroll;
  height: 100vh;
}

header {
  transition: opacity 0.3s;
}

header img {
  height: 100px; /* Ajusta la altura según tu logo */
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
  max-width: 400px;
  margin: 0 auto;
  background-color: white;
  padding: 20px;
  font-family: 'Roboto', sans-serif;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-input {
  display: flex;
  flex-direction: column;
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
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.button-container {
  display: flex;
  justify-content: center;
  margin-top: 800px;
  width: 60%;
  height: fit-content;
  background-color: white;
  padding: 20px;
  font-family: 'Roboto', sans-serif;
  text-align: center;
}

.selection-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 0 10px;
}

.my-table {
  width: 100%;
  border-collapse: collapse;
}

.my-table th,
.my-table td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ccc;
}

.my-table th {
  background-color: #f2f2f2;
}

.my-table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.my-table tbody tr:hover {
  background-color: #e9e9e9;
}
.tabla-container {
  background-color: white;
  width: 100%;
}
</style>
