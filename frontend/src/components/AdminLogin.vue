<template>
    <div class="admin-login">
      <h1>Admin Login</h1>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">Email</label>
          <input type="text" id="email" v-model="email" class="form-control" required>
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>

      <br><br>
      <button @click="navigateToRegister">Register</button>
    </div>
  </template>
  
  <script>
import axios from 'axios';

//   import axios from 'axios';
  
  export default {
    data() {
      return {
        email: '',
        password: '',
      };
    },
    methods: {
      login() {
        axios
        .post('http://127.0.0.1:5000/admin_login', {
          email: this.email,
          password: this.password,
        })
        .then(response => {
          const accessToken = response.data.access_token;
          // Store the access token in local storage or Vuex store
          localStorage.setItem('access_token', accessToken);
          // Optionally, you can redirect the user to their dashboard
          this.$router.push('/admindashboard');
        })
        .catch(error => {
          console.error(error);
        });
    },
    navigateToRegister() {
      this.$router.push('/adminregister'); // Navigate to the registration page
    },
  },
  created(){
    if (localStorage.getItem('access_token')) {
      axios
        .get('http://127.0.0.1:5000/check_login',{
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('access_token')
          }
        })
        .then((response)=> {
          if (response.status==200){
            if (response.data.is_admin === true) {
              this.$router.push('/admindashboard');
            } 
            else {
              this.$router.push('/userdashboard');
            }
          }
        })
        .catch((error)=>{
          localStorage.removeItem('access_token');
          console.error(error);
        });
      } else{
        localStorage.removeItem('access_token');
      }


      }  
        }

  </script>
  
 