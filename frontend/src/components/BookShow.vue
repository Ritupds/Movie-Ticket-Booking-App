
<template>
  <div>
    <div class="container">
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cosmo/bootstrap.min.css" integrity="sha384-5QFXyVb+lrCzdN228VS3HmzpiE7ZVwLQtkt+0d9W43LQMzz4HBnnqvVxKg6O+04d" crossorigin="anonymous">
      <h1>Booking Form</h1>
      <form @submit.prevent="bookShow">
        <label for="show_id">Select a Show:</label>
        <select v-model="formData.show_id" required>
          <!-- Populate this dropdown with available shows from your database -->
          <option v-for="show in shows" :key="show.id" :value="show.id">{{ show.show_name }}</option>
        </select>
        <br>

        <label for="number_of_seats">Number of Seats:</label>
        <input type="number" v-model="formData.number_of_seats" required>
        <br>

        <button type="submit">Book</button>
      </form>
      <div id="message">{{ message }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      token:"",
      formData: {
        show_id: '',
        number_of_seats: 1, // Default value
      },
      shows: [], 
      message: '',
    };
  },
  computed:{
    axiosConfig(){
      let token = localStorage.getItem("access_token");
      return {
        headers: {
          Authorization: `Bearer ${token}`,
        }
      }
    }
  },
  methods: {
    bookShow() {
      const path="http://127.0.0.1:5000/bookings"
      axios
        .post(path, this.formData, this.axiosConfig) 
        
        .then(()=> {
            this.error="";
            if (this.$route.name !== "UserDashboard") {
              this.$router.push({ name: "UserDashboard" });
              this.message = "You have booked a show registered successfully. have fun!.";
            }
          })
        .catch((error) => {
          this.message = error.response.data.message;
        });
    },
  },
  mounted() {
    // Fetch available shows from your Flask API and populate this.shows
    axios.get('http://127.0.0.1:5000/admindashboard/shows', this.axiosConfig) 
      
    .then((response) => {
        this.shows = response.data.shows;
      })
      .catch((error) => {
        console.error('Error fetching shows:', error);
      });
  },
  created() {
    let token = localStorage.getItem("access_token");
    if (token == null){
      this.$router.push("/user_login");
    }

    
    
  },
};
</script>