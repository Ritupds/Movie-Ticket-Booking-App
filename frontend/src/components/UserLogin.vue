<template>
  <div class="user-login">
    <div class="jumbotron vertical-cent">
      <div class="container">
        <!-- Add the Bootstrap stylesheet link here -->
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cosmo/bootstrap.min.css"
          integrity="sha384-5QFXyVb+lrCzdN228VS3HmzpiE7ZVwLQtkt+0d9W43LQMzz4HBnnqvVxKg6O+04d"
          crossorigin="anonymous"
        />

        <div class="row">
          <div class="col-sm-12">
            <br /><br />
            <h1 class="text-center">User Login</h1>

            <form @submit.prevent="login">
              <div class="form-group">
                <label for="Email">Email</label>
                <input type="text" id="Email" v-model="email" class="form-control" required />
              </div>
              <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" v-model="password" class="form-control" required />
              </div>
              <button type="submit" class="btn btn-primary">Login</button>
            </form>
            <br /><br />
            <!-- Add a button to navigate to the registration page -->
            <button @click="navigateToRegister">Register</button>
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
      email: '',
      password: '',
    };
  },
  methods: {
    login() {
      const loginData = {
        email: this.email,
        password: this.password,
      };

      axios
        .post('http://127.0.0.1:5000/user_login', loginData)
        .then((response) => {
          if (response.status === 200) {
            localStorage.setItem('access_token', response.data.access_token);
            if (response.data.is_admin === false) {
              this.$router.push('/userdashboard');
            } else {
              this.error = 'Invalid username or password';
            }
          }
        });
    },
    navigateToRegister() {
      this.$router.push('/userregistration'); // Navigate to the registration page
    },
  },
};
</script>
