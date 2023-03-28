<template>
  <div class="rounded-4 h-100 mh-50 table-color">
    <div v-for="param in this.getParameters()" :key="param" class="pt-1 px-2">
      <number-input v-if="param.type === 'float' || param.type === 'int'" :min="param.values[0]" :max="param.values[1]" />
    </div>
    <div class="text-center buttons position-sticky top-100 mb-1">
      <button type="button" class="btn btn-success btn-sm me-1" data-bs-toggle="modal" data-bs-target="#ModalXlsx">Применить</button>
      <button type="button" class="btn btn-outline-success ms-1 btn-sm mx-auto export_to_xlsx__button" data-bs-toggle="modal" data-bs-target="#ModalXlsx">Экспорт</button>
    </div>
  </div>
</template>

<script>
import {mapActions, mapGetters} from "vuex";
import NumberInput from "./NumberInput.vue";

export default {
  name: "FiltersPanel",
  components: {NumberInput},

  methods: {
    ...mapActions(["loadParameters"]),
    ...mapGetters(["getParameters"]),
  },
  mounted() {
    this.loadParameters();
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