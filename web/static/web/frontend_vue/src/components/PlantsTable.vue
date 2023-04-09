<template>
  <div class="flex-wrapper m-0">
    <table class="table table-hover table-bordered border-light table-color rounded-4 h-100">
      <thead class="thead-dark rounded-4">
      <tr class="content-align">
        <th scope="col">Уникальный номер</th>
        <th scope="col">Наименование растения</th>
        <th scope="col">Латинское наименование растения</th>
        <th scope="col">Род</th>
        <th scope="col">Организация</th>
      </tr>
      </thead>
      <tbody>
      <tr class="content-align" v-for="plant in this.getPlants()" :key="plant.number">
        <td><a :href="`/plants/${plant.number}`">{{ plant.number }}</a></td>
        <td>{{ plant.name }}</td>
        <td>{{ plant.latin_name }}</td>
        <td>{{ plant.genus }}</td>
        <td>{{ plant.organization }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from "vuex";

export default {
  name: "PlantsTable",
  methods: {
    ...mapActions(["loadPlants"]),
    ...mapGetters(["getPlants"]),
    ...mapMutations(["SET_PARAMETERS"])
  },
  watch: {
    $route(to) {
      this.$store.commit("SET_PARAMETERS", { parameters: to.query });
      this.loadPlants(to.href);
    }
  }
};
</script>

<style scoped>

</style>