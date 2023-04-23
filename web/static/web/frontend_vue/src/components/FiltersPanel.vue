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
                      :float="param.type === 'float'" />
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
import { mapActions, mapMutations, mapState } from "vuex";
import CustomDateFilter from "@/components/CustomDateFilter.vue";
import NumberInput from "@/components/NumberInput.vue";
import SearchSelect from "@/components/SearchSelect.vue";

export default {
  name: "FiltersPanel",
  components: { CustomDateFilter, SearchSelect, NumberInput },
  methods: {
    ...mapActions(["loadAttributes"]),
    ...mapMutations(["SET_PARAMETER", "SET_PLANTS"]),
    submitFilters() {
      this.$store.commit("SET_PLANTS", { new_plants: [], reset: true });
      this.$store.commit("SET_PARAMETER", { param: "page", values: 1 });
      this.$router.push({ query: this.parameters });
    }
  },
  computed: {
    ...mapState(["attributes", "parameters"])
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