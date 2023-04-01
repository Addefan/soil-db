<template>
  <div class="rounded-4 h-100 mh-50 table-color">
    <form>
      <div v-for="param in this.getAttributes()" :key="param" class="mt-2 pt-1 px-2">
        {{ param.russian_name }}
        <div v-if="param.type === 'text'">
          <SearchSelect :variants="param.values"
                        @change="(data) => handleFilter(param.english_name, data)"></SearchSelect>
        </div>
        <div v-else-if="param.type === 'date'">
          <CustomDateFilter v-model="date"
                            @change="(data) => handleFilter(param.english_name, data)"></CustomDateFilter>
        </div>
        <number-input v-else-if="param.type === 'float' || param.type === 'int'" :min="param.values[0]"
                      :max="param.values[1]" @change="(data) => handleFilter(param.english_name, data)"/>
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
    ...mapActions(["loadAttributes"]),
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