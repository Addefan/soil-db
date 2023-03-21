<template>
  <p>Vue is running!</p>
</template>

<script>
import axios from "axios";

export default {
  name: "filtersPanel",
  methods: {
    async getPlants() {
      const response = await axios.get(''); // TODO: real api url
      this.$store.state.data = response.data.args;
    }
  }
}
</script>

<style scoped>

</style>