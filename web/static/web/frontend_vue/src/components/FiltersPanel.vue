<template>
  <div class="rounded-4 h-100 mh-50 table-color">
    <div v-for="param in this.$store.state.parameters" :key="param" class="pt-1 px-2">
      {{ param }}
      <!--TODO: component depending on parameter type-->
    </div>
    <div class="text-center buttons position-sticky top-100 mb-1">
      <button type="button" class="btn btn-success btn-sm me-1" data-bs-toggle="modal" data-bs-target="#ModalXlsx">Применить</button>
      <button type="button" class="btn btn-outline-success ms-1 btn-sm mx-auto export_to_xlsx__button" data-bs-toggle="modal" data-bs-target="#ModalXlsx">Экспорт</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "FiltersPanel",
  methods: {
    async getParameters() {
      const response = await axios.get(''); // TODO: real api
      this.$store.SETPARAMETERS(response.data);
    },
    async getPlants() {
      const response = await axios.get(''); // TODO: real api
      this.$store.SETPLANTS(response.data);
    }
  }
}
</script>

<style scoped>
.buttons {
  position: relative
}

.filters {

}
</style>