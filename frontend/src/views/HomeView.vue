<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/booklogo.png" />
    <HelloWorld msg="Welcome to Your Ticket Booking App" />
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: "HomeView",
  components: {
    HelloWorld,
  },
};
</script>
