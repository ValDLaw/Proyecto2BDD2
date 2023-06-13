

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
        <v-data-table
          :headers="tableAHeaders"
          :items="tableAResults"
          class="elevation-1"
        ></v-data-table>
      </div>
      <div v-if="tablaSeleccionada === 'tablaB'" class="tabla-container">
        <v-data-table
          :headers="tableBHeaders"
          :items="tableBResults"
          class="elevation-1"
        ></v-data-table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { assertExpressionStatement } from '@babel/types';

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
      // Headers de las tablas
      tableAHeaders: [
        { text: 'Value', value: 'value' },
        { text: 'Submitter', value: 'submitter' },
        { text: 'Authors', value: 'authors' },
        { text: 'Title', value: 'title' },
        { text: 'Categories', value: 'categories' },
        { text: 'Abstract', value: 'abstract' },
        { text: 'Update Date', value: 'update_date' },
        { text: 'Authors Parsed', value: 'authors_parsed' },
      ],
      tableBHeaders: [
        { text: 'Value', value: 'value' },
        { text: 'Submitter', value: 'submitter' },
        { text: 'Authors', value: 'authors' },
        { text: 'Title', value: 'title' },
        { text: 'Categories', value: 'categories' },
        { text: 'Abstract', value: 'abstract' },
        { text: 'Update Date', value: 'update_date' },
        { text: 'Authors Parsed', value: 'authors_parsed' },
      ],

      // Resultados de las consultas a las tablas
      tableAResults: [],
      tableBResults: [],
    };
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    seleccionarTabla(tabla) {
      this.tablaSeleccionada = tabla;
    },
    handleScroll() {
      this.isScrolled = window.pageYOffset > 0;
    },
    search() {
      // Realizar la búsqueda según la tabla seleccionada
      if (this.tablaSeleccionada === 'tablaA') {
        this.searchTableA();
      } else if (this.tablaSeleccionada === 'tablaB') {
        this.searchTableB();
      }
    },

    searchTableA() {
      axios
        .post('http://127.0.0.1:5002/consulta', {
          parametro: this.searchTerm,
          k: this.topK,
        }, {
          withCredentials: true, // Habilita CORS
        })
        .then((response) => {
          print("hola")
          this.tableAResults = response.data.resultados;
          this.tableAResults = resultados.map((resultado) => ({
            value: resultado.value,
            submitter: resultado.submitter,
            authors: resultado.authors,
            title: resultado.title,
            categories: resultado.categories,
            abstract: resultado.abstract,
            update_date: resultado.update_date,
            authors_parsed: resultado.authors_parsed,
          }));
        })
        .catch((error) => {
          console.error(error);
        });
    },

    searchTableB() {
      axios
        .post('http://127.0.0.1:5001/consulta', {
          parametro: this.searchTerm,
          k: this.topK,
        })
        .then((response) => {
          this.tableBResults = response.data.resultados;
        })
        .catch((error) => {
          console.error(error);
        });
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
  justify-content: center;
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
