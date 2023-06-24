

<template>
  <div class="scrollable-content">
    <div class="background-image"></div>
    <header v-fadeout="{ scrollThreshold: 100 }" class="header-container">
      <img src="./assets/arxiv_logo.png" alt="Logo" class="logo" />
      <h1 class="typing-title">Open-access archive for +2.2M articles</h1>
    </header>
    <div class="search-container">
      <div class="search-input">
        <input type="text" v-model="searchTerm" placeholder="Search scholarly articles" />
        <input type="number" v-model.number="topK" placeholder="Cantidad K" />
        <button @click="search" class="search-button">Search</button>
      </div>
    </div>

    <div id="scroll-target" class="container">
      <div class="button-container">
        <button
          :class="{ 'active': activeButton === 'tablaA' }"
          @click="seleccionarTabla('tablaA')"
          class="selection-button"
        >
          PostgreSQL
        </button>
        <button
          :class="{ 'active': activeButton === 'tablaB' }"
          @click="seleccionarTabla('tablaB')"
          class="selection-button"
        >
          MongoDB
        </button>
        <button
          :class="{ 'active': activeButton === 'tablaC' }"
          @click="seleccionarTabla('tablaC')"
          class="selection-button"
        >
          Self II
        </button>
      </div>

      <div class="tiempo-ejecucion">
          Tiempo de ejecución de la consulta: {{ tiempo_consulta }} segundos
      </div>

      <div class="pagination-buttons">
        <button class="pagination-button" :class="{ disabled: currentPage === 1 }" @click="previousPage">Previous</button>
        <button class="pagination-button" @click="nextPage">Next</button>
      </div>
      
      <!-- Aquí se mostrará la tabla seleccionada -->
      <div v-if="tablaSeleccionada === 'tablaA'" class="tabla-container">
        <table>
          <thead>
            <tr>
              <th v-for="header in tableAHeaders" :key="header.text">{{ header.text }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="result in tableAResults" :key="result[0]">
              <td>{{ result[0] }}</td>
              <td>{{ result[1] }}</td>
              <td>{{ result[2] }}</td>
              <td>{{ result[3] }}</td>
              <td>{{ result[4] }}</td>
              <td>{{ result[5] }}</td>
              <td>{{ result[6] }}</td>
              <td>{{ result[7] }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="tablaSeleccionada === 'tablaB'" class="tabla-container">
        <table>
          <thead>
            <tr>
              <th v-for="header in tableBHeaders" :key="header.text">{{ header.text }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="result in tableBResults" :key="result.value">
              <td>{{ result.id }}</td>
              <td>{{ result.submitter }}</td>
              <td>{{ result.authors }}</td>
              <td>{{ result.title }}</td>
              <td>{{ result.categories }}</td>
              <td>{{ result.abstract }}</td>
              <td>{{ result.update_date }}</td>
              <td>{{ result.authors_parsed }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="tablaSeleccionada === 'tablaC'" class="tabla-container">
        <table>
          <thead>
            <tr>
              <th v-for="header in tableCHeaders" :key="header.text">{{ header.text }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="result in tableCResults" :key="result.value">
              <td>{{ result.id }}</td>
              <td>{{ result.submitter }}</td>
              <td>{{ result.authors }}</td>
              <td>{{ result.title }}</td>
              <td>{{ result.categories }}</td>
              <td>{{ result.abstract }}</td>
              <td>{{ result.update_date }}</td>
              <td>{{ result.authors_parsed }}</td>
            </tr>
          </tbody>
        </table>
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
      tablaSeleccionada: 'tablaC',
      activeButton: 'tablaC',
      tiempo_consulta: 0,
      topK: 5,
      currentPage: 1,
      itemsPerPage: 5,
      tableAHeaders: [
        { text: 'ID', value: 'id' },
        { text: 'Submitter', value: 'submitter' },
        { text: 'Authors', value: 'authors' },
        { text: 'Title', value: 'title' },
        { text: 'Categories', value: 'categories' },
        { text: 'Abstract', value: 'abstract' },
        { text: 'Update Date', value: 'update_date' },
        { text: 'Authors Parsed', value: 'authors_parsed' },
      ],
      tableBHeaders: [
        { text: 'ID', value: 'id' },
        { text: 'Submitter', value: 'submitter' },
        { text: 'Authors', value: 'authors' },
        { text: 'Title', value: 'title' },
        { text: 'Categories', value: 'categories' },
        { text: 'Abstract', value: 'abstract' },
        { text: 'Update Date', value: 'update_date' },
        { text: 'Authors Parsed', value: 'authors_parsed' },
      ],
      tableCHeaders: [
        { text: 'ID', value: 'id' },
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
      tableCResults: [],
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
      this.activeButton = tabla;
      this.search();
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
      } else if (this.tablaSeleccionada === 'tablaC') {
        this.searchTableC();
      }
      const scrollElement = document.getElementById('scroll-target');
  
      if (scrollElement) {
        scrollElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    },

    searchTableA() {
      axios
        .post('http://127.0.0.1:5016/consulta', {
          parametro: this.searchTerm,
          k: this.topK,
        }, {
          withCredentials: true, // Habilita CORS
        })
        .then((response) => {
          console.log(response.data)
          const allResults = response.data.resultados;
          const startIndex = (this.currentPage - 1) * this.itemsPerPage;
          const endIndex = startIndex + this.itemsPerPage;
          this.tableAResults = allResults.slice(startIndex, endIndex);
          this.tiempo_consulta = response.data.tiempo_ejecucion;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    searchTableB() {
      axios
        .post('http://127.0.0.1:5011/consulta', {
          parametro: this.searchTerm,
          k: this.topK,
        }, {
          withCredentials: true, // Habilita CORS
        })
        .then((response) => {
          console.log(response.data)
          const allResults = response.data.resultados;
          const startIndex = (this.currentPage - 1) * this.itemsPerPage;
          const endIndex = startIndex + this.itemsPerPage;
          this.tableBResults = allResults.slice(startIndex, endIndex);
          this.tiempo_consulta = response.data.tiempo_ejecucion;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    searchTableC() {
      axios
        .post('http://127.0.0.1:5023/consulta', {
          parametro: this.searchTerm,
          k: this.topK,
        }, {
          withCredentials: true, // Habilita CORS
        })
        .then((response) => {
          console.log(response.data)
          const allResults = response.data.resultados;
          const startIndex = (this.currentPage - 1) * this.itemsPerPage;
          const endIndex = startIndex + this.itemsPerPage;
          this.tableCResults = allResults.slice(startIndex, endIndex);
          this.tiempo_consulta = response.data.tiempo_ejecucion;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    nextPage() {
      if (this.currentPage - 1 < this.topK/this.itemsPerPage) {
        this.currentPage++;
        this.search();
      }
    },
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.search();
      }
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

.header-container {
  margin-top: 25px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.logo {
  height: 130px; /* Ajusta la altura según tu logo */
  margin-bottom: 170px; /* Espacio entre el logo y el título */
}

#scroll-target {
  scroll-behavior: slow;
}

@keyframes typing {
  from {
    width: 0;
  }
  to {
    width: 100%;
  }
}

.typing-title {
  overflow: hidden;
  font-family: "Courier New";
  white-space: nowrap;
  animation: typing 3s steps(40) 1s infinite;
}


.background-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background-image: url('./assets/cornell_university.avif');
  opacity: 0.7;
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
  background-color: #a61d1b;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.container {
  background-color: white;
  margin-top: 1000px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: fit-content;
}

.button-container {
  display: flex;
  justify-content: center;
  margin-top: 0px;
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
  background-color: #a61d1b;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 0 10px;
}

.pagination-buttons {
  text-align: center;
  margin-top: 10px;
}

.pagination-button {
  padding: 8px 16px;
  border-radius: 4px;
  background-color: #4caf50;
  color: white;
  font-size: 14px;
  cursor: pointer;
  border: none;
  margin-right: 5px;
}

.pagination-button:hover {
  background-color: #45a049;
}

.pagination-button.disabled {
  background-color: #dddddd;
  cursor: not-allowed;
}

.selection-button.active {
  background-color: #f70804;
  color: #fff;
}

.tiempo-ejecucion {
        color: #333;
        font-family: "Courier New";
        font-weight: bold;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
    }

.tabla-container table {
  width: 100%;
  border-collapse: collapse;
}

.tabla-container th,
.tabla-container td {
  padding: 10px;
  text-align: center;
  font-family: "Courier New";
  border-bottom: 1px solid #ccc;
}

.tabla-container th {
  background-color: #f2f2f2;
  font-weight: bold;
  text-align: center;
}

.tabla-container tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.tabla-container tbody tr:hover {
  background-color: #e9e9e9;
}



</style>
