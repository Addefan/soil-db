<template>
  <div class="flex-wrapper m-0">
    <table class="table table-hover table-bordered border-light table-color rounded-4 m-0">
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
      <tr class="content-align" v-for="plant in this.plants" :key="plant.number">
        <td><a :href="`/plants/${plant.number}`">{{ plant.number }}</a></td>
        <td>{{ plant.name }}</td>
        <td>{{ plant.latin_name }}</td>
        <td>{{ plant.genus }}</td>
        <td>{{ plant.organization }}</td>
      </tr>
      </tbody>
    </table>
    <div ref="load-observer"></div>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapMutations, mapState } from "vuex";
import qs from "qs";

export default {
  name: "PlantsTable",
  methods: {
    ...mapActions(["loadPlants", "loadMore"]),
    ...mapMutations({setParameters: "SET_PARAMETERS", switchIsMorePlants: "SWITCH_IS_MORE_PLANTS"}),
  },
  computed: {
    ...mapState(["plants", "parameters", "isMorePlants"]),
    ...mapGetters(["getQueryParams"])
  },
  watch: {
    $route(to) {
      const params = { ...to.query, "page": 1 };
      if (!this.isMorePlants) {
        this.switchIsMorePlants();
      }
      this.setParameters({ parameters: params });
      this.loadMore();
    }
  },
  mounted() {
    const observer_options = {
      rootMargin: '0px',
      threshold: 1.0
    };
      const dynamicLoad = (entries, observer) => {
        if (entries[0].isIntersecting) {
          this.loadMore();
        }
      };
      const observer = new IntersectionObserver(dynamicLoad, observer_options);
      observer.observe(this.$refs["load-observer"]);
  }
};
</script>

<style scoped>

</style>
