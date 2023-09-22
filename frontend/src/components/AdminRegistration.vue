<template>
    <div class="admin-register">
        <div class="jumbotron vertical-cent">
        <div class="container">
          <!-- Add the Bootstrap stylesheet link here -->
          <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cosmo/bootstrap.min.css" integrity="sha384-5QFXyVb+lrCzdN228VS3HmzpiE7ZVwLQtkt+0d9W43LQMzz4HBnnqvVxKg6O+04d" crossorigin="anonymous">
  
          <div class="row">
            <div class="col-sm-12">
              <br /><br />
              <h1 class="text-center">Admin Registration</h1>
      
      <form @submit.prevent="registerAdmin">
        <div class="form-group">
          <label for="name">Name:</label>
          <input v-model="name" type="text" id="name" required>
        </div>
        <div class="form-group">
          <label for="email">email:</label>
          <input v-model="email" type="text" id="email" required>
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input v-model="password" type="password" id="password" required>
        </div>
<br> <br> 
    <button type="submit" class="btn btn-primary">Register</button>
      </form>

      

            </div>
            </div>
        </div>
        </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        name: '',
        email: '',
        password: '',
        // role:'',
      };
    },
    methods: {
      registerAdmin() {
        axios
          .post('http://127.0.0.1:5000/adminregister', {
            name: this.name,
            email: this.email,
            password: this.password,
          })
          .then(response => {
            console.log(response.data.message);
            
          })
          .catch(error => {
            console.error(error);
            
          });
      },
    },
  };
  </script>