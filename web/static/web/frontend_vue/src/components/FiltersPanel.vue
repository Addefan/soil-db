<template>
  <div class="rounded-4 h-100 mh-50 table-color">
    <form class="pt-2" @submit.prevent="this.loadPlants">
      <div v-for="param in this.getAttributes()" :key="param" class="mb-2">
        <div class="px-2">{{ param.russian_name }}</div>
        <div v-if="param.type === 'text'">
          <SearchSelect :variants="param.values" class="px-2"
                        @change="(data) => handleFilter(param.english_name, data)"></SearchSelect>
        </div>
        <div v-else-if="param.type === 'date'">
          <CustomDateFilter class="px-2"
              @change="(data) => handleFilter(param.english_name, data)"></CustomDateFilter>
        </div>
        <number-input v-else-if="param.type === 'float' || param.type === 'int'" :min="param.values[0]"
                      :max="param.values[1]" @change="(data) => handleFilter(param.english_name, data)"
                      class="py-2 px-3"/>
      </div>
      <div class="text-center buttons position-sticky top-100 mb-1">
        <button class="btn btn-success btn-sm me-1">
          Применить
        </button>
        <button type="button" class="btn btn-outline-success ms-1 btn-sm mx-auto export_to_xlsx__button"
                data-bs-toggle="modal" data-bs-target="#ModalXlsx">Экспорт
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations} from "vuex";
import CustomDateFilter from "@/components/CustomDateFilter.vue";
import NumberInput from "@/components/NumberInput.vue";
import SearchSelect from "@/components/SearchSelect.vue";

export default {
  name: "FiltersPanel",
  components: {CustomDateFilter, SearchSelect, NumberInput},
  methods: {
    ...mapActions(["loadAttributes", "loadPlants"]),
    ...mapGetters(["getAttributes"]),
    ...mapMutations(["SET_PARAMETER"]),
    handleFilter(param, values) {
      this.$store.commit('SET_PARAMETER', { param, values });
    },
  },
  mounted() {
    this.loadAttributes();
  }
}
</script>

<style scoped>
.buttons {
  position: relative
}
</style>