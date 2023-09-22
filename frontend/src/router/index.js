import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import AdminDashboard from "../components/AdminDashboard.vue"
import AdminRegistration from "../components/AdminRegistration.vue"
import AdminLogin from "../components/AdminLogin.vue"
import UserLogin from "../components/UserLogin.vue"
import UserDashboard from "../components/UserDashboard.vue"
import BookShow from "../components/BookShow.vue"
import UserRegistration from "../components/UserRegistration.vue"
// import BookingInfo from "../components/BookingInfo.vue"


Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },

  {
    path: "/admindashboard",
    name: "AdminDashboard",
    component: AdminDashboard,
  },

  {
    path: "/userdashboard",
    name: "UserDashboard",
    component: UserDashboard,
  },

  {
    path: "/admin_login",
    name: "AdminLogin",
    component: AdminLogin,
  },

  {
    path: "/user_login",
    name: "UserLogin",
    component: UserLogin,
  },
  {
    path: "/userregistration",
    name: "UserRegistration",
    component: UserRegistration,
  },
  {
    path: "/adminregister",
    name: "AdminRegistration",
    component: AdminRegistration,
  },

  
  {
    path: '/bookings/:showId',
    name: 'bookShow',
    component: BookShow, // Replace with the actual component for your booking form
    props: true, // Pass the show ID as a prop to the component
  },

];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
