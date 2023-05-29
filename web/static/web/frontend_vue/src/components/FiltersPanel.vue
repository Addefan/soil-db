<template>
  <div class="rounded-4 mh-50 table-color">
    <form class="pt-2" @submit.prevent="submitFilters">
      <div v-for="(param, index) in this.attributes" :key="index" class="mb-2">
        <div class="px-2">{{ param.russian_name }}</div>
        <div v-if="param.type === 'text'">
          <SearchSelect :variants="param.values" class="px-2" :attrName="param.english_name"></SearchSelect>
        </div>
        <div v-else-if="param.type === 'date'">
          <CustomDateFilter class="px-2" :attrName="param.english_name"></CustomDateFilter>
        </div>
        <number-input v-else-if="param.type === 'float' || param.type === 'int'" :min="param.values[0]"
                      :max="param.values[1]" :attrName="param.english_name" class="py-2 px-3"
                      :isFloat="param.type === 'float'" />
      </div>
      <div class="text-center buttons position-sticky top-100 mb-1">
        <button class="btn btn-success btn-sm me-1 mb-2 mt-1" :disabled="isLoading">
          <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true" v-if="isLoading"></span>
          Применить
        </button>
        <button type="button" class="btn btn-outline-success ms-1 btn-sm mx-auto mb-2 mt-1"
                data-bs-toggle="modal" data-bs-target="#ModalXlsx" v-if="getIsAuthenticated()" :disabled="isLoading">Экспорт
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { mapActions, mapMutations, mapState } from "vuex";
import CustomDateFilter from "@/components/CustomDateFilter.vue";
import NumberInput from "@/components/NumberInput.vue";
import SearchSelect from "@/components/SearchSelect.vue";

export default {
  name: "FiltersPanel",
  components: { CustomDateFilter, SearchSelect, NumberInput },
  methods: {
    ...mapActions(["loadAttributes"]),
    ...mapMutations({setParameter: "SET_PARAMETER", setPlants: "SET_PLANTS"}),
    submitFilters() {
      this.setPlants({ new_plants: [], reset: true });
      this.setParameter({ param: "page", values: 1 });
      this.$router.push({ query: this.parameters });
    },
    getIsAuthenticated() {
      const value = document.querySelector("#isAuthenticated").value;
      console.log(value);
      return value === "True";
    }
  },
  computed: {
    ...mapState(["attributes", "parameters", "isLoading"]),
  },
  created() {
    this.loadAttributes();
  }
};
</script>

<style scoped>
.buttons {
  position: relative
}
</style>
