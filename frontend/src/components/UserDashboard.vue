<template>
  <div class="user-dashboard">
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
            <h2 class="text-center">Welcome to User Dashboard</h2>
            <br> <br> 
            

            <!-- Search Bar -->
            <div class="input-group mb-3">
              <input
                type="text"
                class="form-control"
                v-model="searchQuery"
                @input="search"
                placeholder="Search venues and shows"
              />
            </div>
            

            <!-- Shows Table -->
            <div class="table-responsive">
              <h3 class="text-center">Shows</h3>
              <table class="table table-bordered">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th>available_seats</th>
                    <th>Venue Name/Place</th>
                    <th>Venue City</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="show in shows" :key="show.id">
                    <td>{{ show.show_name }}</td>
                    <td>{{ show.date }}</td>
                    <td>{{ show.time }}</td>
                    <td>{{ show.available_seats }}</td>
                    <td>{{ show.venue.name }},{{ show.venue.place }}</td>
                    <td>{{ show.venue.city }}</td>
                    <td>
                      <router-link :to="'/bookings/' + show.id"
                        >Book Show</router-link
                      >
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-for="booking in bookings" :key="booking.id">
      <h2>Booking Information</h2>
      <p>ID: {{ booking.id }}</p>
      <p>Show ID: {{ booking.show_id }}</p>
      <p>Number of Seats: {{ booking.number_of_seats }}</p>

      <div v-if="showDetails[booking.show_id]">
        <p>Show Name: {{ showDetails[booking.show_id].show_name }}</p>
        <p>Show Date: {{ showDetails[booking.show_id].date }}</p>
        <p>Show Time: {{ showDetails[booking.show_id].time }}</p>
        <p>Venue Name: {{ showDetails[booking.show_id].venue.name }}</p>
        <p>Venue City: {{ showDetails[booking.show_id].venue.city }}</p>
        
        
      </div>

      <div v-else>
        <p>No show information available for this booking.</p>
      </div>
    </div>

    <br />
    <br />
    <button @click="logout" class="btn btn-danger">Logout</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      token: "",
      venues: [],
      shows: [],
      searchQuery: "",
      booking_list:[],
      booking: null,
      bookings: [],
      showDetails: {},
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
  
    fetchVenues() {
      const path = "http://127.0.0.1:5000/admindashboard/venues";
      axios
        .get(path,this.axiosConfig)
        .then((response) => {
          this.venues = response.data.venues;
        })
        .catch((error) => {
          console.error("Error fetching venues:", error);
        });
    },
    fetchShows() {
      const path="http://127.0.0.1:5000/admindashboard/shows";
      axios
        .get(path,this.axiosConfig)
        .then((response) => {
          this.shows = response.data.shows;
        })
        .catch((error) => {
          console.error("Error fetching shows:", error);
        });
    },
    fetchShowDetails(showId) {
      const path=`http://127.0.0.1:5000/admindashboard/shows/${showId}`;
      axios
        .get(path,this.axiosConfig)
        .then((response) => {
          this.$set(this.showDetails, showId, response.data);
        })
        .catch((error) => {
          console.error(`Error fetching show details for show ID ${showId}:`, error);
        });
    },
    fetchBookings() {
      const path="http://127.0.0.1:5000/bookings";
      axios
        .get(path,this.axiosConfig)
        .then((response) => {
          this.bookings = response.data.bookings;
          this.bookings.forEach((booking) => {
            this.fetchShowDetails(booking.show_id);
          });
        })
        .catch((error) => {
          console.error("Error fetching bookings:", error);
        });
    },
    search() {
      axios.get(`http://127.0.0.1:5000/search/venues?query=${this.searchQuery}`)
        .then((response) => {
          this.venues = response.data.venues;
        })
        .catch((error) => {
          console.error('Error while searching venues:', error);
        });

      axios.get(`http://127.0.0.1:5000/search/shows?query=${this.searchQuery}`)
        .then((response) => {
          this.shows = response.data.shows;
        })
        .catch((error) => {
          console.error('Error while searching shows:', error);
        });
    },
    bookShow(show) {
      this.$router.push({ name: 'BookShow', params: { showId: show.id } });
    },
    logout() {
      this.$router.push({ name: "UserLogin" });
    },
  },
  created() {
    let token = localStorage.getItem("access_token");
    if (token == null){
      this.$router.push("/user_login");
    } 
    this.fetchVenues();
    this.fetchShows();
    this.fetchBookings();
  },
};
</script>
