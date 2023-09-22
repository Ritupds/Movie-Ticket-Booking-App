<template>
  <div class="admin-dashboard">
    <!-- Venue Details Section -->
    <div class="jumbotron vertical-cent">
      <!-- ... Your Venue Details Template ... -->
      <div class="container">
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cosmo/bootstrap.min.css"
          integrity="sha384-5QFXyVb+lrCzdN228VS3HmzpiE7ZVwLQtkt+0d9W43LQMzz4HBnnqvVxKg6O+04d"
          crossorigin="anonymous"
        />
        <div class="row">
          <div class="col-sm-12">
            <br /><br />

            <h1>Venue Details</h1>
            <hr />
            <br />
            <!--alert messg-->
            <b-alert variant="success" v-if="showMessage" show>
              {{ message }}
            </b-alert>
            <button
              type="button"
              class="btn btn-success btn-sm"
              v-b-modal.venue-modal
            >
              Add Venue
            </button>

            <br /><br />
            <table class="table table-hover">
              <thead>
                <tr>
                  <!--table header cells-->
                  <th scope="col">Venue Name</th>
                  <th scope="col">Venue Place</th>
                  <th scope="col">Venue City</th>
                  <th scope="col">Venue Capacity</th>
                  
                  <th scope="col">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(venue, index) in venues" :key="index">
                  <td>{{ venue.name }}</td>
                  <td>{{ venue.place }}</td>
                  <td>{{ venue.city }}</td>
                  <td>{{ venue.capacity }}</td>
                  <td>
                    <div class="btn-group" role="group">
                      <button
                        type="button"
                        class="btn btn-info btn-sm"
                        v-b-modal.venue-update-modal
                        @click="venueEditModel(venue)"
                      >
                        Update
                      </button>
                      <button
                        type="button"
                        class="btn btn-danger btn-sm"
                        @click="deleteVenue(venue)"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!--first modal-->
        <b-modal
          ref="addVenueModal"
          id="venue-modal"
          title="Add a new venue"
          hide-backdrop
          hide-footer
        >
          <b-form @submit="onVenueSubmit" @reset="onReset" class="w-100">
            <b-form-group
              id="form-name-group"
              label="Name:"
              label-for="form-name-input"
            >
              <b-form-input
                id="form-name-input"
                type="text"
                v-model="addVenueForm.name"
                placeholder="Enter venue"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-place-group"
              label="Place:"
              label-for="form-place-input"
            >
              <b-form-input
                id="form-place-input"
                type="text"
                v-model="addVenueForm.place"
                placeholder="Enter place"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-city-group"
              label="City:"
              label-for="form-city-input"
            >
              <b-form-input
                id="form-city-input"
                type="text"
                v-model="addVenueForm.city"
                placeholder="Enter city"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-capacity-group"
              label="Capacity:"
              label-for="form-capacity-input"
            >
              <b-form-input
                id="form-capacity-input"
                type="number"
                v-model="addVenueForm.capacity"
                placeholder="Enter capacity"
              >
              </b-form-input>
            </b-form-group>

            <b-button type="submit" variant="outline-info">Submit</b-button>
            <b-button type="reset" variant="outline-danger">Reset</b-button>
          </b-form>
        </b-modal>

        <!-- start of modal 2 -->

        <b-modal
          ref="editVenueModal"
          id="venue-update-modal"
          title="Update"
          hide-backdrop
          hide-footer
        >
          <b-form @submit="onUpdateVenue" @reset="onResetUpdate" class="w-100">
            <b-form-group
              id="form-name-edit-group"
              label="Name:"
              label-for="form-name-edit-input"
            >
              <b-form-input
                id="form-name-edit-input"
                type="text"
                v-model="editForm.name"
                required
                placeholder="Enter venue"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-place-edit-group"
              label="Place:"
              label-for="form-place-edit-input"
            >
              <b-form-input
                id="form-place-edit-input"
                type="text"
                v-model="editForm.place"
                required
                placeholder="Enter place"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-city-edit-group"
              label="City:"
              label-for="form-city-edit-input"
            >
              <b-form-input
                id="form-city-edit-input"
                type="text"
                v-model="editForm.city"
                required
                placeholder="Enter city"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-capacity-edit-group"
              label="Capacity:"
              label-for="form-capacity-edit-input"
            >
              <b-form-input
                id="form-capacity-edit-input"
                type="number"
                v-model="editForm.capacity"
                required
                placeholder="Enter capacity"
              >
              </b-form-input>
            </b-form-group>

            <b-button type="submit" variant="outline-info">Submit</b-button>
            <b-button type="cancel" variant="outline-danger">cancel</b-button>
          </b-form>
        </b-modal>
      </div>
    </div>

    <!-- Show Details Section -->
    <div class="jumbotron vertical-cent">
      <!-- ... Your Show Details Template ... -->
      <div class="container">
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cosmo/bootstrap.min.css"
          integrity="sha384-5QFXyVb+lrCzdN228VS3HmzpiE7ZVwLQtkt+0d9W43LQMzz4HBnnqvVxKg6O+04d"
          crossorigin="anonymous"
        />
        <div class="row">
          <div class="col-sm-12">
            <h1>Show Details</h1>
            <hr />
            <br />
            <!--alert messg-->
            <!-- <b-alert variant="success" v-if="showMessage" show> {{ message }} </b-alert> -->
            <button
              type="button"
              class="btn btn-success btn-sm"
              v-b-modal.show-modal
            >
              Add Show
            </button>
            <br /><br />
            <table class="table table-hover">
              <thead>
                <tr>
                  <!--table header cells-->
                  <th scope="col">Name</th>
                  <th scope="col">Genre</th>
                  <th scope="col">Rating</th>
                  <th scope="col">Price</th>
                  <th scope="col">Date</th>
                  <th scope="col">Time</th>
                  <th scope="col">Available Seats</th>
                  <th scope="col">Venue</th>
                  <th scope="col">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(show, index) in shows" :key="index">
                  <td>{{ show.show_name }}</td>
                  <td>{{ show.genre }}</td>
                  <td>{{ show.rating }}</td>
                  <td>{{ show.price }}</td>
                  <td>{{ show.date }}</td>
                  <td>{{ show.time }}</td>
                  <td>{{ show.available_seats }}</td>
                  <td>
                    {{ show.venue.name }} <br />
                    {{ show.venue.place }}
                  </td>

                  <td>
                    <div class="btn-group" role="group">
                      <button
                        type="button"
                        class="btn btn-info btn-sm"
                        v-b-modal.show-update-modal
                        @click="showEditModel(show)"
                      >
                        Update
                      </button>
                      <button
                        type="button"
                        class="btn btn-danger btn-sm"
                        @click="deleteShow(show)"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!--first modal-->
        <b-modal
          ref="addShowModal"
          id="show-modal"
          title="Add a new show"
          hide-backdrop
          hide-footer
        >
          <b-form @submit="onShowSubmit" @reset="onReset" class="w-100">
            <b-form-group
              id="form-name-group"
              label="Name:"
              label-for="form-name-input"
            >
              <b-form-input
                id="form-name-input"
                type="text"
                v-model="addShowForm.show_name"
                placeholder="Enter show"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-genre-group"
              label="Genre:"
              label-for="form-genre-input"
            >
              <b-form-input
                id="form-genre-input"
                type="text"
                v-model="addShowForm.genre"
                placeholder="Enter genre"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-rating-group"
              label="Rating:"
              label-for="form-rating-input"
            >
              <b-form-input
                id="form-rating-input"
                type="number"
                v-model="addShowForm.rating"
                placeholder="Enter rating"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-price-group"
              label="Price:"
              label-for="form-price-input"
            >
              <b-form-input
                id="form-price-input"
                type="number"
                v-model="addShowForm.price"
                placeholder="Enter price"
              >
              </b-form-input>
            </b-form-group>
            <b-form-group
              id="form-date-group"
              label="Date:"
              label-for="form-date-input"
            >
              <b-form-input
                id="form-date-input"
                type="date"
                v-model="addShowForm.date"
                required
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-time-group"
              label="Time:"
              label-for="form-time-input"
            >
              <b-form-input
                id="form-time-input"
                type="time"
                v-model="addShowForm.time"
                required
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-available-seats-group"
              label="Available Seats:"
              label-for="form-available-seats-input"
            >
              <b-form-input
                id="form-available-seats-input"
                type="number"
                v-model="addShowForm.available_seats"
                placeholder="Enter available seats"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-venue-group"
              label="Venue:"
              label-for="form-venue-input"
            >
              <b-form-select
                id="form-venue-input"
                v-model="addShowForm.venue_id"
                required
                placeholder="Select venue"
              >
                <option
                  v-for="venue in venues"
                  :key="venue.id"
                  :value="venue.id"
                >
                  {{ venue.name }} {{ venue.place }} {{ venue.city }}
                </option>
              </b-form-select>
            </b-form-group>

            <b-button type="submit" variant="outline-info">Submit</b-button>
            <b-button type="reset" variant="outline-danger">Reset</b-button>
          </b-form>
        </b-modal>

        <!-- start of modal 2 -->

        <b-modal
          ref="editShowModal"
          id="show-update-modal"
          title="Update"
          hide-backdrop
          hide-footer
        >
          <b-form @submit="onUpdateShow" @reset="onResetUpdate" class="w-100">
            <b-form-group
              id="form-name-edit-group"
              label="Name:"
              label-for="form-name-edit-input"
            >
              <b-form-input
                id="form-name-edit-input"
                type="text"
                v-model="editShowForm.show_name"
                required
                placeholder="Enter show"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-genre-edit-group"
              label="Genre:"
              label-for="form-genre-edit-input"
            >
              <b-form-input
                id="form-genre-edit-input"
                type="text"
                v-model="editShowForm.genre"
                required
                placeholder="Enter genre"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-rating-edit-group"
              label="Rating:"
              label-for="form-rating-edit-input"
            >
              <b-form-input
                id="form-rating-edit-input"
                type="number"
                v-model="editShowForm.rating"
                required
                placeholder="Enter rating"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-price-edit-group"
              label="Price:"
              label-for="form-price-edit-input"
            >
              <b-form-input
                id="form-price-edit-input"
                type="number"
                v-model="editShowForm.price"
                required
                placeholder="Enter price"
              >
              </b-form-input>

              <b-form-group
                id="form-available-seats-edit-group"
                label="Available Seats:"
                label-for="form-available-seats-edit-input"
              >
                <b-form-input
                  id="form-available-seats-edit-input"
                  type="number"
                  v-model="editShowForm.available_seats"
                  required
                  placeholder="Enter available seats"
                >
                </b-form-input>
              </b-form-group>
            </b-form-group>
            <b-form-group
              id="form-date-edit-group"
              label="Date:"
              label-for="form-date-edit-input"
            >
              <b-form-input
                id="form-date-edit-input"
                type="date"
                v-model="editShowForm.date"
                required
                placeholder="Enter date"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-time-edit-group"
              label="Time:"
              label-for="form-time-edit-input"
            >
              <b-form-input
                id="form-time-edit-input"
                type="time"
                v-model="editShowForm.time"
                required
                placeholder="Enter time"
              >
              </b-form-input>
            </b-form-group>

            <b-form-group
              id="form-venue-edit-group"
              label="Venue:"
              label-for="form-venue-edit-input"
            >
              <b-form-select
                id="form-venue-edit-input"
                v-model="editShowForm.venue_id"
                required
                placeholder="Select venue"
              >
                <option
                  v-for="venue in venues"
                  :key="venue.id"
                  :value="venue.id"
                >
                  {{ venue.name }} <br />{{ venue.place }}<br />
                  {{ venue.city }}
                </option>
              </b-form-select>
            </b-form-group>

            <b-button type="submit" variant="outline-info">Submit</b-button>
            <b-button type="cancel" variant="outline-danger">cancel</b-button>
          </b-form>
        </b-modal>
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
      addVenueForm: {
        name: "",
        place: "",
        city: "",
        capacity: "",
        // shows: [],
      },
      editForm: {
        name: "",
        place: "",
        city: "",
        capacity: "",
        // shows: [],
      },

      // availableShows: [],

      addShowForm: {
        show_name: "",
        genre: "",
        rating: "",
        price: "",
        date: "",
        time: "",
        available_seats: "",
        venue_id: "",
      },
      editShowForm: {
        show_name: "",
        genre: "",
        rating: "",
        price: "",
        date: "",
        time: "",
        available_seats: "",
        venue_id: "",
      },
      message: "",
      showMessage: false,
    };
  },
  computed: {
    axiosConfig() {
      let token = localStorage.getItem("access_token");
      return {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
    },
  },

  methods: {
    // Venue Methods
    getVenues() {
      const path = "http://127.0.0.1:5000/admindashboard/venues";
      axios
        .get(path, this.axiosConfig)
        .then((res) => {
          this.venues = res.data.venues;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    getShows() {
      const path = "http://127.0.0.1:5000/admindashboard/shows";
      axios
        .get(path, this.axiosConfig)
        .then((res) => {
          this.shows = res.data.shows;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    showAddShowModal() {
      this.$refs.addShowModal.show();
    },
    showAddVenueModal() {
      this.$refs.addVenueModal.show();
    },
    addVenue(payload) {
      const path = "http://127.0.0.1:5000/admindashboard/venues";
      axios
        .post(path, payload, this.axiosConfig)
        .then((response) => {
          if (response.data.status==="success") {
            this.venues.push(response.data.venue);
            this.message="Venue added!";
            this.showMessage=true;
          }else{
          console.error("Failed to add venue", response.data.message);
          }

        })
        .catch((error) => {
          console.error("Failed to add venue", error);
        });
    },
    addShow(payload) {
      const path = "http://127.0.0.1:5000/admindashboard/shows";
      axios
        .post(path, payload, this.axiosConfig)
        .then((response)=>{
          if (response.data.status === "success") {
            this.shows.push(response.data.show);
            this.message="Show added!";
            this.showMessage=true;
          }else{
            console.error("Failed to add show", response.data.message);
          }
        })
        .catch((error)=>{
          console.error("Failed to add show", error);
        });
    },
    // updateVenue(payload, venueID) {
    //   const path = `http://127.0.0.1:5000/admindashboard/venues/${venueID}`;
    //   axios
    //     .put(path, payload, this.axiosConfig)
    //     .then(() => {
    //       this.venues=this.venues.map((venue)=>
    //       venue.id===venueID?{...venue,...payload}:venue
    //       );
    //       this.message = "Venue updated!";
    //       this.showMessage = true;
    //       this.$refs.editVenueModal.hide();
    //       this.getVenues();
    //     })
    //     .catch((err) => {
    //       console.error(err);
    //     });
    // },

    

  updateVenue(payload, venueID) {
    const path = `http://127.0.0.1:5000/admindashboard/venues/${venueID}`;
    axios
      .put(path, payload, this.axiosConfig)
      .then(() => {
        // Update the venues array with the updated venue data
        this.venues = this.venues.map((venue) =>
          venue.id === venueID ? { ...venue, ...payload } : venue
        );
        this.message = "Venue updated!";
        this.showMessage = true;
        this.$refs.editVenueModal.hide();
      })
      .catch((error) => {
        console.error(error);
      });
  },
    updateShow(payload, showID) {
      const path = `http://127.0.0.1:5000/admindashboard/shows/${showID}`;
      axios
        .put(path, payload, this.axiosConfig)
        .then(() => {
         this.shows=this.shows.map((show)=>
          show.id===showID?{...show,...payload}:show
          );
          this.getShows();
          this.message = "Show updated!";
          this.showMessage = true;
          this.$refs.editShowModal.hide();

        })
        .catch((err) => {
          console.error(err);

        });
    },

    showEditModel(show){
      this.editShowForm={...show};
      console.log(this.editShowForm)
      this.$refs.editShowModal.show();
    },

    venueEditModel(venue){
      this.editForm={...venue};
      console.log(this.editForm)
      this.$refs.editVenueModal.show();
    },

    // deleteVenue(venueID){
    //   const path = `http://127.0.0.1:5000/admindashboard/venues/${venueID}`;
    //   axios
    //     .delete(path,this.axiosConfig)
    //     .then(()=>{
    //       this.venues=this.venues.filter((venue)=>venue.id!==venueID);
    //       this.message="Venue deleted!";
    //       this.showMessage=true;
    //     })
    //     .catch((err)=>{
    //       console.error(err);
    //     });
    // },

    removeVenue(venueID) {
    const confirmed = window.confirm('Are you sure you want to delete this venue?');
      if (!confirmed) {
        // If the user cancels the deletion, do nothing
        return;
      }
      const path = `http://127.0.0.1:5000/admindashboard/venues/${venueID}`;
      axios.delete(path, this.axiosConfig) // Add this.axiosConfig
        .then(() => {
          this.getVenues();
          this.showMessage = true;
          this.message = "Venue deleted!";
        })
        .catch((err) => {
          console.error(err);
          this.getVenues();
        });
  },
  deleteVenue(venue) {
    this.removeVenue(venue.id);

  },
  removeShow(showID) {
    const confirmed = window.confirm('Are you sure you want to delete this show?');
    if (!confirmed) {
      // If the user cancels the deletion, do nothing
      return;
    }
    const path = `http://127.0.0.1:5000/admindashboard/shows/${showID}`;
    axios.delete(path, this.axiosConfig) // Add this.axiosConfig
      .then(() => {
        this.getShows();
        this.showMessage = true;
        this.message = "Show deleted!";
      })
      .catch((err) => {
        console.error(err);
        this.getShows();
      });
  },
  deleteShow(show) {
    this.removeShow(show.id);
  },

    initShowForm(){
      this.addShowForm.show_name="";
      this.addShowForm.genre="";
      this.addShowForm.rating="";
      this.addShowForm.price="";
      this.addShowForm.date="";
      this.addShowForm.time="";
      this.addShowForm.available_seats="";
      this.addShowForm.venue_id="";
      this.editShowForm.show_name="";
      this.editShowForm.genre="";
      this.editShowForm.rating="";
      this.editShowForm.price="";
      this.editShowForm.date="";
      this.editShowForm.time="";
      this.editShowForm.available_seats="";
      this.editShowForm.venue_id="";
      
    },  
    initVenueForm(){
      this.addVenueForm.name="";
      this.addVenueForm.place="";
      this.addVenueForm.city="";
      this.addVenueForm.capacity="";
      this.editForm.name="";
      this.editForm.place="";
      this.editForm.city="";
      this.editForm.capacity="";
      
    },

    
    onShowSubmit(e){
      e.preventDefault();
      this.$refs.addShowModal.hide();
      const payload={
        show_name: this.addShowForm.show_name,
        genre: this.addShowForm.genre,
        rating: this.addShowForm.rating,
        price: this.addShowForm.price,
        date: this.addShowForm.date,
        time: this.addShowForm.time,
        available_seats: this.addShowForm.available_seats,
        venue_id: this.addShowForm.venue_id,
      };
      this.addShow(payload,this.addShowForm.id);
      this.initShowForm();
    },
    
    onVenueSubmit(e) {
      e.preventDefault();
      this.$refs.addVenueModal.hide();
      const payload = {
        name: this.addVenueForm.name,
        place: this.addVenueForm.place,
        city: this.addVenueForm.city,
        capacity: this.addVenueForm.capacity,
      };
      this.addVenue(payload, this.addVenueForm.id);
      this.initVenueForm();
  },
  
    onReset(e) {
      e.preventDefault();
      this.$refs.addShowModal.hide();
      this.$refs.addVenueModal.hide();
      this.initForm();
    },

    onUpdateVenue(e){
      e.preventDefault();
      this.$refs.editVenueModal.hide();
      const payload={
        name: this.editForm.name,
        place: this.editForm.place,
        city: this.editForm.city,
        capacity: this.editForm.capacity,
      };
      this.updateVenue(payload,this.editForm.id);
      this.initVenueForm();
      },

  
    onUpdateShow(e){
      e.preventDefault();
      this.$refs.editShowModal.hide();
      const payload={
        show_name: this.editShowForm.show_name,
        genre: this.editShowForm.genre,
        rating: this.editShowForm.rating,
        price: this.editShowForm.price,
        date: this.editShowForm.date,
        time: this.editShowForm.time,
        available_seats: this.editShowForm.available_seats,
        venue_id: this.editShowForm.venue_id,
      };
      this.updateShow(payload,this.editShowForm.id);


    },

  onResetUpdate(e) {
    e.preventDefault();
    this.$refs.editShowModal.hide();
    this.$refs.editVenueModal.hide();
    this.initForm();
    this.getShows();
    this.getVenues();
  },
  logout() {
    // Perform any necessary logout actions, such as clearing session data, tokens, or local storage.
    // For simplicity, we will redirect to the admin login page.
    localStorage.removeItem("access_token");
    this.$router.push({ name: "AdminLogin" });
  },
  },
  created() {
  let token = localStorage.getItem("access_token");
  if (token == null) {
    this.$router.push("/admin_login");
  }
  this.getShows();
  this.getVenues();
  },

}

</script>
